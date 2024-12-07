import os
from enum import Enum

# path to source directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SOURCE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CORS config
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://panel.dev.oao.ai",
    "https://clients-app.dev.oao.ai",
]

ALLOWED_ORIGIN_REGEX = r"https:\/\/.*\.oao\.co"
ALLOWED_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
ALLOWED_HEADERS = ["*"]
EXPOSED_HEADERS = ["Content-Disposition"]


class TokenType(str, Enum):
    ACCESS_TOKEN: str = "access_token"
    REFRESH_TOKEN: str = "refresh_token"


class ParticipationStatus(str, Enum):
    DUE: str = "due"
    INVITED: str = "invited"
    SCHEDULED: str = "scheduled"
    CANCELED: str = "canceled"
    FAILED: str = "failed"
    RESPONDED: str = "responded"
    IDEA_SUBMITTED: str = "idea_submitted"


class FocusArea(str, Enum):
    readiness: str = "READINESS"
    execution: str = "EXECUTION"
    guidance: str = "GUIDANCE"


class StorageType(str, Enum):
    local_storage: str = "LOCAL_STORAGE"
    s3: str = "S3"


class PreferredLang(str, Enum):
    french: str = "fr"
    english: str = "en"


class ReportStatus(str, Enum):
    CREATED: str = "created"
    READY: str = "ready"
    PUBLISHED: str = "published"
