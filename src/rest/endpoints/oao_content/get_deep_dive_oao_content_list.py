from datetime import datetime
from typing import Self

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, OAOContent, File
from services import get_deep_dive_oao_content_list
from settings import configs
from ..dependencies import EmployeeRequired, auth_header
from ...router import router, Tags


class OAOContentResponse(BaseModel):
    id: int
    title: str
    short_description: str
    long_description: str
    content_url: str
    thumbnail_url: str
    deep_dive_id: int
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: OAOContent) -> Self:
        assert isinstance(entity.id, int)
        assert isinstance(entity.deep_dive_id, int)
        assert isinstance(entity.thumbnail, File)
        assert isinstance(entity.thumbnail.file_path, str)
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)
        return cls(
            id=entity.id,
            title=entity.title,
            short_description=entity.short_description,
            long_description=entity.long_description,
            content_url=entity.content_url,
            thumbnail_url=entity.thumbnail.file_url,
            deep_dive_id=entity.deep_dive_id,
            created_at=entity.created_at.strftime(configs.date_time_format),
            updated_at=entity.updated_at.strftime(configs.date_time_format),
        )


class GetOAOContentListResponseModel(BaseModel):
    total_count: int
    result: list[OAOContentResponse]


@router.get("/deep_dives/{_id}/oao_content/", tags=[Tags.participation])
def get_deep_dive_oao_content_list_endpoint(
    _id: int,
    offset: int = 0,
    limit: int = 5,
    _: User = Depends(EmployeeRequired()),
    __: str = Security(auth_header),
) -> GetOAOContentListResponseModel:
    total_count, content_list = get_deep_dive_oao_content_list(
        offset=offset,
        limit=limit,
        deep_dive_id=_id,
    )
    response_models = [OAOContentResponse.from_entity(item) for item in content_list]
    return GetOAOContentListResponseModel(
        result=response_models, total_count=total_count
    )
