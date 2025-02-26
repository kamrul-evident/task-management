import enum
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from .base import (
    BaseModelWithUUID,
)  # Assuming the base model is in app/models/base.py

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(enum.Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    MANAGER = "manager"
    OTHER = "other"
    FRONTEND_ENGINEER = "frontend_engineer"
    DEV_OPS_ENGINEER = "dev_ops_engineer"
    BACKEND_ENGINEER = "backend_engineer"

class User(BaseModelWithUUID):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.OTHER)
    #Add relationship for tasks assigned to this user
    tasks = relationship("Task", back_populates="assignee")

    # Not every User has to be an Employee, so no backref on the User side

    def __repr__(self):
        return f"<User(email='{self.email}', role='{self.role.value}')>"

    def set_password(self, password: str):
        """Hash the password and store it"""
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash"""
        return pwd_context.verify(password, self.hashed_password)
