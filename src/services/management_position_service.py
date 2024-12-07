from datetime import datetime

from cexceptions import NotFoundException, DoesNotBelongException
from entity import ManagementPosition
from repository import (
    ManagementPositionRepository,
    OrganizationRepository,
    BusinessUnitRepository,
    EmployeeRepository,
)
from settings import ParticipationStatus
from .report_service import get_report_participant_ids_between, get_last_report_end_date


def _check_management_position_exists(_id: int):
    if not ManagementPositionRepository.exists(_id=_id):
        raise NotFoundException(entity="ManagementPosition", arg="ID", value=str(_id))


def _check_employee_exists_in_organization(employee_id: int, organization_id: int):
    if not EmployeeRepository.check_employee_exists_in_organization(
        employee_id=employee_id, organization_id=organization_id
    ):
        raise NotFoundException(
            entity="Employee",
            arg="ID",
            value=str(employee_id),
        )


def _check_management_position_belongs_to_organization(
    position_id: int, organization_id: int
):
    if not ManagementPositionRepository.check_belongs_to_organization(
        position_id=position_id, organization_id=organization_id
    ):
        raise DoesNotBelongException(
            first_entity="Management Position",
            first_value=str(position_id),
            second_entity="Organization",
            second_value=str(organization_id),
        )


def _enrich_pending_participation_data(
    management_position: ManagementPosition,
) -> ManagementPosition:
    assert isinstance(management_position.id, int)
    position_id = management_position.id
    last_report_end_date = get_last_report_end_date(position_id=position_id)
    pending_participants_count = len(
        get_report_participant_ids_between(
            position_id=position_id,
            start_date=last_report_end_date,
            end_date=datetime.now(),
            status_list=[
                ParticipationStatus.RESPONDED,
                ParticipationStatus.IDEA_SUBMITTED,
            ],
        )
    )
    management_position.pending_participants_count = pending_participants_count
    management_position.last_report_end_date = last_report_end_date
    return management_position


def create_management_position(
    organization_id: int, name: str, business_unit_ids: list[int]
) -> None:
    if not OrganizationRepository.exists(organization_id=organization_id):
        raise NotFoundException(
            entity="Organization", arg="ID", value=str(organization_id)
        )
    for bu_id in business_unit_ids:
        if not BusinessUnitRepository.exists(
            _id=bu_id, organization_id=organization_id
        ):
            raise DoesNotBelongException(
                first_entity="Business Unit ID",
                first_value=str(bu_id),
                second_entity="Organization ID",
                second_value=str(organization_id),
            )

    management_position = ManagementPosition(
        organization_id=organization_id, name=name, role_ids=business_unit_ids
    )
    ManagementPositionRepository.store(management_position=management_position)


def update_management_position_details(position_id: int, name: str):
    if not ManagementPositionRepository.exists(
        _id=position_id,
    ):
        raise NotFoundException(
            entity="Management Position", arg="ID", value=str(position_id)
        )
    ManagementPositionRepository.update(_id=position_id, name=name)


def add_manager_to_management_position(
    management_position_id: int, manager_email: str, organization_id: int
) -> None:
    manager_id = EmployeeRepository.get_id_by_email(email=manager_email)
    _check_management_position_exists(_id=management_position_id)
    _check_management_position_belongs_to_organization(
        organization_id=organization_id, position_id=management_position_id
    )
    _check_employee_exists_in_organization(
        employee_id=manager_id, organization_id=organization_id
    )
    if not ManagementPositionRepository.check_if_employee_is_in_management_position(
        manager_id=manager_id, position_id=management_position_id
    ):
        ManagementPositionRepository.add_manager(
            manager_id=manager_id, position_id=management_position_id
        )
    return


def remove_manager_from_management_position(
    management_position_id: int, manager_id: int, organization_id: int
) -> None:
    _check_management_position_exists(_id=management_position_id)
    _check_management_position_belongs_to_organization(
        organization_id=organization_id, position_id=management_position_id
    )
    _check_employee_exists_in_organization(
        employee_id=manager_id, organization_id=organization_id
    )
    if not ManagementPositionRepository.check_if_employee_is_in_management_position(
        manager_id=manager_id, position_id=management_position_id
    ):
        raise DoesNotBelongException(
            first_entity="Manager",
            first_value=str(manager_id),
            second_entity="Management Position",
            second_value=str(organization_id),
        )
    ManagementPositionRepository.remove_manager(
        manager_id=manager_id, position_id=management_position_id
    )
    return


def get_management_position_list(
    organization_id: int, offset: int, limit: int
) -> tuple[int, list[ManagementPosition]]:
    total_count, management_positions = ManagementPositionRepository.get_list(
        organization_id=organization_id,
        offset=offset,
        limit=limit,
    )
    enriched_management_positions = [
        _enrich_pending_participation_data(mp) for mp in management_positions
    ]
    return total_count, enriched_management_positions


def get_management_position_details(position_id: int) -> ManagementPosition:
    management_position = ManagementPositionRepository.get(
        _id=position_id,
    )
    return _enrich_pending_participation_data(management_position)
