from starlette.status import HTTP_200_OK

from repository.tests.helpers import create_some_file
from .helpers import URLs, get_admin_token


def test_get_files_list(fast_client, cleanup_database, cleanup_media):
    create_some_file(name="Test File", user_email="test_get_files_list@email.com")
    token = get_admin_token()
    response = fast_client.get(URLs.files, headers=dict(Authorization=token))
    assert response.status_code == HTTP_200_OK
    assert response.json()["total_count"] == 1
    data = response.json()["result"]
    assert len(data) == 1
    assert set(data[0].keys()) == {
        "id",
        "name",
        "user_id",
        "file_url",
        "content_type",
        "created_at",
        "updated_at",
    }


def test_get_files_list_does_not_return_more_than_50_results(
    fast_client, cleanup_database, cleanup_media
):
    for i in range(100):
        create_some_file(
            name=f"Test{i+1}",
            user_email=f"test{i}@example.com",
        )
    token = get_admin_token()
    response = fast_client.get(
        URLs.files,
        params=dict(limit=100, offset=0),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert len(response.json()["result"]) == 50
