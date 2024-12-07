from copy import deepcopy

from cexceptions import NotFoundException
from entity import ReportGoal
from repository.queries import (
    CREATE_REPORT_GOAL,
    GET_REPORT_GOALS,
    GET_REPORT_GOALS_WITH_FOCUS_AREA,
    GET_MANGER_GOALS_COUNT,
    OFFSET_AND_LIMIT,
)
from settings import FocusArea
from settings.connections import postgres_connection_manager


def _enrich_report_goal(data: dict) -> ReportGoal:
    return ReportGoal(
        id=data["id"],
        title=data["title"],
        manager_id=data["manager_id"],
        description=data["description"],
        focus_area=FocusArea(data["focus_area"]),
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


class ReportGoalRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def store(cls, report_goal: ReportGoal) -> ReportGoal:
        result = cls.connection_manager.execute_atomic_query(
            query=CREATE_REPORT_GOAL,
            variables=(
                report_goal.report_id,
                report_goal.manager_id,
                report_goal.title,
                report_goal.description,
                report_goal.focus_area.value,
            ),
        )
        result_goal = deepcopy(report_goal)
        result_goal.id = result["id"]
        result_goal.created_at = result["created_at"]
        result_goal.updated_at = result["updated_at"]
        return result_goal

    @classmethod
    def get_list(
        cls,
        manager_id: int | None,
        report_id: int,
        limit: int,
        offset: int,
    ) -> tuple[int, list[ReportGoal]]:
        query = GET_REPORT_GOALS
        if manager_id:
            query += f"AND manager_id = {manager_id}"
        query += OFFSET_AND_LIMIT
        result = cls.connection_manager.execute_atomic_query_all(
            query=query,
            variables=(report_id, offset, limit),
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        return total_count, [_enrich_report_goal(goal_data) for goal_data in result]

    @classmethod
    def get_list_with_focus_area(
        cls,
        report_id: int,
        manager_id: int | None,
        focus_area: FocusArea,
        limit: int,
        offset: int,
    ) -> tuple[int, list[ReportGoal]]:
        query = GET_REPORT_GOALS_WITH_FOCUS_AREA
        if manager_id:
            query += f"AND manager_id = {manager_id}"
        query += OFFSET_AND_LIMIT
        result = cls.connection_manager.execute_atomic_query_all(
            query=query,
            variables=(report_id, focus_area.value, offset, limit),
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        return total_count, [_enrich_report_goal(goal_data) for goal_data in result]

    @classmethod
    def get_manager_goals_count(cls, manager_id: int | None, report_id: int) -> int:
        query = GET_MANGER_GOALS_COUNT
        if manager_id:
            query += f"AND manager_id = {manager_id}"
        result = cls.connection_manager.execute_atomic_query(
            query=query,
            variables=(report_id,),
        )
        if not result:
            raise NotFoundException(
                entity="Report",
                arg="ID",
                value=str(report_id),
            )
        return result["count"]
