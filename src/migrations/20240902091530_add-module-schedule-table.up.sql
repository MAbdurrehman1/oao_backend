CREATE TABLE IF NOT EXISTS module_schedules (
  id SERIAL PRIMARY KEY NOT NULL,
  participation_id UUID NOT NULL,
  module_id INTEGER NOT NULL,
  selected_date TIMESTAMP NOT NULL,
  ms_graph_event_id VARCHAR(250) NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL,

  CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id),
  CONSTRAINT module_id_fk FOREIGN KEY (module_id) REFERENCES modules (id)
);


CREATE UNIQUE INDEX unique_participation_id_module_id ON module_schedules (
    participation_id,
    module_id
);
