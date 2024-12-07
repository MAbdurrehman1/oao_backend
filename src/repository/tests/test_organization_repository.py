from entity import Organization
from repository import OrganizationRepository
from repository.tests.helpers import create_some_organization, create_some_file


def _assert_equal_organization(org1: Organization, org2: Organization):
    assert org1.company_name == org2.company_name
    assert org1.industry == org2.industry
    assert org1.hq_location == org2.hq_location
    assert org1.size == org2.size
    assert isinstance(org1.id, int)
    assert org1.id == org2.id
    assert org1.logo_id == org2.logo_id


def test_store_round_trip(cleanup_database):
    logo = create_some_file()
    organization = Organization(
        company_name="Test Company",
        industry="Test Industry",
        hq_location="Test Location",
        size="Test Size",
        logo_id=logo.id,
    )
    result_org = OrganizationRepository.store(organization)
    assert isinstance(result_org.id, int)
    retrieved_org = OrganizationRepository.get_by_id(result_org.id)
    _assert_equal_organization(retrieved_org, result_org)


def test_get_list_limit_offset(cleanup_database):
    total_count, all_orgs = OrganizationRepository.get_list(offset=0, limit=10)
    assert isinstance(all_orgs, list)
    assert len(all_orgs) == 0
    assert total_count == 0

    for i in range(0, 6):
        create_some_organization(
            company_name=f"test{i+1}",
            logo_user_email=f"test{i}@example.com",
            logo_name=f"logo_{i}.png",
        )

    total_count, all_orgs = OrganizationRepository.get_list(offset=0, limit=10)
    assert len(all_orgs) == 6
    assert total_count == 6
    assert {org.company_name for org in all_orgs} == {f"test{i+1}" for i in range(0, 6)}

    total_count, last_3 = OrganizationRepository.get_list(offset=0, limit=3)
    assert len(last_3) == 3
    assert total_count == 6
    assert {org.company_name for org in last_3} == {"test6", "test5", "test4"}

    total_count, first_3 = OrganizationRepository.get_list(offset=3, limit=3)
    assert len(last_3) == 3
    assert total_count == 6
    assert {org.company_name for org in first_3} == {"test1", "test2", "test3"}
