from cexceptions import NotFoundException, DoesNotBelongException
from repository import (
    ReportRepository,
    ReportGoalRepository,
    InnovationIdeaRepository,
    EmployeeRepository,
)
from entity import ExecutiveSummary


def _check_admin_report_exists(report_id: int):
    if not ReportRepository.exists(_id=report_id):
        raise NotFoundException(entity="Report", arg="ID", value=str(report_id))


def _check_manager_report_exists(report_id: int, user_id: int):
    if not ReportRepository.is_published(_id=report_id):
        raise NotFoundException(entity="Report", arg="ID", value=str(report_id))
    if not ReportRepository.report_belong_to_user(
        user_id=user_id,
        report_id=report_id,
    ):
        raise DoesNotBelongException(
            first_entity="Report ID",
            first_value=str(report_id),
            second_entity="User ID",
            second_value=str(user_id),
        )


def get_executive_summary(
    report_id: int, user_id: int, is_admin: bool
) -> ExecutiveSummary:
    if is_admin:
        _check_admin_report_exists(report_id=report_id)
        employee_id = None
    else:
        _check_manager_report_exists(report_id=report_id, user_id=user_id)
        employee_id = EmployeeRepository.get_employee_id_by_user_id(user_id=user_id)
    snapshots: int = ReportRepository.get_responded_participant_count(_id=report_id)
    recommendations_generated: int = ReportGoalRepository.get_manager_goals_count(
        report_id=report_id, manager_id=employee_id
    )
    ideas_reviewed: int = InnovationIdeaRepository.get_ideas_rated_count(
        report_id=report_id, manager_id=employee_id
    )
    return ExecutiveSummary(
        snapshots=snapshots,
        recommendations_generated=recommendations_generated,
        ideas_reviewed=ideas_reviewed,
        key_insights=0,
        speed_of_transformation=0,
    )
