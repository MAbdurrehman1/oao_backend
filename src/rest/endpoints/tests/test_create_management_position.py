from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_business_unit,
)
from rest.endpoints.tests.helpers import URLs, get_admin_token
from services.management_position_service import get_management_position_list


def test_create_management_position(cleanup_database, fast_client, cleanup_media):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    e = create_some_employee(
        email="test@example.com", organization_id=org.id, business_unit_id=bu.id
    )
    assert isinstance(e.id, int)
    assert isinstance(bu.id, int)
    mp_name = "management_position title"
    data = dict(name=mp_name, business_unit_ids=[bu.id])
    token = get_admin_token()
    response = fast_client.post(
        URLs.organization_management_positions.format(id=org.id),
        headers=dict(Authorization=token),
        json=data,
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Management Position Created Successfully"}
    total_count, mps = get_management_position_list(
        organization_id=org.id, offset=0, limit=100
    )
    assert total_count == 1
    assert len(mps) == 1
    assert mps[0].name == mp_name
    assert mps[0].role_ids is not None
    assert len(mps[0].role_ids) == 1
    assert mps[0].role_ids[0] == bu.id
