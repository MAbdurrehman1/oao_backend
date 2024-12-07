from settings import configs
from settings.connections import redis_connection_manager


class ReminderRepository:
    connection_manager = redis_connection_manager
    prefix: str = "reminder:"

    @classmethod
    def store_success(cls, postfix: str, identifier: any):  # type: ignore
        key = cls.prefix + postfix + str(identifier)
        cls.connection_manager.set_value(
            key=key,
            value="success",
            exp=configs.first_participant_schedule_reminder_expire,
        )

    @classmethod
    def get_successful_reminders(
        cls,
        postfix: str,
    ) -> list[str]:
        prefix = cls.prefix + postfix
        keys = cls.connection_manager.get_keys_with_prefix(prefix)
        return keys
