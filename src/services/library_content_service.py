from entity import LibraryContent
from repository import (
    LibraryContentRepository,
    InformationLibraryRepository,
    EmployeeRepository,
)
from cexceptions import DoesNotBelongException


def get_library_content_list(
    user_id: int,
    library_id: int,
    limit: int,
    offset: int,
) -> tuple[int, list[LibraryContent]]:
    employee_id = EmployeeRepository.get_employee_id_by_user_id(user_id=user_id)
    if not InformationLibraryRepository.library_belong_to_employee(
        employee_id=employee_id,
        library_id=library_id,
    ):
        raise DoesNotBelongException(
            first_entity="Information Library ID",
            first_value=str(library_id),
            second_entity="Employee ID",
            second_value=str(employee_id),
        )
    total_count, library_contents = LibraryContentRepository.get_list(
        library_id=library_id,
        offset=offset,
        limit=limit,
    )
    return total_count, library_contents
