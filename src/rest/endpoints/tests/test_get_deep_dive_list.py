from starlette.status import HTTP_200_OK

from repository.tests.helpers import (
    create_some_employee,
    create_some_deep_dive,
    create_some_employee_survey_campaign,
    get_campaign_participant_ids,
    store_deep_dive_strategy,
)
from rest.endpoints.tests.helpers import URLs, get_access_token


def test_get_deep_dive_list(cleanup_database, cleanup_media, fast_client):
    e = create_some_employee()
    sc = create_some_employee_survey_campaign(
        organization_id=e.organization_id,
        participant_ids=[e.id],
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(campaign_id=sc.id)[0]
    store_deep_dive_strategy(
        participation_id=p_id,
        slug_list=["test_deep_dive_1", "test_deep_dive_2"],
    )
    [
        create_some_deep_dive(
            title=f"some title {i}",
            file_user_id=e.user.id,
            file_name=f"some_file_{i}.png",
        )
        for i in range(3)
    ]
    [
        create_some_deep_dive(
            title=f"test_deep_dive_{i}_title",
            file_user_id=e.user.id,
            file_name=f"test_deep_dive_{i}_file.png",
            slug=f"test_deep_dive_{i}",
        )
        for i in range(3)
    ]
    token = get_access_token(e.user)
    response = fast_client.get(
        url=URLs.deep_dive + f"?participation_id={p_id}",
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["total_count"] == 5
    data = response.json()["result"]
    assert len(data) == 5
    assert set(data[0].keys()) == {
        "id",
        "title",
        "slug",
        "description",
        "url",
        "created_at",
        "updated_at",
    }
