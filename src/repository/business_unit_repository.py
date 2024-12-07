from copy import deepcopy
from datetime import datetime
from uuid import UUID

from psycopg2.errors import UniqueViolation

from cexceptions import UniqueException, NotFoundException
from entity import BusinessUnit
from settings.connections import postgres_connection_manager
from .queries import (
    CREATE_BUSINESS_UNIT,
    CHECK_BUSINESS_UNIT_IDS_EXIST,
    GET_BUSINESS_UNIT_BY_ID,
    GET_BUSINESS_UNITS_HIERARCHY,
    GET_BUSINESS_UNIT_CHILDREN_IDS,
    CHECK_IF_ORGANIZATION_HAS_A_ROOT_BUSINESS_UNIT,
    CHECK_BUSINESS_UNIT_BELONGS_TO_ORGANIZATION,
    UPDATE_BUSINESS_UNIT,
    GET_SUB_BUSINESS_UNITS_HIERARCHY,
    GET_SUB_BUSINESS_UNITS_WITH_PARTICIPATION,
    CHECK_BUSINESS_UNIT_IDS_BELONG_TO_ORGANIZATION_ID,
)


def _enrich_business_unit(data: dict) -> BusinessUnit:
    return BusinessUnit(
        id=data["id"],
        name=data["name"],
        parent_id=data["parent_id"],
        organization_id=data["organization_id"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


class BusinessUnitRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def store(cls, business_unit: BusinessUnit) -> BusinessUnit:
        assert isinstance(
            business_unit.organization_id, int
        ), "organization_id must not be null on store business unit"
        try:
            result = cls.connection_manager.execute_atomic_query(
                query=CREATE_BUSINESS_UNIT,
                variables=(
                    business_unit.name,
                    business_unit.organization_id,
                    business_unit.parent_id,
                ),
            )
        except UniqueViolation:
            raise UniqueException(
                arg="name-organization_id-parent_id",
                value="-".join(
                    [
                        business_unit.name,
                        str(business_unit.organization_id),
                        str(business_unit.parent_id),
                    ]
                ),
            )
        result_bu = deepcopy(business_unit)
        result_bu.id = result["id"]
        result_bu.created_at = result["created_at"]
        result_bu.updated_at = result["updated_at"]
        return result_bu

    @classmethod
    def get_missing_business_unit_ids(
        cls, organization_id: int, _ids: list[int]
    ) -> list:
        results = cls.connection_manager.execute_atomic_query_all(
            query=CHECK_BUSINESS_UNIT_IDS_EXIST,
            variables=(tuple(_ids), organization_id),
        )
        if len(results) == len(_ids):
            return []
        retrieved_ids = {item["id"] for item in results}
        return list(set(_ids) - retrieved_ids)

    @classmethod
    def get_by_id(cls, _id: int) -> BusinessUnit:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_BUSINESS_UNIT_BY_ID, variables=(_id,)
        )
        if not result:
            raise NotFoundException(entity="BusinessUnit", arg="ID", value=str(_id))
        business_unit = _enrich_business_unit(result)
        return business_unit

    @classmethod
    def get_hierarchy(cls, organization_id: int) -> list[BusinessUnit]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_BUSINESS_UNITS_HIERARCHY,
            variables=(organization_id, organization_id),
        )
        if not result:
            return []

        return [_enrich_business_unit(data) for data in result]

    @classmethod
    def get_sub_units_hierarchy(cls, business_unit_id: int) -> list[BusinessUnit]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_SUB_BUSINESS_UNITS_HIERARCHY,
            variables=(business_unit_id,),
        )
        if not result:
            return []
        return [_enrich_business_unit(data) for data in result]

    @classmethod
    def get_children_ids(cls, _ids: list[int]) -> list[int]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_BUSINESS_UNIT_CHILDREN_IDS,
            variables=(tuple(_ids),),
        )
        if not result:
            return []

        return [data["id"] for data in result]

    @classmethod
    def organization_root_business_unit_exists(cls, organization_id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_IF_ORGANIZATION_HAS_A_ROOT_BUSINESS_UNIT,
            variables=(organization_id,),
        )
        return result["exists"]

    @classmethod
    def exists(cls, _id: int, organization_id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_BUSINESS_UNIT_BELONGS_TO_ORGANIZATION,
            variables=(
                _id,
                organization_id,
            ),
        )
        return result["exists"]

    @classmethod
    def update(cls, business_unit: BusinessUnit) -> BusinessUnit:
        now = datetime.now()
        cls.connection_manager.execute_atomic_query(
            query=UPDATE_BUSINESS_UNIT,
            variables=(
                business_unit.name,
                business_unit.parent_id,
                now,
                business_unit.id,
            ),
        )
        business_unit.updated_at = now
        return business_unit

    @classmethod
    def get_sub_units_with_participation(
        cls, business_unit_ids: list[int]
    ) -> list[tuple[int, UUID]]:
        if not business_unit_ids:
            return []
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_SUB_BUSINESS_UNITS_WITH_PARTICIPATION,
            variables=(tuple(business_unit_ids),),
        )
        if not result:
            return []

        return [(data["id"], UUID(data["participation_id"])) for data in result]

    @classmethod
    def check_belong_to_organization(
        cls,
        organization_id: int,
        unit_ids: list[int],
    ):
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_BUSINESS_UNIT_IDS_BELONG_TO_ORGANIZATION_ID,
            variables=(unit_ids, organization_id, unit_ids),
        )
        return result["exists"]
