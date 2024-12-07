import os
import random
import shutil
import tempfile
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from PIL import Image

from settings import ParticipationStatus, FocusArea, ReportStatus
from settings.connections import postgres_connection_manager, redis_connection_manager
from .test_queries import DELETE_ALL_TABLES
from entity.kpi_entity import KPI_MAPPING
from entity import (
    User,
    Organization,
    BusinessUnit,
    Employee,
    SurveyCampaign,
    ManagementPosition,
    Report,
    ReportGoal,
    InnovationIdea,
    ReportKPI,
    File,
    Module,
    ContentSummary,
    ModuleSchedule,
    DeepDive,
    InformationLibrary,
    OAOContent,
    Outcome,
    LibraryContent,
    InnovationIdeaRate,
)
from ..module_schedule_repository import ModuleScheduleRepository
from ..file_repository import FileRepository
from ..report_repository import ReportRepository
from ..report_goal_repository import ReportGoalRepository
from ..magic_link_repository import MagicLinkRepository
from ..management_position_repository import ManagementPositionRepository
from ..employee_repository import EmployeeRepository
from ..user_repository import UserRepository
from ..organization_repositoy import OrganizationRepository
from ..business_unit_repository import BusinessUnitRepository
from ..survey_campaign_repository import SurveyCampaignRepository
from ..participation_repository import ParticipationRepository
from ..innovation_idea_repository import InnovationIdeaRepository
from ..report_kpi_repository import ReportKPIRepository
from ..module_repository import ModuleRepository
from ..content_summary_repository import ContentSummaryRepository
from ..deep_dive_repository import DeepDiveRepository
from ..information_library_repository import InformationLibraryRepository
from ..oao_content_repository import OAOContentRepository
from ..outcome_repository import OutcomeRepository
from ..library_content_repository import LibraryContentRepository
from ..innovation_idea_rate_repository import InnovationIdeaRateRepository


def cleanup_database_fn():
    delete_all_tables_data_query = DELETE_ALL_TABLES
    postgres_connection_manager.execute_atomic_query(query=delete_all_tables_data_query)


def cleanup_redis_fn():
    redis_connection_manager._delete_all()


def create_some_user(
    email: str = "johndoe@example.com",
    password: str = "PASSWORD",
    first_name: str = "John",
    last_name: str = "Doe",
    is_admin: bool = False,
):
    user = User(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_admin=is_admin,
    )
    stored_user = UserRepository.store(user)
    return stored_user


def create_some_organization(
    company_name: str = "CompanyName",
    hq_location: str = "london-UK",
    size: str = "50-100",
    industry: str = "transportation",
    meta_data: dict | None = None,
    logo_id: int | None = None,
    logo_user_email: str = "test@example.ai",
    logo_name: str = "some_logo.png",
) -> Organization:
    if not logo_id:
        logo = create_some_file(user_email=logo_user_email, name=logo_name)
        logo_id = logo.id
    organization = Organization(
        company_name=company_name,
        hq_location=hq_location,
        size=size,
        industry=industry,
        meta_data=meta_data,
        logo_id=logo_id,
    )
    result = OrganizationRepository.store(organization)
    return result


def create_some_business_unit(
    organization_id: int,
    name: str = "test_bu",
    parent_id: int | None = None,
) -> BusinessUnit:
    business_unit = BusinessUnit(
        organization_id=organization_id,
        name=name,
        parent_id=parent_id,
    )
    result = BusinessUnitRepository.store(business_unit)
    return result


def create_some_employee(
    email: str = "johndoe@example.com",
    password: str = "PASSWORD",
    first_name: str = "John",
    last_name: str = "Doe",
    is_admin: bool = False,
    role_title: str = "Test Employee",
    organization_id: int | None = None,
    location: str = "Test Location",
    business_unit_id: int | None = None,
):
    if organization_id is None:
        organization = create_some_organization()
        organization_id = organization.id
    if business_unit_id is None:
        assert isinstance(organization_id, int)
        bu = create_some_business_unit(organization_id=organization_id)
        business_unit_id = bu.id
    user = User(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_admin=is_admin,
    )
    employee = Employee(
        user=user,
        organization_id=organization_id,
        role_title=role_title,
        location=location,
        business_unit_id=business_unit_id,
    )
    return EmployeeRepository.store(employee=employee)


def create_some_employee_survey_campaign(
    title: str = "Test Survey Campaign",
    start_date: datetime = datetime.now() + timedelta(days=2),
    end_date: datetime = datetime.now() + timedelta(days=10),
    organization_id: int | None = None,
    participant_ids: list[int] | None = None,
) -> SurveyCampaign:
    if not organization_id:
        organization = create_some_organization()
        employee = create_some_employee(organization_id=organization.id)
        organization_id = organization.id
        participant_ids = [employee.id]
    elif not participant_ids:
        employee = create_some_employee(organization_id=organization_id)
        participant_ids = [employee.id]

    campaign = SurveyCampaign(
        title=title,
        start_date=start_date,
        end_date=end_date,
        organization_id=organization_id,
        participant_ids=participant_ids,
    )
    retrieved_campaign = SurveyCampaignRepository.store(survey_campaign=campaign)
    return retrieved_campaign


def get_campaign_participant_ids(
    campaign_id: int, limit: int = 10, offset: int = 0
) -> list[UUID]:
    _, participants = ParticipationRepository.get_survey_campaign_participants(
        campaign_id=campaign_id,
        limit=limit,
        offset=offset,
    )
    return [p.id for p in participants]  # type: ignore


def change_participant_status(participant_id: UUID, status: ParticipationStatus):
    ParticipationRepository.update_status(_id=participant_id, status=status)


def get_participant_status(participant_id: UUID) -> ParticipationStatus:
    return ParticipationRepository.get_status(_id=participant_id)


def create_some_management_position(
    organization_id: int,
    name: str = "Test Position",
    role_ids: list[int] | None = None,
    manager_ids: list[int] | None = None,
) -> ManagementPosition:
    if role_ids is None:
        bu = create_some_business_unit(organization_id=organization_id)
        assert isinstance(bu.id, int)
        role_ids = [bu.id]
    if manager_ids is None:
        e = create_some_employee(organization_id=organization_id)
        manager_ids = [e.id]

    management_position = ManagementPosition(
        organization_id=organization_id,
        name=name,
        role_ids=role_ids,
        manager_ids=manager_ids,
    )
    stored_position = ManagementPositionRepository.store(management_position)
    for manager_id in manager_ids:
        ManagementPositionRepository.add_manager(
            manager_id=manager_id, position_id=stored_position.id  # type: ignore
        )
    return stored_position


def set_magic_link_token(email: str) -> UUID:
    token = uuid4()
    user = UserRepository.get_user_by_email(email=email)
    assert isinstance(user.id, int)
    MagicLinkRepository.set_magic_link(user_id=user.id, token=token)
    return token


def create_some_report(
    position_id: int,
    end_date: datetime = datetime.now() - timedelta(days=3),
    title: str = "Test Report",
    status: ReportStatus = ReportStatus.CREATED,
) -> Report:
    report = Report(
        management_position_id=position_id,
        title=title,
        end_date=end_date,
        status=status,
    )
    stored_report = ReportRepository.store(report)
    return stored_report


def create_some_report_goal(
    report_id: int,
    manager_id: int,
    title: str = "Test Title",
    description: str = "Test Description",
    focus_area: FocusArea = FocusArea.readiness,
) -> ReportGoal:
    goal = ReportGoal(
        report_id=report_id,
        title=title,
        manager_id=manager_id,
        description=description,
        focus_area=focus_area,
    )
    stored_goal = ReportGoalRepository.store(goal)
    return stored_goal


def create_some_innovation_idea(
    participation_id: UUID,
    title: str = "Test Title",
    description: str = "Test Description",
    feasibility_score: int = 1,
    confidence_score: int = 2,
    impact_score: int = 3,
) -> InnovationIdea:
    idea = InnovationIdea(
        title=title,
        description=description,
        feasibility_score=feasibility_score,
        confidence_score=confidence_score,
        impact_score=impact_score,
        participation_id=participation_id,
    )
    stored_idea = InnovationIdeaRepository.store(innovation_idea=idea)
    return stored_idea


def add_participants_to_report(report_id: int, participation_ids: list[UUID]):
    ReportRepository.store_report_participation_ids(
        report_id=report_id, participation_ids=participation_ids
    )


def create_some_kpis(report_id: int):
    kpis = []
    for kpi in KPI_MAPPING.values():
        k = ReportKPI(
            name=kpi.name,
            score=random.randint(0, 90),
            standard_deviation=random.randint(0, 40),
            report_id=report_id,
        )
        kpis.append(k)
    ReportKPIRepository.store(report_kpis=kpis)


def rate_idea(idea_id: int, manager_id: int, rate: int):
    InnovationIdeaRateRepository.store(
        InnovationIdeaRate(innovation_idea_id=idea_id, manager_id=manager_id, rate=rate)
    )


def delete_directory(directory_path):
    if os.path.isdir(directory_path):
        shutil.rmtree(directory_path)


def get_temp_image() -> bytes:
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    image = Image.new("RGB", (100, 100), color="blue")
    image.save(tmp_file, format="PNG")
    tmp_file.seek(0)
    return tmp_file.file.read()


def create_some_file(
    name: str = "some_file_name.png",
    content: bytes = get_temp_image(),
    content_type: str = "image/png",
    user_id: int | None = None,
    user_email: str = "johndoe@example.com",
) -> File:
    if not user_id:
        user = create_some_user(email=user_email)
        user_id = user.id
    file = File(
        name=name,
        file_content=content,
        user_id=user_id,
        content_type=content_type,
    )
    stored_file = FileRepository.store(file=file)
    return stored_file


def create_some_module(
    still_thumbnail_id: int,
    animated_thumbnail_id: int,
    title: str = "Test Title",
    description: str = "Test Description",
    duration: int = 10,
    order: int = 0,
    url: str = "https://example.com",
) -> Module:
    module = Module(
        title=title,
        description=description,
        duration=duration,
        order=order,
        url=url,
        still_thumbnail_id=still_thumbnail_id,
        animated_thumbnail_id=animated_thumbnail_id,
    )
    stored_module = ModuleRepository.store(module=module)
    return stored_module


def create_some_module_response(
    participation_id: UUID,
    module_id: int,
    updated_at: datetime | None = None,
):
    ModuleRepository.store_module_answer(
        participation_id=participation_id,
        module_id=module_id,
    )
    last_order = ModuleRepository.get_last_answered_module_order(
        participation_id=participation_id,
    )
    ModuleRepository.update_last_order(
        participation_id=participation_id,
        last_answered_module_order=last_order,
    )
    if updated_at:
        ModuleRepository.update_module_answer_updated_at(
            participation_id=participation_id,
            module_id=module_id,
            updated_at=updated_at,
        )


def create_some_content_summary(
    module_id: int,
    title: str = "Test Title",
    description: str = "Some Description",
):
    content_summary = ContentSummary(
        title=title,
        description=description,
        module_id=module_id,
    )
    stored_content_summary = ContentSummaryRepository.store(
        content_summary=content_summary,
    )
    return stored_content_summary


def create_some_module_schedule(
    module_id: int,
    participation_id: UUID,
    selected_date: datetime = datetime.now() + timedelta(days=1),
) -> ModuleSchedule:
    module_schedule = ModuleSchedule(
        participation_id=participation_id,
        module_id=module_id,
        selected_date=selected_date,
    )
    stored_module_schedule = ModuleScheduleRepository.store(
        module_schedule=module_schedule
    )
    return stored_module_schedule


def create_some_deep_dive(
    title: str = "Test Title",
    description: str = "Some Description",
    slug: str | None = None,
    thumbnail_id: int | None = None,
    file_user_id: int | None = None,
    file_name: str = "some_file_name.png",
) -> DeepDive:
    if not thumbnail_id:
        if not file_user_id:
            user = create_some_user()
            file_user_id = user.id
        thumbnail = create_some_file(
            user_id=file_user_id,
            name=file_name,
        )
        thumbnail_id = thumbnail.id
    deep_dive = DeepDive(
        title=title,
        slug=slug,
        description=description,
        thumbnail_id=thumbnail_id,
    )
    stored_deep_dive = DeepDiveRepository.store(deep_dive=deep_dive)
    return stored_deep_dive


def store_deep_dive_strategy(
    participation_id: UUID,
    slug_list: list[str],
):
    DeepDiveRepository.store_deep_dive_strategy(
        slug_list=slug_list,
        participation_id=participation_id,
    )


def create_some_information_library(
    deep_dive_id: int,
    organization_id: int | None = None,
    title: str = "Test Title",
    short_description: str = "Test Short Description",
    long_description: str = "Test Long Description",
) -> InformationLibrary:
    information_library = InformationLibrary(
        title=title,
        short_description=short_description,
        long_description=long_description,
        organization_id=organization_id,
        deep_dive_id=deep_dive_id,
    )
    stored_library = InformationLibraryRepository.store(
        information_library=information_library
    )
    return stored_library


def create_some_oao_content(
    thumbnail_id: int,
    deep_dive_id: int,
    title: str = "Test Title",
    short_description: str = "Test Short Description",
    long_description: str = "Test Long Description",
    content_url: str = "http://example.com",
) -> OAOContent:
    oao_content = OAOContent(
        title=title,
        short_description=short_description,
        long_description=long_description,
        content_url=content_url,
        deep_dive_id=deep_dive_id,
        thumbnail_id=thumbnail_id,
    )

    stored_oao_content = OAOContentRepository.store(oao_content=oao_content)
    return stored_oao_content


def create_some_outcome(
    oao_content_id: int,
    title: str = "Test Title",
    description: str = "Test Description",
) -> Outcome:
    outcome = Outcome(
        title=title,
        description=description,
        oao_content_id=oao_content_id,
    )
    stored_outcome = OutcomeRepository.store(outcome=outcome)
    return stored_outcome


def create_some_library_content(
    library_id: int,
    thumbnail_id: int,
    title: str = "Test Title",
    description: str = "Test Description",
    content_url: str = "https://example.com/content/",
) -> LibraryContent:
    library_content = LibraryContent(
        title=title,
        description=description,
        content_url=content_url,
        thumbnail_id=thumbnail_id,
        information_library_id=library_id,
    )
    stored_library_content = LibraryContentRepository.store(
        library_content=library_content
    )
    return stored_library_content


def create_some_oao_content_view(content_id: int, participation_id: UUID):
    OAOContentRepository.upsert_oao_content_view(
        content_id=content_id, participation_id=participation_id
    )


def get_preferred_lang(employee_id: int) -> str:
    return EmployeeRepository.get_preferred_lang(employee_id)


def publish_report(report_id: int):
    ReportRepository.update_status(_id=report_id, status=ReportStatus.PUBLISHED)


def update_module_answer_updated_at(
    module_id: int,
    participation_id: UUID,
    updated_at: datetime,
):
    ModuleRepository.update_module_answer_updated_at(
        module_id=module_id,
        participation_id=participation_id,
        updated_at=updated_at,
    )
