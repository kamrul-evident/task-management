from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.task import Task
from app.serializers.task import TaskCreate, TaskUpdate, TaskResponse

async def create_task_controller(task: TaskCreate, db: Session):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


async def get_task_controller(task_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

async def get_tasks_controller(db: Session, skip: int=0, limit: int=100):
    return db.query(Task).offset(skip).limit(limit).all()

async def update_task_controller(task_id: int, task: TaskUpdate, db: Session):
    db_task = await get_task_controller(task_id, db)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

async def delete_task_controller(task_id: int, db: Session):
    db_task = await get_task_controller(task_id, db)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task Deleted Successfully!!!"}