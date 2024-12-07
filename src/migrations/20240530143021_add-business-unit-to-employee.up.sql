ALTER TABLE employees
ADD COLUMN business_unit_id INTEGER;

ALTER TABLE employees
ADD CONSTRAINT business_unit_id_fk
FOREIGN KEY (business_unit_id)
REFERENCES business_units (id);
