from uuid import uuid4, UUID

from repository import (
    CeleryRetryRepository,
    ParticipationRepository,
    SurveyCampaignRepository,
)
from repository.tests.helpers import (
    create_some_employee_survey_campaign,
    create_some_organization,
    create_some_employee,
    get_campaign_participant_ids,
)
from settings import ParticipationStatus
from ..send_survey_campaign_emails import (
    SendSurveyCampaignEmailsTask,
    send_individual_campaign_email,
)


def test_send_survey_campaign_emails(
    cleanup_database, cleanup_redis, mock_azure_requests, cleanup_media
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    employee = create_some_employee(organization_id=org.id, email="example@email.com")
    campaign = create_some_employee_survey_campaign(
        organization_id=org.id, participant_ids=[employee.id]
    )
    assert isinstance(campaign.id, int)
    SendSurveyCampaignEmailsTask.execute(campaign.id)
    participants_data = SurveyCampaignRepository.get_participants_data(
        survey_campaign_id=campaign.id
    )
    assert len(participants_data.keys()) == 1
    status = ParticipationRepository.get_status(
        _id=UUID(list(participants_data.keys())[0])
    )
    assert status == ParticipationStatus.INVITED


def _assert_retry_state(
    expected_retry_count: int, campaign_id: int, participation_id: UUID
):
    failed_emails = CeleryRetryRepository.get_batch_keys(
        postfix="survey_campaign_emails:", batch_id=campaign_id
    )
    assert len(failed_emails) == 1
    assert int(failed_emails[0].split(":")[2]) == campaign_id
    assert UUID(failed_emails[0].split(":")[-1]) == participation_id
    retry_count = CeleryRetryRepository.get_retry_count(
        postfix="survey_campaign_emails:",
        identifier=f"{campaign_id}:{participation_id}",
    )
    assert retry_count == expected_retry_count


def _assert_deleted_state(campaign_id: int, participation_id: UUID):
    failed_emails = CeleryRetryRepository.get_batch_keys(
        postfix="survey_campaign_emails:",
        batch_id=campaign_id,
    )
    assert failed_emails == []
    archived_failed_emails = CeleryRetryRepository.get_archived_batch_keys(
        postfix="survey_campaign_emails:",
        batch_id=campaign_id,
    )
    assert len(archived_failed_emails) == 1
    assert int(archived_failed_emails[0].split(":")[3]) == campaign_id
    assert UUID(archived_failed_emails[0].split(":")[-1]) == participation_id


def test_retry_send_participant_email(cleanup_database, mock_send_mail, cleanup_redis):
    participation_id = uuid4()
    campaign_id = 1
    CeleryRetryRepository.set_retry_count(
        postfix="survey_campaign_emails:",
        identifier=f"{campaign_id}:{participation_id}",
    )
    _assert_retry_state(
        expected_retry_count=0,
        campaign_id=campaign_id,
        participation_id=participation_id,
    )
    SendSurveyCampaignEmailsTask.batch_id = campaign_id
    SendSurveyCampaignEmailsTask._retry()
    _assert_deleted_state(campaign_id=campaign_id, participation_id=participation_id)


def test_send_individual_campaign_email(
    cleanup_database, mock_send_mail, cleanup_redis, cleanup_media
):
    org = create_some_organization()
    assert isinstance(org.id, int)
    employee = create_some_employee(
        organization_id=org.id, email="sorkhemiri@gmail.com"
    )
    campaign = create_some_employee_survey_campaign(
        organization_id=org.id, participant_ids=[employee.id]
    )
    assert isinstance(campaign.id, int)
    p_id = get_campaign_participant_ids(campaign_id=campaign.id)[0]
    send_individual_campaign_email(participation_id=p_id)
    participants_data = SurveyCampaignRepository.get_participants_data(
        survey_campaign_id=campaign.id
    )
    assert len(participants_data.keys()) == 1
    status = ParticipationRepository.get_status(
        _id=UUID(list(participants_data.keys())[0])
    )
    assert status == ParticipationStatus.INVITED
