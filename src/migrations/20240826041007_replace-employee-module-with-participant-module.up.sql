DROP TABLE IF EXISTS employee_modules;
CREATE TABLE IF NOT EXISTS participation_modules (
  PRIMARY KEY (participation_id, module_id),
  participation_id UUID NOT NULL,
  module_id INTEGER NOT NULL,

  CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id),
  CONSTRAINT module_id_fk FOREIGN KEY (module_id) REFERENCES modules (id)
);
