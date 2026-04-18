from fastapi import APIRouter

from app.api.api_v1.endpoints import documents, qa, login

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["认证"])
api_router.include_router(documents.router, prefix="/documents", tags=["文档"])
api_router.include_router(qa.router, prefix="/qa", tags=["问答"])