from copy import deepcopy

import requests
from requests import Response

from cexceptions import ExternalSourceException
from entity import CalendarEvent, User
from settings import configs
from settings.connections import azure_client


def _get_attendees_data(attendees: list[User]) -> list[dict]:
    attendees_data = []
    for attendee in attendees:
        full_name = f"{attendee.first_name } {attendee.last_name}"
        attendee_data = {
            "emailAddress": {
                "address": attendee.email,
                "name": full_name,
            },
            "type": "required",
        }
        attendees_data.append(attendee_data)
    return attendees_data


class CalendarRepository:
    client = azure_client
    base_url = (
        configs.ms_graph_api_base_url + "/users/" + configs.ms_graph_user + "/events"
    )

    @classmethod
    def _send_request(
        cls, method: str, data: dict, url_postfix: str | None = None
    ) -> Response:
        try:
            token = cls.client.get_token(configs.ms_graph_scope)
        except Exception as e:
            raise ExternalSourceException(
                source="Calendar Service", source_error=str(e)
            )
        headers = {
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json",
        }
        url = cls.base_url + url_postfix if url_postfix else cls.base_url
        if method == "POST":
            try:
                response = requests.post(
                    url=url,
                    headers=headers,
                    json=data,
                )
                response.raise_for_status()
            except Exception as e:
                raise ExternalSourceException(
                    source="Calendar Service", source_error=str(e)
                )
            return response
        elif method == "PATCH":
            try:
                response = requests.patch(
                    url=url,
                    headers=headers,
                    json=data,
                )
                response.raise_for_status()
            except Exception as e:
                raise ExternalSourceException(
                    source="Calendar Service", source_error=str(e)
                )
            return response
        else:
            raise NotImplementedError

    @classmethod
    def create_event(
        cls,
        calendar_event: CalendarEvent,
    ) -> CalendarEvent:
        start_datetime = calendar_event.start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        end_datetime = calendar_event.end_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        subject = calendar_event.title
        event_url = calendar_event.event_url
        reschedule_url = calendar_event.reschedule_url
        event = {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                # commented out cause we will need this later.
                # calendar_event.description
                "content": f"<br/>Click to attend now: {event_url}"
                + f"<br/>Click to reschedule this session: {reschedule_url}",
            },
            "start": {
                "dateTime": start_datetime,
                "timeZone": "",
            },
            "end": {
                "dateTime": end_datetime,
                "timeZone": "",
            },
            "location": {
                "displayName": event_url,
            },
            "attendees": _get_attendees_data(attendees=calendar_event.attendees),
        }
        response = cls._send_request(method="POST", data=event)
        submitted_event = deepcopy(calendar_event)
        submitted_event.id = response.json()["id"]
        return submitted_event

    @classmethod
    def update_event(
        cls,
        calendar_event: CalendarEvent,
    ) -> CalendarEvent:
        subject = calendar_event.title
        start_datetime = calendar_event.start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        end_datetime = calendar_event.end_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        update_event_payload = {
            "subject": subject,
            "start": {
                "dateTime": start_datetime,
                "timeZone": "",
            },
            "end": {
                "dateTime": end_datetime,
                "timeZone": "",
            },
        }
        cls._send_request(
            method="PATCH",
            data=update_event_payload,
            url_postfix=f"/{calendar_event.id}",
        )
        return calendar_event
