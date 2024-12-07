from io import BytesIO

from starlette.status import HTTP_200_OK

from repository.tests.helpers import get_temp_image
from rest.endpoints.tests.helpers import URLs, get_admin_token


def test_upload(cleanup_media, fast_client, cleanup_database):
    file = get_temp_image()
    upload_file = "name.png", BytesIO(file), "image/png"
    token = get_admin_token()
    response = fast_client.post(
        URLs.upload,
        files={"file": upload_file},
        headers=dict(Authorization=token),
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()["result"]
    assert list(data.keys()) == ["file_id"]
