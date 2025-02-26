import logging
from http import HTTPStatus

from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.config.database import Session, get_db

from app.routes.user import user_routes

from app.routes.auth import auth_router

from app.routes.task import task_routes

from app.middlewares.auth import AuthMiddleware
from app.utils.auth import get_current_user

logger = logging.getLogger("fastapi")
app = FastAPI(dependencies=[Depends(get_db)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add auth middleware to the app
# app.add_middleware(AuthMiddleware)


@app.get("/")
def health_check():
    db = Session()

    response = {}
    response["server_health"] = "Employee Management System Server API health OK"
    response["database_health"] = "OK" if db.is_active else "disconnected"

    return ORJSONResponse(content=response, status_code=HTTPStatus.OK)


@app.get("/private")
async def private_route(current_user: dict = Depends(get_current_user)):
    """A private route that requires authentication."""
    return {"message": "This is a private route.", "user": current_user}


# include routers
app.include_router(auth_router)
app.include_router(user_routes)
app.include_router(task_routes)