STORE_REPORT_KPIS = """
INSERT INTO report_kpis (
name, report_id, score, standard_deviation, business_unit_id
) VALUES %s;
"""

GET_KPI_VALUES = """
SELECT
id,
name,
report_id,
score,
standard_deviation,
created_at,
updated_at
FROM report_kpis
WHERE name IN %s
AND report_id = %s
AND ((business_unit_id = %s) OR (business_unit_id IS NULL));
"""

GET_REPORT_BENCHMARKS_LIST = """
SELECT DISTINCT
bu.id,
bu.name
FROM business_units bu
INNER JOIN report_kpis rk on bu.id = rk.business_unit_id
WHERE rk.report_id = %s;
"""
