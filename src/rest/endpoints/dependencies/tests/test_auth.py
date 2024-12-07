import pytest
from fastapi import FastAPI, Depends
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_200_OK
from starlette.testclient import TestClient

from ..auth import AdminRequired, EmployeeRequired
from utils.error_handler import (
    setup_exception_handlers,
)
from repository.tests.helpers import (
    create_some_user,
    create_some_employee,
    create_some_organization,
    create_some_business_unit,
)
from services.auth_service import create_access_token
from entity import User
from rest.error_handler import exception_handlers


def get_test_client():
    app = FastAPI()
    setup_exception_handlers(app, handlers=exception_handlers)

    @app.get("/admin")
    def some_admin_endpoint(
        _: User = Depends(AdminRequired()),
    ):
        return {"result": "Success"}

    @app.get("/check-impersonation")
    def some_impersonation_endpoint(
        user: User = Depends(EmployeeRequired()),
    ):
        return {"first name": user.first_name}

    client = TestClient(app)
    return client


def test_admin_required_with_no_header():
    client = get_test_client()
    res = client.get("/admin", headers={})
    assert res.status_code == HTTP_400_BAD_REQUEST
    assert res.json() == {"error": "Authorization Header must be provided."}


def test_admin_required_with_invalid_header():
    client = get_test_client()
    res = client.get("/admin", headers={"Authorization": "Bearer Invalid Token"})
    assert res.status_code == HTTP_403_FORBIDDEN
    assert res.json() == {"error": "Token is invalid."}


@pytest.mark.parametrize(
    "is_admin, expected_status,expected_message",
    [
        (
            False,
            HTTP_403_FORBIDDEN,
            {"error": "user is not authorized to visit the content."},
        ),
        (True, HTTP_200_OK, {"result": "Success"}),
    ],
)
def test_admin_required_with_not_admin_token(
    cleanup_database, is_admin, expected_status, expected_message
):
    user = create_some_user(is_admin=is_admin)
    token = create_access_token(identifier=user.email)
    client = get_test_client()
    res = client.get("/admin", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == expected_status
    assert res.json() == expected_message


def test_admin_impersonation(cleanup_database):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    assert isinstance(bu.id, int)
    employee1 = create_some_employee(
        email="test1@example.com",
        is_admin=True,
        organization_id=org.id,
        business_unit_id=bu.id,
    )
    employee2 = create_some_employee(
        first_name="TestName",
        email="test2@example.com",
        organization_id=org.id,
        business_unit_id=bu.id,
    )
    token = create_access_token(identifier=employee1.user.email)
    client = get_test_client()
    res = client.get(
        "/check-impersonation", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == HTTP_200_OK
    assert res.json() == {"first name": "John"}
    res = client.get(
        "/check-impersonation?impersonation=true",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == HTTP_400_BAD_REQUEST
    assert res.json() == {"error": "User ID must be provided."}
    res = client.get(
        f"/check-impersonation?impersonation=true&user_id={employee2.user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == HTTP_200_OK
    assert res.json() == {"first name": "TestName"}
