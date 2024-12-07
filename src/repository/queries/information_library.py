STORE_INFORMATION_LIBRARY = """
INSERT INTO information_libraries (
title,
short_description,
long_description,
organization_id,
deep_dive_id
) VALUES (%s, %s, %s, %s, %s) RETURNING id, created_at, updated_at;
"""

GET_EMPLOYEE_INFORMATION_LIBRARIES = """
SELECT
COUNT(il.id) OVER() AS total_count,
il.id,
title,
short_description,
long_description,
deep_dive_id,
il.organization_id,
il.created_at,
il.updated_at
FROM information_libraries il
LEFT JOIN employees e ON il.organization_id = e.organization_id
WHERE (e.id = %s OR il.organization_id IS NULL)
AND deep_dive_id = %s
OFFSET %s
LIMIT %s;
"""

CHECK_LIBRARY_BELONG_TO_EMPLOYEE = """
SELECT EXISTS(
SELECT il.id
FROM information_libraries il
LEFT JOIN employees e ON il.organization_id = e.organization_id
WHERE (e.id = %s AND il.id = %s) OR (il.id = %s AND il.organization_id IS NULL)
);
"""
