from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.task import TaskStatus, Priority


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Priority = Priority.LOW
    category: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    assignee_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = None
    category: Optional[str] = None
    status: Optional[TaskStatus] = None
    assignee_id: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    uid: str
    slug: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
