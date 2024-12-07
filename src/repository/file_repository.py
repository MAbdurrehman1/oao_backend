from copy import deepcopy

from cexceptions import NotFoundException
from entity import Employee, File
from repository.queries import (
    CREATE_FILE_RECORD,
    CHECK_FILE_NAME_EXISTS,
    CHECK_FILE_EXISTS_BY_ID,
    GET_FILE_PATH_BY_ID,
    GET_FILES_LIST,
)
from settings.connections import postgres_connection_manager
from settings.storage import storage


def _enrich_employee(data: dict) -> Employee:
    return Employee(
        id=data["id"],
        role_title=data["role_title"],
        location=data["location"],
        organization_id=data["organization_id"],
    )


def _enrich_file(data: dict) -> File:
    return File(
        id=data["id"],
        content_type=data["content_type"],
        name=data["name"],
        user_id=data["user_id"],
        file_path=data["file_path"],
        created_at=data["created_at"],
        updated_at=data["created_at"],
    )


class FileRepository:
    storage = storage
    connection_manager = postgres_connection_manager

    @classmethod
    def store(cls, file: File) -> File:
        assert isinstance(file.file_content, bytes)
        assert isinstance(file.name, str)
        assert isinstance(file.content_type, str)
        file_path = cls.storage.store_file(
            file_data=file.file_content,
            file_name=file.name,
            content_type=file.content_type,
        )
        stored_file = deepcopy(file)
        stored_file.file_path = file_path
        result = cls.connection_manager.execute_atomic_query(
            query=CREATE_FILE_RECORD,
            variables=(
                stored_file.name,
                stored_file.file_path,
                stored_file.user_id,
                file.content_type,
            ),
        )
        stored_file.id = result["id"]
        stored_file.created_at = result["created_at"]
        stored_file.updated_at = result["updated_at"]
        return stored_file

    @classmethod
    def file_name_exists(cls, file_name: str) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_FILE_NAME_EXISTS,
            variables=(file_name,),
        )
        return result["exists"]

    @classmethod
    def exists(cls, _id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_FILE_EXISTS_BY_ID,
            variables=(_id,),
        )
        return result["exists"]

    @classmethod
    def get_path_by_id(cls, _id: int) -> str:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_FILE_PATH_BY_ID,
            variables=(_id,),
        )
        if not result:
            raise NotFoundException(entity="File", arg="ID", value=str(_id))
        return result["file_path"]

    @classmethod
    def get_list(cls, offset: int, limit: int) -> tuple[int, list[File]]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_FILES_LIST, variables=(offset, limit)
        )
        if not result:
            return 0, []
        total_count = result[0]["total_count"]
        return total_count, [_enrich_file(data) for data in result]
