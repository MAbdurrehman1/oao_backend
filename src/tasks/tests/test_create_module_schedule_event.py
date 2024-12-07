from repository.tests.helpers import (
    create_some_organization,
    create_some_employee,
    create_some_employee_survey_campaign,
    get_campaign_participant_ids,
    create_some_module,
    create_some_module_schedule,
    create_some_file,
)
from ..create_module_schedule_event import CreateModuleScheduleTask


def test_create_module_event(
    cleanup_database, cleanup_media, cleanup_redis, mock_azure_requests
):
    file = create_some_file()
    assert isinstance(file.id, int)
    m = create_some_module(
        animated_thumbnail_id=file.id,
        still_thumbnail_id=file.id,
    )
    org = create_some_organization(logo_id=file.id)
    assert isinstance(org.id, int)
    e = create_some_employee(organization_id=org.id)
    assert isinstance(e.id, int)
    sc = create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e.id],
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(campaign_id=sc.id)[0]
    assert isinstance(m.id, int)
    ms = create_some_module_schedule(
        module_id=m.id,
        participation_id=p_id,
    )
    assert isinstance(ms.id, int)
    CreateModuleScheduleTask.execute(ms.id)
