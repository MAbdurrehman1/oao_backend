from typing import Type

from entity import ReportKPI, BusinessUnit
from entity.kpi_entity import AbstractKPI
from repository.queries import (
    STORE_REPORT_KPIS,
    GET_KPI_VALUES,
    GET_REPORT_BENCHMARKS_LIST,
)
from settings.connections import postgres_connection_manager


def _enrich_kpi(data: dict) -> ReportKPI:
    return ReportKPI(
        id=data["id"],
        name=data["name"],
        report_id=data["report_id"],
        score=data["score"],
        standard_deviation=data["standard_deviation"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


def _enrich_benchmark(data: dict) -> BusinessUnit:
    return BusinessUnit(
        name=data["name"],
        id=data["id"],
    )


class ReportKPIRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def store(
        cls,
        report_kpis: list[ReportKPI],
    ) -> None:
        kpi_data = [
            (
                kpi.name,
                kpi.report_id,
                kpi.score,
                kpi.standard_deviation,
                kpi.business_unit_id,
            )
            for kpi in report_kpis
        ]
        cls.connection_manager.execute_values_atomic_query(
            query=STORE_REPORT_KPIS,
            variables=kpi_data,
            fetch=False,
        )

    @classmethod
    def get_kpi_values(
        cls, kpis: list[Type[AbstractKPI]], report_id: int, benchmark_id: int | None
    ) -> list[ReportKPI]:
        kpi_names = tuple([kpi.name for kpi in kpis])
        if not kpi_names:
            return []
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_KPI_VALUES,
            variables=(kpi_names, report_id, benchmark_id),
        )
        if not result:
            return []
        return [_enrich_kpi(kpi_data) for kpi_data in result]

    @classmethod
    def get_benchmarks_list(cls, report_id: int) -> list[BusinessUnit]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=GET_REPORT_BENCHMARKS_LIST,
            variables=(report_id,),
        )
        if not result:
            return []
        return [_enrich_benchmark(data) for data in result]
