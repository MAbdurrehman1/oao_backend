from entity import InformationLibrary
from repository import EmployeeRepository, InformationLibraryRepository


def get_information_library_list(
    deep_dive_id: int,
    user_id: int,
    limit: int,
    offset: int,
) -> tuple[int, list[InformationLibrary]]:
    employee_id = EmployeeRepository.get_employee_id_by_user_id(user_id=user_id)
    total_count, libraries = InformationLibraryRepository.get_list(
        deep_dive_id=deep_dive_id,
        employee_id=employee_id,
        offset=offset,
        limit=limit,
    )
    return total_count, libraries
