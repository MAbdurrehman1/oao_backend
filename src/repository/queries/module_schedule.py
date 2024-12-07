UPSERT_MODULE_SCHEDULE = """
INSERT INTO module_schedules (
participation_id,
module_id,
selected_date
) VALUES (%s, %s, %s)
ON CONFLICT (participation_id, module_id) DO UPDATE
SET selected_date = excluded.selected_date
RETURNING id, created_at, updated_at;
"""

GET_MODULE_SCHEDULE = """
SELECT
    ms.id,
    ms.ms_graph_event_id,
    ms.selected_date,
    e.id AS employee_id,
    e.role_title,
    e.location,
    u.id AS user_id,
    u.first_name,
    u.last_name,
    u.email,
    m.id AS module_id,
    m.title AS module_title,
    m.description AS module_description,
    m.duration AS module_duration,
    m.module_order
FROM module_schedules ms
LEFT JOIN modules m ON m.id = ms.module_id
LEFT JOIN survey_campaign_employees sce ON sce.participation_id = ms.participation_id
LEFT JOIN employees e ON e.id = sce.employee_id
LEFT JOIN users u ON u.id = e.user_id
WHERE ms.id = %s;
"""


GET_LAST_SCHEDULED_DATE_PASSED_PARTICIPANT_ID = """
SELECT selected_date
FROM module_schedules
WHERE participation_id = %s
AND selected_date < NOW()
ORDER BY selected_date DESC
LIMIT 1;
"""

GET_FIRST_SCHEDULED_DATE_AHEAD_PARTICIPANT_ID = """
SELECT selected_date
FROM module_schedules
WHERE participation_id = %s
AND selected_date > NOW()
ORDER BY selected_date
LIMIT 1;
"""

STORE_MODULE_SCHEDULE_EVENT_ID = """
UPDATE module_schedules
SET ms_graph_event_id = %s
WHERE id = %s;
"""

GET_MODULE_SCHEDULES_BY_PARTICIPATION_ID = """
SELECT
id,
module_id,
selected_date,
participation_id,
created_at,
updated_at
FROM module_schedules
WHERE participation_id = %s;
"""


CHECK_PARTICIPANT_SCHEDULED_ALL = """
SELECT NOT EXISTS (
        SELECT 1
        FROM modules m
        LEFT JOIN module_schedules ms
            ON m.id = ms.module_id
            AND ms.participation_id = %s
    ) AS responded_all;
"""
