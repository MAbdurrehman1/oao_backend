CREATE_ORGANIZATION = """
INSERT INTO organizations (
    company_name, industry, hq_location, organization_size, metadata, logo_id
) VALUES (
    %s, %s, %s, %s, %s, %s
) RETURNING id, created_at, updated_at;
"""
GET_ORGANIZATION_BY_ID = """
SELECT
    o.id,
    f.id AS logo_id,
    f.file_path AS logo_url,
    company_name,
    industry,
    hq_location,
    organization_size,
    metadata,
    o.created_at,
    o.updated_at
FROM organizations o
INNER JOIN files f ON o.logo_id = f.id
WHERE o.id = %s
"""

GET_ORGANIZATIONS_LIST = """
SELECT
    COUNT(o.id) OVER () AS total_count,
    o.id,
    f.id as logo_id,
    f.file_path as logo_url,
    company_name,
    industry,
    hq_location,
    organization_size,
    metadata,
    o.created_at,
    o.updated_at
FROM organizations o
INNER JOIN files f ON o.logo_id = f.id
ORDER BY o.updated_at DESC
OFFSET %s
LIMIT %s;
"""

CHECK_ORGANIZATION_EXISTS = """
SELECT EXISTS(
SELECT 1
FROM organizations WHERE id = %s);
"""


GET_ORGANIZATION_BY_USER_ID = """
SELECT
    o.id,
    f.id AS logo_id,
    f.file_path AS logo_url,
    company_name,
    industry,
    hq_location,
    organization_size,
    metadata,
    o.created_at,
    o.updated_at
FROM organizations o
INNER JOIN files f ON o.logo_id = f.id
INNER JOIN employees e ON e.organization_id = o.id
WHERE e.user_id = %s
"""


GET_ORGANIZATION_BY_CAMPAIGN_ID = """
SELECT
    o.id,
    f.id AS logo_id,
    f.file_path AS logo_url,
    company_name,
    industry,
    hq_location,
    organization_size,
    metadata,
    o.created_at,
    o.updated_at
FROM organizations o
INNER JOIN files f ON o.logo_id = f.id
INNER JOIN employees e ON e.organization_id = o.id
INNER JOIN survey_campaign_employees sce ON sce.employee_id = e.id
WHERE sce.survey_campaign_id = %s
"""
