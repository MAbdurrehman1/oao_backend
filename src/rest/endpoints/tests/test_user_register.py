from copy import deepcopy

from .helpers import URLs, get_admin_token
from starlette.status import (
    HTTP_200_OK,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_400_BAD_REQUEST,
)


def test_user_register_with_incomplete_payload(fast_client):
    data = {
        "email": "JohnDoe@example.com",
        "password": "pass1234",
        "first_name": "John",
        "last_name": "Doe",
    }
    token = get_admin_token()
    for key in data.keys():
        payload = deepcopy(data)
        del payload[key]
        response = fast_client.post(
            url=URLs.user_register, json=payload, headers=dict(Authorization=token)
        )
        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_user_register_with_valid_payload(fast_client, cleanup_database):
    data = {
        "email": "JohnDoe1@example.com",
        "password": "pass1234",
        "first_name": "John",
        "last_name": "Doe",
    }
    token = get_admin_token()
    response = fast_client.post(
        url=URLs.user_register, json=data, headers=dict(Authorization=token)
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"result": "User registered successfully"}


def test_user_register_with_invalid_email(fast_client, cleanup_database):
    data = {
        "email": "JohnDoe",
        "password": "pass1234",
        "first_name": "John",
        "last_name": "Doe",
    }
    token = get_admin_token()
    response = fast_client.post(
        url=URLs.user_register, json=data, headers=dict(Authorization=token)
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json() == {"error": "(JohnDoe) is/are not valid value for Email."}


def test_user_register_with_duplicated_email(fast_client, cleanup_database):
    data = {
        "email": "JohnDoe1@example.com",
        "password": "pass1234",
        "first_name": "John",
        "last_name": "Doe",
    }
    token = get_admin_token()
    first_response = fast_client.post(
        url=URLs.user_register, json=data, headers=dict(Authorization=token)
    )
    assert first_response.status_code == HTTP_200_OK
    assert first_response.json() == {"result": "User registered successfully"}
    second_response = fast_client.post(
        url=URLs.user_register, json=data, headers=dict(Authorization=token)
    )
    assert second_response.status_code == HTTP_400_BAD_REQUEST
    assert second_response.json() == {
        "error": "Email (johndoe1@example.com) already exists."
    }
