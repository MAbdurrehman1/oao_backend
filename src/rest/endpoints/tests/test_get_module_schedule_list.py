from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_employee_survey_campaign,
    create_some_module,
    create_some_module_schedule,
    get_campaign_participant_ids,
    create_some_file,
)
from rest.endpoints.tests.helpers import get_access_token, URLs


def test_get_module_schedule_list(cleanup_database, cleanup_media, fast_client):
    file = create_some_file()
    assert isinstance(file.id, int)
    org = create_some_organization(logo_id=file.id)
    assert isinstance(org.id, int)
    e = create_some_employee(
        organization_id=org.id,
        email="sorkhemiri@gmail.com",
    )
    assert isinstance(e.id, int)
    sc = create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e.id],
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(campaign_id=sc.id)[0]
    m = create_some_module(
        still_thumbnail_id=file.id,
        animated_thumbnail_id=file.id,
    )
    assert isinstance(m.id, int)
    create_some_module_schedule(
        module_id=m.id,
        participation_id=p_id,
    )
    token = get_access_token(e.user)
    response = fast_client.get(
        url=URLs.module_schedule_list, headers=dict(Authorization=token)
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert len(data) == 1
    assert set(data[0].keys()) == {
        "id",
        "participation_id",
        "module_id",
        "selected_date",
        "created_at",
        "updated_at",
    }
