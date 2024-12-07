import os.path
from datetime import datetime
from uuid import UUID

from jinja2 import Template


from celery_app import celery_app
from cexceptions import MissingEntityException
from entity import User, Organization
from repository import (
    CeleryRetryRepository,
    ParticipationRepository,
    SurveyCampaignRepository,
    CeleryTaskRepository,
    OrganizationRepository,
)
from repository.mail_repository import MailRepository
from services import generate_magic_token
from settings import SOURCE_DIR, configs, ParticipationStatus
from utils.interfaces import AbstractRetryTask


def _get_email_template() -> Template:
    template_path = os.path.join(
        SOURCE_DIR, "templates", "survey_campaign_email_template.html"
    )
    with open(template_path, "r") as file:
        template_str = file.read()
        template = Template(template_str)
        return template


def send_participant_email(
    survey_url: str,
    participant: User,
    organization: Organization,
    survey_end_date: datetime,
):
    assert isinstance(participant.id, int)
    token = generate_magic_token(user_id=participant.id)
    url_with_token = f"{survey_url}?token={token}"
    email_template = _get_email_template()
    rendered_html = email_template.render(
        first_name=participant.first_name,
        last_name=participant.last_name,
        survey_url=survey_url,
        url_with_token=url_with_token,
        company_name=organization.company_name,
        survey_campaign_end_date=survey_end_date.strftime(configs.date_format),
    )
    MailRepository.send_mail(
        sender_email=configs.email_sender_address,
        recipients=[participant.email],
        subject=f"Welcome to the OAO x {organization.company_name} "
        f"Program! - Scheduling of sessions and OAO Portal access",
        html_str=rendered_html,
    )


def _archive_failed_participation(participation_id: UUID, campaign_id: int) -> None:
    CeleryRetryRepository.archive_failed_attempt(
        postfix="survey_campaign_emails:",
        identifier=f"{campaign_id}:{participation_id}",
    )
    ParticipationRepository.update_status(
        _id=participation_id, status=ParticipationStatus.FAILED
    )


def _get_email_context(
    campaign_id: int, participation_id: UUID
) -> tuple[User, Organization, str, datetime]:
    user: User = SurveyCampaignRepository.get_participant_data(
        participant_id=participation_id
    )
    assert isinstance(user.id, int)
    survey_end_date: datetime = SurveyCampaignRepository.get_end_date(_id=campaign_id)
    organization: Organization = OrganizationRepository.get_organization_by_user_id(
        user_id=user.id
    )
    survey_url = configs.participant_dashboard_url
    return user, organization, survey_url, survey_end_date


def _submit_successful_invite(participation_id: UUID) -> None:
    ParticipationRepository.update_status(
        _id=participation_id, status=ParticipationStatus.INVITED
    )


class SendSurveyCampaignEmailsTask(AbstractRetryTask):
    postfix = "survey_campaign_emails:"

    @classmethod
    def translate_key_to_id(cls, key) -> str:
        participation_id = UUID(key.split(":")[-1])
        campaign_id = int(key.split(":")[-2])
        return f"{campaign_id}:{participation_id}"

    @staticmethod
    def _get_campaign_id(*args, **kwargs) -> int:
        if "campaign_id" in kwargs.keys():
            return kwargs["campaign_id"]
        elif args:
            return args[0]
        else:
            raise MissingEntityException(
                entity="campaign_id",
            )

    @classmethod
    def _unpack_identifiers(cls, key: str) -> tuple[int, UUID]:
        campaign_id, participant_id = key.split(":")
        return int(campaign_id), UUID(participant_id)

    @classmethod
    def _get_campaign_identifiers(cls, *args, **kwargs) -> tuple[int, UUID]:
        if "key" in kwargs.keys():
            key = kwargs["key"]
            return cls._unpack_identifiers(key)
        elif args:
            key = args[0]
            return cls._unpack_identifiers(key)
        else:
            raise MissingEntityException(
                entity="Key",
            )

    @classmethod
    def main(cls, *args, **kwargs):
        campaign_id = cls._get_campaign_id(*args, **kwargs)
        CeleryTaskRepository.remove_task_id(
            post_fix="survey_campaign:send_email_task:",
            identifier=campaign_id,
        )
        survey_url = configs.participant_dashboard_url
        organization = OrganizationRepository.get_organization_by_campaign_id(
            campaign_id=campaign_id
        )
        survey_end_date = SurveyCampaignRepository.get_end_date(_id=campaign_id)
        participants_data = SurveyCampaignRepository.get_participants_data(
            survey_campaign_id=campaign_id
        )
        for key, value in participants_data.items():
            try:
                send_participant_email(
                    survey_url=survey_url,
                    participant=value,
                    organization=organization,
                    survey_end_date=survey_end_date,
                )
                _submit_successful_invite(participation_id=UUID(key))
            except Exception as e:
                cls._set_retry(identifier=f"{campaign_id}:{key}")
                cls.catch_exceptions(e)

    @classmethod
    def single_item_retry(cls, *args, **kwargs):
        campaign_id, participation_id = cls._get_campaign_identifiers(*args, **kwargs)
        user, organization, survey_url, survey_end_date = _get_email_context(
            participation_id=participation_id, campaign_id=campaign_id
        )
        send_participant_email(
            participant=user,
            organization=organization,
            survey_url=survey_url,
            survey_end_date=survey_end_date,
        )
        _submit_successful_invite(participation_id=participation_id)


@celery_app.task
def send_survey_campaign_emails_task(campaign_id: int):
    task = SendSurveyCampaignEmailsTask
    task.batch_id = campaign_id
    task.execute(campaign_id)


def send_individual_campaign_email(participation_id: UUID):
    campaign_id = ParticipationRepository.get_campaign_id(
        participation_id=participation_id
    )
    user, organization, survey_url, survey_end_date = _get_email_context(
        participation_id=participation_id,
        campaign_id=campaign_id,
    )
    send_participant_email(
        participant=user,
        survey_url=survey_url,
        organization=organization,
        survey_end_date=survey_end_date,
    )
    _submit_successful_invite(participation_id=participation_id)


@celery_app.task
def send_individual_campaign_email_task(campaign_id: int, participation_id: UUID):
    try:
        send_individual_campaign_email(participation_id=participation_id)
    except Exception:
        CeleryRetryRepository.set_retry_count(
            postfix="survey_campaign_emails:",
            identifier=f"{campaign_id}:{participation_id}",
        )
