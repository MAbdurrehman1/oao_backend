from datetime import datetime

from entity import Employee, User
from ..employee_repository import EmployeeRepository
from ..user_repository import UserRepository
from .helpers import (
    create_some_organization,
    create_some_business_unit,
    create_some_employee,
)


def test_store_employee(cleanup_database, cleanup_media):
    organization = create_some_organization()
    user = User(
        first_name="John",
        last_name="Doe",
        email="JohnDoe@example.com",
    )
    assert isinstance(organization.id, int)
    bu = create_some_business_unit(organization_id=organization.id, name="bu")
    employee = Employee(
        user=user,
        organization=organization,
        role_title="CEO",
        location="london-UK",
        business_unit_id=bu.id,  # type: ignore
    )
    retrieved_employee = EmployeeRepository.store(employee)
    assert isinstance(retrieved_employee.id, int)
    assert isinstance(retrieved_employee.created_at, datetime)
    assert isinstance(retrieved_employee.updated_at, datetime)


def test_store_employee_with_updated_into_updates_user_data(
    cleanup_database, cleanup_media
):
    organization = create_some_organization()
    assert isinstance(organization.id, int)
    bu = create_some_business_unit(organization_id=organization.id, name="bu")
    user = User(
        first_name="John",
        last_name="Doe",
        email="JohnDoe@example.com",
    )
    employee = Employee(
        user=user,
        organization=organization,
        role_title="CEO",
        location="london-UK",
        business_unit=bu,
    )
    EmployeeRepository.store(employee)
    retrieved_user1 = UserRepository.get_user_by_email(user.email)
    modified_user = User(
        first_name="Jane",
        last_name="Doe..",
        email=user.email,
    )
    employee.user = modified_user
    EmployeeRepository.store(employee)
    retrieved_user2 = UserRepository.get_user_by_email(user.email)
    assert retrieved_user1.first_name != retrieved_user2.first_name
    assert retrieved_user1.last_name != retrieved_user2.last_name
    assert retrieved_user1.email == retrieved_user2.email


def test_get_exiting_ids_by_email(cleanup_database, cleanup_media):
    first_email = "first@email.example"
    second_email = "second@email.example"
    third_email = "third@email.example"
    emails_list = [first_email, second_email, first_email, third_email]
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    first_employee = create_some_employee(
        email=first_email, organization_id=org.id, business_unit_id=bu.id
    )
    second_employee = create_some_employee(
        email=second_email, organization_id=org.id, business_unit_id=bu.id
    )
    data = EmployeeRepository.get_exiting_ids_by_email(
        emails=emails_list, organization_id=first_employee.organization_id
    )
    assert data == {first_email: first_employee.id, second_email: second_employee.id}
