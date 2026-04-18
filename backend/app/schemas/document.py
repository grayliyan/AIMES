from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class DocumentBase(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    tags: Optional[str] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(DocumentBase):
    pass


class DocumentInDBBase(DocumentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Document(DocumentInDBBase):
    pass