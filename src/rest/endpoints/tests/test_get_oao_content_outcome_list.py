from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_employee,
    create_some_file,
    create_some_deep_dive,
    create_some_oao_content,
    create_some_outcome,
)
from rest.endpoints.tests.helpers import URLs, get_access_token


def test_get_oao_content_outcome_list(
    cleanup_media,
    cleanup_database,
    fast_client,
):
    thumbnail = create_some_file()
    assert isinstance(thumbnail.id, int)
    e = create_some_employee()
    dd = create_some_deep_dive(thumbnail_id=thumbnail.id)
    assert isinstance(dd.id, int)
    content = create_some_oao_content(deep_dive_id=dd.id, thumbnail_id=thumbnail.id)
    assert isinstance(content.id, int)
    [
        create_some_outcome(oao_content_id=content.id, title=f"Test Title {i}")
        for i in range(3)
    ]
    token = get_access_token(e.user)
    response = fast_client.get(
        url=URLs.oao_content_outcome.format(id=content.id),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["total_count"] == 3
    data = response.json()["result"]
    assert len(data) == 3
    assert set(data[0].keys()) == {
        "id",
        "title",
        "description",
        "oao_content_id",
        "created_at",
        "updated_at",
    }
