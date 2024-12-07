from datetime import datetime
from typing import Self
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel

from entity import User, DeepDive, File
from services import get_deep_dive_list
from settings import configs
from ..dependencies import EmployeeRequired
from ...router import router, Tags


class DeepDiveResponse(BaseModel):
    id: int
    title: str
    slug: str | None
    description: str | None
    url: str
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: DeepDive) -> Self:
        assert isinstance(entity.id, int)
        assert isinstance(entity.thumbnail, File)
        assert isinstance(entity.thumbnail.file_path, str)
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)
        return cls(
            id=entity.id,
            title=entity.title,
            slug=entity.slug,
            description=entity.description,
            url=entity.thumbnail.file_path,
            created_at=entity.created_at.strftime(configs.date_time_format),
            updated_at=entity.updated_at.strftime(configs.date_time_format),
        )


class GetDeepDiveListResponseModel(BaseModel):
    total_count: int
    result: list[DeepDiveResponse]


@router.get(
    "/deep_dives/",
    tags=[Tags.participation],
)
def get_deep_dive_list_endpoint(
    participation_id: UUID,
    offset: int = 0,
    limit: int = 10,
    _: User = Depends(EmployeeRequired()),
) -> GetDeepDiveListResponseModel:
    total_count, deep_dives = get_deep_dive_list(
        offset=offset,
        limit=limit,
        participation_id=participation_id,
    )
    deep_dives_response = [
        DeepDiveResponse.from_entity(entity=item) for item in deep_dives
    ]
    return GetDeepDiveListResponseModel(
        result=deep_dives_response, total_count=total_count
    )
