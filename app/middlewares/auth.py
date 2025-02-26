from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.utils.auth import verify_access_token


OPEN_ROUTES = [
    "http://localhost:8000/",
    "http://localhost:8000/docs",
    "http://localhost:8000/openapi.json",
    "http://localhost:8000/login",
]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("request url:", request.url)
        if request.url not in OPEN_ROUTES:
            auth_header = request.headers.get("Authorization", None)
            if not auth_header or auth_header.startswith("Bearer"):
                return JSONResponse(
                    status_code=401, content={"detail": "Unauthorized."}
                )
            token = auth_header.split(" ")[1]
            try:
                request.state.user = verify_access_token(token)
            except HTTPException as e:
                return JSONResponse(
                    status_code=e.status_code, content={"detail": e.detail}
                )
        return await call_next(request)
