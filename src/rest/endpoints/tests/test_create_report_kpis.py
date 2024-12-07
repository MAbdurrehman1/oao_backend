from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_management_position,
    create_some_report,
    create_some_business_unit,
)
from rest.endpoints.tests.helpers import URLs, get_etl_token
from .data_samples import REPORT_KPI_DATA


def test_create_report_kpis(cleanup_database, fast_client, cleanup_media):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    e = create_some_employee(
        email="test@example.com", organization_id=org.id, business_unit_id=bu.id
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
    r = create_some_report(position_id=mp.id)
    token = get_etl_token()
    data = dict(
        kpi_data=REPORT_KPI_DATA,
    )
    response = fast_client.post(
        URLs.report_kpis.format(id=r.id),
        headers=dict(Authorization=token),
        json=data,
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Report KPIs Created Successfully"}
