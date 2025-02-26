from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.serializers.auth import LoginResponse, LoginRequest
from app.config.database import get_db
from app.models.user import User
from app.utils.utils import create_access_token


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if user.verify_password(password):
        return {"sub": email}
    return None


async def login_controller(payload: LoginRequest, db: Session):
    user = authenticate_user(email=payload.email, password=payload.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # generate JWT token
    access_token = create_access_token(data={"sub": user["sub"]})
    return {"access_token": access_token, "token_type": "bearer"}
