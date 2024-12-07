import pytest
from collections.abc import Generator

import requests

from .helpers import test_client


@pytest.fixture
def fast_client():
    yield test_client


@pytest.fixture
def mock_post_request(monkeypatch):
    def mock_post(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.status_code = 200

        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)


@pytest.fixture
def mock_post_request_failure(monkeypatch):
    def mock_post(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.status_code = 503
                self.reason = "Service unavailable"

        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)
