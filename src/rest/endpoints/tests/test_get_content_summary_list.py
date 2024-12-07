from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_module,
    create_some_content_summary,
    create_some_employee,
    create_some_file,
    create_some_organization,
)
from rest.endpoints.tests.helpers import URLs, get_access_token


def test_get_content_summary_list(cleanup_media, cleanup_database, fast_client):
    file = create_some_file()
    assert isinstance(file.id, int)
    module = create_some_module(
        still_thumbnail_id=file.id,
        animated_thumbnail_id=file.id,
    )
    org = create_some_organization(logo_id=file.id)
    e = create_some_employee(organization_id=org.id)
    assert isinstance(module.id, int)
    [
        create_some_content_summary(module_id=module.id, title=f"Test Title {i}")
        for i in range(3)
    ]
    token = get_access_token(e.user)
    response = fast_client.get(
        url=URLs.content_summary.format(id=module.id), headers=dict(Authorization=token)
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["total_count"] == 3
    data = response.json()["result"]
    assert set(data[0].keys()) == {
        "id",
        "title",
        "description",
        "module_id",
        "created_at",
        "updated_at",
    }
