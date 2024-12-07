from starlette.status import HTTP_200_OK

from repository.management_position_repository import ManagementPositionRepository
from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_business_unit,
    create_some_management_position,
)
from rest.endpoints.tests.helpers import get_admin_token, URLs


def test_update_management_position_details(
    cleanup_database, fast_client, cleanup_media
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    e = create_some_employee(
        email="test1@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    assert isinstance(e.id, int)
    assert isinstance(bu.id, int)
    mp = create_some_management_position(
        manager_ids=[e.id],
        name="Test Position",
        role_ids=[bu.id],
        organization_id=org.id,
    )
    assert isinstance(mp.id, int)
    updated_name = "Post update name"
    data = dict(name=updated_name)
    token = get_admin_token()
    response = fast_client.put(
        URLs.update_management_position.format(
            organization_id=org.id, position_id=mp.id
        ),
        headers=dict(Authorization=token),
        json=data,
    )
    assert response.status_code == HTTP_200_OK
    result = response.json()["result"]
    assert result == "Position Updated Successfully"
    retrieved_mp = ManagementPositionRepository.get(_id=mp.id)
    assert retrieved_mp.name == updated_name
