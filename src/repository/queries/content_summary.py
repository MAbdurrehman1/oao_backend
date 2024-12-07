GET_CONTENT_SUMMARY_LIST = """
SELECT
COUNT(id) OVER () AS total_count,
id,
title,
module_id,
description,
created_at,
updated_at
FROM content_summaries
WHERE module_id = %s
ORDER BY content_order
OFFSET %s
LIMIT %s;
"""

STORE_CONTENT_SUMMARY = """
INSERT INTO content_summaries
(title, description, module_id)
VALUES (%s, %s, %s) RETURNING id, created_at, updated_at;
"""
