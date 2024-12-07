from .health_check import health_check
from .user import (
    user_register_endpoint,
    user_login_endpoint,
    refresh_token_endpoint,
    send_magic_link_endpoint,
    login_with_magic_link_endpoint,
)
from .employee import upload_contacts_list_endpoint, get_auth_employee_data_endpoint
from .organization import (
    get_organizations_list_endpoint,
    create_organization_endpoint,
)
from .business_unit import get_business_unit_tree_endpoint
from .survey_campaign import (
    create_survey_campaign_endpoint,
    update_survey_campaign_endpoint,
    get_survey_campaign_endpoint,
    get_organization_survey_campaigns_endpoint,
)
from .participation import (
    get_survey_campaign_participants_endpoint,
    add_survey_campaign_participant_endpoint,
    update_survey_campaign_participant_status_endpoint,
)
from .management_position import (
    get_management_positions_list_endpoint,
    get_management_position_details_endpoint,
    create_management_position_endpoint,
    update_management_position_details_endpoint,
    add_manager_to_management_position_endpoint,
    remove_manager_from_management_position_endpoint,
)
from .report import (
    get_report_responded_participant_ids_endpoint,
    create_report,
)
from .manager import get_manager_reports_list_endpoint
from .report_goal import (
    create_report_goal_endpoint,
    get_report_goals_endpoint,
)
from .innovation_idea import (
    create_innovation_idea_endpoint,
    get_innovation_idea_endpoint,
    get_report_innovation_ideas_list_endpoint,
    rate_innovation_idea_endpoint,
    get_employee_innovation_idea_endpoint,
    get_report_matrix_innovation_ideas_list_endpoint,
)
from .report_kpi import create_report_kpis_endpoint, get_report_kpis_endpoint
from .executive_summary import get_executive_summary_endpoint
from .file import upload_endpoint
from .module import (
    get_modules_list_endpoint,
    get_modules_urls_endpoint,
    create_module_answer_endpoint,
)
from .content_summary import get_content_summary_list_endpoint
from .module_schedule import (
    upsert_module_schedule_endpoint,
    get_module_schedule_list_endpoint,
)
from .deep_dive import get_deep_dive_list_endpoint
from .information_library import get_information_library_list_endpoint
from .oao_content import (
    get_deep_dive_oao_content_list_endpoint,
    view_oao_content_endpoint,
    get_participant_viewed_oao_content_ids_list_endpoint,
)
from .outcomes import get_oao_content_outcome_list_endpoint
from .library_content import get_library_content_list_endpoint
from .toolkit import (
    run_task_endpoint,
)
from .preferred_lang import submit_preferred_lang_endpoint
from .benchmark import (
    store_report_benchmarks_kpi_endpoint,
    get_benchmark_categories_endpoint,
    get_benchmarks_list_endpoint,
)
