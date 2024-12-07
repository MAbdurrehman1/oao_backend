ALTER TABLE report_goals
ADD COLUMN manager_id INTEGER;
ALTER TABLE report_goals
ADD CONSTRAINT manager_id_fk FOREIGN KEY (manager_id) REFERENCES employees (id);
