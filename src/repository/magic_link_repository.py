from uuid import UUID

from cexceptions import CredentialValidationException
from settings import configs
from settings.connections import redis_connection_manager


class MagicLinkRepository:
    connection_manager = redis_connection_manager
    prefix: str = "magic-links:token:"

    @classmethod
    def set_magic_link(cls, user_id: int, token: UUID) -> None:
        key = cls.prefix + str(token)
        cls.connection_manager.set_value(
            key, str(user_id), exp=configs.magic_link_exp_mins * 60
        )

    @classmethod
    def get_user_id(cls, token: UUID) -> int:
        key = cls.prefix + str(token)
        value = cls.connection_manager.get_value(key)
        if value is None:
            raise CredentialValidationException(
                entity="Magic Link",
            )
        return int(value)

    @classmethod
    def remove_magic_link(cls, token: UUID) -> None:
        key = cls.prefix + str(token)
        cls.connection_manager.delete_key(key)
