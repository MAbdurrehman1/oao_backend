import re
from typing import BinaryIO
from uuid import UUID

import pandas as pd

from cexceptions import MissingValuesException, ValidationException, NotFoundException
from entity import Employee, User, Organization
from repository import (
    OrganizationRepository,
    BusinessUnitRepository,
    EmployeeRepository,
    ParticipationRepository,
)
from .utils import uploaded_csv_to_df
from utils.validation_helpers import assert_email_validation


def _enrich_user(data) -> User:
    return User(
        email=data["email"].lower(),
        first_name=data["first_name"],
        last_name=data["last_name"],
        is_admin=False,
    )


def _enrich_employee(organization: Organization, user: User, data) -> Employee:
    return Employee(
        role_title=data["role_title"],
        location=data["location"],
        user=user,
        organization=organization,
        business_unit_id=int(data["business_unit"].split("-")[0]),
    )


def _assert_business_units_existence(df: pd.DataFrame, organization_id: int) -> None:
    business_units_ids = list(
        set(int(row.split("-")[0]) for row in df["business_unit"])
    )
    missing_ids = BusinessUnitRepository.get_missing_business_unit_ids(
        organization_id, business_units_ids
    )
    if missing_ids:
        raise NotFoundException(entity="BusinessUnit", arg="ID", value=missing_ids[0])


def _enrich_employee_from_df(
    organization: Organization, df: pd.DataFrame
) -> list[Employee]:
    employees = []
    for row in df.to_dict(orient="records"):
        user = _enrich_user(row)
        employee = _enrich_employee(user=user, organization=organization, data=row)
        employees.append(employee)
    return employees


def _assert_business_unit_format(business_unit_set: str):
    if not re.match(r"^\d+-.*", str(business_unit_set)):
        raise ValidationException(entities="Business Unit", values=business_unit_set)


def _assert_null_columns(df: pd.DataFrame) -> None:
    is_null_columns = df.isnull()
    if is_null_columns.values.any():
        null_column_names = is_null_columns.columns[is_null_columns.iloc[0]].tolist()
        raise ValidationException(entities=str(null_column_names), values="null")


def import_contact_list(
    organization_id: int, contacts_csv_file: BinaryIO
) -> list[Employee]:
    organization = OrganizationRepository.get_by_id(organization_id)
    df = uploaded_csv_to_df(contacts_csv_file)
    required_columns = [
        "first_name",
        "last_name",
        "email",
        "role_title",
        "location",
        "business_unit",
    ]
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise MissingValuesException(
            entities="Contacts List", values=str(tuple(missing_columns))
        )
    _assert_null_columns(df)
    df["email"].apply(assert_email_validation)
    df["business_unit"].apply(_assert_business_unit_format)
    _assert_business_units_existence(df, organization.id)
    employees = _enrich_employee_from_df(organization, df)
    stored_employees = []
    for employee in employees:
        stored_employee = EmployeeRepository.store(employee)
        stored_employees.append(stored_employee)
    return stored_employees


def check_user_is_employee(user_id: int) -> bool:
    return EmployeeRepository.check_user_is_employee(user_id=user_id)


def get_auth_employee_data(user: User) -> tuple[Employee, UUID | None]:
    assert isinstance(user.id, int)
    employee = EmployeeRepository.get_by_user_id(user_id=user.id)
    assert isinstance(employee.organization_id, int)
    organization = OrganizationRepository.get_by_id(
        organization_id=employee.organization_id
    )
    employee.organization = organization
    employee.user = user
    try:
        participation_id = ParticipationRepository.get_participation_id_by_user_id(
            user_id=user.id
        )
        return employee, participation_id
    except NotFoundException:
        return employee, None
