from fastapi import UploadFile, Depends, Security
from pydantic import BaseModel

from entity import User
from services import upload_file
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class FileUploadResponse(BaseModel):
    file_id: int


class UploadResponseModel(BaseModel):
    result: FileUploadResponse


@router.post("/upload/", tags=[Tags.admin])
def upload_endpoint(
    file: UploadFile,
    user: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> UploadResponseModel:
    assert isinstance(user.id, int)
    assert isinstance(file.filename, str)
    assert isinstance(file.content_type, str)
    stored_file = upload_file(
        file_content=file.file.read(),
        user_id=user.id,
        file_name=file.filename,
        content_type=file.content_type,
    )
    assert isinstance(stored_file.id, int)
    return UploadResponseModel(result=FileUploadResponse(file_id=stored_file.id))
