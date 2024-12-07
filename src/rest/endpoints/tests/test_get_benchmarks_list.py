from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_file,
    create_some_organization,
    create_some_business_unit,
    create_some_employee,
    create_some_employee_survey_campaign,
    get_campaign_participant_ids,
    change_participant_status,
    create_some_management_position,
    create_some_report,
)
from rest.endpoints.tests.data_samples import REPORT_KPI_DATA
from rest.endpoints.tests.helpers import get_etl_token, URLs, get_access_token
from settings import ParticipationStatus


def test_get_benchmarks_list(cleanup_media, cleanup_database, fast_client):
    f = create_some_file()
    o = create_some_organization(logo_id=f.id)
    assert isinstance(o.id, int)
    bu1 = create_some_business_unit(organization_id=o.id, name="origin", parent_id=None)
    bu2 = create_some_business_unit(organization_id=o.id, name="sub1", parent_id=bu1.id)
    bu3 = create_some_business_unit(organization_id=o.id, name="sub2", parent_id=bu1.id)
    bu4 = create_some_business_unit(
        organization_id=o.id, name="sub1-sub1", parent_id=bu2.id
    )
    bu5 = create_some_business_unit(
        organization_id=o.id, name="sub2-sub1", parent_id=bu3.id
    )
    e1 = create_some_employee(
        organization_id=o.id, business_unit_id=bu1.id, email="test1@example.com"
    )
    e2 = create_some_employee(
        organization_id=o.id, business_unit_id=bu2.id, email="test2@example.com"
    )
    e3 = create_some_employee(
        organization_id=o.id, business_unit_id=bu3.id, email="test3@example.com"
    )
    e4 = create_some_employee(
        organization_id=o.id, business_unit_id=bu4.id, email="test4@example.com"
    )
    e5 = create_some_employee(
        organization_id=o.id, business_unit_id=bu5.id, email="test5@example.com"
    )
    e6 = create_some_employee(
        organization_id=o.id, business_unit_id=bu4.id, email="test6@example.com"
    )
    e7 = create_some_employee(
        organization_id=o.id, business_unit_id=bu5.id, email="test7@example.com"
    )
    e8 = create_some_employee(
        organization_id=o.id, business_unit_id=bu3.id, email="test8@example.com"
    )
    e9 = create_some_employee(
        organization_id=o.id, business_unit_id=bu2.id, email="test9@example.com"
    )
    sc = create_some_employee_survey_campaign(
        start_date=datetime.now() - timedelta(days=10),
        end_date=datetime.now() - timedelta(days=1),
        organization_id=o.id,
        participant_ids=[e2.id, e3.id, e4.id, e5.id, e6.id, e7.id, e8.id, e9.id],
    )
    assert isinstance(sc.id, int)
    pid_list = get_campaign_participant_ids(campaign_id=sc.id)
    [
        change_participant_status(
            participant_id=pid, status=ParticipationStatus.IDEA_SUBMITTED
        )
        for pid in pid_list
    ]
    mp = create_some_management_position(
        organization_id=o.id,
        role_ids=[bu2.id, bu3.id],  # type: ignore
        manager_ids=[
            e1.id,
        ],
    )
    assert isinstance(mp.id, int)
    r = create_some_report(
        position_id=mp.id,
    )
    benchmarks = [
        dict(
            business_unit_id=bu2.id,
            kpi_data=REPORT_KPI_DATA,
        ),
        dict(
            business_unit_id=bu3.id,
            kpi_data=REPORT_KPI_DATA,
        ),
    ]
    etl_token = get_etl_token()
    response = fast_client.post(
        url=URLs.benchmarks.format(id=r.id),
        json=dict(benchmarks=benchmarks),
        headers=dict(Authorization=etl_token),
    )
    assert response.status_code == HTTP_200_OK
    manager_token = get_access_token(e1.user)
    response = fast_client.get(
        url=URLs.benchmarks.format(id=r.id),
        headers=dict(Authorization=manager_token),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert len(data) == 2
    names = [item["name"] for item in data]
    assert set(names) == {"sub1", "sub2"}
