ALTER TABLE business_units
ADD COLUMN organization_id INTEGER;

ALTER TABLE business_units
ADD CONSTRAINT organization_id_fk
FOREIGN KEY (organization_id)
REFERENCES organizations (id);

CREATE UNIQUE INDEX unique_name_organization_parent ON business_units (
    name,
    organization_id,
    COALESCE(parent_id::text, 'null-value')
);

ALTER TABLE business_units
DROP CONSTRAINT owner_id_fk;

DROP INDEX unique_name_owner_parent;

ALTER TABLE business_units
DROP COLUMN owner_id;
