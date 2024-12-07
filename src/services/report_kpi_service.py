from copy import deepcopy
from typing import Type

from cexceptions import NotFoundException, ValidationException, DoesNotBelongException
from entity import ReportKPI, BusinessUnit
from entity.kpi_entity import (
    GeneralKPI,
    ValuedKPI,
    AbstractKPI,
    KPIEnum,
    KPI_MAPPING,
    PARENT_KPI_SET,
)
from repository import ReportRepository, ReportKPIRepository, BusinessUnitRepository
from settings import ReportStatus


def _check_admin_report_exists(report_id: int):
    if not ReportRepository.exists(_id=report_id):
        raise NotFoundException(
            entity="Report",
            arg="ID",
            value=str(report_id),
        )


def _check_manager_report_exists(report_id: int):
    if not ReportRepository.is_published(_id=report_id):
        raise NotFoundException(
            entity="Report",
            arg="ID",
            value=str(report_id),
        )


def _get_all_children(
    kpi: Type[AbstractKPI],
) -> tuple[list[Type[AbstractKPI]], dict[str, dict]]:
    direct_children: list[Type[AbstractKPI]] = kpi.get_children()
    children: list[Type[AbstractKPI]] = deepcopy(direct_children)
    hierarchy: dict = {kpi.name: {} for kpi in children}
    if direct_children:
        for child in direct_children:
            g_children, g_hierarchy = _get_all_children(child)
            children.extend(g_children)
            hierarchy[child.name] = g_hierarchy
        return children, hierarchy
    else:
        return [], {}


def _get_kpi_set(
    parent_kpi: str | None,
) -> tuple[list[Type[AbstractKPI]], dict[str, dict]]:
    if parent_kpi:
        try:
            kpi_key = KPIEnum(parent_kpi)
        except Exception:
            raise ValidationException(
                entities="KPI",
                values="parent_kpi",
            )
        kpi = KPI_MAPPING[kpi_key.value]
        kpi_set, hierarchy = _get_all_children(kpi)
    else:
        kpi_set: list[Type[AbstractKPI]] = PARENT_KPI_SET  # type: ignore
        hierarchy = {}  # type: ignore
    return kpi_set, hierarchy


def _fetch_kpi_values(
    kpi_set: list[Type[AbstractKPI]], report_id: int, benchmark_id: int | None
):
    return ReportKPIRepository.get_kpi_values(
        kpis=kpi_set,
        report_id=report_id,
        benchmark_id=benchmark_id,
    )


def _enrich_kpis(
    data: dict, report_id: int, root_kpi: Type[AbstractKPI]
) -> list[ValuedKPI]:
    kpis = []
    kpi = root_kpi.get_valued_kpi(
        report_id=report_id,
        data=data,
    )
    kpis.append(kpi)
    children = root_kpi.get_children()
    if children:
        for child in children:
            child_kpis = _enrich_kpis(data=data, report_id=report_id, root_kpi=child)
            kpis.extend(child_kpis)
    return kpis


def create_report_kpis(report_id: int, kpi_data: dict) -> None:
    _check_admin_report_exists(report_id=report_id)
    valued_kpis = _enrich_kpis(report_id=report_id, data=kpi_data, root_kpi=GeneralKPI)
    report_kpis = [ReportKPI.from_valued_kpi(valued_kpi) for valued_kpi in valued_kpis]
    ReportKPIRepository.store(report_kpis=report_kpis)
    ReportRepository.update_status(_id=report_id, status=ReportStatus.READY)


def get_report_kpis(
    report_id: int, parent_kpi: str | None, is_admin: bool, benchmark_id: int | None
) -> tuple[list[ReportKPI], dict[str, dict]]:
    if is_admin:
        _check_admin_report_exists(report_id=report_id)
    else:
        _check_manager_report_exists(report_id=report_id)
    kpi_set, hierarchy = _get_kpi_set(parent_kpi=parent_kpi)
    return (
        _fetch_kpi_values(
            kpi_set=kpi_set, report_id=report_id, benchmark_id=benchmark_id
        ),
        hierarchy,
    )


def store_benchmark_kpis(report_id: int, benchmark_kpi_data: list[dict]):
    if not ReportRepository.exists(_id=report_id):
        raise NotFoundException(
            entity="Report",
            arg="ID",
            value=str(report_id),
        )
    organization_id = ReportRepository.get_organization_id(_id=report_id)
    unit_ids = []
    kpi_store_entities = []
    for kpi_data in benchmark_kpi_data:
        business_unit_id: int = int(kpi_data["business_unit_id"])
        valued_kpis = _enrich_kpis(
            report_id=report_id, data=kpi_data["kpi_data"], root_kpi=GeneralKPI
        )
        report_kpis = [
            ReportKPI.from_valued_kpi(
                valued_kpi=valued_kpi, business_unit_id=business_unit_id
            )
            for valued_kpi in valued_kpis
        ]
        unit_ids.append(business_unit_id)
        kpi_store_entities.extend(report_kpis)
    if not BusinessUnitRepository.check_belong_to_organization(
        organization_id=organization_id, unit_ids=unit_ids  # type: ignore
    ):
        raise DoesNotBelongException(
            first_entity="BusinessUnits",
            first_value=str(tuple(unit_ids)),
            second_entity="Organization ID",
            second_value=str(organization_id),
        )
    ReportKPIRepository.store(
        report_kpis=kpi_store_entities,
    )


def get_benchmarks_list(report_id: int) -> list[BusinessUnit]:
    if not ReportRepository.exists(_id=report_id):
        raise NotFoundException(
            entity="Report",
            arg="ID",
            value=str(report_id),
        )

    business_units = ReportKPIRepository.get_benchmarks_list(
        report_id=report_id,
    )
    return business_units
