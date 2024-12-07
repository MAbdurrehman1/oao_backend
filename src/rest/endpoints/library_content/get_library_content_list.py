from datetime import datetime
from typing import Self

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User, File, LibraryContent
from services import get_library_content_list
from settings import configs
from ..dependencies import EmployeeRequired, auth_header
from ...router import router, Tags


class LibraryContentResponse(BaseModel):
    id: int
    title: str
    description: str
    content_url: str
    thumbnail_url: str
    information_library_id: int
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: LibraryContent) -> Self:
        assert isinstance(entity.id, int)
        assert isinstance(entity.information_library_id, int)
        assert isinstance(entity.thumbnail, File)
        assert isinstance(entity.thumbnail.file_path, str)
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            content_url=entity.content_url,
            thumbnail_url=entity.thumbnail.file_url,
            information_library_id=entity.information_library_id,
            created_at=entity.created_at.strftime(configs.date_time_format),
            updated_at=entity.updated_at.strftime(configs.date_time_format),
        )


class GetLibraryContentListResponseModel(BaseModel):
    total_count: int
    result: list[LibraryContentResponse]


@router.get("/libraries/{_id}/content/", tags=[Tags.participation])
def get_library_content_list_endpoint(
    _id: int,
    offset: int = 0,
    limit: int = 5,
    user: User = Depends(EmployeeRequired()),
    __: str = Security(auth_header),
) -> GetLibraryContentListResponseModel:
    assert isinstance(user.id, int)
    total_count, content_list = get_library_content_list(
        offset=offset,
        limit=limit,
        library_id=_id,
        user_id=user.id,
    )
    response_models = [
        LibraryContentResponse.from_entity(item) for item in content_list
    ]
    return GetLibraryContentListResponseModel(
        result=response_models, total_count=total_count
    )
