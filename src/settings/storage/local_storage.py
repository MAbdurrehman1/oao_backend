import os
from pathlib import Path
from .i_storage import StorageInterface


class LocalStorage(StorageInterface):
    def __init__(self, base_path: str, media_url: str):
        self.base_path = base_path
        self.media_url = media_url
        Path(base_path).mkdir(parents=True, exist_ok=True)
        assert os.path.isdir(base_path)

    def store_file(self, file_data: bytes, file_name: str, content_type: str) -> str:
        file_path = os.path.join(self.base_path, file_name)
        media_path = os.path.join(self.media_url, file_name)
        with open(file_path, "wb") as f:
            f.write(file_data)
        return media_path
