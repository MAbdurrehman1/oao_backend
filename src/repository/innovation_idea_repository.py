from copy import deepcopy
from uuid import UUID

from cexceptions import NotFoundException
from entity import InnovationIdea, User, Employee, MatrixInnovationIdea
from repository.queries import (
    CREATE_INNOVATION_IDEA,
    GET_INNOVATION_IDEA_BY_ID,
    CHECK_IDEA_BELONG_TO_MANAGER,
    GET_IDEAS_LIST_PART_ONE,
    GET_IDEAS_LIST_PART_TWO,
    GET_IDEAS_LIST_SELECT_RATE,
    GET_IDEAS_LIST_BY_REPORT_ID,
    GET_MANAGER_RATED_IDEAS_COUNT,
    GET_EMPLOYEE_LAST_CAMPAIGN_INNOVATION_IDEA,
    OFFSET_AND_LIMIT,
    GET_IDEAS_MATRIX_LIST_BY_REPORT_ID,
)
from settings.connections import postgres_connection_manager


def _enrich_innovation_idea(data: dict) -> InnovationIdea:
    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
    )
    employee = Employee(
        role_title=data["role_title"],
        location=data["location"],
        user=user,
    )
    return InnovationIdea(
        id=data["id"],
        title=data["title"],
        description=data["description"],
        feasibility_score=data["feasibility_score"],
        confidence_score=data["confidence_score"],
        impact_score=data["impact_score"],
        participation_id=UUID(data["participation_id"]),
        employee=employee,
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


def _enrich_innovation_idea_with_rate(data: dict) -> InnovationIdea:
    idea = _enrich_innovation_idea(data)
    idea.rate = data["manager_rate"] if "manager_rate" in data else None
    return idea


def _enrich_matrix_innovation_idea(data: dict) -> MatrixInnovationIdea:
    return MatrixInnovationIdea(
        id=data["id"],
        title=data["title"],
        feasibility_score=data["feasibility_score"],
        confidence_score=data["confidence_score"],
        impact_score=data["impact_score"],
    )


class InnovationIdeaRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def store(cls, innovation_idea: InnovationIdea) -> InnovationIdea:
        result = cls.connection_manager.execute_atomic_query(
            query=CREATE_INNOVATION_IDEA,
            variables=(
                str(innovation_idea.participation_id),
                innovation_idea.title,
                innovation_idea.description,
                innovation_idea.feasibility_score,
                innovation_idea.confidence_score,
                innovation_idea.impact_score,
            ),
        )
        result_idea = deepcopy(innovation_idea)
        result_idea.id = result["id"]
        result_idea.created_at = result["created_at"]
        result_idea.updated_at = result["updated_at"]
        return result_idea

    @classmethod
    def get(cls, _id: int, manager_id: int) -> InnovationIdea:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_INNOVATION_IDEA_BY_ID,
            variables=(
                manager_id,
                _id,
            ),
        )
        if not result:
            raise NotFoundException(
                entity="Innovation Idea",
                arg="ID",
                value=str(_id),
            )
        return _enrich_innovation_idea_with_rate(result)

    @classmethod
    def check_idea_belongs_to_manager(cls, idea_id: int, user_id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_IDEA_BELONG_TO_MANAGER,
            variables=(idea_id, user_id),
        )
        return result["exists"]

    @classmethod
    def get_report_matrix_innovation_ideas(
        cls, report_id: int
    ) -> list[MatrixInnovationIdea]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_IDEAS_MATRIX_LIST_BY_REPORT_ID,
            variables=(report_id,),
        )
        if not result:
            return []
        return [_enrich_matrix_innovation_idea(idea_data) for idea_data in result]

    @classmethod
    def get_list_by_report_id(
        cls,
        report_id: int,
        manager_id: int | None,
        offset: int,
        limit: int,
        rate: int | None,
        unrated: bool | None,
    ) -> tuple[int, list[InnovationIdea]]:
        query = GET_IDEAS_LIST_PART_ONE
        query += GET_IDEAS_LIST_SELECT_RATE if manager_id else ""
        query += GET_IDEAS_LIST_PART_TWO
        if manager_id:
            query += f"""
                LEFT JOIN innovation_idea_rates iir ON
                (iir.innovation_idea_id = i.id AND iir.manager_id = {manager_id})
            """
        query += GET_IDEAS_LIST_BY_REPORT_ID
        if rate:
            query += f"\nAND iir.rate = {rate}\n"
        elif unrated:
            query += "AND iir.id IS NULL"
        query += OFFSET_AND_LIMIT
        result = cls.connection_manager.execute_atomic_query_all(
            query=query,
            variables=(report_id, offset, limit),
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        return total_count, [
            _enrich_innovation_idea_with_rate(idea_data) for idea_data in result
        ]

    @classmethod
    def get_ideas_rated_count(cls, report_id: int, manager_id: int | None) -> int:
        query = GET_MANAGER_RATED_IDEAS_COUNT
        if manager_id:
            query += f"AND mi.manager_id = {manager_id}"
        result = cls.connection_manager.execute_atomic_query(
            query=GET_MANAGER_RATED_IDEAS_COUNT,
            variables=(report_id,),
        )

        if not result:
            raise NotFoundException(
                entity="Report",
                arg="ID",
                value=str(report_id),
            )
        return result["count"]

    @classmethod
    def get_employees_last_campaign_innovation_idea(
        cls, employee_id: int
    ) -> InnovationIdea:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_EMPLOYEE_LAST_CAMPAIGN_INNOVATION_IDEA,
            variables=(employee_id, employee_id),
        )
        if not result:
            raise NotFoundException(
                entity="Innovation Idea", arg="Employee ID", value=str(employee_id)
            )
        return _enrich_innovation_idea(result)
