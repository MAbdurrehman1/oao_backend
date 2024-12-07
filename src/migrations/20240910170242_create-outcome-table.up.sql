CREATE TABLE IF NOT EXISTS outcomes (
  id SERIAL PRIMARY KEY NOT NULL,
  title VARCHAR(250) NOT NULL,
  description TEXT NOT NULL,
  oao_content_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT oao_content_id_fk FOREIGN KEY (oao_content_id) REFERENCES oao_content (id)
);
