CREATE_REPORT_GOAL = """
INSERT INTO
report_goals (report_id, manager_id, title, description, focus_area)
VALUES (%s, %s, %s, %s, %s)
RETURNING id, created_at, updated_at;
"""

GET_REPORT_GOALS = """
SELECT
COUNT(id) OVER () AS total_count,
id, title, manager_id, description, focus_area, created_at, updated_at
FROM report_goals
WHERE report_id = %s
"""

GET_REPORT_GOALS_WITH_FOCUS_AREA = """
SELECT
COUNT(id) OVER () AS total_count,
id, title, manager_id, description, focus_area, created_at, updated_at
FROM report_goals
WHERE report_id = %s
AND focus_area = %s
"""

GET_MANGER_GOALS_COUNT = """
SELECT COUNT(id) FROM report_goals
WHERE report_id = %s
"""
