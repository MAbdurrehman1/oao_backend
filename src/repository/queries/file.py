CHECK_FILE_NAME_EXISTS = """
SELECT EXISTS(
SELECT id FROM files
WHERE name = %s
);
"""

CREATE_FILE_RECORD = """
INSERT INTO files (name, file_path, user_id, content_type)
VALUES (%s, %s, %s, %s) RETURNING id, created_at, updated_at;
"""

GET_FILE_PATH_BY_ID = """
SELECT file_path FROM files
WHERE id = %s
"""

CHECK_FILE_EXISTS_BY_ID = """
SELECT EXISTS(
SELECT id FROM files
WHERE id = %s
);
"""

GET_FILES_LIST = """
SELECT
    COUNT(id) OVER () AS total_count,
    id,
    name,
    user_id,
    content_type,
    file_path,
    created_at,
    updated_at
FROM files
ORDER BY updated_at DESC
OFFSET %s
LIMIT %s;
"""
