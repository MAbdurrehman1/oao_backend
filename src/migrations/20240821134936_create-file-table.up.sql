CREATE TABLE IF NOT EXISTS files (
  id SERIAL PRIMARY KEY NOT NULL,
  name VARCHAR(250) UNIQUE NOT NULL,
  file_path VARCHAR(500) NOT NULL,
  user_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE INDEX idx_file_name ON files (name);
