from datetime import datetime
from typing import Self

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, Module, File
from services import get_modules_list
from settings import configs
from ..dependencies import EmployeeRequired, auth_header
from ...router import router, Tags


class ModuleResponse(BaseModel):
    title: str
    description: str
    end_date: str
    duration: int
    order: int
    animated_thumbnail_url: str
    still_thumbnail_url: str
    id: int
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: Module) -> Self:
        assert isinstance(entity.id, int)
        assert isinstance(entity.end_date, datetime)
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)
        assert isinstance(entity.still_thumbnail, File)
        assert isinstance(entity.animated_thumbnail, File)
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            end_date=entity.end_date.strftime(configs.date_time_format),
            duration=entity.duration,
            order=entity.order,
            animated_thumbnail_url=entity.animated_thumbnail.file_url,
            still_thumbnail_url=entity.still_thumbnail.file_url,
            created_at=entity.created_at.strftime(configs.date_time_format),
            updated_at=entity.updated_at.strftime(configs.date_time_format),
        )


class GetModulesListResponseModel(BaseModel):
    total_count: int
    result: list[ModuleResponse]


@router.get("/modules/", tags=[Tags.participation])
def get_modules_list_endpoint(
    offset: int = 0,
    limit: int = 5,
    user: User = Depends(EmployeeRequired()),
    __: str = Security(auth_header),
):
    assert isinstance(user.id, int)
    total_count, modules_list = get_modules_list(
        offset=offset,
        limit=limit,
        user_id=user.id,
    )
    response_models = [ModuleResponse.from_entity(m) for m in modules_list]
    return GetModulesListResponseModel(result=response_models, total_count=total_count)
