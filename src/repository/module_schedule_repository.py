from copy import deepcopy
from datetime import datetime
from uuid import UUID

from cexceptions import NotFoundException
from entity import ModuleSchedule, Module, Participant, Employee, User
from repository.queries import (
    UPSERT_MODULE_SCHEDULE,
    GET_MODULE_SCHEDULE,
    STORE_MODULE_SCHEDULE_EVENT_ID,
    GET_MODULE_SCHEDULES_BY_PARTICIPATION_ID,
    CHECK_PARTICIPANT_SCHEDULED_ALL,
    GET_SCHEDULE_MISSING_PARTICIPANTS,
    GET_LAST_SCHEDULED_DATE_PASSED_PARTICIPANT_ID,
    GET_FIRST_SCHEDULED_DATE_AHEAD_PARTICIPANT_ID,
)
from settings import ParticipationStatus
from settings.connections import postgres_connection_manager


def _enrich_module_schedule(data: dict) -> ModuleSchedule:
    module = Module(
        id=data["module_id"],
        title=data["module_title"],
        description=data["module_description"],
        duration=data["module_duration"],
        order=data["module_order"],
    )
    user = User(
        id=data["user_id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
    )
    employee = Employee(
        id=data["employee_id"],
        role_title=data["role_title"],
        location=data["location"],
        user=user,
    )
    participant = Participant(
        status=ParticipationStatus.INVITED,
        employee=employee,
    )
    return ModuleSchedule(
        id=data["id"],
        ms_graph_event_id=data["ms_graph_event_id"],
        selected_date=data["selected_date"],
        module=module,
        participant=participant,
    )


def enrich_module_schedules_minimal(data: dict) -> ModuleSchedule:
    return ModuleSchedule(
        id=data["id"],
        selected_date=data["selected_date"],
        module_id=data["module_id"],
        participation_id=data["participation_id"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


class ModuleScheduleRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def store(cls, module_schedule: ModuleSchedule) -> ModuleSchedule:
        result = cls.connection_manager.execute_atomic_query(
            query=UPSERT_MODULE_SCHEDULE,
            variables=(
                str(module_schedule.participation_id),
                str(module_schedule.module_id),
                module_schedule.selected_date,
            ),
        )
        result_module_schedule = deepcopy(module_schedule)
        result_module_schedule.id = result["id"]
        result_module_schedule.created_at = result["created_at"]
        result_module_schedule.updated_at = result["updated_at"]
        return result_module_schedule

    @classmethod
    def get(cls, _id: int) -> ModuleSchedule:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_MODULE_SCHEDULE,
            variables=(_id,),
        )
        if not result:
            raise NotFoundException(
                entity="Module Schedule",
                arg="ID",
                value=str(_id),
            )
        return _enrich_module_schedule(result)

    @classmethod
    def get_last_scheduled_date_passed_participant_id(
        cls, participant_id: UUID
    ) -> datetime:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_LAST_SCHEDULED_DATE_PASSED_PARTICIPANT_ID,
            variables=(participant_id,),
        )
        if not result:
            raise NotFoundException(
                entity="Module Schedule",
                arg="Participant ID",
                value=str(participant_id),
            )
        return result["selected_date"]

    @classmethod
    def get_next_session_date(cls, participant_id: UUID) -> datetime:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_FIRST_SCHEDULED_DATE_AHEAD_PARTICIPANT_ID,
            variables=(participant_id,),
        )
        if not result:
            raise NotFoundException(
                entity="Module Schedule",
                arg="Participant ID",
                value=str(participant_id),
            )
        return result["selected_date"]

    @classmethod
    def store_event_id(cls, _id: int, event_id: str):
        cls.connection_manager.execute_atomic_query(
            query=STORE_MODULE_SCHEDULE_EVENT_ID,
            variables=(event_id, _id),
        )

    @classmethod
    def get_list_by_participation_id(
        cls, participation_id: UUID
    ) -> list[ModuleSchedule]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_MODULE_SCHEDULES_BY_PARTICIPATION_ID,
            variables=(participation_id,),
        )
        if not result:
            return []

        return [enrich_module_schedules_minimal(item) for item in result]

    @classmethod
    def did_schedule_all(cls, participation_id: UUID) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_PARTICIPANT_SCHEDULED_ALL,
            variables=(str(participation_id),),
        )
        return result["responded_all"]

    @classmethod
    def get_schedule_missing_participants(
        cls,
        before_hours: int,
        after_hours: int,
        status: ParticipationStatus,
        exclude: list[UUID],
    ) -> list[UUID]:
        query = GET_SCHEDULE_MISSING_PARTICIPANTS
        variables = [
            after_hours,
            before_hours,
            status.value,
        ]
        if exclude:
            query += " AND sce.participation_id NOT IN %s"
            exclude_ids = tuple([str(item) for item in exclude])
            variables.append(exclude_ids)
        result = cls.connection_manager.execute_atomic_query_all(
            query=query,
            variables=tuple(variables),
        )
        if not result:
            return []
        return [item["participation_id"] for item in result]
