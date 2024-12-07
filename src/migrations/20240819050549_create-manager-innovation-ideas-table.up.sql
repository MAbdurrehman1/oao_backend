CREATE TABLE IF NOT EXISTS manager_innovation_ideas (
  PRIMARY KEY (manager_id, innovation_idea_id),
  manager_id INTEGER,
  innovation_idea_id INTEGER,

  CONSTRAINT manager_id_fk FOREIGN KEY (manager_id) REFERENCES employees (id),
  CONSTRAINT innovation_idea_id_fk FOREIGN KEY (innovation_idea_id) REFERENCES innovation_ideas (id)
);
