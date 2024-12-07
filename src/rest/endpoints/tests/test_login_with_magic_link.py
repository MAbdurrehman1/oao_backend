from starlette.status import HTTP_200_OK

from repository.tests.helpers import create_some_user, set_magic_link_token
from rest.endpoints.tests.helpers import URLs


def test_login_with_magic_link(cleanup_database, cleanup_redis, fast_client):
    email = "test@example.com"
    create_some_user(email=email)
    token = set_magic_link_token(email=email)
    response = fast_client.post(url=URLs.magic_link_login, json=dict(token=str(token)))
    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert set(data.keys()) == {"access_token", "refresh_token"}
