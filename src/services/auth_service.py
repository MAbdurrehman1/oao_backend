from datetime import datetime, timedelta

import jwt

from cexceptions import ExpireException, CredentialValidationException
from settings import configs, TokenType


def create_access_token(identifier: str) -> str:
    access_token_expire = datetime.utcnow() + timedelta(
        seconds=configs.access_token_expire_seconds
    )
    return create_token(
        data=dict(identifier=identifier, type=TokenType.ACCESS_TOKEN.value),
        expire=access_token_expire,
    )


def create_refresh_token(identifier: str) -> str:
    refresh_token_expire = datetime.utcnow() + timedelta(
        days=configs.refresh_token_expire_days
    )
    return create_token(
        data=dict(identifier=identifier, type=TokenType.REFRESH_TOKEN.value),
        expire=refresh_token_expire,
    )


def create_tokens(identifier: str) -> dict[str, str]:
    access_token = create_access_token(identifier)
    refresh_token = create_refresh_token(identifier)
    return dict(access_token=access_token, refresh_token=refresh_token)


def create_token(data: dict, expire: datetime) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, configs.auth_secret_key, algorithm=configs.encoding_algorithm
    )
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token, configs.auth_secret_key, algorithms=[configs.encoding_algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ExpireException(entity="Token")
    except jwt.PyJWTError:
        raise CredentialValidationException(entity="Token")


def refreshing_token(access_token: str, refresh_token: str) -> dict[str, str]:
    try:
        access_token_data = decode_token(access_token)
        refresh_token_data = decode_token(refresh_token)
        if access_token_data.get("type") != TokenType.ACCESS_TOKEN:
            raise CredentialValidationException(entity="Token")
        if refresh_token_data.get("type") != TokenType.REFRESH_TOKEN:
            raise CredentialValidationException(entity="Token")
        if not access_token_data["identifier"] == refresh_token_data["identifier"]:
            raise CredentialValidationException(entity="Token")
        return dict(access_token=access_token, refresh_token=refresh_token)
    except ExpireException:
        token_data = decode_token(refresh_token)
        access_token = create_access_token(identifier=token_data["identifier"])
        return dict(access_token=access_token, refresh_token=refresh_token)


def check_etl_token(token: str) -> bool:
    token_data = decode_token(token)
    return token_data["identifier"] == "ETL"
