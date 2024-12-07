from starlette.status import HTTP_200_OK

from repository.tests.helpers import create_some_employee
from rest.endpoints.tests.helpers import get_access_token
from .helpers import URLs


def _assert_correctness(response_data: dict):
    assert set(response_data.keys()) == {
        "first_name",
        "last_name",
        "email",
        "user_id",
        "location",
        "role_title",
        "employee_id",
        "organization_name",
        "organization_logo_url",
        "organization_id",
        "participation_id",
    }


def test_get_auth_employee_data(fast_client, cleanup_database, cleanup_media):
    employee = create_some_employee(is_admin=True)
    token = get_access_token(employee.user)
    response = fast_client.get(
        url=URLs.auth_employee,
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    _assert_correctness(data)
