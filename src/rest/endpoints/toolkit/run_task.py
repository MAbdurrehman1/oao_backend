from fastapi import Depends, Security
from pydantic import BaseModel

from services import run_task
from ..dependencies import AdminRequired, auth_header
from ...router import router, Tags


class RunTaskRequestModel(BaseModel):
    args: list[str]


class RunTaskResponseModel(BaseModel):
    result: str = "Task Started"


@router.post("/tasks/{slug}/run/", tags=[Tags.admin])
def run_task_endpoint(
    slug: str,
    payload: RunTaskRequestModel,
    _: bool = Depends(AdminRequired()),
    __: str = Security(auth_header),
) -> RunTaskResponseModel:
    run_task(slug, *payload.args)
    return RunTaskResponseModel()
