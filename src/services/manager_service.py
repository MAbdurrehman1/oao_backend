from entity import Report
from repository import ManagementPositionRepository, ReportRepository


def get_manager_reports_list(
    manager_id: int,
    offset: int,
    limit: int,
) -> tuple[int, list[Report]]:
    total_count, reports = ReportRepository.get_list_by_manager_id(
        manager_id=manager_id,
        offset=offset,
        limit=limit,
    )
    return total_count, reports


def check_user_is_manager(user_id: int) -> bool:
    return ManagementPositionRepository.is_user_manager(user_id=user_id)
