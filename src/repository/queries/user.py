CREATE_USER = """
INSERT INTO users (
    first_name, last_name, email, password, is_admin
) values (
    %s, %s, %s, %s, %s
) RETURNING id, created_at, updated_at;
"""

UPSERT_USER = """
INSERT INTO users (
    first_name, last_name, email, password, is_admin
) VALUES (
    %s, %s, %s, %s, %s
)
ON CONFLICT (email) DO UPDATE
SET
    first_name = excluded.first_name,
    last_name = excluded.last_name
RETURNING id, created_at, updated_at;
"""


GET_USER_BY_EMAIL = """
SELECT
    id, first_name, last_name, email, password, is_admin, created_at, updated_at
from users
WHERE email = %s
"""


GET_EMAIL_BY_USER_ID = """
SELECT
    email
from users
WHERE id = %s
"""


GET_PASSWORD_BY_EMAIL = """
SELECT
    password
from users
WHERE email = %s
"""

GET_USER_BY_ID = """
SELECT
    id, first_name, last_name, email, password, is_admin, created_at, updated_at
from users
WHERE id = %s
"""
