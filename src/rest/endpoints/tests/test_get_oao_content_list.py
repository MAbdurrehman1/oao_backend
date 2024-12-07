from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_deep_dive,
    create_some_file,
    create_some_employee,
    create_some_oao_content,
)
from rest.endpoints.tests.helpers import URLs, get_access_token


def test_get_oao_content_list(cleanup_media, cleanup_database, fast_client):
    e = create_some_employee()
    file = create_some_file(user_id=e.user_id)
    assert isinstance(file.id, int)
    deep_dive = create_some_deep_dive(thumbnail_id=file.id)
    assert isinstance(deep_dive.id, int)
    create_some_oao_content(deep_dive_id=deep_dive.id, thumbnail_id=file.id)
    token = get_access_token(e.user)
    response = fast_client.get(
        url=URLs.oao_content.format(id=deep_dive.id), headers=dict(Authorization=token)
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["total_count"] == 1
    data = response.json()["result"]
    assert len(data) == 1
    assert set(data[0].keys()) == {
        "id",
        "title",
        "short_description",
        "long_description",
        "content_url",
        "thumbnail_url",
        "deep_dive_id",
        "created_at",
        "updated_at",
    }
