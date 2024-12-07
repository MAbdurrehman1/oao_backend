CREATE TABLE IF NOT EXISTS library_content (
  id SERIAL PRIMARY KEY NOT NULL,
  title VARCHAR(250) NOT NULL,
  description VARCHAR(500) NOT NULL,
  content_url VARCHAR(300) NOT NULL,
  thumbnail_id INTEGER NOT NULL,
  library_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT thumbnail_id_fk FOREIGN KEY (thumbnail_id) REFERENCES files (id),
  CONSTRAINT library_id_fk FOREIGN KEY (library_id) REFERENCES information_libraries (id)
);
