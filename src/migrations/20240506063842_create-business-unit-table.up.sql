CREATE TABLE IF NOT EXISTS business_units (
  id SERIAL PRIMARY KEY NOT NULL,
  owner_id INTEGER NOT NULL,
  parent_id INTEGER,
  name VARCHAR(500) NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT owner_id_fk FOREIGN KEY (owner_id) REFERENCES organizations (id),
  CONSTRAINT parent_id_fk FOREIGN KEY (parent_id) REFERENCES business_units (id)
);

CREATE UNIQUE INDEX unique_name_owner_parent ON business_units (
    name,
    owner_id,
    COALESCE(parent_id::text, 'null-value')
);
