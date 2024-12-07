from starlette.status import HTTP_200_OK

from repository.tests.helpers import create_some_user
from .helpers import URLs


def test_send_magic_link(mock_send_mail, cleanup_redis, cleanup_database, fast_client):
    email = "test@example.com"
    create_some_user(email=email)
    response = fast_client.post(url=URLs.magic_link, json=dict(email=email))
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Magic Link sent Successfully"}
