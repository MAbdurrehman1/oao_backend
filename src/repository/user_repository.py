from copy import deepcopy

from psycopg2.errors import UniqueViolation

from entity import User
from cexceptions import UniqueException, NotFoundException
from settings.connections import postgres_connection_manager
from .queries import (
    CREATE_USER,
    GET_USER_BY_EMAIL,
    GET_PASSWORD_BY_EMAIL,
    GET_EMAIL_BY_USER_ID,
    GET_USER_BY_ID,
)


def _enrich_user(data: dict) -> User:
    return User(
        id=data["id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=data["password"],
        is_admin=data["is_admin"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


class UserRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def store(cls, user: User) -> User:
        try:
            result = cls.connection_manager.execute_atomic_query(
                query=CREATE_USER,
                variables=(
                    user.first_name,
                    user.last_name,
                    user.email.lower(),
                    user.password,
                    user.is_admin,
                ),
            )
        except UniqueViolation:
            raise UniqueException(arg="Email", value=user.email)
        retrieved_user = deepcopy(user)
        retrieved_user.id = result["id"]
        retrieved_user.created_at = result["created_at"]
        retrieved_user.updated_at = result["updated_at"]
        return retrieved_user

    @classmethod
    def get_user_by_email(cls, email: str) -> User:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_USER_BY_EMAIL, variables=(email.lower(),)
        )
        if not result:
            raise NotFoundException(entity="User", arg="Email", value=email)
        user = _enrich_user(result)
        return user

    @classmethod
    def get_user_by_id(cls, _id: int) -> User:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_USER_BY_ID, variables=(_id,)
        )
        if not result:
            raise NotFoundException(entity="User", arg="ID", value=str(_id))
        user = _enrich_user(result)
        return user

    @classmethod
    def get_email_by_user_id(cls, _id: int) -> str:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_EMAIL_BY_USER_ID, variables=(_id,)
        )
        if not result:
            raise NotFoundException(entity="User", arg="ID", value=str(_id))
        return result["email"]

    @classmethod
    def get_password_by_email(cls, email: str) -> str:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_PASSWORD_BY_EMAIL, variables=(email.lower(),)
        )
        if not result:
            raise NotFoundException(entity="User", arg="Email", value=email)
        return result["password"]
