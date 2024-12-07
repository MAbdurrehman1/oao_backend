from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import publish_report
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class PublishReportResponseModel(BaseModel):
    result: str = "Report Published Successfully"


@router.post("/reports/{_id}/publish/", tags=[Tags.admin])
def publish_report_endpoint(
    _id: int,
    _: User = Depends(AdminRequired()),
    __: str = Security(auth_header),
):
    publish_report(
        _id=_id,
    )
    return PublishReportResponseModel()
