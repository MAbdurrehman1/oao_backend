from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from repository.tests.helpers import (
    create_some_file,
    create_some_organization,
    create_some_employee,
    create_some_deep_dive,
    create_some_information_library,
    create_some_library_content,
)
from rest.endpoints.tests.helpers import URLs, get_access_token


def test_get_library_content_list(cleanup_media, cleanup_database, fast_client):
    file = create_some_file()
    org1 = create_some_organization(logo_id=file.id)
    org2 = create_some_organization(logo_id=file.id)
    dd = create_some_deep_dive(thumbnail_id=file.id)
    assert isinstance(dd.id, int)
    assert isinstance(file.id, int)
    il = create_some_information_library(deep_dive_id=dd.id, organization_id=org1.id)
    assert isinstance(il.id, int)
    [
        create_some_library_content(
            library_id=il.id,
            title="Test Title {i}",
            thumbnail_id=file.id,
        )
        for i in range(5)
    ]
    e1 = create_some_employee(
        email="test1@example.com",
        organization_id=org1.id,
    )
    e2 = create_some_employee(
        email="test2@example.com",
        organization_id=org2.id,
    )

    token1 = get_access_token(e1.user)
    response1 = fast_client.get(
        url=URLs.library_content.format(id=il.id), headers=dict(Authorization=token1)
    )
    assert response1.status_code == HTTP_200_OK
    assert response1.json()["total_count"] == 5
    data = response1.json()["result"]
    assert len(data) == 5
    assert set(data[0].keys()) == {
        "id",
        "title",
        "description",
        "thumbnail_url",
        "content_url",
        "information_library_id",
        "created_at",
        "updated_at",
    }

    token2 = get_access_token(e2.user)
    response2 = fast_client.get(
        url=URLs.library_content.format(id=il.id), headers=dict(Authorization=token2)
    )
    assert response2.status_code == HTTP_400_BAD_REQUEST
