from datetime import datetime
from typing import Self

from fastapi import Depends
from pydantic import BaseModel

from entity import User, ContentSummary
from services import get_content_summary_list
from settings import configs
from ..dependencies import EmployeeRequired
from ...router import router, Tags


class ContentSummaryResponse(BaseModel):
    id: int
    module_id: int
    title: str
    description: str
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: ContentSummary) -> Self:
        assert isinstance(entity.id, int)
        assert isinstance(entity.module_id, int)
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)
        return cls(
            id=entity.id,
            module_id=entity.module_id,
            title=entity.title,
            description=entity.description,
            created_at=entity.created_at.strftime(configs.date_time_format),
            updated_at=entity.updated_at.strftime(configs.date_time_format),
        )


class GetContentSummaryListResponseModel(BaseModel):
    total_count: int
    result: list[ContentSummaryResponse]


@router.get(
    "/modules/{_id}/content-summaries/",
    tags=[Tags.participation],
)
def get_content_summary_list_endpoint(
    _id: int,
    offset: int = 0,
    limit: int = 10,
    _: User = Depends(EmployeeRequired()),
) -> GetContentSummaryListResponseModel:
    total_count, summaries = get_content_summary_list(
        module_id=_id,
        offset=offset,
        limit=limit,
    )
    summaries_response = [
        ContentSummaryResponse.from_entity(entity=item) for item in summaries
    ]
    return GetContentSummaryListResponseModel(
        result=summaries_response, total_count=total_count
    )
