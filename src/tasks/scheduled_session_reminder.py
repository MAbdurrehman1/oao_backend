import os
from uuid import UUID

from jinja2 import Template

from celery_app import celery_app
from cexceptions import MissingEntityException
from repository import (
    ReminderRepository,
    ParticipationRepository,
    OrganizationRepository,
    ModuleScheduleRepository,
    MailRepository,
)
from services import generate_magic_token
from settings import configs, ParticipationStatus, SOURCE_DIR
from utils.interfaces import AbstractRetryTask


def _get_email_template() -> Template:
    template_path = os.path.join(
        SOURCE_DIR, "templates", "scheduled_session_reminder_template.html"
    )
    with open(template_path, "r") as file:
        template_str = file.read()
        template = Template(template_str)
        return template


def send_participant_schedule_reminder_email(participation_id: UUID):
    survey_url = configs.participant_dashboard_url
    reschedule_url = configs.reschedule_session_url
    user = ParticipationRepository.get_user(participation_id=participation_id)
    assert isinstance(user.id, int)
    organization = OrganizationRepository.get_organization_by_user_id(user_id=user.id)
    next_session_datetime = ModuleScheduleRepository.get_next_session_date(
        participant_id=participation_id
    )
    next_session_date = next_session_datetime.strftime("%Y-%m-%d")
    next_session_time = next_session_datetime.strftime("%H:%M:%S")
    token = generate_magic_token(user_id=user.id)
    url_with_token = f"{survey_url}?token={token}"
    email_template = _get_email_template()
    rendered_html = email_template.render(
        first_name=user.first_name,
        survey_url=url_with_token,
        reschedule_url=reschedule_url,
        scheduled_date=next_session_date,
        scheduled_time=next_session_time,
        company_name=organization.company_name,
    )
    MailRepository.send_mail(
        sender_email="rene.eber@oao.co",
        recipients=[user.email],
        subject=f"Your OAO x {organization.company_name} Session Tomorrow",
        html_str=rendered_html,
    )
    ReminderRepository.store_success(
        postfix="scheduled_session:001:",
        identifier=participation_id,
    )


class ScheduledSessionReminderTask(AbstractRetryTask):
    postfix = "scheduled_session:001:"

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
            postfix="scheduled_session:001:"
        )
        notified_participation_ids = [UUID(item.split(":")[-1]) for item in keys]
        participation_ids = ParticipationRepository.get_scheduled_participants(
            after_hours=configs.scheduled_session_reminder_hand_off_hours,
            before_hours=configs.scheduled_session_reminder_before_hours,
            status=ParticipationStatus.SCHEDULED,
            exclude=notified_participation_ids,
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
def scheduled_session_reminder():
    ScheduledSessionReminderTask.execute()
