from typing import List, Optional

from pydantic import BaseModel


class Question(BaseModel):
    question: str
    context: Optional[str] = None


class Source(BaseModel):
    document_id: int
    title: str
    excerpt: str


class Answer(BaseModel):
    answer: str
    sources: List[Source] = []
    confidence: float = 0.0