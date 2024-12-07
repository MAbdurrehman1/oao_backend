from fastapi import UploadFile, Request, Depends, Security
from pydantic import BaseModel

from entity import User
from services import import_contact_list
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class UploadContactsListResponseModel(BaseModel):
    result: str = "Successful Contacts List Upload"


@router.post("/contacts/upload/", tags=[Tags.admin])
def upload_contacts_list_endpoint(
    request: Request,
    file: UploadFile,
    organization_id: int,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
):
    import_contact_list(organization_id, file.file)
    return UploadContactsListResponseModel()
