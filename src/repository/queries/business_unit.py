CREATE_BUSINESS_UNIT = """
INSERT INTO business_units (name, organization_id, parent_id) VALUES (%s, %s, %s)
RETURNING id, created_at, updated_at;
"""

CHECK_BUSINESS_UNIT_IDS_EXIST = """
SELECT
    id
FROM business_units
WHERE id in %s
AND organization_id = %s
"""

GET_BUSINESS_UNIT_BY_ID = """
SELECT
    id, name, parent_id, organization_id, created_at, updated_at
FROM business_units
WHERE id=%s
"""


GET_BUSINESS_UNITS_HIERARCHY = """
WITH RECURSIVE entity_hierarchy AS (
    SELECT
          id,
          parent_id,
          name,
          organization_id,
          0 AS level,
          created_at,
          updated_at
    FROM business_units
    WHERE parent_id IS NULL AND organization_id = %s

    UNION ALL

    SELECT
           bu.id,
           bu.parent_id,
           bu.name,
           bu.organization_id,
           buh.level + 1,
           bu.created_at,
           bu.updated_at
    FROM business_units bu
    INNER JOIN entity_hierarchy buh ON bu.parent_id = buh.id
    WHERE bu.organization_id = %s
)
SELECT *
FROM entity_hierarchy
ORDER BY level, id;
"""


GET_SUB_BUSINESS_UNITS_HIERARCHY = """
WITH RECURSIVE entity_hierarchy AS (
    SELECT
          id,
          parent_id,
          name,
          organization_id,
          0 AS level,
          created_at,
          updated_at
    FROM business_units
    WHERE id = %s

    UNION ALL

    SELECT
           bu.id,
           bu.parent_id,
           bu.name,
           bu.organization_id,
           buh.level + 1,
           bu.created_at,
           bu.updated_at
    FROM business_units bu
    INNER JOIN entity_hierarchy buh ON bu.parent_id = buh.id
)
SELECT *
FROM entity_hierarchy
ORDER BY level, id;
"""


GET_BUSINESS_UNIT_CHILDREN_IDS = """
WITH RECURSIVE business_hierarchy AS (
    SELECT
        id
    FROM
        business_units
    WHERE
        id IN %s
    UNION ALL

    SELECT
        bu.id
    FROM
        business_units bu
    INNER JOIN
        business_hierarchy bh ON bu.parent_id = bh.id
)
SELECT
    id
FROM
    business_hierarchy
"""

GET_SUB_BUSINESS_UNITS_WITH_PARTICIPATION = """
WITH RECURSIVE business_hierarchy AS (
    SELECT
        id
    FROM
        business_units
    WHERE
        id IN %s
    UNION ALL

    SELECT
        bu.id
    FROM
        business_units bu
    INNER JOIN
        business_hierarchy bh ON bu.parent_id = bh.id
)
SELECT bh.id, sce.participation_id
FROM business_hierarchy bh
INNER JOIN employees e ON e.business_unit_id = bh.id
INNER JOIN survey_campaign_employees sce on sce.employee_id = e.id
"""

CHECK_IF_ORGANIZATION_HAS_A_ROOT_BUSINESS_UNIT = """
SELECT EXISTS(
SELECT id FROM business_units
WHERE parent_id IS NULL
AND organization_id = %s);
"""

CHECK_BUSINESS_UNIT_BELONGS_TO_ORGANIZATION = """
SELECT EXISTS(
SELECT
    id
FROM business_units
WHERE id = %s
AND organization_id = %s
);
"""

UPDATE_BUSINESS_UNIT = """
UPDATE business_units
SET
    name = %s,
    parent_id = %s,
    updated_at = %s
WHERE id = %s
RETURNING updated_at;
"""

CHECK_BUSINESS_UNIT_IDS_BELONG_TO_ORGANIZATION_ID = """
SELECT EXISTS(
    SELECT 1
    FROM business_units
    WHERE id = ANY(%s)
    AND organization_id = %s
    GROUP BY organization_id
    HAVING COUNT(*) = array_length(%s, 1)
);
"""
