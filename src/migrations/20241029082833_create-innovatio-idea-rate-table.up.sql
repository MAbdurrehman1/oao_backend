CREATE TABLE IF NOT EXISTS innovation_idea_rates (
  id SERIAL PRIMARY KEY NOT NULL,
  manager_id INTEGER NOT NULL,
  innovation_idea_id INTEGER NOT NULL,
  rate INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT manager_id_fk FOREIGN KEY (manager_id) REFERENCES employees (id),
  CONSTRAINT innovation_idea_id_fk FOREIGN KEY (innovation_idea_id) REFERENCES innovation_ideas (id)
);

