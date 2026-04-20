from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Role])
def read_roles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    获取角色列表
    """
    roles = crud.role.get_multi(db, skip=skip, limit=limit)
    return roles


@router.post("/", response_model=schemas.Role)
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role_in: schemas.RoleCreate,
) -> Any:
    """
    创建新角色
    """
    # 检查角色名是否已存在
    role = crud.role.get_by_name(db, name=role_in.name)
    if role:
        raise HTTPException(
            status_code=400,
            detail="该角色名称已存在"
        )
    role = crud.role.create(db, obj_in=role_in)
    return role


@router.get("/{id}", response_model=schemas.Role)
def read_role(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    获取角色详情
    """
    role = crud.role.get(db=db, id=id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    return role


@router.put("/{id}", response_model=schemas.Role)
def update_role(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    role_in: schemas.RoleUpdate,
) -> Any:
    """
    更新角色
    """
    role = crud.role.get(db=db, id=id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    role = crud.role.update(db=db, db_obj=role, obj_in=role_in)
    return role


@router.delete("/{id}", response_model=schemas.Role)
def delete_role(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    删除角色
    """
    role = crud.role.get(db=db, id=id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    role = crud.role.remove(db=db, id=id)
    return role