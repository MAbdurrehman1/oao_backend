from io import BytesIO
from uuid import UUID

import pandas as pd

from repository import SurveyCampaignRepository


def tribble(columns: list[str], *data) -> pd.DataFrame:
    """https://stackoverflow.com/a/54368508/5730291"""
    return pd.DataFrame(
        data=list(zip(*[iter(data)] * len(columns))),
        columns=columns,
    )


def string_to_byte_file(file_str: str) -> BytesIO:
    file = BytesIO(file_str.encode("utf-8"))
    return file


def _join_csv_rows(rows: list[str]) -> str:
    return "\n".join(rows)


def _get_import_contacts_list_csv_headers() -> str:
    return "first_name,last_name,email,role_title,location,business_unit"


def _get_import_contacts_list_csv_1_row(business_units_id: int) -> str:
    business_units_str = f"{business_units_id}-test-business-units"
    return f"John,Doe,JohnDoe@example.com,CTO,london-UK,{business_units_str}"


def get_contacts_list_with_one_row_csv_text(business_units_id: int):
    return _join_csv_rows(
        [
            _get_import_contacts_list_csv_headers(),
            _get_import_contacts_list_csv_1_row(business_units_id),
        ]
    )


def get_contacts_list_with_one_row_csv_bytes(business_units_id: int):
    return string_to_byte_file(
        get_contacts_list_with_one_row_csv_text(business_units_id)
    )


def get_campaign_participant_ids(campaign_id: int) -> list[UUID]:
    result = SurveyCampaignRepository.get_participants_data(campaign_id)
    return [UUID(_id) for _id in result.keys()]
