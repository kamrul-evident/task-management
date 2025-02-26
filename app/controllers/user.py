from http import HTTPStatus

from fastapi import HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session, defer
from uuid import UUID

from app.models.user import User
from app.serializers.user import UserBase, UserPost, UserResponse, UserUpdate


async def get_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!!!")
    return user

async def create_user_controller(payload: UserPost, db: Session):
    user = db.query(User).filter_by(email=payload.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    # Create new user
    user = User(
        email=payload.email,
        role=payload.role,
        is_active=payload.is_active,
        is_admin=payload.is_admin,
    )
    user.set_password(payload.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

async def get_user_controller(user_id: int, db: Session):
    return await get_user(user_id, db)

async def get_users_controller(db: Session, skip:int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


async def update_user_controller(user_id: int, payload: UserUpdate, db: Session):
    user = await get_user(user_id, db)
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


async def delete_user_controller(user_id: int, db: Session):
    user = await get_user(user_id, db)
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
