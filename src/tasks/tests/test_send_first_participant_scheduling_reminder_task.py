from datetime import datetime, timedelta
from uuid import UUID

from repository import ReminderRepository
from repository.tests.helpers import (
    create_some_employee,
    create_some_employee_survey_campaign,
    get_campaign_participant_ids,
    change_participant_status,
)
from settings import ParticipationStatus
from ..send_first_participant_scheduling_reminder import (
    SendFirstParticipantSchedulingReminderTask,
)


def test_send_participant_scheduling_reminder(
    cleanup_database,
    cleanup_redis,
    cleanup_media,
    mock_azure_requests,
):
    e = create_some_employee()
    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now() + timedelta(days=5)
    sc = create_some_employee_survey_campaign(
        organization_id=e.organization_id,
        participant_ids=[
            e.id,
        ],
        start_date=start_date,
        end_date=end_date,
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(sc.id)[0]
    change_participant_status(
        participant_id=p_id,
        status=ParticipationStatus.INVITED,
    )
    SendFirstParticipantSchedulingReminderTask.execute()
    key = ReminderRepository.get_successful_reminders(
        postfix="participant_scheduling:001:",
    )[0]
    reminder_id = UUID(key.split(":")[-1])
    assert reminder_id == p_id
