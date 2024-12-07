from starlette.status import HTTP_200_OK

from repository.tests.helpers import create_some_file
from rest.endpoints.tests.helpers import URLs, get_admin_token


def test_create_organization(cleanup_database, cleanup_media, fast_client):
    file = create_some_file(user_email="test@example.com")
    token = get_admin_token()
    data = dict(
        company_name="CompanyName",
        hq_location="london-UK",
        size="50-100",
        industry="transportation",
        meta_data=dict(foo="bar"),
        logo_id=file.id,
    )
    response = fast_client.post(
        url=URLs.organization,
        headers=dict(Authorization=token),
        json=data,
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "organization created successfully"}
