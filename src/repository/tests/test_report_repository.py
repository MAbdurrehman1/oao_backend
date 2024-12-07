from datetime import datetime, timedelta

from .helpers import (
    create_some_business_unit,
    create_some_employee,
    create_some_management_position,
    create_some_organization,
    create_some_report,
)
from repository import ReportRepository


def test_delete_report(cleanup_database, mock_post_request):
    org = create_some_organization()
    assert isinstance(org.id, int)
    bu = create_some_business_unit(organization_id=org.id, name="BU1")
    e1 = create_some_employee(
        email="test1@example.org", business_unit_id=bu.id, organization_id=org.id
    )
    assert isinstance(e1.id, int)
    assert isinstance(bu.id, int)
    mp = create_some_management_position(
        organization_id=org.id, role_ids=[bu.id], manager_ids=[e1.id]
    )
    assert isinstance(mp.id, int)
    report = create_some_report(
        title="test", position_id=mp.id, end_date=datetime.now() - timedelta(days=90)
    )
    assert isinstance(report.id, int)
    result = ReportRepository.exists(_id=report.id)
    assert result is True
    ReportRepository.delete(_id=report.id)
    result = ReportRepository.exists(_id=report.id)
    assert result is False
