from entity import File
from repository import FileRepository
from .utils import generate_random_string


def _get_file_extension(file_name: str) -> str:
    return file_name.split(".")[-1]


def _get_random_file_name(file_extension: str, length: int = 20) -> str:
    return f"{generate_random_string(length)}.{file_extension}"


def _get_new_file_name(file_extension: str) -> str:
    file_name = _get_random_file_name(file_extension=file_extension)
    if not FileRepository.file_name_exists(file_name=file_name):
        return file_name
    else:
        return _get_new_file_name(file_extension=file_extension)


def upload_file(file_content: bytes, file_name: str, user_id: int, content_type: str):
    file = File(
        file_content=file_content,
        user_id=user_id,
        content_type=content_type,
    )
    extension = _get_file_extension(file_name=file_name)
    file_name = _get_new_file_name(file_extension=extension)
    file.name = file_name
    stored_file = FileRepository.store(file)
    return stored_file


def get_files_list(
    limit: int,
    offset: int,
) -> tuple[int, list[File]]:
    limit = 50 if limit > 50 else limit
    total_count, files = FileRepository.get_list(offset, limit=limit)
    return total_count, files
