from typing import Self
from uuid import UUID

from fastapi import Request, Depends, Security
from pydantic import BaseModel

from entity import User, Employee, Organization, File
from services import get_auth_employee_data
from ..dependencies import EmployeeRequired, auth_header
from ...router import router, Tags


class EmployeeResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    user_id: int
    location: str
    role_title: str
    employee_id: int
    organization_name: str
    organization_logo_url: str
    organization_id: int
    participation_id: str | None

    @classmethod
    def from_entity(cls, employee: Employee, participation_id: UUID | None) -> Self:
        assert isinstance(employee.user, User)
        assert isinstance(employee.organization, Organization)
        assert isinstance(employee.user.first_name, str)
        assert isinstance(employee.user.last_name, str)
        assert isinstance(employee.user.email, str)
        assert isinstance(employee.user.id, int)
        assert isinstance(employee.location, str)
        assert isinstance(employee.role_title, str)
        assert isinstance(employee.id, int)
        assert isinstance(employee.organization.id, int)
        assert isinstance(employee.organization.company_name, str)
        assert isinstance(employee.organization.logo, File)
        return cls(
            first_name=employee.user.first_name,
            last_name=employee.user.last_name,
            email=employee.user.email,
            user_id=employee.user.id,
            location=employee.location,
            role_title=employee.role_title,
            employee_id=employee.id,
            organization_name=employee.organization.company_name,
            organization_logo_url=employee.organization.logo.file_url,
            organization_id=employee.organization.id,
            participation_id=str(participation_id) if participation_id else None,
        )


class GetAuthEmployeeResponseModel(BaseModel):
    result: EmployeeResponse


@router.get("/auth/employee/", tags=[Tags.general])
def get_auth_employee_data_endpoint(
    request: Request,
    user: User = Depends(EmployeeRequired()),
    __: str = Security(auth_header),
) -> GetAuthEmployeeResponseModel:
    employee, participation_id = get_auth_employee_data(user=user)
    return GetAuthEmployeeResponseModel(
        result=EmployeeResponse.from_entity(
            employee=employee, participation_id=participation_id
        )
    )
