STORE_DEEP_DIVE = """
INSERT INTO deep_dives
(title, description, thumbnail_id, slug) VALUES
(%s, %s, %s, %s) RETURNING id, created_at, updated_at;
"""


GET_DEEP_DIVE_LIST = """
SELECT
COUNT(d.id) OVER () as total_count,
d.id,
title,
description,
f.id as thumbnail_id,
f.file_path as thumbnail_url,
d.created_at,
d.updated_at
FROM deep_dives d
INNER JOIN files f on d.thumbnail_id = f.id
OFFSET %s
LIMIT %s;
"""

CHECK_DEEP_DIVE_EXISTS = """
SELECT EXISTS(
SELECT id
FROM deep_dives WHERE id = %s);
"""


UPSERT_DEEP_DIVE_SLUG_LIST = """
INSERT INTO deep_dive_participation(participation_id, deep_dive_slugs)
VALUES (%s, %s)
ON CONFLICT (participation_id)
DO UPDATE
SET
deep_dive_slugs = EXCLUDED.deep_dive_slugs
RETURNING id;
"""

GET_DEEP_DIVE_SLUG_LIST = """
SELECT deep_dive_slugs
FROM deep_dive_participation
WHERE participation_id = %s
"""


GET_DEEP_DIVE_LIST_BY_SLUG = """
SELECT
COUNT(d.id) OVER () as total_count,
d.id,
title,
description,
f.id as thumbnail_id,
f.file_path as thumbnail_url,
d.created_at,
d.updated_at
FROM deep_dives d
INNER JOIN files f on d.thumbnail_id = f.id
WHERE (d.slug IN %s OR d.slug IS NULL)
OFFSET %s
LIMIT %s;
"""
