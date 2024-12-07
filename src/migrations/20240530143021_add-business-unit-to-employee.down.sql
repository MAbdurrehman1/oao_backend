ALTER TABLE employees
DROP CONSTRAINT business_unit_id_fk;

ALTER TABLE employees
DROP COLUMN business_unit_id;
