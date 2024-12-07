from settings import ParticipationStatus

CHECK_SURVEY_CAMPAIGN_EXIST = """
SELECT EXISTS( SELECT 1
FROM survey_campaigns
WHERE id = %s
);
"""

CREATE_SURVEY_CAMPAIGN = """
INSERT INTO survey_campaigns (
title,
start_date,
end_date,
organization_id
) VALUES (%s, %s, %s, %s)
RETURNING id, created_at, updated_at;
"""

CREATE_SURVEY_CAMPAIGN_EMPLOYEE = """
INSERT INTO survey_campaign_employees (
survey_campaign_id,
employee_id
) VALUES %s;
"""

GET_SURVEY_CAMPAIGN_PARTICIPANTS_DATA = """
SELECT u.id, u.email, u.first_name, u.last_name, sce.participation_id
FROM users u
LEFT JOIN employees e on u.id = e.user_id
LEFT JOIN survey_campaign_employees sce on sce.employee_id = e.id
WHERE sce.survey_campaign_id = %s;
"""


GET_PARTICIPANT_DATA = """
SELECT u.id, u.first_name, u.last_name, u.email
FROM survey_campaign_employees sce
LEFT JOIN employees e on sce.employee_id = e.id
LEFT JOIN users u on u.id = e.user_id
WHERE sce.participation_id = %s;
"""

UPDATE_PARTICIPATION_STATUS = """
UPDATE survey_campaign_employees
SET status = %s
WHERE participation_id = %s;
"""


GET_PARTICIPATION_STATUS = """
SELECT status
from survey_campaign_employees
WHERE participation_id = %s;
"""


GET_SURVEY_CAMPAIGN = f"""
SELECT
sc.id,
sc.title,
sc.start_date,
sc.end_date,
sc.organization_id,
COUNT(sce.participation_id) AS participants_count,
COUNT(sce.participation_id)
    FILTER
    (
        WHERE sce.status IN (
            '{ParticipationStatus.INVITED.value}',
            '{ParticipationStatus.RESPONDED.value}',
            '{ParticipationStatus.IDEA_SUBMITTED.value}',
            '{ParticipationStatus.SCHEDULED.value}'
        )
    ) AS invited_count,
COUNT(sce.participation_id)
    FILTER
    (
        WHERE sce.status IN (
            '{ParticipationStatus.RESPONDED.value}',
            '{ParticipationStatus.IDEA_SUBMITTED.value}'
            )
    ) AS responded_count,
sc.created_at,
sc.updated_at
FROM survey_campaigns sc
LEFT JOIN survey_campaign_employees sce on sce.survey_campaign_id = sc.id
WHERE id = %s
GROUP BY sc.id;
"""

GET_ORGANIZATION_SURVEY_CAMPAIGNS = f"""
SELECT
COUNT(sc.id) OVER () AS total_count,
sc.id,
sc.title,
sc.start_date,
sc.end_date,
sc.organization_id,
COUNT(sce.participation_id) AS participants_count,
COUNT(sce.participation_id)
    FILTER
    (
        WHERE sce.status IN (
            '{ParticipationStatus.INVITED.value}',
            '{ParticipationStatus.RESPONDED.value}',
            '{ParticipationStatus.IDEA_SUBMITTED.value}',
            '{ParticipationStatus.SCHEDULED.value}'
        )
    ) AS invited_count,
COUNT(sce.participation_id)
    FILTER
    (
        WHERE sce.status IN (
            '{ParticipationStatus.RESPONDED.value}',
            '{ParticipationStatus.IDEA_SUBMITTED.value}'
            )
    ) AS responded_count,
sc.created_at,
sc.updated_at
FROM survey_campaigns sc
LEFT JOIN organizations org ON org.id = sc.organization_id
LEFT JOIN survey_campaign_employees sce ON sce.survey_campaign_id = sc.id
WHERE org.id = %s
GROUP BY sc.id
OFFSET %s
LIMIT %s;
"""

UPDATE_SURVEY_CAMPAIGN = """
UPDATE survey_campaigns
SET
    title = %s,
    start_date = %s,
    end_date = %s,
    updated_at = %s
WHERE id = %s
RETURNING updated_at;
"""

GET_ORGANIZATION_ID_BY_SURVEY_CAMPAIGN_ID = """
SELECT
    organization_id
FROM survey_campaigns
WHERE id = %s
"""

GET_SURVEY_CAMPAIGN_START_DATE = """
SELECT start_date from survey_campaigns
WHERE id = %s;
"""


GET_SURVEY_CAMPAIGN_IDS_BETWEEN = """
SELECT id FROM survey_campaigns
WHERE start_date > %s AND end_date <= %s
AND organization_id = %s;
"""


GET_SURVEY_CAMPAIGN_END_DATE = """
SELECT end_date from survey_campaigns
WHERE id = %s;
"""

GET_SURVEY_CAMPAIGN_END_DATE_BY_PARTICIPATION_ID = """
SELECT sc.end_date
from survey_campaigns sc
INNER JOIN survey_campaign_employees sce ON sce.survey_campaign_id = sc.id
WHERE sce.participation_id = %s;
"""
