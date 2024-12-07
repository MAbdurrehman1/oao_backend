from datetime import datetime, timedelta
from uuid import UUID

from repository import ReminderRepository
from repository.tests.helpers import (
    create_some_file,
    create_some_organization,
    create_some_employee,
    create_some_employee_survey_campaign,
    get_campaign_participant_ids,
    create_some_module,
    create_some_module_response,
    change_participant_status,
    update_module_answer_updated_at,
)
from settings import ParticipationStatus
from ..delayed_innovation_idea_reminder import DelayedInnovationIdeaReminderTask


def test_delayed_innovation_idea(
    cleanup_database,
    cleanup_media,
    mock_azure_requests,
    cleanup_redis,
):
    f = create_some_file()
    assert isinstance(f.id, int)
    o = create_some_organization(logo_id=f.id)
    assert isinstance(o.id, int)
    e = create_some_employee(organization_id=o.id)
    m = create_some_module(
        order=1,
        still_thumbnail_id=f.id,
        animated_thumbnail_id=f.id,
    )
    assert isinstance(m.id, int)
    sc = create_some_employee_survey_campaign(
        participant_ids=[e.id],
        organization_id=o.id,
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(campaign_id=sc.id)[0]
    create_some_module_response(
        participation_id=p_id,
        module_id=m.id,
    )
    change_participant_status(
        participant_id=p_id,
        status=ParticipationStatus.RESPONDED,
    )
    update_module_answer_updated_at(
        module_id=m.id,
        participation_id=p_id,
        updated_at=datetime.now() - timedelta(days=1),
    )
    DelayedInnovationIdeaReminderTask.execute()
    key = ReminderRepository.get_successful_reminders(
        postfix="delayed_innovation_idea_reminder:001:",
    )[0]
    reminder_id = UUID(key.split(":")[-1])
    assert reminder_id == p_id
