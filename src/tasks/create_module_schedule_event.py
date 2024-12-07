from datetime import timedelta

from celery_app import celery_app
from cexceptions import MissingEntityException
from entity import CalendarEvent, Module, Participant, Employee, User
from repository import (
    CeleryTaskRepository,
    ModuleScheduleRepository,
    CalendarRepository,
)
from settings import configs
from utils.interfaces import AbstractRetryTask


def create_event(module_schedule_id: int):
    module_schedule = ModuleScheduleRepository.get(_id=module_schedule_id)
    assert isinstance(module_schedule.module, Module)
    assert isinstance(module_schedule.participant, Participant)
    assert isinstance(module_schedule.participant.employee, Employee)
    assert isinstance(module_schedule.participant.employee.user, User)
    calendar_event = CalendarEvent(
        id=module_schedule.ms_graph_event_id,
        start_date=module_schedule.selected_date,
        end_date=(
            module_schedule.selected_date
            + timedelta(seconds=60 * module_schedule.module.duration)
        ),
        description=module_schedule.module.description,
        title="OAO Training Session",
        event_url=configs.attend_module_event_url,
        reschedule_url=configs.reschedule_module_event_url.format(
            module_id=module_schedule.module_id
        ),
        attendees=[
            module_schedule.participant.employee.user,
        ],
    )
    if module_schedule.ms_graph_event_id:
        calendar_event.title = "Updated Event: OAO Training Session"
        CalendarRepository.update_event(calendar_event=calendar_event)
    else:
        stored_calendar_event = CalendarRepository.create_event(
            calendar_event=calendar_event
        )
        assert isinstance(stored_calendar_event.id, str)
        assert isinstance(module_schedule.id, int)
        ModuleScheduleRepository.store_event_id(
            event_id=stored_calendar_event.id, _id=module_schedule.id
        )


class CreateModuleScheduleTask(AbstractRetryTask):
    postfix = "module_schedules:"

    @classmethod
    def translate_key_to_id(cls, key) -> int:
        _id = int(key.split(":")[-1])
        return _id

    @staticmethod
    def _get_module_schedule_id(*args, **kwargs) -> int:
        if "module_schedule_id" in kwargs.keys():
            return kwargs["module_schedule_id"]
        elif args:
            return args[0]
        else:
            raise MissingEntityException(
                entity="module_schedule_id",
            )

    @classmethod
    def main(cls, *args, **kwargs):
        module_schedule_id = cls._get_module_schedule_id(*args, **kwargs)
        CeleryTaskRepository.remove_task_id(
            post_fix="module:schedule_module_task:",
            identifier=module_schedule_id,
        )
        try:
            create_event(module_schedule_id=module_schedule_id)
        except Exception as e:
            cls._set_retry(identifier=module_schedule_id)
            cls.catch_exceptions(e)

    @classmethod
    def single_item_retry(cls, *args, **kwargs):
        module_schedule_id = cls._get_module_schedule_id(*args, **kwargs)
        create_event(module_schedule_id)


@celery_app.task
def create_module_schedule_event_task(module_schedule_id: int):
    CreateModuleScheduleTask.execute(module_schedule_id)
