from uuid import UUID

from cexceptions import (
    GreaterThanOrEqualException,
    DoesNotBelongException,
    NotFoundException,
)
from entity import InnovationIdea, InnovationIdeaRate, MatrixInnovationIdea
from repository import (
    InnovationIdeaRepository,
    InnovationIdeaRateRepository,
    ParticipationRepository,
    ReportRepository,
    EmployeeRepository,
)
from settings import ParticipationStatus


def _check_admin_report_exists(report_id: int):
    if not ReportRepository.exists(_id=report_id):
        raise NotFoundException(
            entity="Report",
            arg="ID",
            value=str(report_id),
        )


def _check_manager_report_exists(report_id: int, user_id: int):
    if not ReportRepository.is_published(_id=report_id):
        raise NotFoundException(
            entity="Report",
            arg="ID",
            value=str(report_id),
        )
    if not ReportRepository.report_belong_to_user(report_id=report_id, user_id=user_id):
        raise DoesNotBelongException(
            first_entity="Report ID",
            first_value=str(report_id),
            second_entity="User ID",
            second_value=str(user_id),
        )


def _check_idea_belongs_to_manager(user_id: int, idea_id: int):
    if not InnovationIdeaRepository.check_idea_belongs_to_manager(
        user_id=user_id,
        idea_id=idea_id,
    ):
        raise NotFoundException(
            entity="Innovation Idea",
            arg="ID",
            value=str(idea_id),
        )


def create_innovation_idea(
    participation_id: UUID,
    user_id: int,
    title: str,
    description: str,
    feasibility_score: int,
    confidence_score: int,
    impact_score: int,
) -> InnovationIdea:
    if not ParticipationRepository.participation_belongs_to_user(
        user_id=user_id, participant_id=participation_id
    ):
        raise DoesNotBelongException(
            first_entity="Participation ID",
            first_value=str(participation_id),
            second_entity="User ID",
            second_value=str(user_id),
        )
    if feasibility_score < 0 or confidence_score < 0 or impact_score < 0:
        raise GreaterThanOrEqualException(first_entity="score", second_entity="0")
    idea = InnovationIdea(
        participation_id=participation_id,
        title=title,
        description=description,
        feasibility_score=feasibility_score,
        confidence_score=confidence_score,
        impact_score=impact_score,
    )
    stored_idea = InnovationIdeaRepository.store(innovation_idea=idea)
    ParticipationRepository.update_status(
        _id=participation_id,
        status=ParticipationStatus.IDEA_SUBMITTED,
    )
    return stored_idea


def get_innovation_idea(idea_id: int, user_id: int) -> InnovationIdea:
    _check_idea_belongs_to_manager(idea_id=idea_id, user_id=user_id)
    manager_id = EmployeeRepository.get_employee_id_by_user_id(user_id=user_id)
    idea = InnovationIdeaRepository.get(_id=idea_id, manager_id=manager_id)
    return idea


def get_report_innovation_ideas(
    report_id: int,
    user_id: int,
    offset: int,
    limit: int,
    is_admin: bool,
    rate: int | None,
    unrated: bool | None,
) -> tuple[int, list[InnovationIdea]]:
    if is_admin:
        _check_admin_report_exists(report_id=report_id)
        manager_id = None
    else:
        _check_manager_report_exists(report_id=report_id, user_id=user_id)
        manager_id = EmployeeRepository.get_employee_id_by_user_id(user_id=user_id)
    # if the user is an admin, and an organization manager at the same time
    if is_admin and ReportRepository.report_belong_to_user(
        report_id=report_id, user_id=user_id
    ):
        manager_id = EmployeeRepository.get_employee_id_by_user_id(user_id=user_id)
    total_count, ideas = InnovationIdeaRepository.get_list_by_report_id(
        report_id=report_id,
        manager_id=manager_id,
        offset=offset,
        limit=limit,
        rate=rate,
        unrated=unrated,
    )
    return total_count, ideas


def get_report_matrix_innovation_ideas(
    report_id: int,
    user_id: int,
) -> list[MatrixInnovationIdea]:
    _check_manager_report_exists(report_id=report_id, user_id=user_id)
    ideas = InnovationIdeaRepository.get_report_matrix_innovation_ideas(
        report_id=report_id,
    )
    return ideas


def rate_innovation_idea(
    user_id: int, innovation_idea_id: int, rate: int
) -> InnovationIdeaRate:
    _check_idea_belongs_to_manager(idea_id=innovation_idea_id, user_id=user_id)
    employee_id = EmployeeRepository.get_employee_id_by_user_id(user_id=user_id)
    innovation_idea_rate = InnovationIdeaRate(
        innovation_idea_id=innovation_idea_id, manager_id=employee_id, rate=rate
    )
    stored_rate = InnovationIdeaRateRepository.store(
        innovation_idea_rate=innovation_idea_rate
    )
    return stored_rate


def get_employee_innovation_idea(user_id: int) -> InnovationIdea:
    employee_id = EmployeeRepository.get_employee_id_by_user_id(user_id=user_id)
    idea = InnovationIdeaRepository.get_employees_last_campaign_innovation_idea(
        employee_id=employee_id,
    )
    return idea
