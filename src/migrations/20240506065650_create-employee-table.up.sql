CREATE TABLE IF NOT EXISTS employees (
  id SERIAL PRIMARY KEY NOT NULL,
  user_id INTEGER NOT NULL,
  role_title VARCHAR(400) NOT NULL,
  organization_id INTEGER NOT NULL,
  location VARCHAR(500) NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id),
  CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users (id)
);
