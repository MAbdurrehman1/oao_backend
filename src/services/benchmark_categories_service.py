from entity import BusinessUnitHierarchy
from repository import ManagementPositionRepository, BusinessUnitRepository


def get_benchmark_categories_hierarchy(position_id: int):
    unit_ids = ManagementPositionRepository.get_business_unit_ids_by_id(
        _id=position_id,
    )
    all_units_hierarchy = []
    for unit_id in unit_ids:
        hierarchy_business_units = BusinessUnitRepository.get_sub_units_hierarchy(
            business_unit_id=unit_id,
        )
        root_node = hierarchy_business_units.pop(0)
        result = BusinessUnitHierarchy(business_unit=root_node)
        result.add_children(result, children=hierarchy_business_units)
        all_units_hierarchy.append(result)
    return all_units_hierarchy
