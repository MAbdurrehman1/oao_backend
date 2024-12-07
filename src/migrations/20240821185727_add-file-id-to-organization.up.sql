ALTER TABLE organizations
ADD COLUMN logo_id INT;

ALTER TABLE organizations
ADD CONSTRAINT logo_id_fk
FOREIGN KEY (logo_id)
REFERENCES files(id);
