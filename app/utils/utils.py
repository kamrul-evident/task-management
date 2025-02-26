from datetime import UTC, datetime, timedelta
from typing import Dict, Optional
import jwt


def utc_now():
    return datetime.now(tz=UTC)


SECRET_KEY = "58d83fab2b8543f4fffad3e5d2840b1103ddf84d6d8a1e47e0ff972bf5626921"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generate a JWT token with the given data."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=UTC) + expires_delta
    else:
        expire = datetime.now(tz=UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str) -> Dict:
    """Decode the JWT token and return the payload (user data)."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise Exception("Invalid token or expired token")
