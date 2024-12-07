from datetime import datetime
from uuid import UUID

from celery_app import celery_app
from cexceptions import (
    NotFoundException,
    LessThanOrEqualException,
    GreaterThanOrEqualException,
)
from entity import ModuleSchedule
from repository import (
    ModuleRepository,
    ParticipationRepository,
    EmployeeRepository,
    ModuleScheduleRepository,
    CeleryTaskRepository,
)
from settings import configs, ParticipationStatus
from utils.validation_helpers import string_to_date


def _selected_date_validation(selected_date: datetime, user_id: int):
    employee_id = EmployeeRepository.get_employee_id_by_user_id(user_id=user_id)
    survey_campaign_end_date = (
        ParticipationRepository.employee_survey_campaign_end_date(
            employee_id=employee_id
        )
    )
    if survey_campaign_end_date < selected_date:
        raise LessThanOrEqualException(
            first_entity="Selected Date",
            second_entity="Survey Campaign end date",
        )
    if datetime.now() > selected_date:
        raise GreaterThanOrEqualException(
            first_entity="Selected Date",
            second_entity="Current Time",
        )


def _set_async_task(module_schedule_id: int):
    task_id = CeleryTaskRepository.get_task_id(
        post_fix="module:schedule_module_task:", identifier=module_schedule_id
    )
    if task_id is not None:
        assert isinstance(task_id, UUID)
        celery_app.control.revoke(task_id, terminate=True)
    task = celery_app.send_task(
        "tasks.create_module_schedule_event.create_module_schedule_event_task",
        args=[module_schedule_id],
    )
    CeleryTaskRepository.set_task_id(
        post_fix="module:schedule_module_task:",
        identifier=module_schedule_id,
        task_id=task.id,
    )


def _change_status_to_scheduled(participation_id: UUID):
    if ModuleScheduleRepository.did_schedule_all(
        participation_id=participation_id,
    ):
        ParticipationRepository.update_status(
            _id=participation_id, status=ParticipationStatus.SCHEDULED
        )


def upsert_module_schedule(
    user_id: int,
    module_id: int,
    selected_date_str: str,
) -> ModuleSchedule:
    selected_date = string_to_date(selected_date_str, configs.date_time_format)
    if not ModuleRepository.exists(_id=module_id):
        raise NotFoundException(entity="Module", arg="ID", value=str(module_id))
    participation_id = ParticipationRepository.get_participation_id_by_user_id(
        user_id=user_id
    )
    _selected_date_validation(selected_date=selected_date, user_id=user_id)
    module_schedule = ModuleSchedule(
        participation_id=participation_id,
        selected_date=selected_date,
        module_id=module_id,
    )
    stored_module_schedule = ModuleScheduleRepository.store(
        module_schedule=module_schedule
    )
    assert isinstance(stored_module_schedule.id, int)
    _set_async_task(module_schedule_id=stored_module_schedule.id)
    _change_status_to_scheduled(participation_id=participation_id)
    return stored_module_schedule


def get_module_schedules_list(user_id: int) -> list[ModuleSchedule]:
    participation_id = ParticipationRepository.get_participation_id_by_user_id(
        user_id=user_id
    )
    schedules = ModuleScheduleRepository.get_list_by_participation_id(
        participation_id=participation_id
    )
    return schedules
