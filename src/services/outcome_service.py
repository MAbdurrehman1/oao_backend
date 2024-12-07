from entity import Outcome
from repository import OutcomeRepository


def get_oao_content_outcomes_list(
    oao_content_id: int,
    limit: int,
    offset: int,
) -> tuple[int, list[Outcome]]:
    total_count, outcomes = OutcomeRepository.get_list(
        oao_content_id=oao_content_id,
        limit=limit,
        offset=offset,
    )
    return total_count, outcomes
