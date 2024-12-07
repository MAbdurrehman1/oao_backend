STORE_OAO_CONTENT = """
INSERT INTO oao_content (
               title,
               short_description,
               long_description,
               content_url,
               deep_dive_id,
               thumbnail_id
) VALUES (%s, %s, %s, %s, %s, %s)
RETURNING id, created_at, updated_at;
"""

GET_OAO_CONTENT_LIST = """
SELECT
COUNT(oc.id) OVER () AS total_count,
oc.id,
title,
short_description,
long_description,
content_url,
deep_dive_id,
f.id AS thumbnail_id,
f.file_path AS thumbnail_url,
oc.created_at,
oc.updated_at
FROM oao_content oc
INNER JOIN files f ON f.id = oc.thumbnail_id
WHERE deep_dive_id = %s
ORDER BY oc.updated_at DESC
OFFSET %s
LIMIT %s;
"""

UPSERT_OAO_CONTENT_VIEW = """
INSERT INTO oao_content_views
(participation_id, oao_content_id)
VALUES (%s, %s)
ON CONFLICT (participation_id, oao_content_id)
DO NOTHING
"""


CHECK_OAO_CONTENT_EXISTS = """
SELECT EXISTS(SELECT id
FROM oao_content
WHERE id = %s);
"""


GET_VIEWED_OAO_CONTENT_IDS_LIST = """
SELECT oao_content_id
FROM oao_content_views
WHERE participation_id = %s
"""
