GET_LAST_REPORT_END_DATE = """
SELECT end_date
FROM reports
WHERE management_position_id = %s
ORDER BY updated_at DESC;
"""

STORE_REPORT = """
INSERT INTO reports (title, management_position_id, end_date, status) VALUES
(%s, %s, %s, %s)
RETURNING id, created_at, updated_at;
"""

CHECK_REPORT_EXISTS = """
SELECT EXISTS(SELECT 1 FROM
reports WHERE id = %s
);
"""

CREATE_REPORT_PARTICIPANTS = """
INSERT INTO report_participants (report_id, participation_id) VALUES %s
"""

CHECK_REPORT_BELONG_TO_USER = """
SELECT EXISTS(
SELECT 1 FROM management_position_managers mpm
INNER JOIN employees e ON e.id = mpm.employee_id
INNER JOIN reports r ON r.management_position_id = mpm.management_position_id
WHERE r.id = %s
AND e.user_id = %s
);
"""


GET_RESPONDED_PARTICIPANTS_COUNT = """
SELECT COUNT(participation_id)
FROM report_participants
WHERE report_id = %s;
"""

GET_ORGANIZATION_REPORTS_LIST = """
SELECT
    COUNT(r.id) OVER () AS total_count,
    r.id,
    r.title,
    r.end_date,
    r.status,
    r.updated_at,
    r.created_at,
    r.management_position_id,
    mp.name AS management_position_name
FROM reports r
LEFT JOIN management_positions mp ON mp.id = r.management_position_id
WHERE mp.organization_id = %s
ORDER BY r.updated_at DESC
OFFSET %s
LIMIT %s;
"""

DELETE_REPORT = """
DELETE FROM reports WHERE id = %s;
"""

GET_MANAGER_REPORTS_LIST = """
SELECT
    COUNT(r.id) OVER () AS total_count,
    r.id,
    r.title,
    r.management_position_id,
    r.status,
    mp.name AS management_position_name
FROM reports r
INNER JOIN management_positions mp ON mp.id = r.management_position_id
INNER JOIN management_position_managers mpm ON
r.management_position_id = mpm.management_position_id
INNER JOIN employees e ON e.id = mpm.employee_id
WHERE e.id = %s
AND r.status = %s
ORDER BY r.updated_at DESC
OFFSET %s
LIMIT %s;
"""

UPDATE_REPORT_STATUS = """
UPDATE reports
SET
status = %s,
updated_at = %s
WHERE id = %s;
"""

CHECK_REPORT_PUBLISHED = """
SELECT EXISTS(SELECT 1 FROM
reports WHERE id = %s
AND status = %s
);
"""

GET_ORGANIZATION_ID_BY_REPORT_ID = """
SELECT o.id
FROM organizations o
INNER JOIN management_positions mp ON mp.organization_id = o.id
INNER JOIN reports r on r.management_position_id = mp.id
WHERE r.id = %s
"""
