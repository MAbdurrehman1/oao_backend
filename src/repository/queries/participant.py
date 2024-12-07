GET_SURVEY_CAMPAIGN_PARTICIPANTS = """
SELECT
    COUNT(sce.participation_id) OVER () AS total_count,
    sce.participation_id,
    sce.status,
    sce.employee_id,
    sce.survey_campaign_id,
    e.location,
    e.role_title,
    u.id as user_id,
    u.first_name,
    u.last_name,
    u.email,
    bu.id as business_unit_id,
    bu.name as business_unit_name
FROM survey_campaign_employees sce
LEFT JOIN employees e on e.id = sce.employee_id
LEFT JOIN users u ON u.id = e.user_id
LEFT JOIN business_units bu ON bu.id = e.business_unit_id
WHERE sce.survey_campaign_id = %s
"""

UPSERT_PARTICIPANT_TO_SURVEY_CAMPAIGN = """
INSERT INTO survey_campaign_employees (
    survey_campaign_id, employee_id, status
) VALUES (
    %s, %s, %s
)
ON CONFLICT (survey_campaign_id, employee_id) DO UPDATE
SET
    status = excluded.status
RETURNING participation_id;
"""

UPSERT_PARTICIPANT_TO_SURVEY_CAMPAIGN = """
INSERT INTO survey_campaign_employees (
    survey_campaign_id, employee_id, status
) VALUES (
    %s, %s, %s
)
ON CONFLICT (survey_campaign_id, employee_id) DO UPDATE
SET
    status = excluded.status
RETURNING participation_id;
"""

CHECK_PARTICIPANT_BELONGS_TO_SURVEY_CAMPAIGN = """
SELECT EXISTS(
SELECT 1 FROM survey_campaign_employees
WHERE survey_campaign_id = %s
AND participation_id = %s);
"""

CHECK_PARTICIPATION_BELONGS_TO_USER = """
SELECT EXISTS(
SELECT 1 FROM survey_campaign_employees sce
INNER JOIN employees e ON e.id = sce.employee_id
WHERE e.user_id = %s
AND sce.participation_id = %s
);
"""


GET_SURVEY_CAMPAIGNS_PARTICIPANT_IDS = """
SELECT sce.participation_id
FROM survey_campaign_employees sce
LEFT JOIN employees e on sce.employee_id = e.id
WHERE sce.survey_campaign_id IN %s
AND e.business_unit_id IN %s
AND sce.status IN %s
"""

FILTER_USERS_WITH_SURVEY_CAMPAIGN = """
SELECT u.email
FROM users u
INNER JOIN employees e on u.id = e.user_id
INNER JOIN survey_campaign_employees sce ON sce.employee_id = e.id
INNER JOIN survey_campaigns sc ON sce.survey_campaign_id = sc.id
WHERE u.email IN %s
AND sc.end_date > NOW();
"""

GET_SURVEY_CAMPAIGN_END_DATE_BY_EMPLOYEE_ID = """
SELECT end_date FROM survey_campaigns sc
INNER JOIN survey_campaign_employees sce ON sce.survey_campaign_id = sc.id
WHERE sce.employee_id = %s
AND end_date > NOW();
"""


CHECK_PARTICIPATION_ID_EXISTS = """
SELECT EXISTS(
SELECT participation_id
FROM survey_campaign_employees
WHERE participation_id = %s);
"""

GET_PARTICIPATION_ID_BY_USER_ID = """
SELECT participation_id
FROM survey_campaign_employees sce
INNER JOIN survey_campaigns sc ON sce.survey_campaign_id = sc.id
INNER JOIN employees e on sce.employee_id = e.id
WHERE e.user_id = %s
ORDER BY sc.end_date DESC
LIMIT 1;
"""

GET_CAMPAIGN_ID_BY_PARTICIPATION_ID = """
SELECT survey_campaign_id
FROM survey_campaign_employees
WHERE participation_id = %s
"""


GET_INVITED_PARTICIPATION_IDS_AFTER_DATE = """
SELECT participation_id
FROM survey_campaign_employees sce
INNER JOIN survey_campaigns sc ON sce.survey_campaign_id = sc.id
WHERE sc.start_date <= NOW() - INTERVAL '%s hours'
AND sc.start_date >= NOW() - INTERVAL '%s hours'
AND sc.end_date >= NOW()
AND sce.status = %s
"""


GET_PARTICIPATION_IDS_BEFORE_DATE = """
SELECT participation_id
FROM survey_campaign_employees sce
INNER JOIN survey_campaigns sc ON sce.survey_campaign_id = sc.id
WHERE sc.start_date <= NOW()
AND sc.end_date <= NOW() + INTERVAL '%s hours'
AND sce.status = %s
AND sc.end_date > NOW()
AND EXTRACT(EPOCH FROM (sc.end_date - sc.start_date)) > %s
"""


GET_USER_BY_PARTICIPATION_ID = """
SELECT
u.id,
u.first_name,
u.last_name,
u.email
FROM users u
INNER JOIN employees e ON e.user_id = u.id
INNER JOIN survey_campaign_employees sce ON sce.employee_id = e.id
WHERE sce.participation_id = %s;
"""

GET_IDEA_DELAYED_PARTICIPANTS = """
SELECT sce.participation_id
FROM survey_campaign_employees sce
INNER JOIN survey_campaigns sc ON sce.survey_campaign_id = sc.id
LEFT JOIN (
    SELECT
        pm.participation_id,
        MAX(pm.updated_at) AS last_answered_date
    FROM
        participation_modules pm
    GROUP BY
        pm.participation_id
) pm ON sce.participation_id = pm.participation_id
WHERE pm.last_answered_date <= NOW() - INTERVAL '%s hours'
AND pm.last_answered_date >= NOW() - INTERVAL '%s hours'
AND sce.status = %s
AND sc.end_date > NOW()
"""


GET_SCHEDULED_PARTICIPANTS = """
SELECT sce.participation_id
FROM survey_campaign_employees sce
INNER JOIN module_schedules ms ON sce.participation_id = ms.participation_id
WHERE ms.selected_date <= NOW() + INTERVAL '%s hours'
AND ms.selected_date >= NOW() + INTERVAL '%s hours'
AND sce.status = %s
"""
