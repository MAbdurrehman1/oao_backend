from dataclasses import dataclass

from fastapi import FastAPI
from starlette.testclient import TestClient
from utils.error_handler import (
    setup_exception_handlers,
)
from rest.error_handler import (
    ExceptionHandler,
)
import services.i18n  # noqa: F401 (register YAMLs & additional translate functions)
from cexceptions import AbstractException


def _assert_translate_is_correct(client, url, expected_translation):
    res_en = client.get(url, headers={"Accept-Language": "en"})
    assert res_en.json()["error"] == expected_translation.english

    res_de = client.get(url, headers={"Accept-Language": "de"})
    assert res_de.json()["error"] == expected_translation.german

    res_de = client.get(url)  # german is default language of responses
    assert res_de.json()["error"] == expected_translation.german


def test_translation_of_errors():
    @dataclass(kw_only=True)
    class CustomException(AbstractException):
        message: str = "a-translatable-error-message"

    @dataclass(kw_only=True)
    class CustomDynamicException(AbstractException):
        message: str = "these are test attributes: {test_attrs}"
        test_attrs: str

    app = FastAPI()
    setup_exception_handlers(
        app,
        handlers=[
            ExceptionHandler(exception=CustomException),
            ExceptionHandler(exception=CustomDynamicException),
        ],
    )

    @app.get(static_message_url := "/some-endpoint")
    def some_static_error_endpoint():
        raise CustomException()

    @app.get(dynamic_message_url := "/some-dynamic-endpoint")
    def some_dynamic_error_endpoint():
        raise CustomDynamicException(test_attrs="THIS ATTRIBUTE")

    client = TestClient(app)

    class ExpectedStaticMessage:
        english = "a-translatable-error-message"
        german = "a-translatable-error-message-in-german"

    _assert_translate_is_correct(
        client=client,
        url=static_message_url,
        expected_translation=ExpectedStaticMessage,
    )

    class ExpectedDynamicMessage:
        english = "these are test attributes: THIS ATTRIBUTE"
        german = "dies sind Testattribute: THIS ATTRIBUTE"

    _assert_translate_is_correct(
        client=client,
        url=dynamic_message_url,
        expected_translation=ExpectedDynamicMessage,
    )
