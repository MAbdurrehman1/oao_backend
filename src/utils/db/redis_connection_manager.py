import time
from typing import TypedDict

from redis import BlockingConnectionPool, StrictRedis, Redis


class RedisConnectionPoolKwargs(TypedDict, total=False):
    max_connections: int
    timeout: int
    host: str
    port: int
    db: int
    username: str
    password: str


class RedisConnectionManager:
    _singleton_pool: BlockingConnectionPool | None = None

    def _get_pool(self) -> BlockingConnectionPool:
        if self._singleton_pool:
            return self._singleton_pool

        raise AttributeError(
            "RedisConnectionManager has not been initialized! "
            "Use RedisConnectionManager.initialize to do so."
        )

    @classmethod
    def initialize(cls, pool_kwargs: RedisConnectionPoolKwargs, n_retries: int = 2):
        if not cls._singleton_pool:
            cls._singleton_pool = cls._create_pool_with_retry(
                pool_kwargs=pool_kwargs, n_retries=n_retries
            )

        return cls()

    @classmethod
    def _create_pool_with_retry(
        cls, pool_kwargs: RedisConnectionPoolKwargs, n_retries: int = 2
    ) -> BlockingConnectionPool:
        try:
            return BlockingConnectionPool(**pool_kwargs)
        except Exception as e:
            if n_retries <= 0:
                raise e

            time.sleep(1)
            return cls._create_pool_with_retry(
                pool_kwargs=pool_kwargs, n_retries=n_retries - 1
            )

    def _get_connection(self) -> StrictRedis:
        connection = Redis(connection_pool=self._get_pool())
        return connection

    def get_value(self, key):
        connection = self._get_connection()
        return connection.get(key)

    def exists_key(self, key):
        connection = self._get_connection()
        return True if connection.exists(key) == 1 else False

    def set_value(self, key, value, exp: int | None = None):
        connection = self._get_connection()
        connection.set(key, value)
        if exp:
            connection.expire(key, time=exp)

    def delete_key(self, key):
        connection = self._get_connection()
        connection.delete(key)

    def get_keys_with_prefix(self, prefix: str):
        connection = self._get_connection()
        return [
            item.decode("utf-8")
            for item in connection.keys(prefix + "*")  # type: ignore
        ]

    def push_values(self, key, values: list, exp: int | None = None):
        connection = self._get_connection()
        connection.lpush(key, *values)
        if exp:
            connection.expire(key, time=exp)

    def get_all_list_values(self, key: str):
        connection = self._get_connection()
        values_list = connection.lrange(key, 0, -1)
        values_list = [item.decode("utf-8") for item in values_list]  # type: ignore
        return values_list

    def _delete_all(self):
        connection = self._get_connection()
        connection.flushdb()
