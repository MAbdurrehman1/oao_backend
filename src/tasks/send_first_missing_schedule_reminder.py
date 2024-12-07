import os
from datetime import datetime
from uuid import UUID

from jinja2 import Template

from celery_app import celery_app
from cexceptions import MissingEntityException
from repository import (
    ModuleScheduleRepository,
    OrganizationRepository,
    SurveyCampaignRepository,
    MailRepository,
    ReminderRepository,
    ParticipationRepository,
)
from services import generate_magic_token
from settings import configs, SOURCE_DIR, ParticipationStatus
from utils.interfaces import AbstractRetryTask


class SendFirstMissingScheduleReminderTask(AbstractRetryTask):
    postfix = "participant_missing_schedule:001:"

    @classmethod
    def translate_key_to_id(cls, key) -> UUID:
        return UUID(key.split(":")[-1])

    @staticmethod
    def _participation_id(*args, **kwargs) -> UUID:
        if "participation_id" in kwargs.keys():
            return kwargs["participation_id"]
        elif args:
            return args[0]
        else:
            raise MissingEntityException(
                entity="participation_id",
            )

    @classmethod
    def main(cls, *args, **kwargs):
        keys = ReminderRepository.get_successful_reminders(
            postfix="participant_missing_schedule:001:"
        )
        notified_participation_ids = [UUID(item.split(":")[-1]) for item in keys]
        participation_ids = ModuleScheduleRepository.get_schedule_missing_participants(
            after_hours=configs.first_missing_schedule_reminder_delay_hours,
            before_hours=configs.first_missing_schedule_reminder_hand_off_hours,
            status=ParticipationStatus.SCHEDULED,
            exclude=notified_participation_ids,
        )
        for participation_id in participation_ids:
            try:
                send_participation_schedule_reminder_email(participation_id)
            except Exception as e:
                cls._set_retry(identifier=participation_id)
                cls.catch_exceptions(e)

    @classmethod
    def single_item_retry(cls, *args, **kwargs):
        participation_id = cls._participation_id(*args, **kwargs)
        send_participation_schedule_reminder_email(participation_id=participation_id)


def _get_email_template() -> Template:
    template_path = os.path.join(
        SOURCE_DIR, "templates", "first_missing_schedule_reminder_template.html"
    )
    with open(template_path, "r") as file:
        template_str = file.read()
        template = Template(template_str)
        return template


def send_participation_schedule_reminder_email(participation_id: UUID):
    survey_url = configs.participant_dashboard_url
    user = ParticipationRepository.get_user(participation_id=participation_id)
    assert isinstance(user.id, int)
    organization = OrganizationRepository.get_organization_by_user_id(user_id=user.id)
    survey_end_date = SurveyCampaignRepository.get_end_date_by_participation_id(
        participation_id=participation_id
    )
    schedule_date: datetime = (
        ModuleScheduleRepository.get_last_scheduled_date_passed_participant_id(
            participant_id=participation_id,
        )
    )
    passed_time = datetime.now() - schedule_date
    passed_hours = int(passed_time.total_seconds() // 3600)
    token = generate_magic_token(user_id=user.id)
    url_with_token = f"{survey_url}?token={token}"
    email_template = _get_email_template()
    rendered_html = email_template.render(
        first_name=user.first_name,
        survey_url=url_with_token,
        company_name=organization.company_name,
        campaign_end_date=survey_end_date.strftime(configs.date_format),
        delay_hours=passed_hours,
    )
    MailRepository.send_mail(
        sender_email="rene.eber@oao.co",
        recipients=[user.email],
        subject="Not Decided Yet",
        html_str=rendered_html,
    )
    ReminderRepository.store_success(
        postfix="participant_missing_schedule:001:",
        identifier=participation_id,
    )


@celery_app.task
def send_first_missing_schedule_reminder_task():
    SendFirstMissingScheduleReminderTask.execute()
