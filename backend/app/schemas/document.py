from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class DocumentBase(BaseModel):
    title: str
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None


class DocumentCreate(DocumentBase):
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    ragflow_dataset_id: Optional[str] = None
    ragflow_document_id: Optional[str] = None
    parse_status: Optional[str] = "pending"


class DocumentUpdate(DocumentBase):
    pass


class DocumentInDBBase(DocumentBase):
    id: int
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    ragflow_dataset_id: Optional[str] = None
    ragflow_document_id: Optional[str] = None
    parse_status: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Document(DocumentInDBBase):
    pass