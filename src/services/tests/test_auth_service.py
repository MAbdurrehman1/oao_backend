import re
from datetime import datetime, timedelta
from time import sleep

import pytest

from cexceptions import ExpireException, CredentialValidationException
from settings import configs
from ..auth_service import (
    create_token,
    decode_token,
    create_tokens,
    refreshing_token,
    create_access_token,
    create_refresh_token,
)


def test_create_token_roundtrip():
    test_data = {"test": "example"}
    expire = datetime.utcnow() + timedelta(minutes=5)
    token = create_token(data=test_data, expire=expire)
    token_data = decode_token(token)
    assert set(token_data.keys()) == {"test", "exp"}
    assert token_data["test"] == "example"


def test_token_expire():
    expire = datetime.utcnow() + timedelta(seconds=2)
    test_data = {"test": "example"}
    token = create_token(data=test_data, expire=expire)
    token_data = decode_token(token)
    assert set(token_data.keys()) == {"test", "exp"}
    sleep(2)
    with pytest.raises(ExpireException, match=re.escape("Token is no longer valid.")):
        decode_token(token)


def test_decode_invalid_token():
    with pytest.raises(
        CredentialValidationException, match=re.escape("Token is invalid.")
    ):
        decode_token("invalid_token")


def test_refresh_token_returns_same_token_before_expiration():
    tokens_data = create_tokens(identifier="test")
    refreshed_token_data = refreshing_token(**tokens_data)
    assert refreshed_token_data == tokens_data


def test_access_token_refresh_after_expiration():
    original_value = configs.access_token_expire_seconds
    configs.access_token_expire_seconds = 0
    tokens_data = create_tokens(identifier="test")
    configs.access_token_expire_seconds = original_value
    refreshed_token_data = refreshing_token(**tokens_data)
    assert refreshed_token_data != tokens_data


def test_refreshing_token_with_incorrect_types():
    tokens_data = create_tokens(identifier="test")
    with pytest.raises(
        CredentialValidationException, match=re.escape("Token is invalid.")
    ):
        refreshing_token(
            access_token=tokens_data["refresh_token"],
            refresh_token=tokens_data["access_token"],
        )


def test_refreshing_token_with_different_identifiers():
    access_token = create_access_token(identifier="test1")
    refresh_token = create_refresh_token(identifier="test2")
    with pytest.raises(
        CredentialValidationException, match=re.escape("Token is invalid.")
    ):
        refreshing_token(
            access_token=access_token,
            refresh_token=refresh_token,
        )
