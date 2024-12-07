from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_employee,
    get_preferred_lang,
)
from rest.endpoints.tests.helpers import URLs, get_access_token
from settings import PreferredLang


def test_submit_preferred_lang(cleanup_media, cleanup_database, fast_client):
    e = create_some_employee()
    token = get_access_token(e.user)
    response = fast_client.post(
        url=URLs.preferred_lang,
        json=dict(lang=PreferredLang.french.value),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Preferred Language Submitted Successfully"}
    assert get_preferred_lang(e.id) == PreferredLang.french
