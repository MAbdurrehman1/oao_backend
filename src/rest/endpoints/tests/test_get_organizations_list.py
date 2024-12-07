from starlette.status import HTTP_200_OK

from repository.tests.helpers import create_some_organization
from .helpers import URLs, get_admin_token


def test_get_organizations_list(fast_client, cleanup_database, cleanup_media):
    create_some_organization(
        company_name="Test Company",
        industry="Test Industry",
        size="50-100",
        hq_location="Test HQ Location",
        meta_data={"test_key": "test_value"},
    )
    token = get_admin_token()
    response = fast_client.get(URLs.organization, headers=dict(Authorization=token))
    assert response.status_code == HTTP_200_OK
    assert response.json()["total_count"] == 1
    data = response.json()["result"]
    assert len(data) == 1
    assert set(data[0].keys()) == {
        "id",
        "company_name",
        "industry",
        "hq_location",
        "size",
        "logo_url",
        "meta_data",
        "created_at",
        "updated_at",
    }


def test_get_organizations_list_does_not_return_more_than_50_results(
    fast_client, cleanup_database, cleanup_media
):
    for i in range(100):
        create_some_organization(
            company_name=f"Test{i+1}",
            logo_user_email=f"test{i}@example.com",
            logo_name=f"logo_{i}.png",
        )
    token = get_admin_token()
    response = fast_client.get(
        URLs.organization,
        params=dict(limit=100, offset=0),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert len(response.json()["result"]) == 50
