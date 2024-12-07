ALTER TABLE modules
ADD COLUMN animated_thumbnail_id INTEGER,
ADD COLUMN still_thumbnail_id INTEGER,
ADD CONSTRAINT animated_thumbnail_id_fk FOREIGN KEY (animated_thumbnail_id) REFERENCES files (id),
ADD CONSTRAINT still_thumbnail_id_fk FOREIGN KEY (still_thumbnail_id) REFERENCES files (id)
