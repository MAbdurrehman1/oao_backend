import base64
import os
import secrets
from uuid import UUID, uuid5, NAMESPACE_DNS

import bcrypt
from jinja2 import Template

from entity import User
from repository import UserRepository, MailRepository, MagicLinkRepository
from cexceptions import CredentialValidationException
from settings import TokenType, SOURCE_DIR, configs
from utils.validation_helpers import assert_email_validation
from .auth_service import create_tokens, decode_token


def hash_password(password) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def create_user(
    first_name: str,
    last_name: str,
    email: str,
    password: str,
):
    hashed_password = hash_password(password)
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password,
    )
    UserRepository.store(user=user)


def login_user(email: str, password: str) -> dict[str, str]:
    email = email.lower()
    assert_email_validation(email)
    hashed_password = UserRepository.get_password_by_email(email=email)
    if not verify_password(password, hashed_password):
        raise CredentialValidationException(entity="Email or Password")
    auth_tokens = create_tokens(identifier=email)
    return auth_tokens


def authenticate_user(token: str) -> User:
    token_data = decode_token(token)
    email = token_data["identifier"]
    if token_data.get("type") != TokenType.ACCESS_TOKEN:
        raise CredentialValidationException(entity="Token")
    user = UserRepository.get_user_by_email(email=email)
    return user


def get_user_by_id(user_id: int) -> User:
    user = UserRepository.get_user_by_id(_id=user_id)
    return user


def _get_email_template() -> Template:
    template_path = os.path.join(
        SOURCE_DIR, "templates", "magic_link_email_template.html"
    )
    with open(template_path, "r") as file:
        template_str = file.read()
        template = Template(template_str)
        return template


def generate_magic_token(user_id: int) -> UUID:
    salt = base64.urlsafe_b64encode(secrets.token_bytes(30)).decode("utf-8")
    token = uuid5(namespace=NAMESPACE_DNS, name=salt)
    MagicLinkRepository.set_magic_link(user_id=user_id, token=token)
    return token


def send_magic_link(email: str) -> None:
    user = UserRepository.get_user_by_email(email=email)
    assert isinstance(user.id, int)
    email_template = _get_email_template()
    token = generate_magic_token(user_id=user.id)
    magic_link = configs.front_end_magic_link_url.format(token=token)
    rendered_html = email_template.render(
        first_name=user.first_name,
        magic_link=magic_link,
    )
    MailRepository.send_mail(
        sender_email=configs.support_email_address,
        recipients=[email],
        subject="Login Email",
        html_str=rendered_html,
    )


def login_user_with_magic_link(token: UUID) -> dict[str, str]:
    user_id = MagicLinkRepository.get_user_id(token=token)
    MagicLinkRepository.remove_magic_link(token=token)
    email = UserRepository.get_email_by_user_id(_id=user_id)
    auth_tokens = create_tokens(identifier=email)
    return auth_tokens
