CREATE_INNOVATION_IDEA = """
INSERT INTO innovation_ideas (
participation_id,
 title,
  description,
    feasibility_score,
     confidence_score,
      impact_score
      ) VALUES (%s, %s, %s, %s, %s, %s)
RETURNING id, created_at, updated_at;
"""

GET_INNOVATION_IDEA_BY_ID = """
SELECT
i.id,
i.participation_id,
u.first_name,
u.last_name,
u.email,
e.role_title,
e.location,
title,
description,
feasibility_score,
confidence_score,
impact_score,
i.created_at,
i.updated_at,
iir.rate AS manager_rate
FROM innovation_ideas i
INNER JOIN survey_campaign_employees sce ON i.participation_id = sce.participation_id
INNER JOIN employees e ON sce.employee_id = e.id
INNER JOIN users u ON e.user_id = u.id
LEFT JOIN innovation_idea_rates iir ON
(iir.innovation_idea_id = i.id AND iir.manager_id = %s)
WHERE i.id = %s
"""

CHECK_IDEA_BELONG_TO_MANAGER = """
SELECT EXISTS(
SELECT 1 FROM innovation_ideas i
INNER JOIN report_participants rp ON i.participation_id = rp.participation_id
INNER JOIN reports r ON r.id = rp.report_id
INNER JOIN management_position_managers mpm
ON mpm.management_position_id = r.management_position_id
WHERE mpm.employee_id = %s
);
"""

GET_IDEAS_LIST_PART_ONE = """
SELECT
COUNT(i.id) OVER () AS total_count,
i.id,
i.participation_id,
u.first_name,
u.last_name,
u.email,
e.role_title,
e.location,
i.title,
i.description,
i.feasibility_score,
i.confidence_score,
i.impact_score,
i.created_at,
i.updated_at
"""

GET_IDEAS_LIST_PART_TWO = """
FROM innovation_ideas i
INNER JOIN report_participants rp ON i.participation_id = rp.participation_id
INNER JOIN survey_campaign_employees sce ON i.participation_id = sce.participation_id
INNER JOIN employees e ON sce.employee_id = e.id
INNER JOIN users u ON e.user_id = u.id
"""

GET_IDEAS_LIST_SELECT_RATE = ",\niir.rate AS manager_rate\n"

GET_IDEAS_LIST_BY_REPORT_ID = """
WHERE report_id = %s
"""

GET_IDEAS_MATRIX_LIST_BY_REPORT_ID = """
SELECT
i.id,
i.title,
i.feasibility_score,
i.confidence_score,
i.impact_score
FROM innovation_ideas i
INNER JOIN report_participants rp ON i.participation_id = rp.participation_id
WHERE report_id = %s;
"""

GET_MANAGER_RATED_IDEAS_COUNT = """
SELECT COUNT(innovation_idea_id) FROM innovation_idea_rates iir
INNER JOIN innovation_ideas i on i.id = iir.innovation_idea_id
INNER JOIN report_participants rp ON i.participation_id = rp.participation_id
WHERE rp.report_id = %s
"""

GET_EMPLOYEE_LAST_CAMPAIGN_INNOVATION_IDEA = """
SELECT
i.id,
i.participation_id,
u.first_name,
u.last_name,
u.email,
e.role_title,
e.location,
i.title,
i.description,
i.feasibility_score,
i.confidence_score,
i.impact_score,
i.created_at,
i.updated_at
FROM innovation_ideas i
INNER JOIN survey_campaign_employees sce ON i.participation_id = sce.participation_id
INNER JOIN employees e ON e.id = sce.employee_id
INNER JOIN users u ON e.user_id = u.id
WHERE sce.employee_id = %s
AND sce.survey_campaign_id = (
SELECT sc.id
FROM survey_campaigns sc
WHERE EXISTS (
            SELECT 1
            FROM survey_campaign_employees sce
            WHERE sce.employee_id = %s
            AND sce.survey_campaign_id = sc.id
        )
ORDER BY sc.end_date DESC
LIMIT 1
);
"""
