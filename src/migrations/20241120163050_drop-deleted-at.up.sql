ALTER TABLE business_units DROP COLUMN deleted_at;
ALTER TABLE content_summaries DROP COLUMN deleted_at;
ALTER TABLE deep_dives DROP COLUMN deleted_at;
ALTER TABLE employees DROP COLUMN deleted_at;
ALTER TABLE files DROP COLUMN deleted_at;
ALTER TABLE information_libraries DROP COLUMN deleted_at;
ALTER TABLE innovation_idea_rates DROP COLUMN deleted_at;
ALTER TABLE innovation_ideas DROP COLUMN deleted_at;
ALTER TABLE library_content DROP COLUMN deleted_at;
ALTER TABLE management_positions DROP COLUMN deleted_at;
ALTER TABLE module_schedules DROP COLUMN deleted_at;
ALTER TABLE modules DROP COLUMN deleted_at;
ALTER TABLE oao_content DROP COLUMN deleted_at;
ALTER TABLE organizations DROP COLUMN deleted_at;
ALTER TABLE outcomes DROP COLUMN deleted_at;
ALTER TABLE report_goals DROP COLUMN deleted_at;
ALTER TABLE report_kpis DROP COLUMN deleted_at;
ALTER TABLE reports DROP COLUMN deleted_at;
ALTER TABLE survey_campaigns DROP COLUMN deleted_at;
ALTER TABLE users DROP COLUMN deleted_at;

-- DROP CONSTRAINTS

ALTER TABLE business_units
DROP CONSTRAINT organization_id_fk,
DROP CONSTRAINT parent_id_fk;

ALTER TABLE content_summaries
DROP CONSTRAINT module_id_fk;

ALTER TABLE deep_dive_participation
DROP CONSTRAINT participation_id_fk;

ALTER TABLE deep_dives
DROP CONSTRAINT thumbnail_id_fk;

ALTER TABLE employee_business_units
DROP CONSTRAINT business_unit_id_fk,
DROP CONSTRAINT employee_id_fk;

ALTER TABLE employees
DROP CONSTRAINT business_unit_id_fk,
DROP CONSTRAINT organization_id_fk,
DROP CONSTRAINT user_id_fk;

ALTER TABLE files
DROP CONSTRAINT user_id_fk;

ALTER TABLE information_libraries
DROP CONSTRAINT deep_dive_id_fk,
DROP CONSTRAINT organization_id_fk;

ALTER TABLE innovation_idea_rates
DROP CONSTRAINT innovation_idea_id_fk,
DROP CONSTRAINT manager_id_fk;

ALTER TABLE innovation_ideas
DROP CONSTRAINT participation_id_fk;

ALTER TABLE library_content
DROP CONSTRAINT library_id_fk,
DROP CONSTRAINT thumbnail_id_fk;

ALTER TABLE management_position_business_units
DROP CONSTRAINT business_unit_id_fk,
DROP CONSTRAINT management_position_id_fk;

ALTER TABLE management_position_managers
DROP CONSTRAINT employee_id_fk,
DROP CONSTRAINT management_position_id_fk;

ALTER TABLE management_positions
DROP CONSTRAINT organization_id_fk;

ALTER TABLE manager_innovation_ideas
DROP CONSTRAINT innovation_idea_id_fk,
DROP CONSTRAINT manager_id_fk;

ALTER TABLE module_schedules
DROP CONSTRAINT module_id_fk,
DROP CONSTRAINT participation_id_fk;

ALTER TABLE modules
DROP CONSTRAINT animated_thumbnail_id_fk,
DROP CONSTRAINT still_thumbnail_id_fk;

ALTER TABLE oao_content
DROP CONSTRAINT deep_dive_id_fk,
DROP CONSTRAINT thumbnail_id_fk;

ALTER TABLE oao_content_views
DROP CONSTRAINT oao_content_id_fk,
DROP CONSTRAINT participation_id_fk;

ALTER TABLE organizations
DROP CONSTRAINT logo_id_fk;

ALTER TABLE outcomes
DROP CONSTRAINT oao_content_id_fk;

ALTER TABLE participation_modules
DROP CONSTRAINT module_id_fk,
DROP CONSTRAINT participation_id_fk;

ALTER TABLE report_goals
DROP CONSTRAINT manager_id_fk,
DROP CONSTRAINT report_id_fk;

ALTER TABLE report_kpis
DROP CONSTRAINT report_id_fk;

ALTER TABLE report_participants
DROP CONSTRAINT report_id_fk,
DROP CONSTRAINT participation_id_fk;

ALTER TABLE reports
DROP CONSTRAINT management_position_id_fk;

ALTER TABLE survey_campaign_employees
DROP CONSTRAINT employee_id_fk,
DROP CONSTRAINT survey_campaign_id_fk;

ALTER TABLE survey_campaigns
DROP CONSTRAINT organization_id_fk;

-- ADD NEW CONSTRAINTS

ALTER TABLE business_units
ADD CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id) ON DELETE CASCADE,
ADD CONSTRAINT parent_id_fk FOREIGN KEY (parent_id) REFERENCES business_units (id) ON DELETE CASCADE;

ALTER TABLE content_summaries
ADD CONSTRAINT module_id_fk FOREIGN KEY (module_id) REFERENCES modules (id) ON DELETE CASCADE;

ALTER TABLE deep_dive_participation
ADD CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id) ON DELETE CASCADE;

ALTER TABLE deep_dives
ADD CONSTRAINT thumbnail_id_fk FOREIGN KEY (thumbnail_id) REFERENCES files (id) ON DELETE CASCADE;

ALTER TABLE employee_business_units
ADD CONSTRAINT business_unit_id_fk FOREIGN KEY (business_unit_id) REFERENCES business_units (id) ON DELETE CASCADE,
ADD CONSTRAINT employee_id_fk FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE;

ALTER TABLE employees
ADD CONSTRAINT business_unit_id_fk FOREIGN KEY (business_unit_id) REFERENCES business_units (id) ON DELETE CASCADE,
ADD CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id) ON DELETE CASCADE,
ADD CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE;

ALTER TABLE files
ADD CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE;

ALTER TABLE information_libraries
ADD CONSTRAINT deep_dive_id_fk FOREIGN KEY (deep_dive_id) REFERENCES deep_dives (id) ON DELETE CASCADE,
ADD CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id) ON DELETE CASCADE;

ALTER TABLE innovation_idea_rates
ADD CONSTRAINT innovation_idea_id_fk FOREIGN KEY (innovation_idea_id) REFERENCES innovation_ideas (id) ON DELETE CASCADE,
ADD CONSTRAINT manager_id_fk FOREIGN KEY (manager_id) REFERENCES employees (id) ON DELETE CASCADE;

ALTER TABLE innovation_ideas
ADD CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id) ON DELETE CASCADE;

ALTER TABLE library_content
ADD CONSTRAINT library_id_fk FOREIGN KEY (library_id) REFERENCES information_libraries (id) ON DELETE CASCADE,
ADD CONSTRAINT thumbnail_id_fk FOREIGN KEY (thumbnail_id) REFERENCES files (id) ON DELETE CASCADE;

ALTER TABLE management_position_business_units
ADD CONSTRAINT business_unit_id_fk FOREIGN KEY (business_unit_id) REFERENCES business_units (id) ON DELETE CASCADE,
ADD CONSTRAINT management_position_id_fk FOREIGN KEY (management_position_id) REFERENCES management_positions (id) ON DELETE CASCADE;

ALTER TABLE management_position_managers
ADD CONSTRAINT employee_id_fk FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE,
ADD CONSTRAINT management_position_id_fk FOREIGN KEY (management_position_id) REFERENCES management_positions (id) ON DELETE CASCADE;

ALTER TABLE management_positions
ADD CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id) ON DELETE CASCADE;

ALTER TABLE manager_innovation_ideas
ADD CONSTRAINT innovation_idea_id_fk FOREIGN KEY (innovation_idea_id) REFERENCES innovation_ideas (id) ON DELETE CASCADE,
ADD CONSTRAINT manager_id_fk FOREIGN KEY (manager_id) REFERENCES employees (id) ON DELETE CASCADE;

ALTER TABLE module_schedules
ADD CONSTRAINT module_id_fk FOREIGN KEY (module_id) REFERENCES modules (id) ON DELETE CASCADE,
ADD CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id) ON DELETE CASCADE;

ALTER TABLE modules
ADD CONSTRAINT animated_thumbnail_id_fk FOREIGN KEY (animated_thumbnail_id) REFERENCES files (id) ON DELETE CASCADE,
ADD CONSTRAINT still_thumbnail_id_fk FOREIGN KEY (still_thumbnail_id) REFERENCES files (id) ON DELETE CASCADE;

ALTER TABLE oao_content
ADD CONSTRAINT deep_dive_id_fk FOREIGN KEY (deep_dive_id) REFERENCES deep_dives (id) ON DELETE CASCADE,
ADD CONSTRAINT thumbnail_id_fk FOREIGN KEY (thumbnail_id) REFERENCES files (id) ON DELETE CASCADE;

ALTER TABLE oao_content_views
ADD CONSTRAINT oao_content_id_fk FOREIGN KEY (oao_content_id) REFERENCES oao_content (id) ON DELETE CASCADE,
ADD CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id) ON DELETE CASCADE;

ALTER TABLE organizations
ADD CONSTRAINT logo_id_fk FOREIGN KEY (logo_id) REFERENCES files (id) ON DELETE CASCADE;

ALTER TABLE outcomes
ADD CONSTRAINT oao_content_id_fk FOREIGN KEY (oao_content_id) REFERENCES oao_content (id) ON DELETE CASCADE;

ALTER TABLE participation_modules
ADD CONSTRAINT module_id_fk FOREIGN KEY (module_id) REFERENCES modules (id) ON DELETE CASCADE,
ADD CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id) ON DELETE CASCADE;

ALTER TABLE report_goals
ADD CONSTRAINT manager_id_fk FOREIGN KEY (manager_id) REFERENCES employees (id) ON DELETE CASCADE,
ADD CONSTRAINT report_id_fk FOREIGN KEY (report_id) REFERENCES reports (id) ON DELETE CASCADE;

ALTER TABLE report_kpis
ADD CONSTRAINT report_id_fk FOREIGN KEY (report_id) REFERENCES reports (id) ON DELETE CASCADE;

ALTER TABLE report_participants
ADD CONSTRAINT report_id_fk FOREIGN KEY (report_id) REFERENCES reports (id) ON DELETE CASCADE,
ADD CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id) ON DELETE CASCADE;

ALTER TABLE reports
ADD CONSTRAINT management_position_id_fk FOREIGN KEY (management_position_id) REFERENCES management_positions (id) ON DELETE CASCADE;

ALTER TABLE survey_campaign_employees
ADD CONSTRAINT employee_id_fk FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE,
ADD CONSTRAINT survey_campaign_id_fk FOREIGN KEY (survey_campaign_id) REFERENCES survey_campaigns (id) ON DELETE CASCADE;

ALTER TABLE survey_campaigns
ADD CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id) ON DELETE CASCADE;
