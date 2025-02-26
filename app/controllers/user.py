from http import HTTPStatus

from fastapi import HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session, defer
from uuid import UUID

from app.models.user import User
from app.serializers.user import UserBase, UserPost, UserResponse


async def create_user(payload: UserPost, db: Session):
    try:
        user = db.query(User).filter_by(email=payload.email).first()
        if user:
            return ORJSONResponse(
                content={"message": "User with this email already exists"},
                status_code=HTTPStatus.OK,
            )

        user = User(
            email=payload.email,
            role=payload.role,
            is_active=payload.is_active,
            is_admin=payload.is_admin,
        )
        user.set_password(password=payload.password)
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except ValidationError as e:
        return ORJSONResponse(
            content={"error": e.errors()}, status_code=HTTPStatus.UNPROCESSABLE_ENTITY
        )


async def user_list(db: Session):
    return db.query(User).all()


async def get_user_by_uid(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found.")
    return user


async def update_user_controller(id: int, payload: UserPost, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found.")

    user.email = payload.email
    user.role = payload.role
    user.is_active = payload.is_active
    user.is_admin = payload.is_admin
    db.commit()
    db.refresh(user)

    return user


async def delete_user_controller(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
