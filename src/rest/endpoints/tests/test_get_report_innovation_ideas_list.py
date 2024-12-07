from datetime import datetime, timedelta

import httpx
from starlette.status import HTTP_200_OK

from entity import Employee, Report, User

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_business_unit,
    create_some_employee_survey_campaign,
    create_some_innovation_idea,
    get_campaign_participant_ids,
    create_some_management_position,
    create_some_report,
    add_participants_to_report,
    publish_report,
    rate_idea,
)
from .helpers import URLs, get_access_token, get_admin_token


def _create_innovation_idea_for_report(
    publish: bool,
    mock_rate: int | None = None,
    report: Report | None = None,
    is_manager_admin: bool = False,
) -> tuple[Report, Employee]:
    domain = "example2" if report else "example"
    org = create_some_organization(
        logo_user_email=f"test@{domain}.com", logo_name=f"{domain}.png"
    )
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id)
    e1 = create_some_employee(
        email=f"test1@{domain}.com",
        organization_id=org.id,
        business_unit_id=bu.id,
    )
    e2 = create_some_employee(
        email=f"test2@{domain}.com",
        organization_id=org.id,
        business_unit_id=bu.id,
        is_admin=is_manager_admin,
    )
    assert isinstance(bu.id, int)
    assert isinstance(e1.id, int)
    assert isinstance(e2.id, int)
    sc = create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e1.id],
        start_date=datetime.now() - timedelta(days=365),
        end_date=datetime.now() - timedelta(days=20),
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(
        campaign_id=sc.id,
    )[0]
    ii = create_some_innovation_idea(participation_id=p_id)
    assert isinstance(ii.id, int)
    if mock_rate:
        rate_idea(idea_id=ii.id, manager_id=e2.id, rate=mock_rate)
    mp = create_some_management_position(
        organization_id=org.id, manager_ids=[e2.id], role_ids=[bu.id], name=domain
    )
    assert isinstance(mp.id, int)
    if report:
        r = report
    else:
        r = create_some_report(position_id=mp.id)
    assert isinstance(r.id, int)
    add_participants_to_report(report_id=r.id, participation_ids=[p_id])
    if publish:
        publish_report(report_id=r.id)
    return r, e2


def _assert_response_data(response: httpx.Response):
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert len(data) == 1
    assert response.json()["total_count"] == 1
    assert set(data[0].keys()) == {
        "title",
        "description",
        "feasibility_score",
        "confidence_score",
        "impact_score",
        "participation_id",
        "participant_first_name",
        "participant_last_name",
        "participant_email",
        "id",
        "rate",
        "created_at",
        "updated_at",
    }


def test_get_report_innovation_ideas_list_with_rated_idea(
    cleanup_database, fast_client, cleanup_media
):
    report, manager = _create_innovation_idea_for_report(publish=True, mock_rate=1)
    assert isinstance(manager.user, User)
    manager_token = get_access_token(manager.user)
    response = fast_client.get(
        url=URLs.report_ideas.format(id=report.id),
        headers=dict(Authorization=manager_token),
    )
    _assert_response_data(response=response)


def test_get_report_innovation_ideas_list(cleanup_database, fast_client, cleanup_media):
    report, manager = _create_innovation_idea_for_report(publish=True)
    assert isinstance(manager.user, User)
    manager_token = get_access_token(manager.user)
    response = fast_client.get(
        url=URLs.report_ideas.format(id=report.id),
        headers=dict(Authorization=manager_token),
    )
    _assert_response_data(response=response)


def test_get_report_innovation_ideas_list_as_admin(
    cleanup_database, fast_client, cleanup_media
):
    report, _ = _create_innovation_idea_for_report(publish=False)
    admin_token = get_admin_token()
    response = fast_client.get(
        url=URLs.report_ideas.format(id=report.id),
        headers=dict(Authorization=admin_token),
    )
    _assert_response_data(response=response)


def test_get_report_innovation_ideas_with_rate_list(
    cleanup_database, fast_client, cleanup_media
):
    mock_rate = 3
    r, e2 = _create_innovation_idea_for_report(publish=True, mock_rate=mock_rate)
    assert isinstance(e2.user, User)
    manager_token = get_access_token(e2.user)
    response = fast_client.get(
        url=URLs.report_ideas.format(id=r.id),
        headers=dict(Authorization=manager_token),
        params=dict(rate=mock_rate),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert len(data) == 1
    assert response.json()["total_count"] == 1
    assert data[0]["rate"] == mock_rate

    # testing with rate = 1
    response = fast_client.get(
        url=URLs.report_ideas.format(id=r.id),
        headers=dict(Authorization=manager_token),
        params=dict(rate=1),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert len(data) == 0
    assert response.json()["total_count"] == 0


def test_get_report_unrated_innovation_ideas_list(
    cleanup_database, fast_client, cleanup_media
):
    # create one idea for testing
    r, e2 = _create_innovation_idea_for_report(publish=True, mock_rate=None)
    # creating another idea rated by another user
    # to make sure query is working as expected
    _create_innovation_idea_for_report(publish=True, mock_rate=1, report=r)
    assert isinstance(e2.user, User)
    manager_token = get_access_token(e2.user)
    response = fast_client.get(
        url=URLs.report_ideas.format(id=r.id),
        headers=dict(Authorization=manager_token),
        params=dict(unrated=True),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert len(data) == 2
    assert response.json()["total_count"] == 2
    assert data[0]["rate"] is None

    assert isinstance(e2.id, int)
    rate_idea(idea_id=data[0]["id"], manager_id=e2.id, rate=2)
    # testing after rating
    response = fast_client.get(
        url=URLs.report_ideas.format(id=r.id),
        headers=dict(Authorization=manager_token),
        params=dict(unrated=True),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert len(data) == 1
    assert response.json()["total_count"] == 1


def test_get_report_unrated_innovation_ideas_list_as_admin(
    cleanup_database, fast_client, cleanup_media
):
    # create one idea for testing, manager is an admin
    r, e2 = _create_innovation_idea_for_report(
        publish=True, mock_rate=None, is_manager_admin=True
    )
    # creating another idea rated by another user
    # to make sure query is working as expected
    _create_innovation_idea_for_report(publish=True, mock_rate=1, report=r)
    assert isinstance(e2.user, User)
    # this is not a typo, e2 is an admin
    admin_token = get_access_token(e2.user)
    response = fast_client.get(
        url=URLs.report_ideas.format(id=r.id),
        headers=dict(Authorization=admin_token),
        params=dict(unrated=True),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert len(data) == 2
    assert response.json()["total_count"] == 2
    assert data[0]["rate"] is None

    assert isinstance(e2.id, int)
    rate_idea(idea_id=data[0]["id"], manager_id=e2.id, rate=2)
    # testing after rating
    response = fast_client.get(
        url=URLs.report_ideas.format(id=r.id),
        headers=dict(Authorization=admin_token),
        params=dict(unrated=True),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert response.json()["total_count"] == 1
