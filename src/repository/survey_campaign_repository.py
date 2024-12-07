from copy import deepcopy
from datetime import datetime
from uuid import UUID

from psycopg2.extras import execute_values

from cexceptions import NotFoundException
from entity import SurveyCampaign, User
from settings.connections import postgres_connection_manager
from .queries import (
    CREATE_SURVEY_CAMPAIGN,
    CREATE_SURVEY_CAMPAIGN_EMPLOYEE,
    GET_SURVEY_CAMPAIGN_PARTICIPANTS_DATA,
    GET_PARTICIPANT_DATA,
    GET_SURVEY_CAMPAIGN,
    UPDATE_SURVEY_CAMPAIGN,
    GET_ORGANIZATION_SURVEY_CAMPAIGNS,
    CHECK_SURVEY_CAMPAIGN_EXIST,
    GET_ORGANIZATION_ID_BY_SURVEY_CAMPAIGN_ID,
    GET_SURVEY_CAMPAIGN_START_DATE,
    GET_SURVEY_CAMPAIGN_IDS_BETWEEN,
    GET_SURVEY_CAMPAIGN_END_DATE,
    GET_SURVEY_CAMPAIGN_END_DATE_BY_PARTICIPATION_ID,
)


def _enrich_participant(data: dict) -> User:
    return User(
        id=data["id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
    )


def _enrich_survey_campaign(data: dict) -> SurveyCampaign:
    return SurveyCampaign(
        id=data["id"],
        title=data["title"],
        start_date=data["start_date"],
        end_date=data["end_date"],
        organization_id=data["organization_id"],
        participants_count=data["participants_count"],
        invited_participants_count=data["invited_count"],
        responded_participants_count=data["responded_count"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


class SurveyCampaignRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def exists(cls, _id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_SURVEY_CAMPAIGN_EXIST, variables=(_id,)
        )
        return result["exists"]

    @classmethod
    def store(cls, survey_campaign: SurveyCampaign) -> SurveyCampaign:
        with cls.connection_manager.open_cursor() as cursor:
            cursor.execute(
                CREATE_SURVEY_CAMPAIGN,
                (
                    survey_campaign.title,
                    survey_campaign.start_date,
                    survey_campaign.end_date,
                    survey_campaign.organization_id,
                ),
            )
            result = cursor.fetchone()
            result_survey_campaign = deepcopy(survey_campaign)
            result_survey_campaign.id = result["id"]
            result_survey_campaign.created_at = result["created_at"]
            result_survey_campaign.updated_at = result["updated_at"]
            assert isinstance(result_survey_campaign.participant_ids, list)
            survey_campaign_employee_data = [
                (result_survey_campaign.id, participant_id)
                for participant_id in result_survey_campaign.participant_ids
            ]
            execute_values(
                cursor, CREATE_SURVEY_CAMPAIGN_EMPLOYEE, survey_campaign_employee_data
            )

        return result_survey_campaign

    @classmethod
    def get(cls, campaign_id: int) -> SurveyCampaign:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_SURVEY_CAMPAIGN, variables=(str(campaign_id),)
        )
        if not result:
            raise NotFoundException(
                entity="SurveyCampaign", arg="ID", value=str(campaign_id)
            )
        return _enrich_survey_campaign(result)

    @classmethod
    def get_list(
        cls, offset: int, limit: int, organization_id: int
    ) -> tuple[int, list[SurveyCampaign]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_ORGANIZATION_SURVEY_CAMPAIGNS,
            variables=(organization_id, offset, limit),
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        return total_count, [_enrich_survey_campaign(data) for data in result]

    @classmethod
    def update(cls, survey_campaign: SurveyCampaign) -> SurveyCampaign:
        now = datetime.now()
        result = cls.connection_manager.execute_atomic_query(
            query=UPDATE_SURVEY_CAMPAIGN,
            variables=(
                survey_campaign.title,
                survey_campaign.start_date,
                survey_campaign.end_date,
                now,
                survey_campaign.id,
            ),
        )
        survey_campaign.updated_at = result["updated_at"]
        return survey_campaign

    @classmethod
    def get_participants_data(cls, survey_campaign_id: int) -> dict[str, User]:
        results = cls.connection_manager.execute_atomic_query_all(
            query=GET_SURVEY_CAMPAIGN_PARTICIPANTS_DATA, variables=(survey_campaign_id,)
        )
        if not results:
            return {}
        return {
            result["participation_id"]: _enrich_participant(result)
            for result in results
        }

    @classmethod
    def get_participant_data(cls, participant_id: UUID) -> User:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_PARTICIPANT_DATA, variables=(str(participant_id),)
        )
        if not result:
            raise NotFoundException(
                entity="Survey Campaign Participant",
                arg="ID",
                value=str(participant_id),
            )
        user = _enrich_participant(data=result)
        return user

    @classmethod
    def get_organization_id(cls, _id: int) -> int:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_ORGANIZATION_ID_BY_SURVEY_CAMPAIGN_ID, variables=(_id,)
        )
        if not result:
            raise NotFoundException(
                entity="Survey Campaign",
                arg="ID",
                value=str(_id),
            )
        return result["organization_id"]

    @classmethod
    def get_start_date(cls, _id: int) -> datetime:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_SURVEY_CAMPAIGN_START_DATE, variables=(_id,)
        )
        if not result:
            raise NotFoundException(
                entity="Survey Campaign",
                arg="ID",
                value=str(_id),
            )
        return result["start_date"]

    @classmethod
    def get_end_date(cls, _id: int) -> datetime:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_SURVEY_CAMPAIGN_END_DATE, variables=(_id,)
        )
        if not result:
            raise NotFoundException(
                entity="Survey Campaign",
                arg="ID",
                value=str(_id),
            )
        return result["end_date"]

    @classmethod
    def get_end_date_by_participation_id(cls, participation_id: UUID) -> datetime:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_SURVEY_CAMPAIGN_END_DATE_BY_PARTICIPATION_ID,
            variables=(str(participation_id),),
        )
        if not result:
            raise NotFoundException(
                entity="Survey Campaign",
                arg="PARTICIPATION ID",
                value=str(participation_id),
            )
        return result["end_date"]

    @classmethod
    def get_survey_campaign_ids_between(
        cls, start_date: datetime, end_date: datetime, organization_id: int
    ) -> list[int]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_SURVEY_CAMPAIGN_IDS_BETWEEN,
            variables=(start_date, end_date, organization_id),
        )
        if not result:
            return []
        return [data["id"] for data in result]
