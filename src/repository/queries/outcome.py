STORE_OUTCOME = """
INSERT INTO outcomes (title, description, oao_content_id)
VALUES (%s, %s, %s) RETURNING id, created_at, updated_at;
"""

GET_OAO_CONTENT_OUTCOME_LIST = """
SELECT
COUNT(id) OVER () as total_count,
id,
title,
description,
oao_content_id,
created_at,
updated_at
FROM outcomes
WHERE oao_content_id = %s
OFFSET %s
LIMIT %s;
"""
