from starlette.status import HTTP_200_OK

from entity import User
from rest.endpoints.tests.helpers import URLs, get_admin_token
from repository.tests.helpers import (
    create_some_employee,
    create_some_management_position,
    create_some_organization,
    create_some_business_unit,
)
from services import get_management_position_details


def test_add_management_position_manager(
    cleanup_database,
    fast_client,
    cleanup_media,
    cleanup_redis,
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    assert isinstance(bu.id, int)
    employee1 = create_some_employee(
        organization_id=org.id, email="test1@example.com", business_unit_id=bu.id
    )
    mp = create_some_management_position(
        organization_id=org.id, manager_ids=[], role_ids=[bu.id]
    )
    assert isinstance(employee1.id, int)
    assert isinstance(mp.id, int)
    assert isinstance(employee1.user, User)
    data = dict(employee_email=employee1.user.email)
    token = get_admin_token()
    response = fast_client.post(
        url=URLs.management_position_add_manager.format(
            organization_id=org.id, position_id=mp.id
        ),
        headers=dict(Authorization=token),
        json=data,
    )
    response_data = response.json()["result"]
    assert response_data == "Manager Added Successfully"
    assert response.status_code == HTTP_200_OK
    retrieved_mp = get_management_position_details(position_id=mp.id)
    assert retrieved_mp.manager_ids is not None
    assert len(retrieved_mp.manager_ids) == 1
    assert employee1.id in retrieved_mp.manager_ids
    # hitting api one more time to make sure it won't falsly duplicate a manager
    response = fast_client.post(
        url=URLs.management_position_add_manager.format(
            organization_id=org.id, position_id=mp.id
        ),
        headers=dict(Authorization=token),
        json=data,
    )
    response_data = response.json()["result"]
    assert response_data == "Manager Added Successfully"
    assert response.status_code == HTTP_200_OK
    retrieved_mp = get_management_position_details(position_id=mp.id)
    assert retrieved_mp.manager_ids is not None
    assert len(retrieved_mp.manager_ids) == 1
