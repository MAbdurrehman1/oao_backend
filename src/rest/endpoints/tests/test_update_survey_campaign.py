from datetime import datetime, timedelta
from uuid import UUID

import pytz
from starlette.status import HTTP_200_OK

from repository import CeleryTaskRepository
from repository.tests.helpers import (
    create_some_employee_survey_campaign,
    create_some_employee,
    create_some_organization,
)
from celery_app import celery_app
from settings import configs
from .helpers import get_admin_token, URLs


def test_update_survey_campaign(fast_client, cleanup_database, cleanup_media):
    old_start_date = datetime.now() + timedelta(days=1)
    org = create_some_organization()
    e = create_some_employee(email="test@example.com", organization_id=org.id)
    sc = create_some_employee_survey_campaign(
        title="test title",
        start_date=old_start_date,
        end_date=datetime.now() + timedelta(days=5),
        organization_id=org.id,
        participant_ids=[e.id],
    )
    result = celery_app.send_task(
        "tasks.send_survey_campaign_emails.send_survey_campaign_emails_task",
        args=[sc.id],
        eta=pytz.utc.localize(old_start_date),
    )
    assert isinstance(sc.id, int)
    CeleryTaskRepository.set_task_id(
        post_fix="survey_campaign:send_email_task:",
        identifier=sc.id,
        task_id=UUID(result.id),
    )
    title = "test title 1"
    start_date = datetime.now() + timedelta(days=365)
    end_date = start_date + timedelta(days=375)
    data = dict(
        title=title,
        start_date_str=start_date.strftime(configs.date_time_format),
        end_date_str=end_date.strftime(configs.date_time_format),
    )
    token = get_admin_token()
    response = fast_client.put(
        URLs.survey_campaign + f"{sc.id}/", headers=dict(Authorization=token), json=data
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert data["title"] == title
    assert data["start_date"] == start_date.strftime(configs.date_time_format)
    assert data["end_date"] == end_date.strftime(configs.date_time_format)
