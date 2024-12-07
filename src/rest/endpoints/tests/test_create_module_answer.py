from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_module,
    create_some_organization,
    create_some_employee,
    create_some_employee_survey_campaign,
    get_campaign_participant_ids,
    create_some_file,
)
from rest.endpoints.tests.helpers import get_etl_token, URLs


def test_get_modules_urls(cleanup_media, cleanup_database, fast_client):
    file = create_some_file()
    assert isinstance(file.id, int)
    modules = [
        create_some_module(
            title=f"Test Title {i + 1}",
            order=i + 1,
            url=f"http://example.come/{i}",
            still_thumbnail_id=file.id,
            animated_thumbnail_id=file.id,
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
    token = get_etl_token()
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(campaign_id=sc.id)[0]
    response = fast_client.post(
        url=URLs.module_answer.format(id=modules[0].id),
        headers=dict(Authorization=token),
        json=dict(participation_id=str(p_id)),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "Module answer created successfully."}
