import os
import uuid
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.services.ragflow import ragflow_service

router = APIRouter()

# 上传目录
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 允许的文件类型
ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf", ".doc", ".docx"}


def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()


def read_text_file(file_path: str) -> str:
    """读取文本文件内容"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, "r", encoding="gbk") as f:
                return f.read()
        except:
            return ""


async def process_document_with_ragflow(
    db: Session,
    document_id: int,
    file_path: str,
    file_name: str
):
    """后台任务：上传文档到 RAGFlow 并解析"""
    try:
        # 更新解析状态为解析中
        document = crud.document.get(db, id=document_id)
        if document:
            document.parse_status = "parsing"
            db.commit()
        
        # 上传并解析文档
        result = await ragflow_service.upload_and_parse(file_path, file_name)
        
        if result:
            # 更新文档的 RAGFlow 信息
            document = crud.document.get(db, id=document_id)
            if document:
                document.ragflow_dataset_id = result.get("dataset_id")
                document.ragflow_document_id = result.get("document_id")
                document.parse_status = "completed" if result.get("parse_initiated") else "failed"
                db.commit()
        else:
            # 更新解析状态为失败
            document = crud.document.get(db, id=document_id)
            if document:
                document.parse_status = "failed"
                db.commit()
    except Exception as e:
        print(f"处理文档异常: {e}")
        # 更新解析状态为失败
        document = crud.document.get(db, id=document_id)
        if document:
            document.parse_status = "failed"
            db.commit()


@router.get("/", response_model=List[schemas.Document])
def read_documents(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve documents.
    """
    documents = crud.document.get_multi(db, skip=skip, limit=limit)
    return documents


@router.post("/upload", response_model=schemas.Document)
async def upload_document(
    *,
    db: Session = Depends(deps.get_db),
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str = Form(None),
    category: str = Form(None),
    tags: str = Form(None),
) -> Any:
    """
    上传文档文件，并自动发送到 RAGFlow 进行解析
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="未选择文件")
    
    # 检查文件类型
    file_ext = get_file_extension(file.filename)
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"不支持的文件类型。支持的类型: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # 生成唯一文件名
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # 保存文件
    file_content = await file.read()
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    # 读取文本内容（仅对文本文件）
    text_content = ""
    if file_ext in [".txt", ".md"]:
        text_content = read_text_file(file_path)
    
    # 使用文件名作为标题（如果未提供）
    doc_title = title or os.path.splitext(file.filename)[0]
    
    # 创建文档记录
    document_in = schemas.DocumentCreate(
        title=doc_title,
        content=text_content,
        category=category,
        tags=tags,
        file_name=file.filename,
        file_path=file_path,
        file_type=file_ext.lstrip("."),
        file_size=len(file_content),
        parse_status="pending"
    )
    document = crud.document.create(db, obj_in=document_in)
    
    # 添加后台任务：上传到 RAGFlow 并解析
    background_tasks.add_task(
        process_document_with_ragflow,
        db,
        document.id,
        file_path,
        file.filename
    )
    
    return document


@router.post("/", response_model=schemas.Document)
def create_document(
    *,
    db: Session = Depends(deps.get_db),
    document_in: schemas.DocumentCreate,
) -> Any:
    """
    Create new document.
    """
    document = crud.document.create(db, obj_in=document_in)
    return document


@router.get("/{id}", response_model=schemas.Document)
def read_document(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get document by ID.
    """
    document = crud.document.get(db=db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.put("/{id}", response_model=schemas.Document)
def update_document(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    document_in: schemas.DocumentUpdate,
) -> Any:
    """
    Update a document.
    """
    document = crud.document.get(db=db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    document = crud.document.update(db=db, db_obj=document, obj_in=document_in)
    return document


@router.delete("/{id}", response_model=schemas.Document)
def delete_document(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete a document.
    """
    document = crud.document.get(db=db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    document = crud.document.remove(db=db, id=id)
    return document


@router.post("/{id}/reparse", response_model=schemas.Document)
async def reparse_document(
    *,
    db: Session = Depends(deps.get_db),
    background_tasks: BackgroundTasks,
    id: int,
) -> Any:
    """
    重新解析文档
    """
    document = crud.document.get(db=db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not document.file_path:
        raise HTTPException(status_code=400, detail="文档没有关联的文件")
    
    # 更新解析状态为待处理
    document.parse_status = "pending"
    db.commit()
    
    # 添加后台任务：重新上传到 RAGFlow 并解析
    background_tasks.add_task(
        process_document_with_ragflow,
        db,
        document.id,
        document.file_path,
        document.file_name
    )
    
    return document


@router.get("/{id}/parse-status")
def get_parse_status(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    获取文档解析状态
    """
    document = crud.document.get(db=db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {
        "id": document.id,
        "parse_status": document.parse_status,
        "ragflow_dataset_id": document.ragflow_dataset_id,
        "ragflow_document_id": document.ragflow_document_id
    }