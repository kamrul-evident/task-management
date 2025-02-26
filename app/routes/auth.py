from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.serializers.auth import LoginResponse, LoginRequest
from app.config.database import get_db

from app.controllers.auth import login_controller

router = APIRouter(
    prefix="/login",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


def authenticate_user(email: str, password: str) -> bool:
    pass


@router.post("", response_model=LoginResponse)
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return await login_controller(payload, db)


auth_router = router
