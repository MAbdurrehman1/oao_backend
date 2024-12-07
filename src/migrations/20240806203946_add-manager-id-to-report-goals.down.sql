ALTER TABLE report_goals
DROP CONSTRAINT manager_id_fk;

ALTER TABLE report_goals
DROP COLUMN manager_id;
