CREATE TABLE IF NOT EXISTS report_goals (
  id SERIAL PRIMARY KEY NOT NULL,
  title VARCHAR(250) NOT NULL,
  KPI VARCHAR(50) NOT NULL,
  description TEXT NOT NULL,
  report_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT report_id_fk FOREIGN KEY (report_id) REFERENCES reports (id)
);
