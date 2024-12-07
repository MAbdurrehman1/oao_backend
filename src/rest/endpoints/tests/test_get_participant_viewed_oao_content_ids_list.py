from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_employee,
    create_some_file,
    create_some_deep_dive,
    create_some_oao_content,
    create_some_employee_survey_campaign,
    get_campaign_participant_ids,
    create_some_oao_content_view,
)
from rest.endpoints.tests.helpers import get_access_token, URLs


def test_get_participant_viewed_oao_content_ids_list(
    cleanup_media, cleanup_database, fast_client
):
    e = create_some_employee()
    file = create_some_file(user_id=e.user_id)
    assert isinstance(file.id, int)
    deep_dive = create_some_deep_dive(thumbnail_id=file.id)
    assert isinstance(deep_dive.id, int)
    content = create_some_oao_content(deep_dive_id=deep_dive.id, thumbnail_id=file.id)
    sc = create_some_employee_survey_campaign(
        organization_id=e.organization_id,
        participant_ids=[e.id],
    )
    assert isinstance(sc.id, int)
    assert isinstance(content.id, int)
    p_id = get_campaign_participant_ids(campaign_id=sc.id)[0]
    create_some_oao_content_view(
        content_id=content.id,
        participation_id=p_id,
    )
    token = get_access_token(e.user)
    response = fast_client.get(
        url=URLs.oao_content_view_list,
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json()["result"], list)
