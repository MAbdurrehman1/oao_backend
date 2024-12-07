CREATE OR REPLACE FUNCTION enforce_single_root() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.parent_id IS NULL THEN
        IF (SELECT COUNT(*) FROM business_units
            WHERE parent_id IS NULL
            AND organization_id = NEW.organization_id) > 0 THEN
            RAISE EXCEPTION 'Only one root node is allowed per organization';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_single_root
BEFORE INSERT OR UPDATE ON business_units
FOR EACH ROW
EXECUTE FUNCTION enforce_single_root();
