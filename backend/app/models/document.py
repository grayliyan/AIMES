from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger
from sqlalchemy.sql import func

from app.core.config import settings
from app.db.base_class import Base


class Document(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text)
    category = Column(String(100), index=True)
    tags = Column(String(500))  # Comma-separated tags
    # 文件相关字段
    file_name = Column(String(255))  # 原始文件名
    file_path = Column(String(500))  # 存储路径
    file_type = Column(String(50))   # 文件类型 (txt, pdf, doc, docx, md)
    file_size = Column(BigInteger)   # 文件大小(字节)
    # RAGFlow 相关字段
    ragflow_dataset_id = Column(String(100))  # RAGFlow 数据集 ID
    ragflow_document_id = Column(String(100))  # RAGFlow 文档 ID
    parse_status = Column(String(50), default="pending")  # 解析状态: pending, parsing, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())