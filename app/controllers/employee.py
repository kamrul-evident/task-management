from http import HTTPStatus

from fastapi import HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session
from uuid import UUID


from app.models.employee import Employee
from app.models.user import User
from app.models.department import Department
from app.serializers.employee import EmployeePost, EmployeeUpdate, EmployeeDetail
from app.serializers.department import DepartmentResponse
from app.serializers.user import UserResponse


async def employee_list_controller(db: Session):
    return db.query(Employee).all()


async def create_employee_controller(payload: EmployeePost, db: Session):
    try:
        employee = db.query(Employee).filter_by(email=payload.email).first()
        if employee:
            return ORJSONResponse(
                content={"message": "Employee with this email already exists"},
                status_code=HTTPStatus.OK,
            )
        user = User(email=payload.email, role="employee")
        user.set_password(password=payload.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        employee = Employee(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            phone=payload.phone,
            department_id=payload.department_id,
            job_title=payload.job_title,
            user_id=user.id,
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
    except ValidationError as e:
        return ORJSONResponse(
            content={"error": e.errors()}, status_code=HTTPStatus.UNPROCESSABLE_ENTITY
        )


async def get_single_employee_controller(id: int, db: Session):
    employee_query = (
        db.query(Employee, User, Department)
        .join(User, User.id == Employee.user_id, isouter=True)
        .join(Department, Department.id == Employee.department_id, isouter=True)
        .filter(Employee.id == id)
        .first()
    )
    if not employee_query:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Employee not found"
        )
    # Unpack the query results
    employee, user, department = employee_query
    # employee = db.query(Employee).filter(Employee.id == id).first()
    # if not employee:
    #     raise HTTPException(
    #         status_code=HTTPStatus.NOT_FOUND, detail="Employee not found."
    #     )
    # # Ensure related user and department are loaded, then return the response
    # user = db.query(User).filter(User.id == employee.user_id).first()
    # emp_department = (
    #     db.query(Department).filter(Department.id == employee.department_id).first()
    # )
    # Return the detailed response
    return EmployeeDetail(
        id=employee.id,
        uid=employee.uid,
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        phone=employee.phone,
        department_id=employee.department_id,
        job_title=employee.job_title,
        department=DepartmentResponse.model_validate(department),
        user=UserResponse.model_validate(user),
    )


async def update_employee_controller(id: int, payload: EmployeeUpdate, db: Session):
    try:
        employee = db.query(Employee).filter(Employee.id == id).first()
        if not employee:
            return ORJSONResponse(
                content={"message": "Employee does not exists."},
                status_code=HTTPStatus.BAD_REQUEST,
            )
        employee.first_name = payload.first_name
        employee.last_name = payload.last_name
        employee.job_title = payload.job_title
        employee.phone = payload.phone
        employee.department_id = payload.department_id
        employee.email = payload.email
        db.commit()
        db.refresh(employee)
        return employee
    except ValidationError as e:
        return ORJSONResponse(
            content={"error": e.errors()}, status_code=HTTPStatus.UNPROCESSABLE_ENTITY
        )


async def delete_employee_controller(id: int, db: Session):
    employee = db.query(Employee).filter(Employee.id == id).first()
    if not employee:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Employee not found."
        )

    if employee.user_id:
        user = db.query(User).filter(User.id == employee.user_id).first()
        db.delete(user)
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully!!!"}
