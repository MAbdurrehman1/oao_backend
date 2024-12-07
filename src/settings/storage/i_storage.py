from abc import ABC, abstractmethod


class StorageInterface(ABC):
    @abstractmethod
    def store_file(self, file_data: bytes, file_name: str, content_type: str) -> str:
        """Store the file and return the path where it is stored."""
        raise NotImplementedError
