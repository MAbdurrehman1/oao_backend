from datetime import datetime
from uuid import UUID

from cexceptions import NotFoundException, ValidationException
from entity import Participant, User, Employee, BusinessUnit
from .queries import (
    UPDATE_PARTICIPATION_STATUS,
    GET_PARTICIPATION_STATUS,
    GET_SURVEY_CAMPAIGN_PARTICIPANTS,
    ORDER_BY_UPDATED_AT,
    OFFSET_AND_LIMIT,
    GET_SURVEY_CAMPAIGNS_PARTICIPANT_IDS,
    CHECK_PARTICIPATION_BELONGS_TO_USER,
    FILTER_USERS_WITH_SURVEY_CAMPAIGN,
    CHECK_PARTICIPATION_ID_EXISTS,
    GET_PARTICIPATION_ID_BY_USER_ID,
    GET_CAMPAIGN_ID_BY_PARTICIPATION_ID,
    GET_INVITED_PARTICIPATION_IDS_AFTER_DATE,
    GET_USER_BY_PARTICIPATION_ID,
    GET_PARTICIPATION_IDS_BEFORE_DATE,
    GET_IDEA_DELAYED_PARTICIPANTS,
    GET_SCHEDULED_PARTICIPANTS,
)
from settings import ParticipationStatus
from settings.connections import postgres_connection_manager
from .queries import (
    UPSERT_PARTICIPANT_TO_SURVEY_CAMPAIGN,
    CHECK_PARTICIPANT_BELONGS_TO_SURVEY_CAMPAIGN,
    GET_SURVEY_CAMPAIGN_END_DATE_BY_EMPLOYEE_ID,
)


def _enrich_user(data: dict) -> User:
    return User(
        id=data["id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
    )


def _enrich_participants(data: dict) -> Participant:
    user = User(
        id=data["user_id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
    )
    business_unit = BusinessUnit(
        id=data["business_unit_id"],
        name=data["business_unit_name"],
    )
    employee = Employee(
        id=data["employee_id"],
        location=data["location"],
        role_title=data["role_title"],
        user=user,
        business_unit=business_unit,
    )
    participant = Participant(
        employee_id=data["employee_id"],
        employee=employee,
        id=UUID(data["participation_id"]),
        survey_campaign_id=data["survey_campaign_id"],
        status=ParticipationStatus(data["status"]),
    )
    return participant


class ParticipationRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def update_status(cls, _id: UUID, status: ParticipationStatus):
        cls.connection_manager.execute_atomic_query(
            query=UPDATE_PARTICIPATION_STATUS, variables=(status.value, str(_id))
        )

    @classmethod
    def get_status(cls, _id: UUID):
        result = cls.connection_manager.execute_atomic_query(
            query=GET_PARTICIPATION_STATUS, variables=(str(_id),)
        )
        if not result:
            raise NotFoundException(entity="Participation", arg="ID", value=str(_id))

        return ParticipationStatus(result["status"])

    @classmethod
    def get_survey_campaign_participants(
        cls,
        campaign_id: int,
        offset: int,
        limit: int,
        status: ParticipationStatus | None = None,
    ) -> tuple[int, list[Participant]]:
        query = GET_SURVEY_CAMPAIGN_PARTICIPANTS
        variables: list[int | str] = [campaign_id, offset, limit]
        if status is not None:
            query += "AND STATUS = %s "
            variables.insert(1, status.value)
        query += ORDER_BY_UPDATED_AT
        query += OFFSET_AND_LIMIT
        result = cls.connection_manager.execute_atomic_query_all(
            query=query,
            variables=variables,
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        return total_count, [_enrich_participants(data) for data in result]

    @classmethod
    def add_participant_to_campaign(cls, campaign_id: int, employee_id: int) -> UUID:
        result = cls.connection_manager.execute_atomic_query(
            query=UPSERT_PARTICIPANT_TO_SURVEY_CAMPAIGN,
            variables=(campaign_id, employee_id, ParticipationStatus.DUE),
        )
        return UUID(result["participation_id"])

    @classmethod
    def belongs_to_survey_campaign(cls, campaign_id: int, participant_id: UUID) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_PARTICIPANT_BELONGS_TO_SURVEY_CAMPAIGN,
            variables=(campaign_id, str(participant_id)),
        )
        return result["exists"]

    @classmethod
    def participation_belongs_to_user(cls, user_id: int, participant_id: UUID) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_PARTICIPATION_BELONGS_TO_USER,
            variables=(user_id, str(participant_id)),
        )
        return result["exists"]

    @classmethod
    def get_survey_campaigns_participant_ids(
        cls,
        survey_campaign_ids: list[int],
        status_list: list[ParticipationStatus],
        business_unit_ids: list[int],
    ) -> list[UUID]:
        if not status_list:
            raise ValidationException(
                entities="status_list",
                values="Empty List",
            )
        status_values = [item.value for item in status_list]

        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_SURVEY_CAMPAIGNS_PARTICIPANT_IDS,
            variables=(
                tuple(survey_campaign_ids),
                tuple(business_unit_ids),
                tuple(status_values),
            ),
        )
        if not result:
            return []
        else:
            return [data["participation_id"] for data in result]

    @classmethod
    def filter_employees_with_in_progress_survey_campaign(
        cls, emails: list[str]
    ) -> list[str]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=FILTER_USERS_WITH_SURVEY_CAMPAIGN,
            variables=(tuple(emails),),
        )
        if not result:
            return []
        else:
            return [item["email"] for item in result]

    @classmethod
    def employee_survey_campaign_end_date(cls, employee_id: int) -> datetime:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_SURVEY_CAMPAIGN_END_DATE_BY_EMPLOYEE_ID,
            variables=(employee_id,),
        )
        if not result:
            raise NotFoundException(
                entity="Survey Campaign",
                arg="Employee ID",
                value=str(employee_id),
            )
        return result["end_date"]

    @classmethod
    def exists(cls, _id: UUID) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_PARTICIPATION_ID_EXISTS,
            variables=(str(_id),),
        )
        return result["exists"]

    @classmethod
    def get_participation_id_by_user_id(cls, user_id: int) -> UUID:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_PARTICIPATION_ID_BY_USER_ID,
            variables=(user_id,),
        )
        if not result:
            raise NotFoundException(
                entity="Participation",
                arg="User ID",
                value=str(user_id),
            )
        return result["participation_id"]

    @classmethod
    def get_campaign_id(cls, participation_id: UUID) -> int:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_CAMPAIGN_ID_BY_PARTICIPATION_ID,
            variables=(str(participation_id),),
        )
        if not result:
            raise NotFoundException(
                entity="Survey Campaign",
                arg="Participation ID",
                value=str(participation_id),
            )
        return result["survey_campaign_id"]

    @classmethod
    def get_participants_between(
        cls,
        after_hours: int,
        before_hours: int,
        status: ParticipationStatus,
        exclude: list[UUID],
    ):
        variables = [
            after_hours,
            before_hours,
            status,
        ]
        query = GET_INVITED_PARTICIPATION_IDS_AFTER_DATE
        exclude_ids = tuple([str(item) for item in exclude])
        if exclude_ids:
            query += " AND sce.participation_id NOT IN %s"
            variables.append(exclude_ids)
        result = cls.connection_manager.execute_atomic_query_all(
            query=query,
            variables=tuple(variables),
        )
        if not result:
            return []
        return [item["participation_id"] for item in result]

    @classmethod
    def get_user(cls, participation_id: UUID) -> User:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_USER_BY_PARTICIPATION_ID,
            variables=(str(participation_id),),
        )
        if not result:
            raise NotFoundException(
                entity="User",
                arg="Participation ID",
                value=str(participation_id),
            )

        return _enrich_user(result)

    @classmethod
    def get_participants_before_end_date(
        cls,
        before_hours: int,
        status: ParticipationStatus,
        exclude: list[UUID],
        min_campaign_length_hours: int,
    ) -> list[UUID]:
        variables = [
            before_hours,
            status,
            min_campaign_length_hours * 60 * 60,
        ]
        query = GET_PARTICIPATION_IDS_BEFORE_DATE
        exclude_ids = tuple([str(item) for item in exclude])
        if exclude_ids:
            query += " AND sce.participation_id NOT IN %s"
            variables.append(exclude_ids)
        result = cls.connection_manager.execute_atomic_query_all(
            query=query,
            variables=tuple(variables),
        )
        if not result:
            return []
        return [item["participation_id"] for item in result]

    @classmethod
    def get_idea_delayed_participants(
        cls,
        after_hours: int,
        before_hours: int,
        status: ParticipationStatus,
        exclude: list[UUID],
    ) -> list[UUID]:
        variables = [
            after_hours,
            before_hours,
            status,
        ]
        query = GET_IDEA_DELAYED_PARTICIPANTS
        exclude_ids = tuple([str(item) for item in exclude])
        if exclude_ids:
            query += " AND sce.participation_id NOT IN %s"
            variables.append(exclude_ids)
        result = cls.connection_manager.execute_atomic_query_all(
            query=query,
            variables=tuple(variables),
        )
        if not result:
            return []
        return [item["participation_id"] for item in result]

    @classmethod
    def get_scheduled_participants(
        cls,
        after_hours: int,
        before_hours: int,
        status: ParticipationStatus,
        exclude: list[UUID],
    ) -> list[UUID]:
        variables = [
            after_hours,
            before_hours,
            status,
        ]
        query = GET_SCHEDULED_PARTICIPANTS
        exclude_ids = tuple([str(item) for item in exclude])
        if exclude_ids:
            query += " AND sce.participation_id NOT IN %s"
            variables.append(exclude_ids)
        result = cls.connection_manager.execute_atomic_query_all(
            query=query,
            variables=tuple(variables),
        )
        if not result:
            return []
        return [item["participation_id"] for item in result]
