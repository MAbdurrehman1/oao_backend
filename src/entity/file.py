from datetime import datetime

from pydantic import BaseModel

from settings import configs
from .user import User


class File(BaseModel):
    content_type: str | None = None
    file_content: bytes | None = None
    name: str | None = None
    file_path: str | None = None
    user: User | None = None
    user_id: int | None = None
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def file_url(self) -> str:
        assert isinstance(self.file_path, str)
        return configs.storage_url + self.file_path
