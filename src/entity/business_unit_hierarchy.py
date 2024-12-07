from copy import deepcopy
from typing import Self

from pydantic import BaseModel

from .business_unit import BusinessUnit


class BusinessUnitHierarchy(BaseModel):
    business_unit: BusinessUnit
    children: list[Self] | None = None

    @classmethod
    def add_children(
        cls, root_node: "BusinessUnitHierarchy", children: list[BusinessUnit]
    ) -> "BusinessUnitHierarchy":
        node_children = []
        for idx, child in enumerate(children):
            if child.parent_id == root_node.business_unit.id:
                child_children = deepcopy(children)
                child = child_children.pop(idx)
                child_with_children = cls.add_children(
                    BusinessUnitHierarchy(business_unit=child), children=child_children
                )
                node_children.append(child_with_children)
        root_node.children = node_children
        return root_node
