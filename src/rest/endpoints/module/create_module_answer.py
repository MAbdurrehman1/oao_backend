from uuid import UUID

from fastapi import Depends, Security
from pydantic import BaseModel

from entity import User
from services import create_module_answer
from ..dependencies import ETLRequired, auth_header
from ...router import router, Tags


class CreateModuleAnswerRequestModel(BaseModel):
    participation_id: UUID


class CreateModuleAnswerResponseModel(BaseModel):
    result: str = "Module answer created successfully."


@router.post("/modules/{_id}/answer/", tags=[Tags.etl])
def create_module_answer_endpoint(
    _id: int,
    payload: CreateModuleAnswerRequestModel,
    _: User = Depends(ETLRequired()),
    __: str = Security(auth_header),
) -> CreateModuleAnswerResponseModel:
    create_module_answer(
        participation_id=payload.participation_id,
        module_id=_id,
    )
    return CreateModuleAnswerResponseModel()
