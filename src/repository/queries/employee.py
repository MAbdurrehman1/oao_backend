CREATE_EMPLOYEE = """
INSERT INTO employees (user_id, role_title, organization_id, location, business_unit_id)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id)
DO UPDATE SET
role_title = EXCLUDED.role_title,
organization_id = EXCLUDED.organization_id,
location = EXCLUDED.location,
business_unit_id = EXCLUDED.business_unit_id
RETURNING id, created_at, updated_at;
"""

CHECK_EMPLOYEE_EMAILS_EXIST = """
SELECT
    e.id, u.email
FROM employees e
LEFT JOIN users u on u.id = e.user_id
WHERE u.email in %s
AND e.organization_id = %s
"""


CHECK_EMPLOYEE_IS_IN_CAMPAIGN_ORGANIZATION = """
SELECT EXISTS(
SELECT 1
FROM employees
WHERE id = %s
AND organization_id = %s
);
"""

GET_EMPLOYEE_ID_BY_EMAIL = """
SELECT e.id
FROM employees e
LEFT JOIN users u on u.id = e.user_id
WHERE u.email = %s
"""

CHECK_USER_IS_EMPLOYEE_BY_ID = """
SELECT EXISTS(
SELECT 1 FROM employees WHERE user_id = %s
);
"""


GET_EMPLOYEE_BY_USER_ID = """
SELECT
id, role_title, location, organization_id
FROM employees
WHERE user_id = %s
"""

GET_EMPLOYEE_ID_BY_USER_ID = """
SELECT id
FROM employees
WHERE user_id = %s
"""


SUBMIT_PREFERRED_LANG = """
UPDATE employees
SET
preferred_lang = %s,
updated_at = %s
WHERE id = %s
"""

GET_PREFERRED_LANG = """
SELECT preferred_lang
FROM employees
WHERE id = %s
"""
