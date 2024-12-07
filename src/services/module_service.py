from uuid import UUID

from celery_app import celery_app
from cexceptions import NotFoundException
from entity import Module
from repository import (
    ModuleRepository,
    EmployeeRepository,
    ParticipationRepository,
    UserRepository,
)
from settings import ParticipationStatus


def get_modules_list(offset: int, limit: int, user_id: int) -> tuple[int, list[Module]]:
    employee_id = EmployeeRepository.get_employee_id_by_user_id(user_id=user_id)
    survey_end_date = ParticipationRepository.employee_survey_campaign_end_date(
        employee_id=employee_id
    )
    total_count, modules = ModuleRepository.get_list(
        offset=offset,
        limit=limit,
    )
    for module in modules:
        module.end_date = survey_end_date
    return total_count, modules


def get_modules_urls(user_id: int) -> tuple[int, dict]:
    participant_id = ParticipationRepository.get_participation_id_by_user_id(
        user_id=user_id
    )
    employee_id = EmployeeRepository.get_employee_id_by_user_id(
        user_id=user_id,
    )
    email = UserRepository.get_email_by_user_id(_id=user_id)
    last_order = ModuleRepository.get_last_order(participation_id=participant_id)
    module_urls = ModuleRepository.get_modules_data_until_order(order=last_order + 1)
    preferred_lang = EmployeeRepository.get_preferred_lang(employee_id=employee_id)
    module_urls = {
        order: (
            f"{data['url']}/{preferred_lang.value}/?"  # type: ignore
            f"module_id={data['id']}"  # type: ignore
            f"&participation_id={participant_id}"
            f"&email={email}"
            f"&fullscreen"
        )
        for order, data in module_urls.items()
    }
    return last_order, module_urls


def create_module_answer(module_id: int, participation_id: UUID):
    if not ParticipationRepository.exists(_id=participation_id):
        raise NotFoundException(
            entity="Participation",
            arg="ID",
            value=str(participation_id),
        )

    if not ModuleRepository.exists(_id=module_id):
        raise NotFoundException(
            entity="Module",
            arg="ID",
            value=str(module_id),
        )
    if ModuleRepository.is_last_module(_id=module_id):
        ParticipationRepository.update_status(
            _id=participation_id, status=ParticipationStatus.RESPONDED
        )
        celery_app.send_task(
            "tasks.create_deep_dive_list.create_deep_dive_list_task",
            args=[participation_id],
        )
    ModuleRepository.store_module_answer(
        participation_id=participation_id, module_id=module_id
    )
    last_order = ModuleRepository.get_last_answered_module_order(
        participation_id=participation_id,
    )
    ModuleRepository.update_last_order(
        participation_id=participation_id,
        last_answered_module_order=last_order,
    )
