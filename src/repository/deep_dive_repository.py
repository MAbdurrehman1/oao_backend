import json
from copy import deepcopy
from uuid import UUID

from cexceptions import NotFoundException
from settings.connections import postgres_connection_manager
from entity import DeepDive, File
from .queries import (
    STORE_DEEP_DIVE,
    GET_DEEP_DIVE_LIST,
    CHECK_DEEP_DIVE_EXISTS,
    UPSERT_DEEP_DIVE_SLUG_LIST,
    GET_DEEP_DIVE_SLUG_LIST,
    GET_DEEP_DIVE_LIST_BY_SLUG,
)


def _enrich_deep_dive(data: dict) -> DeepDive:
    thumbnail = File(
        id=data["thumbnail_id"],
        file_path=data["thumbnail_url"],
    )
    return DeepDive(
        id=data["id"],
        title=data["title"],
        description=data["description"],
        thumbnail=thumbnail,
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


class DeepDiveRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def exists(cls, _id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_DEEP_DIVE_EXISTS,
            variables=(_id,),
        )
        return result["exists"]

    @classmethod
    def store(cls, deep_dive: DeepDive) -> DeepDive:
        result = cls.connection_manager.execute_atomic_query(
            query=STORE_DEEP_DIVE,
            variables=(
                deep_dive.title,
                deep_dive.description,
                deep_dive.thumbnail_id,
                deep_dive.slug,
            ),
        )
        stored_deep_dive = deepcopy(deep_dive)
        stored_deep_dive.id = result["id"]
        stored_deep_dive.created_at = result["created_at"]
        stored_deep_dive.updated_at = result["updated_at"]
        return stored_deep_dive

    @classmethod
    def get_list(cls, offset: int, limit: int) -> tuple[int, list[DeepDive]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_DEEP_DIVE_LIST,
            variables=(offset, limit),
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        deep_dives = [_enrich_deep_dive(item) for item in result]
        return total_count, deep_dives

    @classmethod
    def store_deep_dive_strategy(
        cls,
        participation_id: UUID,
        slug_list: list,
    ):
        slug_list_json = json.dumps(slug_list)
        cls.connection_manager.execute_atomic_query(
            query=UPSERT_DEEP_DIVE_SLUG_LIST,
            variables=(str(participation_id), slug_list_json),
        )

    @classmethod
    def get_deep_dive_strategy(
        cls,
        participation_id: UUID,
    ) -> list:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_DEEP_DIVE_SLUG_LIST,
            variables=(str(participation_id),),
        )
        if not result:
            raise NotFoundException(
                entity="Deep Dive Strategy List",
                arg="Participation ID",
                value=str(participation_id),
            )
        return result["deep_dive_slugs"]

    @classmethod
    def get_deep_dive_list_by_slug(
        cls,
        slug_list: list[str],
        offset: int,
        limit: int,
    ) -> tuple[int, list[DeepDive]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_DEEP_DIVE_LIST_BY_SLUG,
            variables=(
                tuple(slug_list),
                offset,
                limit,
            ),
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        return total_count, [_enrich_deep_dive(item) for item in result]
