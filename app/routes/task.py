from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.serializers.task import TaskCreate, TaskResponse, TaskUpdate

from app.controllers.task import create_task_controller,get_task_controller, get_tasks_controller, update_task_controller, delete_task_controller



router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

@router.get("", response_model=list[TaskResponse])
async def get_tasks(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    return await get_tasks_controller(db, skip, limit)

@router.post("", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return await create_task_controller(task, db)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    return await get_task_controller(task_id, db)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return await update_task_controller(task_id, task, db)


@router.delete("/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    return await delete_task_controller(task_id, db)

task_routes = router
