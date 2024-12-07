CREATE TABLE IF NOT EXISTS innovation_ideas (
  id SERIAL PRIMARY KEY NOT NULL,
  title VARCHAR(250) NOT NULL,
  description TEXT NOT NULL,
  participation_id UUID NOT NULL,
  feasibility_score INTEGER NOT NULL,
  impact_score INTEGER NOT NULL,
  confidence_score INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id)
);