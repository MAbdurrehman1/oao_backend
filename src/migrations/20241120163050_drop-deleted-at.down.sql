ALTER TABLE business_units ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE content_summaries ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE deep_dives ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE employees ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE files ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE information_libraries ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE innovation_idea_rates ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE innovation_ideas ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE library_content ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE management_positions ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE module_schedules ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE modules ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE oao_content ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE organizations ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE outcomes ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE report_goals ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE report_kpis ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE reports ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE survey_campaigns ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP DEFAULT NULL;

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
ADD CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id),
ADD CONSTRAINT parent_id_fk FOREIGN KEY (parent_id) REFERENCES business_units (id);

ALTER TABLE content_summaries
ADD CONSTRAINT module_id_fk FOREIGN KEY (module_id) REFERENCES modules (id);

ALTER TABLE deep_dive_participation
ADD CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id);

ALTER TABLE deep_dives
ADD CONSTRAINT thumbnail_id_fk FOREIGN KEY (thumbnail_id) REFERENCES files (id);

ALTER TABLE employee_business_units
ADD CONSTRAINT business_unit_id_fk FOREIGN KEY (business_unit_id) REFERENCES business_units (id),
ADD CONSTRAINT employee_id_fk FOREIGN KEY (employee_id) REFERENCES employees (id);

ALTER TABLE employees
ADD CONSTRAINT business_unit_id_fk FOREIGN KEY (business_unit_id) REFERENCES business_units (id),
ADD CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id),
ADD CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users (id);

ALTER TABLE files
ADD CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users (id);

ALTER TABLE information_libraries
ADD CONSTRAINT deep_dive_id_fk FOREIGN KEY (deep_dive_id) REFERENCES deep_dives (id),
ADD CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id);

ALTER TABLE innovation_idea_rates
ADD CONSTRAINT innovation_idea_id_fk FOREIGN KEY (innovation_idea_id) REFERENCES innovation_ideas (id),
ADD CONSTRAINT manager_id_fk FOREIGN KEY (manager_id) REFERENCES employees (id);

ALTER TABLE innovation_ideas
ADD CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id);

ALTER TABLE library_content
ADD CONSTRAINT library_id_fk FOREIGN KEY (library_id) REFERENCES information_libraries (id),
ADD CONSTRAINT thumbnail_id_fk FOREIGN KEY (thumbnail_id) REFERENCES files (id);

ALTER TABLE management_position_business_units
ADD CONSTRAINT business_unit_id_fk FOREIGN KEY (business_unit_id) REFERENCES business_units (id),
ADD CONSTRAINT management_position_id_fk FOREIGN KEY (management_position_id) REFERENCES management_positions (id);

ALTER TABLE management_position_managers
ADD CONSTRAINT employee_id_fk FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE,
ADD CONSTRAINT management_position_id_fk FOREIGN KEY (management_position_id) REFERENCES management_positions (id);

ALTER TABLE management_positions
ADD CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id);

ALTER TABLE manager_innovation_ideas
ADD CONSTRAINT innovation_idea_id_fk FOREIGN KEY (innovation_idea_id) REFERENCES innovation_ideas (id),
ADD CONSTRAINT manager_id_fk FOREIGN KEY (manager_id) REFERENCES employees (id);

ALTER TABLE module_schedules
ADD CONSTRAINT module_id_fk FOREIGN KEY (module_id) REFERENCES modules (id),
ADD CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id);

ALTER TABLE modules
ADD CONSTRAINT animated_thumbnail_id_fk FOREIGN KEY (animated_thumbnail_id) REFERENCES files (id),
ADD CONSTRAINT still_thumbnail_id_fk FOREIGN KEY (still_thumbnail_id) REFERENCES files (id);

ALTER TABLE oao_content
ADD CONSTRAINT deep_dive_id_fk FOREIGN KEY (deep_dive_id) REFERENCES deep_dives (id),
ADD CONSTRAINT thumbnail_id_fk FOREIGN KEY (thumbnail_id) REFERENCES files (id);

ALTER TABLE oao_content_views
ADD CONSTRAINT oao_content_id_fk FOREIGN KEY (oao_content_id) REFERENCES oao_content (id),
ADD CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id);

ALTER TABLE organizations
ADD CONSTRAINT logo_id_fk FOREIGN KEY (logo_id) REFERENCES files (id);

ALTER TABLE outcomes
ADD CONSTRAINT oao_content_id_fk FOREIGN KEY (oao_content_id) REFERENCES oao_content (id);

ALTER TABLE participation_modules
ADD CONSTRAINT module_id_fk FOREIGN KEY (module_id) REFERENCES modules (id),
ADD CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id);

ALTER TABLE report_goals
ADD CONSTRAINT manager_id_fk FOREIGN KEY (manager_id) REFERENCES employees (id),
ADD CONSTRAINT report_id_fk FOREIGN KEY (report_id) REFERENCES reports (id);

ALTER TABLE report_kpis
ADD CONSTRAINT report_id_fk FOREIGN KEY (report_id) REFERENCES reports (id);

ALTER TABLE report_participants
ADD CONSTRAINT report_id_fk FOREIGN KEY (report_id) REFERENCES reports (id),
ADD CONSTRAINT participation_id_fk FOREIGN KEY (participation_id) REFERENCES survey_campaign_employees (participation_id);

ALTER TABLE reports
ADD CONSTRAINT management_position_id_fk FOREIGN KEY (management_position_id) REFERENCES management_positions (id);

ALTER TABLE survey_campaign_employees
ADD CONSTRAINT employee_id_fk FOREIGN KEY (employee_id) REFERENCES employees (id),
ADD CONSTRAINT survey_campaign_id_fk FOREIGN KEY (survey_campaign_id) REFERENCES survey_campaigns (id);

ALTER TABLE survey_campaigns
ADD CONSTRAINT organization_id_fk FOREIGN KEY (organization_id) REFERENCES organizations (id);
