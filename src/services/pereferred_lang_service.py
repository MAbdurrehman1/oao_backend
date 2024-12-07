from cexceptions import ValidationException
from repository import EmployeeRepository
from settings import PreferredLang


def submit_preferred_lang(
    user_id: int,
    lang: str,
) -> None:
    employee_id = EmployeeRepository.get_employee_id_by_user_id(
        user_id=user_id,
    )
    try:
        preferred_lang = PreferredLang(lang)
    except Exception:
        raise ValidationException(
            entities="Preferred Lang",
            values=lang,
        )
    EmployeeRepository.submit_preferred_lang(
        employee_id=employee_id,
        preferred_lang=preferred_lang,
    )
