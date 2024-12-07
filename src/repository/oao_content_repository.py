from copy import deepcopy
from uuid import UUID

from .queries import (
    STORE_OAO_CONTENT,
    GET_OAO_CONTENT_LIST,
    UPSERT_OAO_CONTENT_VIEW,
    CHECK_OAO_CONTENT_EXISTS,
    GET_VIEWED_OAO_CONTENT_IDS_LIST,
)
from entity import OAOContent, File
from settings.connections import postgres_connection_manager


def _enrich_oao_content(data: dict) -> OAOContent:
    thumbnail = File(
        id=data["thumbnail_id"],
        file_path=data["thumbnail_url"],
    )
    return OAOContent(
        id=data["id"],
        title=data["title"],
        short_description=data["short_description"],
        long_description=data["long_description"],
        content_url=data["content_url"],
        thumbnail=thumbnail,
        deep_dive_id=data["deep_dive_id"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


class OAOContentRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def store(cls, oao_content: OAOContent) -> OAOContent:
        result = cls.connection_manager.execute_atomic_query(
            query=STORE_OAO_CONTENT,
            variables=(
                oao_content.title,
                oao_content.short_description,
                oao_content.long_description,
                oao_content.content_url,
                oao_content.deep_dive_id,
                oao_content.thumbnail_id,
            ),
        )
        stored_oao_content = deepcopy(oao_content)
        stored_oao_content.id = result["id"]
        stored_oao_content.created_at = result["created_at"]
        stored_oao_content.updated_at = result["updated_at"]
        return stored_oao_content

    @classmethod
    def get_list(
        cls, deep_dive_id: int, offset: int, limit: int
    ) -> tuple[int, list[OAOContent]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_OAO_CONTENT_LIST,
            variables=(deep_dive_id, offset, limit),
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        return total_count, [_enrich_oao_content(item) for item in result]

    @classmethod
    def upsert_oao_content_view(cls, participation_id: UUID, content_id: int):
        cls.connection_manager.execute_atomic_query(
            query=UPSERT_OAO_CONTENT_VIEW, variables=(str(participation_id), content_id)
        )

    @classmethod
    def exists(cls, _id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_OAO_CONTENT_EXISTS,
            variables=(_id,),
        )
        return result["exists"]

    @classmethod
    def get_viewed_content_ids_list(cls, participation_id: UUID) -> list[int]:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_VIEWED_OAO_CONTENT_IDS_LIST,
            variables=(str(participation_id),),
        )
        if not result:
            return []
        return list(result)
