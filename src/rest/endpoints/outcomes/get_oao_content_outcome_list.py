from datetime import datetime
from typing import Self

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, Outcome
from services import get_oao_content_outcomes_list
from settings import configs
from ..dependencies import EmployeeRequired, auth_header
from ...router import router, Tags


class OutcomeResponse(BaseModel):
    id: int
    title: str
    description: str
    oao_content_id: int
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: Outcome) -> Self:
        assert isinstance(entity.id, int)
        assert isinstance(entity.oao_content_id, int)
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            oao_content_id=entity.oao_content_id,
            created_at=entity.created_at.strftime(configs.date_time_format),
            updated_at=entity.updated_at.strftime(configs.date_time_format),
        )


class GetOAOContentOutcomeListResponseModel(BaseModel):
    total_count: int
    result: list[OutcomeResponse]


@router.get("/oao_content/{_id}/outcomes/", tags=[Tags.participation])
def get_oao_content_outcome_list_endpoint(
    _id: int,
    offset: int = 0,
    limit: int = 5,
    _: User = Depends(EmployeeRequired()),
    __: str = Security(auth_header),
) -> GetOAOContentOutcomeListResponseModel:
    total_count, outcomes = get_oao_content_outcomes_list(
        offset=offset,
        limit=limit,
        oao_content_id=_id,
    )
    response_models = [OutcomeResponse.from_entity(item) for item in outcomes]
    return GetOAOContentOutcomeListResponseModel(
        result=response_models, total_count=total_count
    )
