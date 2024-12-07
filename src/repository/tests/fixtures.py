from pathlib import Path

import pytest
import requests
from requests import Response

import settings
from settings import configs
from .helpers import (
    cleanup_database_fn,
    cleanup_redis_fn,
    delete_directory,
)
from ..mail_repository import MailRepository


@pytest.fixture
def cleanup_database():
    cleanup_database_fn()
    yield
    cleanup_database_fn()


@pytest.fixture
def cleanup_redis():
    cleanup_redis_fn()
    yield
    cleanup_redis_fn()


@pytest.fixture
def mock_send_mail(monkeypatch):
    def send_mail_mock_func(
        sender_email: str,
        recipients: list[str],
        subject: str,
        text: str | None = None,
        html_str: str | None = None,
        bcc: list[str] | None = None,
        cc: list[str] = None,
        reply_to: str = None,
    ) -> None:
        return None

    monkeypatch.setattr(MailRepository, "send_mail", send_mail_mock_func)


@pytest.fixture
def cleanup_media():
    delete_directory(directory_path=configs.media_root)
    Path(configs.media_root).mkdir(parents=True, exist_ok=True)
    yield
    delete_directory(directory_path=configs.media_root)
    Path(configs.media_root).mkdir(parents=True, exist_ok=True)


@pytest.fixture
def mock_azure_requests(monkeypatch):
    def fake_post(url: str, headers: dict, json: dict) -> Response:
        response = Response()
        response.status_code = 201
        response._content = b'{"id": "some_id"}'
        return response

    def fake_patch(url: str, headers: dict, json: dict) -> Response:
        response = Response()
        response.status_code = 200
        return response

    monkeypatch.setattr(requests, "post", fake_post)
    monkeypatch.setattr(requests, "patch", fake_patch)


@pytest.fixture
def mock_etl_get_answer_endpoint(monkeypatch):
    def fake_get(url: str, headers: dict) -> Response:
        response = Response()
        response.status_code = 200
        response._content = b'{"result": ["test_answer_1"]}'
        return response

    monkeypatch.setattr(requests, "get", fake_get)
