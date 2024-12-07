from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_user,
    create_some_file,
    create_some_organization,
    create_some_management_position,
    create_some_business_unit,
    create_some_employee,
)
from rest.endpoints.tests.helpers import URLs, get_admin_token


def test_get_benchmark_categories_endpoint(
    fast_client, cleanup_media, cleanup_database
):
    u = create_some_user(
        email="file@example.com",
    )
    f = create_some_file(user_id=u.id)
    assert isinstance(f.id, int)
    org = create_some_organization(logo_id=f.id)
    assert isinstance(org.id, int)
    bu0 = create_some_business_unit(organization_id=org.id, name="node1")
    bu1 = create_some_business_unit(
        organization_id=org.id, name="node2", parent_id=bu0.id
    )
    bu2 = create_some_business_unit(
        organization_id=org.id, name="node3", parent_id=bu0.id
    )
    bu3 = create_some_business_unit(
        organization_id=org.id, name="node4", parent_id=bu1.id
    )
    bu4 = create_some_business_unit(
        organization_id=org.id, name="node5", parent_id=bu3.id
    )
    e = create_some_employee(
        organization_id=org.id,
        business_unit_id=bu1.id,
        email="test1@example.com",
    )
    assert isinstance(e.id, int)
    mp = create_some_management_position(
        organization_id=org.id,
        manager_ids=[e.id],
        role_ids=[bu1.id, bu2.id],  # type: ignore
    )
    token = get_admin_token()
    response = fast_client.get(
        url=URLs.benchmark_categories.format(id=mp.id),
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert len(data) == 2
    assert data[0]["business_unit"]["name"] == bu1.name
    assert data[0]["children"][0]["business_unit"]["name"] == bu3.name
    assert data[0]["children"][0]["children"][0]["business_unit"]["name"] == bu4.name
