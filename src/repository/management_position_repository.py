from copy import deepcopy

from psycopg2.extras import execute_values

from cexceptions import NotFoundException
from entity import ManagementPosition, BusinessUnit, Employee, User
from settings.connections import postgres_connection_manager
from .queries import (
    GET_MANAGEMENT_POSITIONS_LIST,
    STORE_MANAGEMENT_POSITION,
    ADD_BUSINESS_UNIT_TO_MANAGEMENT_POSITION,
    GET_MANAGEMENT_POSITION_DETAILS,
    ADD_MANAGER_TO_MANAGEMENT_POSITION,
    GET_ORGANIZATION_ID_BY_MANAGEMENT_POSITION_ID,
    GET_BUSINESS_UNIT_IDS_BY_MANAGEMENT_POSITION_ID,
    CHECK_MANAGEMENT_POSITIONS_EXISTS,
    CHECK_IF_USER_IS_MANAGER,
    UPDATE_MANAGEMENT_POSITION,
    CHECK_IF_EMPLOYEE_IS_IN_MANAGEMENT_POSITION,
    CHECK_IF_POSITION_BELONGS_TO_ORGANIZATION,
    REMOVE_MANAGER_FROM_MANAGEMENT_POSITION,
)


def _enrich_business_units(data: dict) -> list[BusinessUnit]:
    return [
        BusinessUnit(name=bu["business_unit_name"], id=bu["business_unit_id"])
        for bu in data["business_units"]
    ]


def _enrich_management_position(data: dict) -> ManagementPosition:
    business_units = _enrich_business_units(data)
    return ManagementPosition(
        id=data["id"],
        name=data["name"],
        roles=business_units,
        managers_count=data["managers_count"],
    )


def _enrich_management_positions_detail(data: dict) -> ManagementPosition:
    business_units = _enrich_business_units(data)
    managers = [
        Employee(
            id=item["employee_id"],
            role_title=item["role_title"],
            location=item["location"],
            user=User(
                first_name=item["user_first_name"],
                last_name=item["user_last_name"],
                email=item["user_email"],
                id=item["user_id"],
            ),
        )
        for item in data["managers"]
    ]
    management_position = ManagementPosition(
        id=data["id"],
        name=data["name"],
        roles=business_units,
        managers=managers,
    )
    return management_position


class ManagementPositionRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def exists(cls, _id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_MANAGEMENT_POSITIONS_EXISTS,
            variables=(_id,),
        )
        return result["exists"]

    @classmethod
    def get(cls, _id: int) -> ManagementPosition:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_MANAGEMENT_POSITION_DETAILS,
            variables=(_id,),
        )
        if not result:
            raise NotFoundException(
                entity="Management Position", arg="ID", value=str(_id)
            )
        management_position = _enrich_management_positions_detail(data=result)
        return management_position

    @classmethod
    def get_list(
        cls, organization_id: int, offset: int, limit: int
    ) -> tuple[int, list[ManagementPosition]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_MANAGEMENT_POSITIONS_LIST,
            variables=(organization_id, offset, limit),
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        return total_count, [_enrich_management_position(data) for data in result]

    @classmethod
    def store(cls, management_position: ManagementPosition) -> ManagementPosition:
        with cls.connection_manager.open_cursor() as cursor:
            cursor.execute(
                STORE_MANAGEMENT_POSITION,
                (
                    management_position.name,
                    management_position.organization_id,
                ),
            )
            management_position_data = cursor.fetchone()
            stored_management_position = deepcopy(management_position)
            stored_management_position.created_at = management_position_data[
                "created_at"
            ]
            stored_management_position.updated_at = management_position_data[
                "updated_at"
            ]
            stored_management_position.id = management_position_data["id"]
            assert isinstance(stored_management_position.role_ids, list)
            business_unit_data = [
                (business_unit_id, stored_management_position.id)
                for business_unit_id in stored_management_position.role_ids
            ]
            execute_values(
                cursor, ADD_BUSINESS_UNIT_TO_MANAGEMENT_POSITION, business_unit_data
            )
            return stored_management_position

    @classmethod
    def add_manager(cls, manager_id: int, position_id: int) -> None:
        cls.connection_manager.execute_atomic_query(
            query=ADD_MANAGER_TO_MANAGEMENT_POSITION,
            variables=(manager_id, position_id),
        )

    @classmethod
    def get_organization_id_by_id(cls, _id: int) -> int:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_ORGANIZATION_ID_BY_MANAGEMENT_POSITION_ID, variables=(_id,)
        )
        if not result:
            raise NotFoundException(
                entity="Management Position", arg="ID", value=str(_id)
            )
        return result["organization_id"]

    @classmethod
    def get_business_unit_ids_by_id(cls, _id: int) -> list[int]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_BUSINESS_UNIT_IDS_BY_MANAGEMENT_POSITION_ID, variables=(_id,)
        )
        if not result:
            return []
        return [data["business_unit_id"] for data in result]

    @classmethod
    def is_user_manager(cls, user_id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_IF_USER_IS_MANAGER,
            variables=(user_id,),
        )
        return result["exists"]

    @classmethod
    def update(cls, _id: int, name: str):
        cls.connection_manager.execute_atomic_query(
            query=UPDATE_MANAGEMENT_POSITION,
            variables=(
                name,
                _id,
            ),
        )
        return

    @classmethod
    def check_if_employee_is_in_management_position(
        cls, manager_id: int, position_id: int
    ) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_IF_EMPLOYEE_IS_IN_MANAGEMENT_POSITION,
            variables=(
                manager_id,
                position_id,
            ),
        )
        return result["exists"]

    @classmethod
    def check_belongs_to_organization(
        cls, position_id: int, organization_id: int
    ) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_IF_POSITION_BELONGS_TO_ORGANIZATION,
            variables=(
                position_id,
                organization_id,
            ),
        )
        return result["exists"]

    @classmethod
    def remove_manager(cls, manager_id: int, position_id: int) -> None:
        cls.connection_manager.execute_atomic_query(
            query=REMOVE_MANAGER_FROM_MANAGEMENT_POSITION,
            variables=(
                manager_id,
                position_id,
            ),
        )
