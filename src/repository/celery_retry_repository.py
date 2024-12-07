from uuid import UUID

from settings.connections import redis_connection_manager


class CeleryRetryRepository:
    connection_manager = redis_connection_manager
    prefix: str = "failed:"

    @classmethod
    def set_retry_count(
        cls,
        postfix: str,
        identifier: int | UUID | str,
        retry_count: int = 0,
    ) -> None:
        key = cls.prefix + postfix + str(identifier)
        cls.connection_manager.set_value(key, retry_count)

    @classmethod
    def get_batch_keys(
        cls,
        postfix: str,
        batch_id: int | str = "",
    ) -> list[str]:
        prefix = cls.prefix + postfix + str(batch_id)
        keys = cls.connection_manager.get_keys_with_prefix(prefix)
        return keys

    @classmethod
    def get_retry_count(
        cls,
        postfix: str,
        identifier: int | UUID | str,
    ) -> int | None:
        key = cls.prefix + postfix + str(identifier)
        value = cls.connection_manager.get_value(key)
        if value:
            return int(value.decode("utf-8"))
        return None

    @classmethod
    def archive_failed_attempt(
        cls,
        postfix: str,
        identifier: int | UUID | str,
    ) -> None:
        key = cls.prefix + postfix + str(identifier)
        cls.connection_manager.delete_key(key)
        archived_key = "archived:" + key
        cls.connection_manager.set_value(archived_key, 0)

    @classmethod
    def remove_failed_attempt(
        cls,
        postfix: str,
        identifier: int | UUID | str,
    ) -> None:
        key = cls.prefix + postfix + str(identifier)
        cls.connection_manager.delete_key(key)

    @classmethod
    def get_archived_batch_keys(
        cls,
        postfix: str,
        batch_id: int | str = "",
    ) -> list[str]:
        prefix = "archived:" + cls.prefix + postfix + str(batch_id)
        keys = cls.connection_manager.get_keys_with_prefix(prefix)
        return keys
