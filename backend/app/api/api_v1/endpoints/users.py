from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core.security import get_password_hash

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    获取用户列表
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    创建新用户
    """
    # 检查用户名是否已存在
    user = crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="该用户名已被注册"
        )
    # 检查邮箱是否已存在
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="该邮箱已被注册"
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/{id}", response_model=schemas.User)
def read_user(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    获取用户详情
    """
    user = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.put("/{id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    user_in: schemas.UserUpdate,
) -> Any:
    """
    更新用户
    """
    user = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user = crud.user.update(db=db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{id}", response_model=schemas.User)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    删除用户
    """
    user = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user = crud.user.remove(db=db, id=id)
    return user


@router.put("/{id}/toggle-active", response_model=schemas.User)
def toggle_user_active(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    切换用户启用/禁用状态
    """
    user = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)
    return user


@router.put("/{id}/assign-role", response_model=schemas.User)
def assign_user_role(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    role_id: int,
) -> Any:
    """
    分配用户角色
    """
    user = crud.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    role = crud.role.get(db=db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    user.role_id = role_id
    db.commit()
    db.refresh(user)
    return user