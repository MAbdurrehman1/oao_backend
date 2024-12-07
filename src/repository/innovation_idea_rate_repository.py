from copy import deepcopy

from entity import InnovationIdeaRate
from repository.queries import (
    CREATE_INNOVATION_IDEA_RATE,
)
from settings.connections import postgres_connection_manager


class InnovationIdeaRateRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def store(cls, innovation_idea_rate: InnovationIdeaRate) -> InnovationIdeaRate:
        result = cls.connection_manager.execute_atomic_query(
            query=CREATE_INNOVATION_IDEA_RATE,
            variables=(
                innovation_idea_rate.innovation_idea_id,
                innovation_idea_rate.manager_id,
                innovation_idea_rate.rate,
            ),
        )
        result_idea = deepcopy(innovation_idea_rate)
        result_idea.id = result["id"]
        result_idea.created_at = result["created_at"]
        result_idea.updated_at = result["updated_at"]
        return result_idea
