CREATE TABLE IF NOT EXISTS deep_dives (
  id SERIAL PRIMARY KEY NOT NULL,
  title VARCHAR(250) NOT NULL,
  thumbnail_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT thumbnail_id_fk FOREIGN KEY (thumbnail_id) REFERENCES files (id)
);
