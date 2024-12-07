DROP TABLE IF EXISTS participation_modules;
CREATE TABLE IF NOT EXISTS employee_modules (
  PRIMARY KEY (employee_id, module_id),
  employee_id INTEGER NOT NULL,
  module_id INTEGER NOT NULL,

  CONSTRAINT employee_id_fk FOREIGN KEY (employee_id) REFERENCES employees (id),
  CONSTRAINT module_id_fk FOREIGN KEY (module_id) REFERENCES modules (id)
);
