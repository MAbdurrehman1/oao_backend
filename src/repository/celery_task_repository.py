from uuid import UUID

from settings.connections import redis_connection_manager


class CeleryTaskRepository:
    connection_manager = redis_connection_manager
    prefix: str = "async_tasks:"

    @classmethod
    def set_task_id(cls, post_fix: str, identifier: int, task_id: UUID) -> None:
        key = cls.prefix + post_fix + f"{identifier}"
        cls.connection_manager.set_value(key, value=str(task_id))

    @classmethod
    def get_task_id(cls, post_fix: str, identifier: int) -> UUID | None:
        key = cls.prefix + post_fix + f"{identifier}"
        value = cls.connection_manager.get_value(key)
        if value:
            return UUID(value.decode("utf-8"))
        return None

    @classmethod
    def remove_task_id(cls, post_fix: str, identifier: int) -> None:
        key = cls.prefix + post_fix + f"{identifier}"
        cls.connection_manager.delete_key(key)
