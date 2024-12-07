CREATE INDEX idx_management_positions_deleted_at ON management_positions(deleted_at);
CREATE INDEX idx_survey_campaigns_deleted_at ON survey_campaigns(deleted_at);
CREATE INDEX idx_business_units_deleted_at ON business_units(deleted_at);
CREATE INDEX idx_employees_deleted_at ON employees(deleted_at);
CREATE INDEX idx_organizations_deleted_at ON organizations(deleted_at);
CREATE INDEX idx_users_deleted_at ON users(deleted_at);
