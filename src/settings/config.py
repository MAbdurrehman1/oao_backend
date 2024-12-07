import logging
import os

import sentry_sdk
from celery.schedules import crontab

from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import ROOT_DIR, SOURCE_DIR, StorageType


class Config(BaseSettings):
    """
    config is used for project's general configurations
    the values of the variables will overwrite from .env
    file in the base directory if present and will set the
    the default values if not present.
    note: this functionality is NOT case sensitive
    """

    debug: bool = True
    is_test_environment: bool = True
    app_title: str = "OAO-backend"
    environment: str = "staging"
    # GENERAL
    date_format: str = "%Y-%m-%d"
    date_time_format: str = "%Y-%m-%d %H:%M:%S"
    logging_on: bool = True
    exposed_port: int = 8000
    # postgres config
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "test_db"
    postgres_max_connections: int = 5
    # redis config
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_user: str = "default"
    redis_password: str = "password"
    redis_db: int = 0
    redis_celery_db: int = 1
    # auth config
    auth_header: str = "Authorization"
    auth_secret_key: str = "your-secret-key"
    encoding_algorithm: str = "HS256"
    access_token_expire_seconds: int = 60 * 30
    refresh_token_expire_days: int = 7
    magic_link_exp_mins: int = 20
    # email service config
    email_sender_name: str = "User Sender name"
    email_sender_address: str = "example@email.com"
    support_email_address: str = "example@email.com"
    email_api_key: str = "email-api-key"
    # Sentry monitoring config
    sentry_dsn: str = "https://examplePublicKey@o0.ingest.sentry.io/0"
    celery_sentry_dsn: str = "https://examplePublicKey@o0.ingest.sentry.io/1"
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=os.path.join(ROOT_DIR, ".env"),
        env_file_encoding="utf-8",
    )
    # Storage
    storage_type: StorageType = StorageType.local_storage
    media_root: str = os.path.join(SOURCE_DIR, "media")
    media_url: str = "media/"
    storage_url: str = "www.storage_domain.com/"
    s3_endpoint_url: str = "some endpoint url"
    s3_secret_access_key: str = "some_s3_secret_access_key"
    s3_access_key_id: str = "some_s3_access_key_id"
    s3_bucket_name: str = "test_bucket"

    # ETL
    etl_domain: str = "https://www.example.com/"
    etl_report_creation_end_point: str = "some_uri/"
    etl_get_answer_keys_end_point: str = "some_uri/"

    # Client
    participant_dashboard_url: str = "https://client.example.com/survey/"
    reschedule_session_url: str = "https://client.example.com/reschedule/"
    innovation_idea_submission_url: str = "https://client.example.com/idea/"
    front_end_magic_link_url: str = "https://www.example.com/magic/?token={token}"
    attend_module_event_url: str = "https://clients-app.dev.oao.ai/training-portal"
    reschedule_module_event_url: str = (
        "https://clients-app.dev.oao.ai/training-portal?reschedule={module_id}"
    )

    # Asure Client
    ms_graph_tenant_id: str = "ms_graph_tenant_id"
    ms_graph_client_id: str = "ms_graph_client_id"
    ms_graph_client_secret: str = "ms_graph_client_secret"
    ms_graph_user: str = "scheduling@oao.xyz"
    ms_graph_api_base_url: str = "https://graph.microsoft.com/v1.0"
    ms_graph_scope: str = "https://graph.microsoft.com/.default"

    # Task Config
    task_max_retry: int = 2
    task_retry_delay: int = 1

    # reminders
    first_participant_schedule_reminder_run_hour: int = 7
    first_participant_schedule_reminder_delay_hours: int = 3
    first_participant_schedule_reminder_hand_off_hours: int = 100
    first_participant_schedule_reminder_expire: int = 60 * 60 * 24 * 7

    second_participant_schedule_reminder_run_hour: int = 8
    second_participant_schedule_reminder_before_hours: int = 24 * 7
    second_reminder_campaign_length_hours: int = 24 * 9

    third_participant_schedule_reminder_run_hour: int = 9
    third_participant_schedule_reminder_before_hours: int = 24 * 7
    third_reminder_campaign_length_hours: int = 24 * 9

    first_missing_schedule_reminder_run_hour: int = 15
    first_missing_schedule_reminder_delay_hours: int = 3
    first_missing_schedule_reminder_hand_off_hours: int = 30

    second_missing_schedule_reminder_run_hour: int = 16
    second_missing_schedule_reminder_delay_hours: int = 30
    second_missing_schedule_reminder_hand_off_hours: int = 100

    delayed_innovation_idea_reminder_run_hour: int = 16
    delayed_innovation_idea_reminder_delay_hours: int = 3
    delayed_innovation_idea_reminder_hand_off_hours: int = 100

    scheduled_session_reminder_run_hour: int = 16
    scheduled_session_reminder_before_hours: int = 12
    scheduled_session_reminder_hand_off_hours: int = 36


configs = Config()

LOG_FORMAT: str = "%(levelname)s | %(asctime)s | %(message)s"  # noqa: E501
LOG_LEVEL: str = "DEBUG"

log_config = {
    # Logging config
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        configs.app_title: {"handlers": ["default"], "level": LOG_LEVEL},
        "data": {"handlers": ["default"], "level": LOG_LEVEL},
    },
}


CELERY_CONFIG = {
    "imports": {
        "tasks",
    },
    "include": {
        "tasks",
    },
    "beat_schedule": {
        "first-schedule-reminder": {
            "task": "tasks.send_first_participant_scheduling_reminder."
            "send_first_participant_scheduling_reminder_task",
            "schedule": crontab(
                hour=configs.first_participant_schedule_reminder_run_hour,
                minute=0,
                day_of_week="1-5",
            ),
        },
        "second-schedule-reminder": {
            "task": "tasks.send_second_participant_schedule_reminder."
            "send_second_participant_schedule_reminder_task",
            "schedule": crontab(
                hour=configs.second_participant_schedule_reminder_run_hour,
                minute=0,
                day_of_week="1-5",
            ),
        },
        "third-schedule-reminder": {
            "task": "tasks.send_third_participant_schedule_reminder."
            "send_third_participant_schedule_reminder_task",
            "schedule": crontab(
                hour=configs.third_participant_schedule_reminder_run_hour,
                minute=0,
                day_of_week="1-5",
            ),
        },
        "first-missing-schedule-reminder": {
            "task": "tasks.send_first_missing_schedule_reminder."
            "send_first_missing_schedule_reminder_task",
            "schedule": crontab(
                hour=configs.first_missing_schedule_reminder_run_hour,
                minute=0,
                day_of_week="1-5",
            ),
        },
        "second-missing-schedule-reminder": {
            "task": "tasks.send_second_missing_schedule_reminder."
            "send_second_missing_schedule_reminder_task",
            "schedule": crontab(
                hour=configs.second_missing_schedule_reminder_run_hour,
                minute=0,
                day_of_week="1-5",
            ),
        },
        "delayed-innovation-idea-reminder": {
            "task": "tasks.delayed_innovation_idea_reminder."
            "delayed_innovation_idea_reminder_task",
            "schedule": crontab(
                hour=configs.delayed_innovation_idea_reminder_run_hour,
                minute=0,
                day_of_week="1-5",
            ),
        },
    },
    "timezone": "UTC",
    "broker_connection_retry_on_startup": True,
    "accept_content": ["pickle", "json", "msgpack", "yaml"],
    "task_serializer": "pickle",
}

logger = logging.getLogger(configs.app_title)


def initiate_sentry(
    sentry_dns: str,
    environment: str = "staging",
) -> None:
    try:
        sentry_sdk.init(
            dsn=sentry_dns,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            traces_sample_rate=1.0,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=1.0,
            enable_tracing=True,
            attach_stacktrace=True,
            environment=environment,
        )
    except Exception as e:
        logger.error("Sentry failed to initiate with error: {}".format(e))
