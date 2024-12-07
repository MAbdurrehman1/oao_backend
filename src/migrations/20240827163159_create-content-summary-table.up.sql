CREATE TABLE IF NOT EXISTS content_summaries (
  id SERIAL PRIMARY KEY NOT NULL,
  title VARCHAR(250) NOT NULL,
  description TEXT NOT NULL,
  module_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT module_id_fk FOREIGN KEY (module_id) REFERENCES modules (id)
);
