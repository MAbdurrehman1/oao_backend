import re
from datetime import datetime

from cexceptions import ValidationException


def assert_email_validation(email: str):
    if not re.match(r"^\S+@\S+\.\S+$", email):
        raise ValidationException(entities="Email", values=email)


def string_to_date(date_str: str, format_str: str) -> datetime:
    try:
        _date = datetime.strptime(date_str, format_str)
        return _date
    except ValueError:
        raise ValidationException(entities="DateTime", values=date_str)
