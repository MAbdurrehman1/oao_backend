ALTER TABLE participation_modules
ADD COLUMN created_at TIMESTAMP DEFAULT now() NOT NULL,
ADD COLUMN updated_at TIMESTAMP DEFAULT now() NOT NULL
