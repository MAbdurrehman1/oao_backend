from copy import deepcopy

from .queries import STORE_OUTCOME
from entity import Outcome
from settings.connections import postgres_connection_manager
from .queries import GET_OAO_CONTENT_OUTCOME_LIST


def _enrich_outcome(data: dict) -> Outcome:
    return Outcome(
        id=data["id"],
        title=data["title"],
        description=data["description"],
        oao_content_id=data["oao_content_id"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


class OutcomeRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def store(cls, outcome: Outcome) -> Outcome:
        result = cls.connection_manager.execute_atomic_query(
            query=STORE_OUTCOME,
            variables=(
                outcome.title,
                outcome.description,
                outcome.oao_content_id,
            ),
        )
        stored_outcome = deepcopy(outcome)
        stored_outcome.id = result["id"]
        stored_outcome.created_at = result["created_at"]
        stored_outcome.updated_at = result["updated_at"]
        return stored_outcome

    @classmethod
    def get_list(
        cls,
        oao_content_id: int,
        limit: int,
        offset: int,
    ) -> tuple[int, list[Outcome]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_OAO_CONTENT_OUTCOME_LIST,
            variables=(oao_content_id, offset, limit),
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        outcomes = [_enrich_outcome(item) for item in result]
        return total_count, outcomes
