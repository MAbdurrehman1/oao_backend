CREATE TABLE IF NOT EXISTS organization_business_units (
  PRIMARY KEY (organization_id, business_unit_id),
  organization_id INTEGER NOT NULL,
  business_unit_id INTEGER NOT NULL,

  CONSTRAINT employee_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id),
  CONSTRAINT business_unit_id_fk FOREIGN KEY (business_unit_id) REFERENCES business_units (id)
);
