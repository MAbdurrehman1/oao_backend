from datetime import datetime

from pydantic import BaseModel

from .user import User


class CalendarEvent(BaseModel):
    start_date: datetime
    end_date: datetime
    description: str
    title: str
    event_url: str
    reschedule_url: str
    attendees: list[User]
    id: str | None = None
