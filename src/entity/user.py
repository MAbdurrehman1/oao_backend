from datetime import datetime

from pydantic import BaseModel, field_validator

from utils.validation_helpers import assert_email_validation


class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    is_admin: bool = False
    id: int | None = None
    password: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_validator("email")
    @classmethod
    def email_validate(cls, v: str) -> str:
        assert_email_validation(v)
        return v.lower()
