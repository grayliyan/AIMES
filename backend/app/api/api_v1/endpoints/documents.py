from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


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