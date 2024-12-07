from azure.identity import ClientSecretCredential
from pydantic import BaseModel

from utils.db import PostgresConnectionManager, RedisConnectionManager
from .config import configs


def _postgres_pool_kwargs():
    keepalive_kwargs = {
        "keepalives": 1,
        "keepalives_idle": 5,
        "keepalives_interval": 1,
        "keepalives_count": 5,
    }
    other_kwargs = dict(
        user=configs.postgres_user,
        password=configs.postgres_password,
        host=configs.postgres_host,
        port=configs.postgres_port,
        database=configs.postgres_db,
        minconn=1,
        maxconn=configs.postgres_max_connections,
    )
    return keepalive_kwargs | other_kwargs


postgres_connection_manager = PostgresConnectionManager.initialize(
    pool_kwargs=_postgres_pool_kwargs()
)


def _redis_pool_kwargs():
    return dict(
        max_connections=5,
        timeout=200,
        host=configs.redis_host,
        port=configs.redis_port,
        db=configs.redis_db,
        password=configs.redis_password,
        username=configs.redis_user,
    )


redis_connection_manager = RedisConnectionManager.initialize(
    pool_kwargs=_redis_pool_kwargs()
)
if configs.is_test_environment:

    class Token(BaseModel):
        token: str

    class TestClient:
        @staticmethod
        def get_token(arg):
            return Token(token="test-token")

    azure_client = TestClient()
else:
    azure_client = ClientSecretCredential(  # type: ignore
        configs.ms_graph_tenant_id,
        configs.ms_graph_client_id,
        configs.ms_graph_client_secret,
    )
