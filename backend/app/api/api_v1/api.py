from fastapi import APIRouter

from app.api.api_v1.endpoints import documents, qa

api_router = APIRouter()
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(qa.router, prefix="/qa", tags=["qa"])