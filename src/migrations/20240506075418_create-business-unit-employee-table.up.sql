CREATE TABLE IF NOT EXISTS employee_business_units (
  PRIMARY KEY (employee_id, business_unit_id),
  business_unit_id INTEGER NOT NULL,
  employee_id INTEGER NOT NULL,

  CONSTRAINT employee_id_fk FOREIGN KEY (employee_id) REFERENCES employees (id),
  CONSTRAINT business_unit_id_fk FOREIGN KEY (business_unit_id) REFERENCES business_units (id)
);
