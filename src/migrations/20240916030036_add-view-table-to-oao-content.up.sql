CREATE TABLE IF NOT EXISTS oao_content_views (
  participation_id UUID NOT NULL,
  oao_content_id INTEGER NOT NULL,

  UNIQUE (participation_id, oao_content_id),
  CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id),
  CONSTRAINT oao_content_id_fk FOREIGN KEY (oao_content_id) REFERENCES oao_content (id)
);
