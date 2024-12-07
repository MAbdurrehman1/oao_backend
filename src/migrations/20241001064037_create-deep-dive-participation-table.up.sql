CREATE TABLE IF NOT EXISTS deep_dive_participation (
    id SERIAL PRIMARY KEY NOT NULL,
    participation_id UUID UNIQUE NOT NULL,
    deep_dive_slugs JSONB NOT NULL,

  CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id)
);
