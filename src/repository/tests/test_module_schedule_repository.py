from datetime import datetime, timedelta
from entity import ModuleSchedule, User, Module, Participant, Employee
from ..module_schedule_repository import ModuleScheduleRepository
from .helpers import (
    create_some_employee_survey_campaign,
    create_some_module,
    create_some_employee,
    create_some_organization,
    get_campaign_participant_ids,
    create_some_file,
)


def _assert_equal_module_schedule(module1: ModuleSchedule, module2: ModuleSchedule):
    assert module1.participation_id == module2.participation_id
    assert module1.module_id == module2.module_id
    assert module1.selected_date == module2.selected_date


def test_store_module_schedule(cleanup_database):
    file = create_some_file()
    assert isinstance(file.id, int)
    module = create_some_module(
        animated_thumbnail_id=file.id,
        still_thumbnail_id=file.id,
    )
    assert isinstance(module.id, int)
    org = create_some_organization(logo_id=file.id)
    e = create_some_employee(organization_id=org.id)
    assert isinstance(e.id, int)
    sc = create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e.id],
        start_date=datetime.now() - timedelta(days=2),
        end_date=datetime.now() + timedelta(days=5),
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(campaign_id=sc.id)[0]
    module_schedule = ModuleSchedule(
        selected_date=datetime.now(), module_id=module.id, participation_id=p_id
    )
    stored_module_schedule = ModuleScheduleRepository.store(
        module_schedule=module_schedule
    )
    assert stored_module_schedule.module_id == module_schedule.module_id
    assert stored_module_schedule.selected_date == module_schedule.selected_date
    assert stored_module_schedule.participation_id == module_schedule.participation_id
    assert stored_module_schedule.id
    assert stored_module_schedule.created_at
    assert stored_module_schedule.updated_at


def test_upsert_module_schedule(cleanup_database):
    file = create_some_file()
    assert isinstance(file.id, int)
    module = create_some_module(
        animated_thumbnail_id=file.id,
        still_thumbnail_id=file.id,
    )
    assert isinstance(module.id, int)
    org = create_some_organization(logo_id=file.id)
    e = create_some_employee(organization_id=org.id)
    assert isinstance(e.id, int)
    sc = create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e.id],
        start_date=datetime.now() - timedelta(days=2),
        end_date=datetime.now() + timedelta(days=5),
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(campaign_id=sc.id)[0]
    module_schedule = ModuleSchedule(
        selected_date=datetime.now(), module_id=module.id, participation_id=p_id
    )
    stored_module_schedule_1 = ModuleScheduleRepository.store(
        module_schedule=module_schedule
    )
    module_schedule_2 = ModuleSchedule(
        selected_date=datetime.today(), module_id=module.id, participation_id=p_id
    )
    stored_module_schedule_2 = ModuleScheduleRepository.store(
        module_schedule=module_schedule_2
    )
    assert stored_module_schedule_1.id == stored_module_schedule_2.id
    assert (
        stored_module_schedule_1.selected_date != stored_module_schedule_2.selected_date
    )


def test_get_module_schedule(cleanup_database):
    file = create_some_file()
    assert isinstance(file.id, int)
    module = create_some_module(
        animated_thumbnail_id=file.id,
        still_thumbnail_id=file.id,
    )
    assert isinstance(module.id, int)
    org = create_some_organization(logo_id=file.id)
    e = create_some_employee(organization_id=org.id)
    assert isinstance(e.user, User)
    assert isinstance(e.id, int)
    sc = create_some_employee_survey_campaign(
        organization_id=org.id,
        participant_ids=[e.id],
        start_date=datetime.now() - timedelta(days=2),
        end_date=datetime.now() + timedelta(days=5),
    )
    assert isinstance(sc.id, int)
    p_id = get_campaign_participant_ids(campaign_id=sc.id)[0]
    module_schedule = ModuleSchedule(
        selected_date=datetime.now(), module_id=module.id, participation_id=p_id
    )
    stored_module_schedule = ModuleScheduleRepository.store(
        module_schedule=module_schedule
    )
    assert isinstance(stored_module_schedule.id, int)
    module_schedule = ModuleScheduleRepository.get(_id=stored_module_schedule.id)
    assert isinstance(module_schedule.participant, Participant)
    assert isinstance(module_schedule.participant.employee, Employee)
    assert isinstance(module_schedule.participant.employee.user, User)
    assert isinstance(module_schedule.module, Module)
    assert module_schedule.participant.employee.user.email == e.user.email
    assert module_schedule.id == stored_module_schedule.id
    assert module_schedule.ms_graph_event_id is None
    assert module_schedule.participant.employee.user.first_name == e.user.first_name
    assert module_schedule.participant.employee.user.last_name == e.user.last_name
    assert module_schedule.selected_date == stored_module_schedule.selected_date
    assert module_schedule.module.id == module.id
    assert module_schedule.module.title == module.title
    assert module_schedule.module.description == module.description
    assert module_schedule.module.duration == module.duration
    assert module_schedule.module.order == module.order

    some_event_id = "some_event_id"
    ModuleScheduleRepository.store_event_id(
        _id=stored_module_schedule.id, event_id=some_event_id
    )
    module_schedule = ModuleScheduleRepository.get(_id=stored_module_schedule.id)
    assert module_schedule.ms_graph_event_id == some_event_id
