STORE_LIBRARY_CONTENT = """
INSERT INTO library_content
(title, description, content_url, thumbnail_id, library_id)
VALUES (%s, %s, %s, %s, %s) RETURNING id, created_at, updated_at;
"""

GET_LIBRARY_CONTENT_LIST = """
SELECT
COUNT(lc.id) OVER () AS total_count,
lc.id,
title,
description,
content_url,
library_id,
f.id AS thumbnail_id,
f.file_path AS thumbnail_url,
lc.created_at,
lc.updated_at
FROM library_content lc
INNER JOIN files f ON lc.thumbnail_id = f.id
WHERE library_id = %s
OFFSET %s
LIMIT %s;
"""
