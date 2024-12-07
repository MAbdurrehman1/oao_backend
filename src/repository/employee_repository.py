from copy import deepcopy
from datetime import datetime

from entity import Employee
from settings import PreferredLang
from settings.connections import postgres_connection_manager
from .queries import (
    UPSERT_USER,
    CREATE_EMPLOYEE,
    CHECK_EMPLOYEE_EMAILS_EXIST,
    CHECK_EMPLOYEE_IS_IN_CAMPAIGN_ORGANIZATION,
    GET_EMPLOYEE_ID_BY_EMAIL,
    CHECK_USER_IS_EMPLOYEE_BY_ID,
    GET_EMPLOYEE_BY_USER_ID,
    GET_EMPLOYEE_ID_BY_USER_ID,
    SUBMIT_PREFERRED_LANG,
    GET_PREFERRED_LANG,
)
from cexceptions import NotFoundException


def _enrich_employee(data: dict) -> Employee:
    return Employee(
        id=data["id"],
        role_title=data["role_title"],
        location=data["location"],
        organization_id=data["organization_id"],
    )


class EmployeeRepository:
    connection_manager = postgres_connection_manager

    @classmethod
    def store(cls, employee: Employee) -> Employee:
        with cls.connection_manager.open_cursor() as cursor:
            assert employee.user, "user must not be null in employee store"
            assert (
                employee.business_unit_id
            ), "business_unit_id must not be null in employee store"
            cursor.execute(
                UPSERT_USER,
                (
                    employee.user.first_name,
                    employee.user.last_name,
                    employee.user.email.lower(),
                    employee.user.password,
                    employee.user.is_admin,
                ),
            )
            employee.user.id = employee.user_id = cursor.fetchone()["id"]
            cursor.execute(
                CREATE_EMPLOYEE,
                (
                    employee.user_id,
                    employee.role_title,
                    employee.organization_id,
                    employee.location,
                    employee.business_unit_id,
                ),
            )
            e_result = cursor.fetchone()
            returned_employee = deepcopy(employee)
            returned_employee.id = e_result["id"]
            returned_employee.created_at = e_result["created_at"]
            returned_employee.updated_at = e_result["updated_at"]
            return returned_employee

    @classmethod
    def get_exiting_ids_by_email(
        cls, emails: list[str], organization_id: int
    ) -> dict[str, int]:
        result = cls.connection_manager.execute_atomic_query_all(
            query=CHECK_EMPLOYEE_EMAILS_EXIST,
            variables=(tuple(set(emails)), organization_id),
        )
        retrieved_emails = {item["email"]: int(item["id"]) for item in result}
        return retrieved_emails

    @classmethod
    def check_employee_exists_in_organization(
        cls, employee_id: int, organization_id: int
    ) -> Employee:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_EMPLOYEE_IS_IN_CAMPAIGN_ORGANIZATION,
            variables=(employee_id, organization_id),
        )
        return result["exists"]

    @classmethod
    def get_id_by_email(cls, email: str) -> int:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_EMPLOYEE_ID_BY_EMAIL,
            variables=(email,),
        )
        if not result:
            raise NotFoundException(entity="Employee", arg="Email", value=email)
        return result["id"]

    @classmethod
    def check_user_is_employee(cls, user_id: int) -> bool:
        result = cls.connection_manager.execute_atomic_query(
            query=CHECK_USER_IS_EMPLOYEE_BY_ID,
            variables=(user_id,),
        )
        return result["exists"]

    @classmethod
    def get_by_user_id(cls, user_id: int) -> Employee:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_EMPLOYEE_BY_USER_ID,
            variables=(user_id,),
        )
        if not result:
            raise NotFoundException(entity="Employee", arg="UserID", value=str(user_id))

        return _enrich_employee(data=result)

    @classmethod
    def get_employee_id_by_user_id(cls, user_id: int) -> int:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_EMPLOYEE_ID_BY_USER_ID,
            variables=(user_id,),
        )
        if not result:
            raise NotFoundException(
                entity="Employee", arg="User ID", value=str(user_id)
            )
        return result["id"]

    @classmethod
    def submit_preferred_lang(
        cls,
        employee_id: int,
        preferred_lang: PreferredLang,
    ):
        updated_at = datetime.now()
        cls.connection_manager.execute_atomic_query(
            query=SUBMIT_PREFERRED_LANG,
            variables=(
                preferred_lang.value,
                updated_at,
                employee_id,
            ),
        )

    @classmethod
    def get_preferred_lang(cls, employee_id: int) -> PreferredLang:
        result = cls.connection_manager.execute_atomic_query(
            query=GET_PREFERRED_LANG,
            variables=(employee_id,),
        )
        if not result:
            raise NotFoundException(
                entity="Employee",
                arg="ID",
                value=str(employee_id),
            )
        try:
            return PreferredLang(result["preferred_lang"])
        except Exception:
            return PreferredLang.english
