CREATE TABLE IF NOT EXISTS information_libraries (
  id SERIAL PRIMARY KEY NOT NULL,
  title VARCHAR(250) NOT NULL,
  short_description VARCHAR(500) NOT NULL,
  long_description TEXT NOT NULL,
  deep_dive_id INTEGER NOT NULL,
  organization_id INTEGER,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT deep_dive_id_fk FOREIGN KEY (deep_dive_id) REFERENCES deep_dives (id),
  CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id)
);
