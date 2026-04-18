from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.qa import Question, Answer

router = APIRouter()


@router.post("/ask", response_model=Answer)
def ask_question(
    *,
    db: Session = Depends(deps.get_db),
    question_in: Question,
) -> Any:
    """
    Ask a question to the knowledge base.
    """
    # TODO: Integrate with RAGFlow
    # For now, return a placeholder response
    return Answer(
        answer="This is a placeholder answer. RAGFlow integration pending.",
        sources=[],
        confidence=0.0
    )