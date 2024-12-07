from datetime import datetime, timedelta
from uuid import UUID

from repository import ReminderRepository
from repository.tests.helpers import (
    create_some_employee,
    create_some_employee_survey_campaign,
    get_campaign_participant_ids,
    change_participant_status,
    create_some_module,
    create_some_file,
    create_some_module_schedule,
    create_some_organization,
)
from settings import ParticipationStatus
from ..send_first_missing_schedule_reminder import (
    SendFirstMissingScheduleReminderTask,
)


def test_send_second_participant_schedule_reminder(
    cleanup_database,
    cleanup_redis,
    cleanup_media,
    mock_azure_requests,
):
    f = create_some_file()
    assert isinstance(f.id, int)
    o = create_some_organization(logo_id=f.id)
    e = create_some_employee(organization_id=o.id)
    start_date = datetime.now() - timedelta(days=14)
    end_date = datetime.now() + timedelta(days=5)
    sc = create_some_employee_survey_campaign(
        organization_id=e.organization_id,
        participant_ids=[
            e.id,
        ],
        start_date=start_date,
        end_date=end_date,
    )
    m = create_some_module(
        still_thumbnail_id=f.id,
        animated_thumbnail_id=f.id,
        order=1,
    )
    assert isinstance(m.id, int)
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(sc.id)[0]
    create_some_module_schedule(
        module_id=m.id,
        participation_id=p_id,
        selected_date=datetime.now() - timedelta(days=1),
    )
    change_participant_status(
        participant_id=p_id,
        status=ParticipationStatus.SCHEDULED,
    )
    SendFirstMissingScheduleReminderTask.execute()
    key = ReminderRepository.get_successful_reminders(
        postfix="participant_missing_schedule:001:",
    )[0]
    reminder_id = UUID(key.split(":")[-1])
    assert reminder_id == p_id
