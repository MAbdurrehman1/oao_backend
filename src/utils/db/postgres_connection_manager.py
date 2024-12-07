import time
from contextlib import contextmanager
from typing import TypedDict

from psycopg2 import OperationalError
from psycopg2.extras import DictCursor, execute_values
from psycopg2.pool import SimpleConnectionPool


class PostgresConnectionPoolKwargs(TypedDict, total=False):
    user: str
    password: str
    host: str
    port: int
    database: str

    minconn: int
    maxconn: int

    keepalives: int
    keepalives_idle: int
    keepalives_interval: int
    keepalives_count: int


class PostgresConnectionManager:
    _singleton_pool: SimpleConnectionPool | None = None

    def _get_pool(self) -> SimpleConnectionPool:
        if self._singleton_pool:
            return self._singleton_pool

        raise AttributeError(
            "PostgresConnectionManager has not been initialized! "
            "Use PostgresConnectionManager.initialize to do so."
        )

    @classmethod
    def initialize(cls, pool_kwargs: PostgresConnectionPoolKwargs, n_retries: int = 2):
        if not cls._singleton_pool:
            cls._singleton_pool = cls._create_pool_with_retry(
                pool_kwargs=pool_kwargs, n_retries=n_retries
            )

        return cls()

    @staticmethod
    def _create_pool_with_retry(
        pool_kwargs: PostgresConnectionPoolKwargs, n_retries: int = 2
    ) -> SimpleConnectionPool:
        try:
            return SimpleConnectionPool(**pool_kwargs)
        except OperationalError as e:
            if n_retries <= 0:
                raise e

            time.sleep(1)
            return PostgresConnectionManager._create_pool_with_retry(
                pool_kwargs=pool_kwargs, n_retries=n_retries - 1
            )

    def execute_atomic_query(self, query: str, variables=None) -> dict:
        with self.open_cursor() as cursor:
            cursor.execute(query, vars=variables)
            if cursor.pgresult_ptr is not None:
                return cursor.fetchone()
            else:
                return {}

    def execute_atomic_query_all(self, query: str, variables=None) -> list:
        with self.open_cursor() as cursor:
            cursor.execute(query, vars=variables)
            if cursor.pgresult_ptr is not None:
                return cursor.fetchall()
            else:
                return []

    def execute_values_atomic_query(
        self, query: str, variables, fetch: bool = True
    ) -> list:
        with self.open_cursor() as cursor:
            result = execute_values(cursor, query, variables, fetch=fetch)
            return result

    @contextmanager
    def open_cursor(self):
        with self._open_connection() as conn:
            cursor = conn.cursor(cursor_factory=DictCursor)
            try:
                yield cursor
            finally:
                cursor.close()

    @contextmanager
    def _open_connection(self):
        connection = self._get_connection()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            self._putback_connection(connection)

    def _get_connection(self):
        connection = self._get_pool().getconn()
        return connection

    def _putback_connection(self, connection):
        self._get_pool().putconn(connection)
