from copy import deepcopy
from datetime import datetime
from uuid import UUID

from cexceptions import NotFoundException
from entity import Report, ManagementPosition
from settings import ReportStatus
from .queries import (
    GET_LAST_REPORT_END_DATE,
    STORE_REPORT,
    CHECK_REPORT_EXISTS,
    CREATE_REPORT_PARTICIPANTS,
    CHECK_REPORT_BELONG_TO_USER,
    GET_RESPONDED_PARTICIPANTS_COUNT,
    GET_ORGANIZATION_REPORTS_LIST,
    DELETE_REPORT,
    GET_MANAGER_REPORTS_LIST,
    UPDATE_REPORT_STATUS,
    CHECK_REPORT_PUBLISHED,
    GET_ORGANIZATION_ID_BY_REPORT_ID,
)
from settings.connections import postgres_connection_manager


def _enrich_report(data: dict) -> Report:
    management_position = ManagementPosition(
        id=data["management_position_id"],
        name=data["management_position_name"],
    )
    report = Report(
        id=data["id"],
        end_date=data["end_date"],
        management_position=management_position,
        title=data["title"],
        status=ReportStatus(data["status"]),
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )
    return report


def _enrich_manager_report(data: dict) -> Report:
    management_position = ManagementPosition(
        id=data["management_position_id"],
        name=data["management_position_name"],
    )
    return Report(
        id=data["id"],
        management_position=management_position,
        title=data["title"],
        status=ReportStatus(data["status"]),
    )


class ReportRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def exists(cls, _id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_REPORT_EXISTS,
            variables=(_id,),
        )
        return result["exists"]

    @classmethod
    def get_organization_id(cls, _id: int) -> int:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_ORGANIZATION_ID_BY_REPORT_ID,
            variables=(_id,),
        )
        if not result:
            raise NotFoundException(
                entity="Organization",
                arg="Report ID",
                value=str(_id),
            )
        return result["id"]

    @classmethod
    def get_last_report_end_date(cls, position_id: int) -> datetime | None:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_LAST_REPORT_END_DATE, variables=(position_id,)
        )
        if result is None:
            return None
        else:
            return result["end_date"]

    @classmethod
    def store(cls, report: Report) -> Report:
        result = cls.connection_manager.execute_atomic_query(
            query=STORE_REPORT,
            variables=(
                report.title,
                report.management_position_id,
                report.end_date,
                ReportStatus.CREATED.value,
            ),
        )
        result_report = deepcopy(report)
        result_report.id = result["id"]
        result_report.created_at = result["created_at"]
        result_report.updated_at = result["updated_at"]
        return result_report

    @classmethod
    def store_report_participation_ids(
        cls, report_id: int, participation_ids: list[UUID]
    ) -> None:
        items = [
            (report_id, str(participation_id)) for participation_id in participation_ids
        ]
        cls.connection_manager.execute_values_atomic_query(
            query=CREATE_REPORT_PARTICIPANTS,
            variables=items,
            fetch=False,
        )

    @classmethod
    def report_belong_to_user(cls, user_id: int, report_id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_REPORT_BELONG_TO_USER, variables=(report_id, user_id)
        )
        return result["exists"]

    @classmethod
    def get_responded_participant_count(cls, _id: int) -> int:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_RESPONDED_PARTICIPANTS_COUNT, variables=(_id,)
        )
        if not result:
            raise NotFoundException(
                entity="Report",
                arg="ID",
                value=str(_id),
            )
        return result["count"]

    @classmethod
    def get_list_by_organization_id(
        cls, organization_id: int, offset: int, limit: int
    ) -> tuple[int, list[Report]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_ORGANIZATION_REPORTS_LIST,
            variables=(organization_id, offset, limit),
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        return total_count, [_enrich_report(data) for data in result]

    @classmethod
    def delete(cls, _id: int) -> None:
        cls.connection_manager.execute_atomic_query(
            query=DELETE_REPORT,
            variables=(_id,),
        )
        return

    @classmethod
    def get_list_by_manager_id(
        cls, manager_id: int, offset: int, limit: int
    ) -> tuple[int, list[Report]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_MANAGER_REPORTS_LIST,
            variables=(manager_id, ReportStatus.PUBLISHED.value, offset, limit),
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        return total_count, [_enrich_manager_report(data) for data in result]

    @classmethod
    def update_status(cls, _id: int, status: ReportStatus) -> None:
        now = datetime.now()
        cls.connection_manager.execute_atomic_query(
            query=UPDATE_REPORT_STATUS,
            variables=(
                status.value,
                now,
                _id,
            ),
        )
        return

    @classmethod
    def is_published(cls, _id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_REPORT_PUBLISHED,
            variables=(_id, ReportStatus.PUBLISHED.value),
        )
        return result["exists"]
