import re

import pytest

from cexceptions import (
    ValidationException,
    NotFoundException,
    CredentialValidationException,
    ExpireException,
)
from entity import User
from settings import configs
from repository.tests.helpers import create_some_user
from ..auth_service import create_access_token, create_refresh_token
from ..user_service import (
    hash_password,
    verify_password,
    create_user,
    login_user,
    authenticate_user,
)
from repository import UserRepository


def test_password_hashing():
    password = "<PASSWORD>"
    hashed_password = hash_password(password)
    assert verify_password(password, hashed_password)
    assert not verify_password("WRONG_<PASSWORD>", hashed_password)


def test_create_user(cleanup_database):
    email = "JohnDoe@example.de"
    password = "<SOME PASSWORD>"
    create_user(first_name="john", last_name="doe", email=email, password=password)
    user = UserRepository.get_user_by_email(email=email)
    assert user.first_name == "john", "first name is incorrect"
    assert user.last_name == "doe", "last name is incorrect"
    assert user.email == email.lower(), "email is incorrect"
    assert isinstance(user.password, str)
    assert verify_password(password, user.password), "password is incorrect"


def test_create_user_with_invalid_email():
    with pytest.raises(
        ValidationException,
        match=re.escape("(JohnDoe) is/are not valid value for Email."),
    ):
        create_user(
            first_name="john",
            last_name="doe",
            email="JohnDoe",
            password="<SOME PASSWORD>",
        )


def test_login_user_with_invalid_email():
    with pytest.raises(
        ValidationException,
        match=re.escape("(johndoe) is/are not valid value for Email."),
    ):
        login_user(email="JohnDoe", password="<PASSWORD>")


def test_login_user_with_not_existing_email():
    with pytest.raises(
        NotFoundException,
        match=re.escape("User with Email (johndoe@example.com) not found."),
    ):
        login_user(email="JohnDoe@example.com", password="<PASSWORD>")


def test_login_user_with_invalid_password(cleanup_database):
    email = "person@example.com"
    create_some_user(email=email, password="PASSWORD")
    with pytest.raises(
        CredentialValidationException, match=re.escape("Email or Password is invalid.")
    ):
        login_user(email, "invalid password")


def test_login_user_is_not_case_sensitive(cleanup_database):
    create_some_user(email="PeRsOn@eXaMpLe.CoM", password=hash_password("PASSWORD"))
    login_user("person@example.com", "PASSWORD")


def test_authenticate_user_with_invalid_token():
    with pytest.raises(
        CredentialValidationException, match=re.escape("Token is invalid.")
    ):
        authenticate_user("invalid_token")


def test_authenticate_user_with_expired_token(cleanup_database):
    email = "person@example.com"
    create_some_user(email=email)
    original_value = configs.access_token_expire_seconds
    configs.access_token_expire_seconds = 0
    token = create_access_token(identifier=email)
    configs.access_token_expire_seconds = original_value
    with pytest.raises(ExpireException, match=re.escape("Token is no longer valid.")):
        authenticate_user(token)


def test_authenticate_user_returns_user_object(cleanup_database):
    email = "person@example.com"
    create_some_user(email=email)
    token = create_access_token(identifier=email)
    user = authenticate_user(token)
    assert isinstance(user, User)
    assert user.email == email


def test_user_authentication_reject_token_with_incorrect_type(cleanup_database):
    email = "person@example.com"
    create_some_user(email=email)
    token = create_refresh_token(identifier=email)
    with pytest.raises(
        CredentialValidationException, match=re.escape("Token is invalid.")
    ):
        authenticate_user(token)
