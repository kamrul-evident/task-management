from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from app.models.user import UserRole


class UserBase(BaseModel):
    email: str
    role: UserRole = UserRole.OTHER
    is_active: bool = True
    is_admin: bool = False

    class Config:
        from_attributes = True


class UserPost(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    uid: UUID

    class Config:
        from_aatributes = True
