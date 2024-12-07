from copy import deepcopy

from entity import InformationLibrary
from settings.connections import postgres_connection_manager
from .queries import (
    STORE_INFORMATION_LIBRARY,
    GET_EMPLOYEE_INFORMATION_LIBRARIES,
    CHECK_LIBRARY_BELONG_TO_EMPLOYEE,
)


def _enrich_information_library(data: dict) -> InformationLibrary:
    return InformationLibrary(
        id=data["id"],
        title=data["title"],
        short_description=data["short_description"],
        long_description=data["long_description"],
        organization_id=data["organization_id"],
        deep_dive_id=data["deep_dive_id"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


class InformationLibraryRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def store(cls, information_library: InformationLibrary) -> InformationLibrary:
        result = cls.connection_manager.execute_atomic_query(
            query=STORE_INFORMATION_LIBRARY,
            variables=(
                information_library.title,
                information_library.short_description,
                information_library.long_description,
                information_library.organization_id,
                information_library.deep_dive_id,
            ),
        )
        stored_information_library = deepcopy(information_library)
        stored_information_library.id = result["id"]
        stored_information_library.created_at = result["created_at"]
        stored_information_library.updated_at = result["updated_at"]
        return stored_information_library

    @classmethod
    def get_list(
        cls,
        deep_dive_id: int,
        employee_id: int,
        offset: int,
        limit: int,
    ) -> tuple[int, list[InformationLibrary]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_EMPLOYEE_INFORMATION_LIBRARIES,
            variables=(employee_id, deep_dive_id, offset, limit),
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        return total_count, [_enrich_information_library(item) for item in result]

    @classmethod
    def library_belong_to_employee(cls, employee_id: int, library_id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_LIBRARY_BELONG_TO_EMPLOYEE,
            variables=(employee_id, library_id, library_id),
        )
        return result["exists"]
