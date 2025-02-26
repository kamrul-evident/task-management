from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.serializers.user import UserResponse, UserPost, UserBase, UserUpdate

from app.controllers.user import (
    create_user_controller,
    get_user_controller, 
    get_users_controller,
    update_user_controller,
    delete_user_controller,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("", tags=["users"], response_model=list[UserResponse])
async def get_users(skip: int=0, limit: int= 100, db: Session = Depends(get_db)):
    return await get_users_controller(db, skip, limit)


@router.post("", tags=["users"], response_model=UserResponse)
async def user_create(payload: UserPost, db=Depends(get_db)):
    return await create_user_controller(payload, db)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return await get_user_controller(user_id, db)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return await update_user_controller(user_id, payload, db)


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    return await delete_user_controller(user_id, db)


user_routes = router
