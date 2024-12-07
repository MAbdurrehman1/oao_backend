from repository.tests.helpers import (
    create_some_business_unit,
    create_some_organization,
    create_some_file,
    create_some_user,
)
from .helpers import get_admin_token, URLs


def test_get_business_units_tree(fast_client, cleanup_database, cleanup_media):
    u = create_some_user(
        email="file@example.com",
    )
    f = create_some_file(user_id=u.id)
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

    token = get_admin_token()
    response = fast_client.get(
        URLs.organization_business_units.format(id=org.id),
        headers=dict(Authorization=token),
    )
    result = response.json()["result"]
    assert result["business_unit"]["name"] == bu0.name
    assert result["children"][0]["business_unit"]["name"] == bu1.name
    assert result["children"][1]["business_unit"]["name"] == bu2.name
    assert result["children"][0]["children"][0]["business_unit"]["name"] == bu3.name
    assert (
        result["children"][0]["children"][0]["children"][0]["business_unit"]["name"]
        == bu4.name
    )


def test_get_empty_business_units_tree(fast_client, cleanup_database):
    org = create_some_organization()
    assert isinstance(org.id, int)
    token = get_admin_token()
    response = fast_client.get(
        URLs.organization_business_units.format(id=org.id),
        headers=dict(Authorization=token),
    )
    assert response.json() == dict(result=None)
