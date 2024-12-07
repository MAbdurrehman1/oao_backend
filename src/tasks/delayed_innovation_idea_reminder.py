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
from settings import ParticipationStatus, SOURCE_DIR, configs
from utils.interfaces import AbstractRetryTask


class DelayedInnovationIdeaReminderTask(AbstractRetryTask):
    postfix = "delayed_innovation_idea_reminder:001:"

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
            postfix="delayed_innovation_idea_reminder:001:"
        )
        notified_participation_ids = [UUID(item.split(":")[-1]) for item in keys]
        participation_ids = ParticipationRepository.get_idea_delayed_participants(
            after_hours=configs.delayed_innovation_idea_reminder_delay_hours,
            before_hours=configs.delayed_innovation_idea_reminder_hand_off_hours,
            status=ParticipationStatus.RESPONDED,
            exclude=notified_participation_ids,
        )
        for participation_id in participation_ids:
            try:
                send_participation_idea_submission_reminder_email(participation_id)
            except Exception as e:
                cls._set_retry(identifier=participation_id)
                cls.catch_exceptions(e)

    @classmethod
    def single_item_retry(cls, *args, **kwargs):
        participation_id = cls._participation_id(*args, **kwargs)
        send_participation_idea_submission_reminder_email(
            participation_id=participation_id
        )


def _get_email_template() -> Template:
    template_path = os.path.join(
        SOURCE_DIR, "templates", "delayed_innovation_idea_reminder_template.html"
    )
    with open(template_path, "r") as file:
        template_str = file.read()
        template = Template(template_str)
        return template


def send_participation_idea_submission_reminder_email(participation_id: UUID):
    idea_url = configs.innovation_idea_submission_url
    user = ParticipationRepository.get_user(participation_id=participation_id)
    assert isinstance(user.id, int)
    organization = OrganizationRepository.get_organization_by_user_id(user_id=user.id)
    survey_end_date = SurveyCampaignRepository.get_end_date_by_participation_id(
        participation_id=participation_id
    )
    token = generate_magic_token(user_id=user.id)
    url_with_token = f"{idea_url}?token={token}"
    email_template = _get_email_template()
    rendered_html = email_template.render(
        first_name=user.first_name,
        innovation_idea_submission_url=url_with_token,
        company_name=organization.company_name,
        campaign_end_date=survey_end_date.strftime(configs.date_format),
    )
    MailRepository.send_mail(
        sender_email="rene.eber@oao.co",
        recipients=[user.email],
        subject=f"Action Needed: Submit Your"
        f" Innovation Idea for OAO x {organization.company_name}",
        html_str=rendered_html,
    )
    ReminderRepository.store_success(
        postfix="delayed_innovation_idea_reminder:001:",
        identifier=participation_id,
    )


@celery_app.task
def delayed_innovation_idea_reminder_task():
    DelayedInnovationIdeaReminderTask.execute()
