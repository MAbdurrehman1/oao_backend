ALTER TABLE users
ADD COLUMN user_type VARCHAR(100);

ALTER TABLE users
DROP COLUMN is_admin;