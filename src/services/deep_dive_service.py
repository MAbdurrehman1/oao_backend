from uuid import UUID

from entity import DeepDive
from repository import DeepDiveRepository


def get_deep_dive_list(
    participation_id: UUID, offset: int, limit: int
) -> tuple[int, list[DeepDive]]:
    deep_dive_slugs = DeepDiveRepository.get_deep_dive_strategy(
        participation_id=participation_id
    )
    total_count, deep_dives = DeepDiveRepository.get_deep_dive_list_by_slug(
        slug_list=deep_dive_slugs,
        offset=offset,
        limit=limit,
    )
    return total_count, deep_dives
