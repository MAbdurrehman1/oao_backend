from celery import Celery
from settings import configs, initiate_sentry
from settings import CELERY_CONFIG

initiate_sentry(
    sentry_dns=configs.celery_sentry_dsn,
    environment=configs.environment,
)

celery_app = Celery(
    "celery_app",
    broker=f"redis://{configs.redis_host}:"
    f"{configs.redis_port}/"
    f"{configs.redis_celery_db}",
)

celery_app.conf.update(CELERY_CONFIG)
