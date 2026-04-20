from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: Optional[str] = None
    is_active: Optional[bool] = True


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[str] = None
    is_active: Optional[bool] = None


class RoleInDBBase(RoleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Role(RoleInDBBase):
    pass