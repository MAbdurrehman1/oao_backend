from uuid import UUID

import requests
from starlette.status import HTTP_200_OK

from celery_app import celery_app
from services import create_access_token
from settings import configs
from cexceptions import ExternalSourceException, MissingEntityException
from repository import DeepDiveRepository
from utils.interfaces import AbstractRetryTask


def _get_etl_url(participant_id: UUID):
    etl_url = configs.etl_domain + configs.etl_get_answer_keys_end_point
    etl_url = f"{etl_url}?participation_id={participant_id}"
    return etl_url


def _assert_response_status(response):
    if not response.status_code == HTTP_200_OK:
        raise ExternalSourceException(source="ETL", source_error=response.json())


def retrieve_deep_dive_list(participant_id: UUID):
    etl_url = _get_etl_url(participant_id)
    token = create_access_token(identifier="Backend")
    response = requests.get(
        url=etl_url,
        headers=dict(Authorization=token),
    )
    _assert_response_status(response)
    answer_slug_list = response.json()["result"]
    DeepDiveRepository.store_deep_dive_strategy(
        participation_id=participant_id,
        slug_list=answer_slug_list,
    )


class CreateDeepDiveListTask(AbstractRetryTask):
    postfix = "deep_dive_strategy:"

    @classmethod
    def translate_key_to_id(cls, key) -> UUID:
        _id = UUID(key.split(":")[-1])
        return _id

    @staticmethod
    def _get_participant_id(*args, **kwargs) -> UUID:
        if "participant_id" in kwargs.keys():
            return kwargs["participant_id"]
        elif args:
            return args[0]
        else:
            raise MissingEntityException(
                entity="participant_id",
            )

    @classmethod
    def main(cls, *args, **kwargs):
        participant_id = cls._get_participant_id(*args, **kwargs)
        try:
            retrieve_deep_dive_list(participant_id=participant_id)
        except Exception as e:
            cls._set_retry(identifier=participant_id)
            cls.catch_exceptions(e)

    @classmethod
    def single_item_retry(cls, *args, **kwargs):
        participant_id = cls._get_participant_id(*args, **kwargs)
        retrieve_deep_dive_list(participant_id=participant_id)


@celery_app.task
def create_deep_dive_list_task(participant_id: UUID):
    CreateDeepDiveListTask.execute(participant_id)
