from io import BytesIO

from fastapi.testclient import TestClient

from app import app
from entity import User
from repository.tests.helpers import create_some_user
from services.auth_service import create_access_token
from services.tests.helpers import (
    get_contacts_list_with_one_row_csv_text,
    string_to_byte_file,
)


class URLs:
    root = "/v1.0/"
    user_register = root + "user/register/"
    upload_contacts_list = root + "contacts/upload/"
    organization = root + "organizations/"
    survey_campaign = root + "survey-campaigns/"
    organization_survey_campaigns = root + "organizations/{id}/survey-campaigns/"
    survey_campaign_participants = root + "survey-campaigns/{id}/participants/"
    organization_business_units = root + "organizations/{id}/business-units/"
    organization_management_positions = (
        root + "organizations/{id}/management-positions/"
    )
    management_position_report_participants = (
        root + "management-position/{id}/report-participants/"
    )
    magic_link = root + "m-link/"
    magic_link_login = root + "m-link/login/"
    manager_reports = root + "manager/{id}/reports/"
    report_goals = root + "reports/{id}/goals/"
    participant_ideas = root + "participants/{p_id}/ideas/"
    innovation_ideas = root + "innovation-ideas/"
    report_ideas = root + "report/{id}/ideas/"
    report_kpis = root + "report/{id}/kpis/"
    report = root + "reports/"
    auth_employee = root + "auth/employee/"
    executive_summary = root + "reports/{_id}/executive_summary/"
    rate_idea = root + "ideas/{_id}/rate/"
    upload = root + "upload/"
    module = root + "modules/"
    module_url = root + "modules/urls/"
    module_answer = root + "modules/{id}/answer/"
    content_summary = root + "modules/{id}/content-summaries/"
    module_schedule = root + "modules/{id}/schedules/"
    module_schedule_list = root + "module-schedules/"
    deep_dive = root + "deep_dives/"
    information_library = root + "deep_dives/{id}/libraries/"
    oao_content = root + "deep_dives/{id}/oao_content/"
    oao_content_view = root + "oao_content/{id}/views/"
    oao_content_view_list = root + "oao_content/views/"
    oao_content_outcome = root + "oao_content/{id}/outcomes/"
    library_content = root + "libraries/{id}/content/"
    employee_idea = root + "employee/idea/"
    organization_business_unit_update = (
        root + "organizations/{o_id}/business-units/{bu_id}/"
    )
    files = root + "files/"
    organization_reports = root + "organizations/{id}/reports/"
    preferred_lang = root + "preferred-lang/"
    publish_report = root + "reports/{id}/publish/"
    report_ideas_matrix = root + "report/{id}/ideas-matrix/"
    benchmark_categories = root + "management-position/{id}/benchmark-categories/"
    update_management_position = (
        root + "organizations/{organization_id}/management-positions/{position_id}/"
    )
    management_position_add_manager = (
        root
        + "organizations/{organization_id}/"
        + "management-positions/{position_id}/add-manager/"
    )
    management_position_remove_manager = (
        root
        + "organizations/{organization_id}/"
        + "management-positions/{position_id}/remove-manager/"
    )
    benchmarks = root + "reports/{id}/benchmarks/"


test_client = TestClient(app)


def get_access_token(user: User) -> str:
    access_token = create_access_token(identifier=user.email)
    return f"Bearer {access_token}"


def get_admin_token() -> str:
    admin_user = create_some_user(is_admin=True)
    token = get_access_token(admin_user)
    return token


def get_etl_token() -> str:
    access_token = create_access_token(identifier="ETL")
    return f"Bearer {access_token}"


def string_to_file_tuple(file_str: str) -> tuple[str, BytesIO, str]:
    file = string_to_byte_file(file_str=file_str)
    return "contacts.csv", file, "text/csv"


def get_contacts_list_with_one_row_file(business_units_id: int):
    return string_to_file_tuple(
        get_contacts_list_with_one_row_csv_text(business_units_id)
    )
