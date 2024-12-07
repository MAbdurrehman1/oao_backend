from datetime import datetime, timedelta
from uuid import UUID

import requests
from starlette.status import HTTP_200_OK

from cexceptions import (
    LessThanOrEqualException,
    GreaterThanOrEqualException,
    NotFoundException,
    EmptyResultException,
)
from cexceptions import ExternalSourceException
from entity import Report
from repository import (
    ReportRepository,
    ManagementPositionRepository,
    BusinessUnitRepository,
    SurveyCampaignRepository,
    ParticipationRepository,
)
from .auth_service import create_access_token
from settings import ParticipationStatus, configs, ReportStatus
from utils.validation_helpers import string_to_date


def get_last_report_end_date(position_id: int) -> datetime:
    end_date = ReportRepository.get_last_report_end_date(position_id=position_id)
    if end_date is None:
        end_date = datetime.now() - timedelta(days=365 * 2)
    return end_date


def get_report_participant_ids_between(
    position_id: int,
    start_date: datetime,
    end_date: datetime,
    status_list: list[ParticipationStatus],
) -> list[UUID]:
    organization_id = ManagementPositionRepository.get_organization_id_by_id(
        _id=position_id
    )
    business_unit_ids = ManagementPositionRepository.get_business_unit_ids_by_id(
        _id=position_id
    )
    business_units_with_children_ids = BusinessUnitRepository.get_children_ids(
        _ids=business_unit_ids
    )
    survey_campaign_ids = SurveyCampaignRepository.get_survey_campaign_ids_between(
        start_date=start_date,
        end_date=end_date,
        organization_id=organization_id,
    )
    if not survey_campaign_ids:
        return []
    participant_ids = ParticipationRepository.get_survey_campaigns_participant_ids(
        survey_campaign_ids=survey_campaign_ids,
        status_list=status_list,
        business_unit_ids=business_units_with_children_ids,
    )
    return participant_ids


def get_report_responded_participant_ids(position_id: int) -> list[UUID]:
    last_report_end_date = get_last_report_end_date(position_id=position_id)
    participants_ids = get_report_participant_ids_between(
        start_date=last_report_end_date,
        end_date=datetime.now(),
        position_id=position_id,
        status_list=[
            ParticipationStatus.RESPONDED,
            ParticipationStatus.IDEA_SUBMITTED,
        ],
    )
    return participants_ids


def _trigger_report_process_in_etl(
    participant_ids: list[UUID],
    report_id: int,
    position_id: int,
) -> requests.Response:
    unit_ids = ManagementPositionRepository.get_business_unit_ids_by_id(
        _id=position_id,
    )
    unit_participation_data = (  # noqa: F841
        BusinessUnitRepository.get_sub_units_with_participation(
            business_unit_ids=unit_ids,
        )
    )
    unit_data: dict[int, list[UUID]] = {item[0]: [] for item in unit_participation_data}
    for item in unit_participation_data:
        unit_data[item[0]].append(item[1])
    benchmark_data = [
        {"business_unit_id": k, "participant_ids": v} for k, v in unit_data.items()
    ]
    participant_ids_str_list = [
        str(participant_id) for participant_id in participant_ids
    ]
    report_data = dict(
        report_id=report_id,
        participant_ids=participant_ids_str_list,
        benchmarks=benchmark_data,
    )
    etl_url = configs.etl_domain + configs.etl_report_creation_end_point
    token = create_access_token(identifier="Backend")
    response = requests.post(
        url=etl_url,
        data=report_data,
        headers=dict(Authorization=token),
    )
    return response


def create_report(
    position_id: int,
    title: str,
    start_date_str: str | None,
    end_date_str: str,
):
    if not ManagementPositionRepository.exists(_id=position_id):
        raise NotFoundException(
            entity="ManagementPosition",
            arg="ID",
            value=str(position_id),
        )
    min_start_date = get_last_report_end_date(position_id=position_id)
    start_date = (
        string_to_date(start_date_str, configs.date_time_format)
        if start_date_str
        else min_start_date
    )
    end_date = string_to_date(end_date_str, configs.date_time_format)
    if start_date < min_start_date:
        raise GreaterThanOrEqualException(
            first_entity="Start Date",
            second_entity=min_start_date.strftime(configs.date_time_format),
        )
    if end_date > datetime.now():
        raise LessThanOrEqualException(
            first_entity="End Date",
            second_entity="Current Time",
        )
    if start_date > end_date:
        raise LessThanOrEqualException(
            first_entity="Start Date",
            second_entity="End Date",
        )
    participant_ids = get_report_responded_participant_ids(position_id=position_id)
    if not participant_ids:
        raise EmptyResultException(
            first_entity="No Participations", second_entity="Selected period"
        )
    report = Report(
        title=title,
        end_date=end_date,
        management_position_id=position_id,
        status=ReportStatus.CREATED,
    )
    stored_report = ReportRepository.store(report=report)
    assert isinstance(stored_report.id, int)
    ReportRepository.store_report_participation_ids(
        report_id=stored_report.id, participation_ids=participant_ids
    )
    etl_response = _trigger_report_process_in_etl(
        participant_ids=participant_ids,
        report_id=stored_report.id,
        position_id=position_id,
    )
    if etl_response.status_code == HTTP_200_OK:
        return stored_report
    # delete the report if etl request was not successful
    ReportRepository.delete(_id=stored_report.id)
    raise ExternalSourceException(source="etl", source_error=etl_response.reason)


def get_organization_reports(
    offset: int, limit: int, organization_id: int
) -> tuple[int, list[Report]]:
    limit = 50 if limit > 50 else limit
    total_count, reports = ReportRepository.get_list_by_organization_id(
        organization_id=organization_id, offset=offset, limit=limit
    )
    return total_count, reports


def publish_report(_id: int) -> None:
    if not ReportRepository.exists(_id=_id):
        raise NotFoundException(
            entity="Report",
            arg="ID",
            value=str(_id),
        )
    ReportRepository.update_status(_id=_id, status=ReportStatus.PUBLISHED)
    return None
