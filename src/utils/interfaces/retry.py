from abc import ABCMeta, abstractmethod
from time import sleep
from uuid import UUID

import sentry_sdk

from repository import CeleryRetryRepository
from settings import configs


class AbstractRetryTask(metaclass=ABCMeta):
    postfix: str
    batch_id: str | int | UUID | None = None

    @classmethod
    @abstractmethod
    def main(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def single_item_retry(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def translate_key_to_id(cls, key):
        raise NotImplementedError

    @classmethod
    def catch_exceptions(cls, e: Exception):
        sentry_sdk.capture_exception(e)

    @classmethod
    def _remove_retry_count(cls, identifier: str | int | UUID):
        CeleryRetryRepository.remove_failed_attempt(
            postfix=cls.postfix,
            identifier=identifier,
        )

    @classmethod
    def _single_retry(cls, key: str):
        identifier = cls.translate_key_to_id(key)
        try:
            retry_count = cls._get_retry_count(identifier)
            if retry_count >= configs.task_max_retry:
                cls._archive_retry(identifier)
            else:
                cls.single_item_retry(identifier)
                cls._remove_retry_count(identifier)
        except Exception as e:
            cls._increment_retry(
                identifier=identifier,
            )
            cls.catch_exceptions(e)

    @classmethod
    def _set_retry(cls, identifier: str | int | UUID):
        CeleryRetryRepository.set_retry_count(
            postfix=cls.postfix,
            identifier=identifier,
        )

    @classmethod
    def _get_retry_count(cls, identifier: str | int | UUID):
        try:
            retrieved_retry_count = CeleryRetryRepository.get_retry_count(
                postfix=cls.postfix,
                identifier=identifier,
            )
            assert isinstance(retrieved_retry_count, int)
            return retrieved_retry_count
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return configs.task_max_retry

    @classmethod
    def _increment_retry(cls, identifier: str | int | UUID):
        retry_count = cls._get_retry_count(identifier=identifier)
        CeleryRetryRepository.set_retry_count(
            postfix=cls.postfix,
            identifier=identifier,
            retry_count=retry_count + 1,
        )

    @classmethod
    def _get_retries(cls):
        return CeleryRetryRepository.get_batch_keys(
            postfix=cls.postfix,
            batch_id=cls.batch_id if cls.batch_id else "",  # type: ignore
        )

    @classmethod
    def _archive_retry(cls, identifier: str | int | UUID):
        cls._remove_retry_count(identifier=identifier)
        return CeleryRetryRepository.archive_failed_attempt(
            postfix=cls.postfix,
            identifier=identifier,
        )

    @classmethod
    def _retry(cls):
        keys = cls._get_retries()
        if not keys:
            return
        sleep(configs.task_retry_delay)
        for key in keys:
            cls._single_retry(key)
        keys = cls._get_retries()
        if keys:
            cls._retry()

    @classmethod
    def execute(cls, *args, **kwargs):
        try:
            cls.main(*args, **kwargs)
        except Exception as e:
            cls.catch_exceptions(e)
        if cls._get_retries():
            cls._retry()
