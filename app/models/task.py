import enum
from sqlalchemy import Column, Enum, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import NameSlugDescriptionBaseModel


class Priority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(enum.Enum):
    ASSIGNED = "assigned"
    PENDING = "pending"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Task(NameSlugDescriptionBaseModel):
    __tablename__ = "tasks"

    due_date = Column(DateTime, nullable=True)
    priority = Column(Enum(Priority), default=Priority.LOW)
    category = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assignee = relationship("User", back_populates="tasks")
