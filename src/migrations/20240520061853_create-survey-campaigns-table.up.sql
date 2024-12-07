CREATE EXTENSION IF NOT EXISTS "uuid-ossp";  -- noqa: RF05

CREATE TABLE IF NOT EXISTS survey_campaigns (
  id SERIAL PRIMARY KEY NOT NULL,
  title VARCHAR(250) NOT NULL,
  survey_url VARCHAR(500) NOT NULL,
  start_date TIMESTAMP NOT NULL,
  end_date TIMESTAMP NOT NULL,
  invitation_sending_due_date TIMESTAMP NOT NULL,
  organization_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id)
);

CREATE TABLE IF NOT EXISTS survey_campaign_employees (
  participation_id UUID PRIMARY KEY NOT NULL DEFAULT uuid_generate_v4(),
  survey_campaign_id INTEGER NOT NULL,
  employee_id INTEGER NOT NULL,

  UNIQUE (survey_campaign_id, employee_id),
  CONSTRAINT employee_id_fk FOREIGN KEY (employee_id) REFERENCES employees (id),
  CONSTRAINT survey_campaign_id_fk FOREIGN KEY (survey_campaign_id) REFERENCES survey_campaigns (id)
);