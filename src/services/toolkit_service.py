from celery_app import celery_app
from cexceptions import ValidationException


def run_task(slug, *args):
    task_mapping = dict(
        first_participant_scheduling_reminder="tasks"
        ".send_first_participant_scheduling_reminder"
        ".send_first_participant_scheduling_reminder_task",
    )
    task_name = task_mapping.get(slug)
    if not task_name:
        raise ValidationException(
            entities="slug",
            values=str(slug),
        )
    celery_app.send_task(
        task_name,
        args=[*args],
    )
