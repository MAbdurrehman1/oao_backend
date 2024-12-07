CREATE TABLE IF NOT EXISTS report_participants (
  PRIMARY KEY (participation_id, report_id),
  participation_id UUID,
  report_id int,

  CONSTRAINT report_id_fk FOREIGN KEY (report_id) REFERENCES reports (id),
  CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id)
);
