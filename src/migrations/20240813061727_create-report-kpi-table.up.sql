CREATE TABLE IF NOT EXISTS report_kpis (
  id SERIAL PRIMARY KEY NOT NULL,
  name VARCHAR(250) NOT NULL,
  score INTEGER NOT NULL,
  standard_deviation INTEGER NOT NULL,
  report_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT report_id_fk FOREIGN KEY (report_id) REFERENCES reports (id)
);