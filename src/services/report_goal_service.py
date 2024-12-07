from cexceptions import NotFoundException, ValidationException, DoesNotBelongException
from entity import ReportGoal
from repository import ReportRepository, ReportGoalRepository, EmployeeRepository
from settings import FocusArea


def _check_manager_report_exists(report_id: int, user_id: int):
    if not ReportRepository.is_published(_id=report_id):
        raise NotFoundException(entity="Report", arg="ID", value=str(report_id))
    if not ReportRepository.report_belong_to_user(user_id=user_id, report_id=report_id):
        raise DoesNotBelongException(
            first_entity="Report ID",
            first_value=str(report_id),
            second_entity="User ID",
            second_value=str(user_id),
        )


def _check_admin_report_exists(report_id: int):
    if not ReportRepository.exists(_id=report_id):
        raise NotFoundException(entity="Report", arg="ID", value=str(report_id))


def _validate_focus_area(focus_area_str: str) -> FocusArea:
    try:
        return FocusArea(focus_area_str)
    except Exception:
        raise ValidationException(
            entities="Focus Area",
            values=focus_area_str,
        )


def create_report_goal(
    report_id: int, user_id: int, title: str, description: str, focus_area: str
) -> ReportGoal:
    _check_manager_report_exists(report_id=report_id, user_id=user_id)
    goal_focus_area = _validate_focus_area(focus_area)
    employee_id = EmployeeRepository.get_employee_id_by_user_id(user_id=user_id)
    goal = ReportGoal(
        report_id=report_id,
        manager_id=employee_id,
        title=title,
        description=description,
        focus_area=goal_focus_area,
    )
    stored_report_goal = ReportGoalRepository.store(report_goal=goal)
    return stored_report_goal


def get_report_goals(
    report_id: int,
    user_id: int,
    focus_area_str: str | None,
    limit: int,
    offset: int,
    is_admin: bool,
) -> tuple[int, list[ReportGoal]]:
    if is_admin:
        _check_admin_report_exists(report_id=report_id)
        employee_id = None
    else:
        _check_manager_report_exists(report_id=report_id, user_id=user_id)
        employee_id = EmployeeRepository.get_employee_id_by_user_id(user_id=user_id)
    if focus_area_str:
        focus_area = _validate_focus_area(focus_area_str=focus_area_str)
        total_count, report_goals = ReportGoalRepository.get_list_with_focus_area(
            report_id=report_id,
            limit=limit,
            offset=offset,
            focus_area=focus_area,
            manager_id=employee_id,
        )
    else:
        total_count, report_goals = ReportGoalRepository.get_list(
            report_id=report_id,
            limit=limit,
            offset=offset,
            manager_id=employee_id,
        )
    return total_count, report_goals
