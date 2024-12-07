CREATE TABLE IF NOT EXISTS management_positions (
  id SERIAL PRIMARY KEY NOT NULL,
  name VARCHAR(250) UNIQUE NOT NULL,
  organization_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id)
);


CREATE TABLE IF NOT EXISTS management_position_business_units (
  PRIMARY KEY (management_position_id, business_unit_id),
  business_unit_id INTEGER NOT NULL,
  management_position_id INTEGER NOT NULL,

  CONSTRAINT management_position_id_fk FOREIGN KEY (management_position_id) REFERENCES management_positions (id),
  CONSTRAINT business_unit_id_fk FOREIGN KEY (business_unit_id) REFERENCES business_units (id)
);


CREATE TABLE IF NOT EXISTS management_position_managers (
  PRIMARY KEY (management_position_id, employee_id),
  employee_id INTEGER NOT NULL,
  management_position_id INTEGER NOT NULL,

  CONSTRAINT management_position_id_fk FOREIGN KEY (management_position_id) REFERENCES management_positions (id),
  CONSTRAINT employee_id_fk FOREIGN KEY (employee_id) REFERENCES employees (id)
);
