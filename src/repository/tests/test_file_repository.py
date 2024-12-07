from entity import File
from repository import FileRepository
from repository.tests.helpers import create_some_file


def _assert_equal_file(file1: File, file2: File):
    assert file1.file_url == file2.file_url
    assert file1.name == file2.name
    assert file1.content_type == file2.content_type
    assert isinstance(file1.id, int)
    assert file1.id == file2.id
    assert file1.user_id == file2.user_id


def test_get_list_limit_offset(cleanup_database):
    total_count, all_files = FileRepository.get_list(offset=0, limit=10)
    assert isinstance(all_files, list)
    assert len(all_files) == 0
    assert total_count == 0

    files = []
    for i in range(0, 6):
        f = create_some_file(
            name=f"test{i+1}",
            user_email=f"test{i}@example.com",
        )
        files.append(f)

    total_count, all_files = FileRepository.get_list(offset=0, limit=10)
    assert len(all_files) == 6
    assert total_count == 6
    for i in range(0, 6):
        _assert_equal_file(all_files[i], files[5 - i])

    total_count, last_3 = FileRepository.get_list(offset=0, limit=3)
    assert len(last_3) == 3
    assert total_count == 6
    for i in range(0, 3):
        _assert_equal_file(last_3[i], files[5 - i])

    total_count, first_3 = FileRepository.get_list(offset=3, limit=3)
    assert len(first_3) == 3
    assert total_count == 6
    for i in range(0, 3):
        _assert_equal_file(first_3[i], files[2 - i])
