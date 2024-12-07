GET_MODULES_LIST = """
SELECT
COUNT(m.id) OVER () AS total_count,
m.id,
at.id AS animated_thumbnail_id,
at.file_path AS animated_thumbnail_url,
st.id AS still_thumbnail_id,
st.file_path AS still_thumbnail_url,
title,
description,
duration,
module_order,
m.created_at,
m.updated_at
FROM modules m
INNER JOIN files at ON at.id = m.animated_thumbnail_id
INNER JOIN files st ON st.id = m.still_thumbnail_id
ORDER BY module_order
OFFSET %s
LIMIT %s
"""

STORE_MODULE = """
INSERT INTO modules (
title,
description,
duration,
module_order,
url,
animated_thumbnail_id,
still_thumbnail_id)
VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id, created_at, updated_at;
"""

STORE_MODULE_ANSWER = """
INSERT INTO participation_modules
(participation_id, module_id) VALUES (%s, %s)
ON CONFLICT (participation_id, module_id)
DO NOTHING;
"""

GET_LAST_ANSWERED_MODULE_ORDER = """
SELECT
module_order
FROM modules m
INNER JOIN participation_modules pm ON pm.module_id = m.id
WHERE pm.participation_id = %s
ORDER BY module_order DESC
LIMIT 1;
"""

GET_MODULE_DATA_UNTIL_ORDER = """
SELECT id, url, module_order
FROM modules
WHERE module_order <= %s;
"""

CHECK_MODULE_ID_EXISTS = """
SELECT EXISTS(
SELECT id
FROM modules
WHERE id = %s);
"""


CHECK_IS_LAST_MODULE = """
SELECT
CASE
WHEN "module_order" = (
        SELECT MAX("module_order")
        FROM modules
        )
        THEN TRUE
        ELSE FALSE
END AS is_last_module
FROM
modules
WHERE
id = %s;
"""


UPDATE_LAST_MODULE_ORDER = """
UPDATE survey_campaign_employees
SET last_answered_module_order = %s
WHERE participation_id = %s
"""


GET_PARTICIPANT_LAST_MODULE_ORDER = """
SELECT last_answered_module_order
FROM survey_campaign_employees
WHERE participation_id = %s
"""

GET_SCHEDULE_MISSING_PARTICIPANTS = """
SELECT sce.participation_id
FROM survey_campaign_employees sce
INNER JOIN (
    SELECT participation_id, COUNT(*) AS past_surveys_count
    FROM module_schedules
    WHERE selected_date <= NOW() - INTERVAL '%s HOUR'
    AND selected_date >= NOW() - INTERVAL '%s HOUR'
    GROUP BY participation_id
) ms ON ms.participation_id = sce.participation_id
INNER JOIN survey_campaigns sc ON sc.id = sce.survey_campaign_id
WHERE ms.past_surveys_count > sce.last_answered_module_order
AND sc.end_date > NOW()
AND sce.status = %s
"""

UPDATE_MODULE_ANSWER_UPDATED_AT = """
UPDATE participation_modules
SET updated_at = %s
WHERE module_id = %s
AND participation_id = %s
"""
