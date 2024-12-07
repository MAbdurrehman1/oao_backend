from enum import Enum

from fastapi import APIRouter

router = APIRouter(prefix="/v1.0")


class Tags(str, Enum):
    """OpenAPI tags"""

    general = "General"
    accounts = "Accounts"
    auth = "Authentication"
    admin = "Admin"
    participation = "Participation"
    management = "Management"
    etl = "ETL"
