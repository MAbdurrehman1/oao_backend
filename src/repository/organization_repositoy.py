from copy import deepcopy
from json import dumps

from cexceptions import NotFoundException
from entity import Organization, File
from .queries import (
    GET_ORGANIZATION_BY_ID,
    CREATE_ORGANIZATION,
    GET_ORGANIZATIONS_LIST,
    CHECK_ORGANIZATION_EXISTS,
    GET_ORGANIZATION_BY_USER_ID,
    GET_ORGANIZATION_BY_CAMPAIGN_ID,
)
from settings.connections import postgres_connection_manager


def _enrich_organization(data: dict) -> Organization:
    logo = File(
        id=data["logo_id"],
        file_path=data["logo_url"],
    )
    organization = Organization(
        id=data["id"],
        logo=logo,
        company_name=data["company_name"],
        industry=data["industry"],
        hq_location=data["hq_location"],
        size=data["organization_size"],
        meta_data=data["metadata"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )
    return organization


class OrganizationRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def exists(cls, organization_id: int):
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_ORGANIZATION_EXISTS, variables=(organization_id,)
        )
        return result["exists"]

    @classmethod
    def get_by_id(cls, organization_id: int):
        result = cls.connection_manager.execute_atomic_query(
            query=GET_ORGANIZATION_BY_ID, variables=(organization_id,)
        )
        if not result:
            raise NotFoundException(
                entity="Organization", arg="ID", value=str(organization_id)
            )
        return _enrich_organization(result)

    @classmethod
    def store(cls, organization: Organization) -> Organization:
        result = cls.connection_manager.execute_atomic_query(
            query=CREATE_ORGANIZATION,
            variables=(
                organization.company_name,
                organization.industry,
                organization.hq_location,
                organization.size,
                dumps(organization.meta_data) if organization.meta_data else None,
                organization.logo_id,
            ),
        )
        result_org = deepcopy(organization)
        result_org.id = result["id"]
        result_org.created_at = result["created_at"]
        result_org.updated_at = result["updated_at"]
        return result_org

    @classmethod
    def get_list(cls, offset: int, limit: int) -> tuple[int, list[Organization]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_ORGANIZATIONS_LIST, variables=(offset, limit)
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        return total_count, [_enrich_organization(data) for data in result]

    @classmethod
    def get_organization_by_user_id(cls, user_id: int) -> Organization:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_ORGANIZATION_BY_USER_ID,
            variables=(user_id,),
        )
        if not result:
            raise NotFoundException(
                entity="Organization",
                arg="User ID",
                value=str(user_id),
            )
        return _enrich_organization(result)

    @classmethod
    def get_organization_by_campaign_id(cls, campaign_id: int) -> Organization:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_ORGANIZATION_BY_CAMPAIGN_ID,
            variables=(campaign_id,),
        )
        if not result:
            raise NotFoundException(
                entity="Organization",
                arg="Campaign ID",
                value=str(campaign_id),
            )
        return _enrich_organization(result)
