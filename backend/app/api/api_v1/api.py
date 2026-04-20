from fastapi import APIRouter

from app.api.api_v1.endpoints import documents, qa, login, roles, users

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["认证"])
api_router.include_router(documents.router, prefix="/documents", tags=["文档"])
api_router.include_router(qa.router, prefix="/qa", tags=["问答"])
api_router.include_router(roles.router, prefix="/roles", tags=["角色管理"])
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])