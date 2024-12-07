from copy import deepcopy

from entity import LibraryContent, File
from settings.connections import postgres_connection_manager
from .queries import (
    STORE_LIBRARY_CONTENT,
    GET_LIBRARY_CONTENT_LIST,
)


def _enrich_library_content(data: dict) -> LibraryContent:
    thumbnail = File(
        id=data["thumbnail_id"],
        file_path=data["thumbnail_url"],
    )
    return LibraryContent(
        id=data["id"],
        title=data["title"],
        description=data["description"],
        content_url=data["content_url"],
        information_library_id=data["library_id"],
        thumbnail=thumbnail,
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


class LibraryContentRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def store(
        cls,
        library_content: LibraryContent,
    ) -> LibraryContent:
        result = cls.connection_manager.execute_atomic_query(
            query=STORE_LIBRARY_CONTENT,
            variables=(
                library_content.title,
                library_content.description,
                library_content.content_url,
                library_content.thumbnail_id,
                library_content.information_library_id,
            ),
        )
        stored_library_content = deepcopy(library_content)
        stored_library_content.id = result["id"]
        stored_library_content.created_at = result["created_at"]
        stored_library_content.updated_at = result["updated_at"]
        return stored_library_content

    @classmethod
    def get_list(
        cls, library_id: int, limit: int, offset: int
    ) -> tuple[int, list[LibraryContent]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_LIBRARY_CONTENT_LIST,
            variables=(library_id, offset, limit),
        )
        if not result:
            return 0, []

        total_count = result[0]["total_count"]
        content = [_enrich_library_content(item) for item in result]
        return total_count, content
