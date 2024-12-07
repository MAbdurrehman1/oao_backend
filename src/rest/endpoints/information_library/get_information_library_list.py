from datetime import datetime
from typing import Self

from fastapi import Depends
from pydantic import BaseModel

from entity import User, InformationLibrary
from services import get_information_library_list
from settings import configs
from ..dependencies import EmployeeRequired
from ...router import router, Tags


class InformationLibraryResponse(BaseModel):
    id: int
    title: str
    short_description: str
    long_description: str
    organization_id: int | None
    deep_dive_id: int
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: InformationLibrary) -> Self:
        assert isinstance(entity.id, int)
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)
        assert isinstance(entity.deep_dive_id, int)
        return cls(
            id=entity.id,
            title=entity.title,
            short_description=entity.short_description,
            long_description=entity.long_description,
            organization_id=entity.organization_id,
            deep_dive_id=entity.deep_dive_id,
            created_at=entity.created_at.strftime(configs.date_time_format),
            updated_at=entity.updated_at.strftime(configs.date_time_format),
        )


class GetInformationLibraryListResponseModel(BaseModel):
    total_count: int
    result: list[InformationLibraryResponse]


@router.get(
    "/deep_dives/{_id}/libraries/",
    tags=[Tags.participation],
)
def get_information_library_list_endpoint(
    _id: int,
    offset: int = 0,
    limit: int = 10,
    user: User = Depends(EmployeeRequired()),
) -> GetInformationLibraryListResponseModel:
    assert isinstance(user.id, int)
    total_count, libraries = get_information_library_list(
        deep_dive_id=_id,
        user_id=user.id,
        offset=offset,
        limit=limit,
    )
    ideas_response = [
        InformationLibraryResponse.from_entity(entity=lib) for lib in libraries
    ]
    return GetInformationLibraryListResponseModel(
        result=ideas_response, total_count=total_count
    )
