from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import submit_preferred_lang
from ..dependencies import EmployeeRequired, auth_header
from ...router import router, Tags


class SubmitPreferredRequestModel(BaseModel):
    lang: str


class SubmitPreferredResponseModel(BaseModel):
    result: str = "Preferred Language Submitted Successfully"


@router.post("/preferred-lang/", tags=[Tags.participation])
def submit_preferred_lang_endpoint(
    payload: SubmitPreferredRequestModel,
    user: User = Depends(EmployeeRequired()),
    __: str = Security(auth_header),
) -> SubmitPreferredResponseModel:
    assert isinstance(user.id, int)
    submit_preferred_lang(
        user_id=user.id,
        lang=payload.lang,
    )
    return SubmitPreferredResponseModel()
