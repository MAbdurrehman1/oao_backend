CREATE TABLE IF NOT EXISTS oao_content (
  id SERIAL PRIMARY KEY NOT NULL,
  title VARCHAR(250) NOT NULL,
  short_description VARCHAR(500) NOT NULL,
  long_description TEXT NOT NULL,
  content_url VARCHAR(300) NOT NULL,
  thumbnail_id INTEGER NOT NULL,
  deep_dive_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT thumbnail_id_fk FOREIGN KEY (thumbnail_id) REFERENCES files (id),
  CONSTRAINT deep_dive_id_fk FOREIGN KEY (deep_dive_id) REFERENCES deep_dives (id)
);
