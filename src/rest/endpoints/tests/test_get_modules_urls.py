from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_module,
    create_some_organization,
    create_some_employee,
    create_some_employee_survey_campaign,
    get_campaign_participant_ids,
    create_some_module_response,
    create_some_file,
)
from rest.endpoints.tests.helpers import get_access_token, URLs


def test_get_modules_urls(cleanup_media, cleanup_database, fast_client):
    file = create_some_file()
    assert isinstance(file.id, int)
    modules = [
        create_some_module(
            still_thumbnail_id=file.id,
            animated_thumbnail_id=file.id,
            title=f"Test Title {i + 1}",
            order=i + 1,
            url=f"http://example.come/{i}",
        )
        for i in range(3)
    ]
    org = create_some_organization(logo_id=file.id)
    e = create_some_employee(organization_id=org.id)

    sc = create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e.id],
        start_date=datetime.now() - timedelta(days=2),
        end_date=datetime.now() + timedelta(days=5),
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(campaign_id=sc.id)[0]
    create_some_module_response(
        participation_id=p_id,
        module_id=modules[0].id,  # type: ignore
    )
    create_some_module_response(
        participation_id=p_id,
        module_id=modules[1].id,  # type: ignore
    )
    token = get_access_token(e.user)
    response = fast_client.get(
        url=URLs.module_url,
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["passed_order"] == 2
    data = response.json()["result"]
    assert set(data[0].keys()) == {
        "order",
        "url",
    }
