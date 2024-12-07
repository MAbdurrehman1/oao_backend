import os
from uuid import UUID

from jinja2 import Template

from celery_app import celery_app
from cexceptions import MissingEntityException
from repository import (
    ReminderRepository,
    ParticipationRepository,
    OrganizationRepository,
    SurveyCampaignRepository,
    MailRepository,
)
from services import generate_magic_token
from settings import configs, ParticipationStatus, SOURCE_DIR
from utils.interfaces import AbstractRetryTask


def _get_email_template() -> Template:
    template_path = os.path.join(
        SOURCE_DIR, "templates", "second_scheduling_delay_reminder_template.html"
    )
    with open(template_path, "r") as file:
        template_str = file.read()
        template = Template(template_str)
        return template


def send_participant_schedule_reminder_email(participation_id: UUID):
    survey_url = configs.participant_dashboard_url
    user = ParticipationRepository.get_user(participation_id=participation_id)
    assert isinstance(user.id, int)
    organization = OrganizationRepository.get_organization_by_user_id(user_id=user.id)
    survey_end_date = SurveyCampaignRepository.get_end_date_by_participation_id(
        participation_id=participation_id
    )
    token = generate_magic_token(user_id=user.id)
    url_with_token = f"{survey_url}?token={token}"
    email_template = _get_email_template()
    rendered_html = email_template.render(
        first_name=user.first_name,
        survey_url=url_with_token,
        company_name=organization.company_name,
        campaign_end_date=survey_end_date.strftime(configs.date_format),
    )
    MailRepository.send_mail(
        sender_email="rene.eber@oao.co",
        recipients=[user.email],
        subject="Schedule Your OAO x"
        f" {organization.company_name} Training Sessions Now",
        html_str=rendered_html,
    )
    ReminderRepository.store_success(
        postfix="participant_scheduling:002:",
        identifier=participation_id,
    )


class SendSecondParticipantScheduleReminderTask(AbstractRetryTask):
    postfix = "participant_scheduling:002:"

    @classmethod
    def translate_key_to_id(cls, key) -> UUID:
        _id = UUID(key.split(":")[-1])
        return _id

    @staticmethod
    def _get_participant_id(*args, **kwargs) -> UUID:
        if "participant_id" in kwargs.keys():
            return kwargs["participant_id"]
        elif args:
            return args[0]
        else:
            raise MissingEntityException(
                entity="participant_id",
            )

    @classmethod
    def main(cls, *args, **kwargs):
        keys = ReminderRepository.get_successful_reminders(
            postfix="participant_scheduling:002:"
        )
        notified_participation_ids = [UUID(item.split(":")[-1]) for item in keys]
        participation_ids = ParticipationRepository.get_participants_before_end_date(
            before_hours=configs.second_participant_schedule_reminder_before_hours,
            status=ParticipationStatus.INVITED,
            exclude=notified_participation_ids,
            min_campaign_length_hours=configs.second_reminder_campaign_length_hours,
        )
        for participation_id in participation_ids:
            try:
                send_participant_schedule_reminder_email(participation_id)
            except Exception as e:
                cls._set_retry(identifier=participation_id)
                cls.catch_exceptions(e)

    @classmethod
    def single_item_retry(cls, *args, **kwargs):
        participant_id = cls._get_participant_id(*args, **kwargs)
        send_participant_schedule_reminder_email(participation_id=participant_id)


@celery_app.task
def send_second_participant_schedule_reminder_task():
    SendSecondParticipantScheduleReminderTask.execute()
