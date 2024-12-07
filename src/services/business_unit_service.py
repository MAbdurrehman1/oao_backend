from cexceptions import (
    NotFoundException,
    DoesNotBelongException,
    ValidationException,
    UniquePerEntityException,
)
from entity import BusinessUnit, BusinessUnitHierarchy
from repository import BusinessUnitRepository, OrganizationRepository


def get_business_units_tree(organization_id: int) -> BusinessUnitHierarchy | None:
    business_units = BusinessUnitRepository.get_hierarchy(
        organization_id=organization_id
    )
    if business_units:
        root_node = business_units.pop(0)
        result = BusinessUnitHierarchy(business_unit=root_node)
        result.add_children(result, children=business_units)
        return result
    else:
        return None


def _validate_business_unit_payload(organization_id: int, parent_id: int | None):
    if not OrganizationRepository.exists(organization_id=organization_id):
        raise NotFoundException(
            entity="Organization", arg="ID", value=str(organization_id)
        )
    if parent_id is not None:
        parent_business_unit_exists = BusinessUnitRepository.exists(
            parent_id, organization_id
        )
        if not parent_business_unit_exists:
            raise DoesNotBelongException(
                first_entity="Parent ID",
                first_value=str(parent_id),
                second_entity="Organization ID",
                second_value=str(organization_id),
            )


def create_business_unit(
    organization_id: int, name: str, parent_id: int | None
) -> BusinessUnit:
    _validate_business_unit_payload(
        organization_id=organization_id, parent_id=parent_id
    )
    trying_to_create_root_business_unit = parent_id is None
    if (
        trying_to_create_root_business_unit
        and BusinessUnitRepository.organization_root_business_unit_exists(
            organization_id=organization_id
        )
    ):
        # there's already a root business_unit.
        raise UniquePerEntityException(
            first_entity="Organization business_unit", second_entity="null parent_id"
        )
    business_unit = BusinessUnitRepository.store(
        BusinessUnit(organization_id=organization_id, name=name, parent_id=parent_id)
    )
    return business_unit


def update_business_unit(
    organization_id: int, _id: int, name: str, parent_id: int | None
) -> BusinessUnit:
    _validate_business_unit_payload(
        organization_id=organization_id, parent_id=parent_id
    )
    # throw if the business_unit is not found in the db
    if not BusinessUnitRepository.exists(_id=_id, organization_id=organization_id):
        raise NotFoundException(entity="Business Unit", arg="ID", value=str(id))

    if parent_id is None:
        # check if this organization already has a root business_unit
        organization_root_business_unit_exists = (
            BusinessUnitRepository.organization_root_business_unit_exists(
                organization_id=organization_id
            )
        )
        business_unit = BusinessUnitRepository.get_by_id(_id=_id)
        # throw if the updating business_unit is not the root business_unit
        if (
            organization_root_business_unit_exists
            and business_unit.parent_id is not None
        ):
            raise UniquePerEntityException(
                first_entity="Organization business_unit",
                second_entity="null parent_id",
            )
    # validations for when parent_id is not None
    else:
        # passed parent_id same as _id
        if _id == parent_id:
            raise ValidationException(entities="Parent Id", values="Instance Id")
        # passed parent_id as one of the children ids
        children_ids = BusinessUnitRepository.get_children_ids([_id])
        if parent_id in children_ids:
            raise ValidationException(
                entities="Parent Id", values=f"Child Id: {parent_id}"
            )

    updated_business_unit = BusinessUnitRepository.update(
        business_unit=BusinessUnit(id=_id, name=name, parent_id=parent_id)
    )
    return updated_business_unit
