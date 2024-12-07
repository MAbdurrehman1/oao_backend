import re
from datetime import datetime

import pytest

from cexceptions import UniqueException, NotFoundException
from entity import User
from repository import UserRepository


def _assert_user_is_correctly_retrieved(user: User, retrieved_user: User):
    assert (
        retrieved_user.first_name == user.first_name
    ), "first_name should be the same in user and retrieved_user"
    assert (
        retrieved_user.last_name == user.last_name
    ), "last_name should be the same in user and"
    assert (
        retrieved_user.email == user.email
    ), "email should be the same in user and retrieved_user"
    assert (
        retrieved_user.password == user.password
    ), "password should be the same in user and retrieved_user"
    assert (
        retrieved_user.is_admin == user.is_admin
    ), "is_admin should be the same in user and retrieved_user"
    assert isinstance(retrieved_user.id, int), "user id should be UUID"
    assert isinstance(
        retrieved_user.created_at, datetime
    ), "created at should be datetime"
    assert isinstance(
        retrieved_user.updated_at, datetime
    ), "update at should be datetime"


@pytest.mark.parametrize("is_admin", [True, False])
def test_store_user(cleanup_database, is_admin: bool):
    user_repository = UserRepository
    user = User(
        first_name="John",
        last_name="Doe",
        email="JohnDoe@example.de",
        password="<PASSWORD>",
        is_admin=is_admin,
    )
    user_repository.store(user=user)
    retrieved_user = user_repository.get_user_by_email(email=user.email)
    _assert_user_is_correctly_retrieved(user, retrieved_user)


def test_store_user_with_duplicated_email(cleanup_database):
    user_repository = UserRepository
    user = User(
        first_name="John",
        last_name="Doe",
        email="JohnDoe@example.de",
        password="<PASSWORD>",
    )
    user_repository.store(user=user)
    with pytest.raises(
        UniqueException, match=re.escape(f"Email ({user.email}) already exists")
    ):
        user_repository.store(user=user)


def test_retrieve_user_by_invalid_email(cleanup_database):
    with pytest.raises(
        NotFoundException,
        match=re.escape("User with Email (InvalidEmail@example.com) not found."),
    ):
        UserRepository.get_user_by_email(email="InvalidEmail@example.com")


def test_retrieve_password_by_invalid_email(cleanup_database):
    with pytest.raises(
        NotFoundException,
        match=re.escape("User with Email (InvalidEmail@example.com) not found."),
    ):
        UserRepository.get_password_by_email(email="InvalidEmail@example.com")


def test_retrieve_password_by_email(cleanup_database):
    email = "JohnDoe@example.de"
    password = "<PASSWORD>"
    user_repository = UserRepository
    user = User(
        first_name="John",
        last_name="Doe",
        email=email,
        password=password,
    )
    user_repository.store(user=user)
    retrieved_password = user_repository.get_password_by_email(email=email)
    assert retrieved_password == password
