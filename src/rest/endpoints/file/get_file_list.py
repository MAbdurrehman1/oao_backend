from datetime import datetime
from typing import Self

from fastapi import Depends
from pydantic import BaseModel
from settings import configs

from entity import User, File
from services import get_files_list
from ..dependencies import AdminRequired
from ...router import router, Tags


class FileResponse(BaseModel):
    id: int
    name: str
    content_type: str | None
    user_id: int
    file_url: str
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: File) -> Self:
        assert isinstance(entity.id, int)
        assert isinstance(entity.user_id, int)
        assert isinstance(entity.name, str)
        assert isinstance(entity.file_path, str)
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)
        return cls(
            id=entity.id,
            name=entity.name,
            content_type=entity.content_type,
            user_id=entity.user_id,
            file_url=entity.file_url,
            created_at=entity.created_at.strftime(configs.date_time_format),
            updated_at=entity.updated_at.strftime(configs.date_time_format),
        )


class GetFilesListResponseModel(BaseModel):
    total_count: int
    result: list[FileResponse]


@router.get(
    "/files/",
    tags=[Tags.admin],
)
def get_files_list_endpoint(
    offset: int = 0,
    limit: int = 10,
    user: User = Depends(AdminRequired()),
) -> GetFilesListResponseModel:
    assert isinstance(user.id, int)
    total_count, files = get_files_list(
        offset=offset,
        limit=limit,
    )
    files_response = [FileResponse.from_entity(entity=file) for file in files]
    return GetFilesListResponseModel(result=files_response, total_count=total_count)
