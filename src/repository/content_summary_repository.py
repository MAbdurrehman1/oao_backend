from copy import deepcopy

from settings.connections import postgres_connection_manager
from entity import ContentSummary
from .queries import GET_CONTENT_SUMMARY_LIST, STORE_CONTENT_SUMMARY


def _enrich_content_summary(data: dict) -> ContentSummary:
    return ContentSummary(
        id=data["id"],
        module_id=data["module_id"],
        title=data["title"],
        description=data["description"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


class ContentSummaryRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def store(cls, content_summary: ContentSummary) -> ContentSummary:
        result = cls.connection_manager.execute_atomic_query(
            query=STORE_CONTENT_SUMMARY,
            variables=(
                content_summary.title,
                content_summary.description,
                content_summary.module_id,
            ),
        )
        stored_content_summary = deepcopy(content_summary)
        stored_content_summary.id = result["id"]
        stored_content_summary.created_at = result["created_at"]
        stored_content_summary.updated_at = result["updated_at"]
        return stored_content_summary

    @classmethod
    def get_list(
        cls, module_id: int, offset: int, limit: int
    ) -> tuple[int, list[ContentSummary]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_CONTENT_SUMMARY_LIST,
            variables=(module_id, offset, limit),
        )
        if not result:
            return 0, []

        total_count = result[0]["total_count"]
        summaries = [_enrich_content_summary(data) for data in result]
        return total_count, summaries
