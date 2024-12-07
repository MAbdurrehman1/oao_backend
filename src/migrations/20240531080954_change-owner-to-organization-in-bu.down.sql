ALTER TABLE business_units
ADD COLUMN owner_id INTEGER;

ALTER TABLE business_units
ADD CONSTRAINT owner_id_fk
FOREIGN KEY (owner_id)
REFERENCES organizations (id);

CREATE UNIQUE INDEX unique_name_owner_parent ON business_units (
    name,
    owner_id,
    COALESCE(parent_id::text, 'null-value')
);

ALTER TABLE business_units
DROP CONSTRAINT organization_id_fk;

DROP INDEX unique_name_organization_parent;

ALTER TABLE business_units
DROP COLUMN organization_id;
