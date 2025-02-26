from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.serializers.user import UserResponse, UserPost, UserBase

from app.controllers.user import (
    create_user,
    user_list,
    get_user_by_uid,
    update_user_controller,
    delete_user_controller,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("", tags=["users"], response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return await user_list(db)


@router.post("", tags=["users"], response_model=UserResponse)
async def user_create(payload: UserPost, db=Depends(get_db)):
    return await create_user(payload=payload, db=db)


@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    return await get_user_by_uid(id, db)


@router.put("/{id}", response_model=UserResponse)
async def update_user(id: int, payload: UserBase, db: Session = Depends(get_db)):
    return await update_user_controller(id, payload, db)


@router.delete("/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    return await delete_user_controller(id, db)


user_routes = router
