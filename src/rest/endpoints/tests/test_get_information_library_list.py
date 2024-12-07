from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_file,
    create_some_organization,
    create_some_employee,
    create_some_deep_dive,
    create_some_information_library,
)
from rest.endpoints.tests.helpers import get_access_token, URLs


def test_get_information_library_list(
    cleanup_media,
    cleanup_database,
    fast_client,
):
    logo = create_some_file()
    org1 = create_some_organization(company_name="Test 1", logo_id=logo.id)
    org2 = create_some_organization(company_name="Test 2", logo_id=logo.id)
    e1 = create_some_employee(
        email="test1@test.com",
        organization_id=org1.id,
    )
    e2 = create_some_employee(email="test2@test.com", organization_id=org2.id)
    deep_dive = create_some_deep_dive(thumbnail_id=logo.id)
    assert isinstance(deep_dive.id, int)
    create_some_information_library(title="Test 1", deep_dive_id=deep_dive.id)
    create_some_information_library(
        title="Test 1",
        deep_dive_id=deep_dive.id,
        organization_id=org2.id,
    )
    token_1 = get_access_token(e1.user)
    response_1 = fast_client.get(
        url=URLs.information_library.format(id=deep_dive.id),
        headers=dict(Authorization=token_1),
    )
    assert response_1.status_code == HTTP_200_OK
    data_1 = response_1.json()["result"]
    assert response_1.json()["total_count"] == 1
    assert len(data_1) == 1
    assert set(data_1[0].keys()) == {
        "id",
        "title",
        "short_description",
        "long_description",
        "organization_id",
        "deep_dive_id",
        "created_at",
        "updated_at",
    }

    token_2 = get_access_token(e2.user)
    response_2 = fast_client.get(
        url=URLs.information_library.format(id=deep_dive.id),
        headers=dict(Authorization=token_2),
    )
    assert response_2.status_code == HTTP_200_OK
    data_2 = response_2.json()["result"]
    assert response_2.json()["total_count"] == 2
    assert len(data_2) == 2
    assert set(data_2[0].keys()) == {
        "id",
        "title",
        "short_description",
        "long_description",
        "organization_id",
        "deep_dive_id",
        "created_at",
        "updated_at",
    }
