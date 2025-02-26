from typing import Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .utils import verify_access_token

# OAuth2PasswordBearer is used to retrieve the token from the "Authorization" header
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_schema)) -> Dict:
    """Get the current user from the JWT token."""
    try:
        user = verify_access_token(token)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
