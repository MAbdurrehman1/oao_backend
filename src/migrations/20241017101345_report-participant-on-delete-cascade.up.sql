ALTER TABLE report_participants DROP CONSTRAINT report_id_fk;
ALTER TABLE report_participants ADD CONSTRAINT report_id_fk 
FOREIGN KEY (report_id) REFERENCES reports (id) ON DELETE CASCADE;