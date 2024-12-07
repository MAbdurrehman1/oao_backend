from entity import ContentSummary
from repository import ContentSummaryRepository


def get_content_summary_list(
    module_id: int,
    offset: int,
    limit: int,
) -> tuple[int, list[ContentSummary]]:
    total_count, summaries = ContentSummaryRepository.get_list(
        module_id=module_id, offset=offset, limit=limit
    )
    return total_count, summaries
