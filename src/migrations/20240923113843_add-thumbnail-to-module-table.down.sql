ALTER TABLE modules
DROP CONSTRAINT animated_thumbnail_id_fk,
DROP CONSTRAINT still_thumbnail_id_fk,
DROP COLUMN animated_thumbnail_id,
DROP COLUMN still_thumbnail_id
