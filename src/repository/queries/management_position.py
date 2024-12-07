GET_MANAGEMENT_POSITIONS_LIST = """
SELECT
    COUNT(mp.id) OVER () AS total_count,
    mp.id,
    mp.name,
    JSON_AGG(
    JSON_BUILD_OBJECT(
    'business_unit_id', bu.id, 'business_unit_name', bu.name
    )
    ) AS business_units,
    COUNT(mpm.employee_id) AS managers_count
FROM management_positions mp
LEFT JOIN management_position_business_units mpbu on mpbu.management_position_id = mp.id
LEFT JOIN management_position_managers mpm on mpm.management_position_id = mp.id
LEFT JOIN business_units bu on mpbu.business_unit_id = bu.id
WHERE mp.organization_id = %s
GROUP BY mp.id
OFFSET %s
LIMIT %s;
"""

STORE_MANAGEMENT_POSITION = """
INSERT INTO management_positions
(name, organization_id)
VALUES (%s, %s) RETURNING id, created_at, updated_at;
"""

ADD_BUSINESS_UNIT_TO_MANAGEMENT_POSITION = """
INSERT INTO management_position_business_units
(business_unit_id, management_position_id) VALUES %s
"""

ADD_MANAGER_TO_MANAGEMENT_POSITION = """
INSERT INTO management_position_managers
(employee_id, management_position_id) values (%s, %s)
"""

GET_MANAGEMENT_POSITION_DETAILS = """
SELECT
    mp.id,
    mp.name,
    JSON_AGG(
    JSON_BUILD_OBJECT(
    'business_unit_id', bu.id, 'business_unit_name', bu.name
    )
    ) AS business_units,
    COALESCE(
    JSON_AGG(
    JSON_BUILD_OBJECT(
     'user_id', u.id,
     'user_email', u.email,
     'user_first_name', u.first_name,
     'user_last_name', u.last_name,
     'location', e.location,
     'role_title', e.role_title,
     'employee_id', e.id
    )) FILTER ( WHERE e.id IS NOT NULL ), '[]'
    ) AS managers
FROM management_positions mp
LEFT JOIN management_position_business_units mpbu on mpbu.management_position_id = mp.id
LEFT JOIN management_position_managers mpm on mpm.management_position_id = mp.id
LEFT JOIN business_units bu on mpbu.business_unit_id = bu.id
LEFT JOIN employees e on mpm.employee_id = e.id
LEFT JOIN users u on e.user_id = u.id
WHERE mp.id = %s
GROUP BY mp.id
"""


GET_ORGANIZATION_ID_BY_MANAGEMENT_POSITION_ID = """
SELECT organization_id
FROM management_positions
WHERE id = %s;
"""

GET_BUSINESS_UNIT_IDS_BY_MANAGEMENT_POSITION_ID = """
SELECT business_unit_id
FROM management_position_business_units
WHERE management_position_id = %s
"""


CHECK_MANAGEMENT_POSITIONS_EXISTS = """
SELECT EXISTS(
 SELECT 1 FROM management_positions
 WHERE id = %s
);
"""


CHECK_IF_USER_IS_MANAGER = """
SELECT EXISTS(
SELECT 1 FROM management_position_managers mpm
INNER JOIN employees e ON e.id = mpm.employee_id
INNER JOIN users u ON u.id = e.user_id
WHERE user_id = %s
);
"""

CHECK_IDEA_BELONG_TO_MANAGER = """
SELECT EXISTS(
SELECT 1 FROM innovation_ideas i
INNER JOIN report_participants rp ON rp.participation_id = i.participation_id
INNER JOIN reports r ON rp.report_id = r.id
INNER JOIN management_position_managers mpm
ON mpm.management_position_id = r.management_position_id
INNER JOIN employees e ON e.id = mpm.employee_id
WHERE i.id = %s
AND e.user_id = %s
);
"""

UPDATE_MANAGEMENT_POSITION = """
UPDATE management_positions SET name = %s
WHERE id = %s;
"""

CHECK_IF_EMPLOYEE_IS_IN_MANAGEMENT_POSITION = """
SELECT EXISTS(
SELECT 1 FROM management_position_managers mpm
INNER JOIN employees e ON e.id = mpm.employee_id
WHERE mpm.employee_id = %s
AND mpm.management_position_id = %s
);
"""

CHECK_IF_POSITION_BELONGS_TO_ORGANIZATION = """
SELECT EXISTS(
 SELECT 1 FROM management_positions
 WHERE id = %s
 AND organization_id = %s
);
"""

REMOVE_MANAGER_FROM_MANAGEMENT_POSITION = """
DELETE FROM management_position_managers WHERE
employee_id = %s
AND management_position_id = %s;
"""
