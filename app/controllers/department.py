from http import HTTPStatus

from fastapi import HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session, defer
from uuid import UUID

from app.models.department import Department
from app.serializers.department import DepartmentPost


async def department_list_controller(db: Session):
    return db.query(Department).all()


async def create_department_controller(payload: DepartmentPost, db: Session):
    try:
        department = db.query(Department).filter_by(name=payload.name).first()
        if department:
            return ORJSONResponse(
                content={"message": "Department with this name already exists"},
                status_code=HTTPStatus.OK,
            )
        department = Department(name=payload.name, description=payload.description)
        db.add(department)
        db.commit()
        db.refresh(department)
        return department

    except ValidationError as e:
        return ORJSONResponse(
            content={"error": e.errors()}, status_code=HTTPStatus.UNPROCESSABLE_ENTITY
        )


async def get_single_department_controller(id: int, db: Session):
    department = db.query(Department).filter(Department.id == id).first()
    if not department:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Department not found."
        )

    return department


async def update_department_controller(id: int, payload: DepartmentPost, db: Session):
    department = db.query(Department).filter(Department.id == id).first()
    if not department:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Department not found."
        )
    department.name = payload.name
    department.description = payload.description
    db.commit()
    db.refresh(department)

    return department


async def delete_department_controller(id: int, db: Session):
    department = db.query(Department).filter(Department.id == id).first()
    if not department:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Department not found."
        )
    db.delete(department)
    db.commit()
    return {"message": "Department deleted successfully!!!"}
