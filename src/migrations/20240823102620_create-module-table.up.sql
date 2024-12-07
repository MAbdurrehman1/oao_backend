CREATE TABLE IF NOT EXISTS modules (
  id SERIAL PRIMARY KEY NOT NULL,
  title VARCHAR(500) NOT NULL,
  description TEXT NOT NULL,
  duration INTEGER NOT NULL,
  module_order INTEGER UNIQUE NOT NULL,
  url VARCHAR(500) NOT NULL,
  created_at TIMESTAMP DEFAULT now() NOT NULL,
  updated_at TIMESTAMP DEFAULT now() NOT NULL,
  deleted_at TIMESTAMP DEFAULT NULL
);


CREATE TABLE IF NOT EXISTS employee_modules (
  PRIMARY KEY (employee_id, module_id),
  employee_id INTEGER NOT NULL,
  module_id INTEGER NOT NULL,

  CONSTRAINT employee_id_fk FOREIGN KEY (employee_id) REFERENCES employees (id),
  CONSTRAINT module_id_fk FOREIGN KEY (module_id) REFERENCES modules (id)
);
