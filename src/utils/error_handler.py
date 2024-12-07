import logging
from dataclasses import dataclass
from typing import TypeVar, Generic, Callable, ClassVar
import sentry_sdk
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from cexceptions import AbstractException

from .i18n import Language, translate

E = TypeVar("E", bound=Exception)


def generate_http_error_json_response(
    status_code: int,
) -> Callable[[E], JSONResponse]:
    def _generate_http_error_json_response(exc: E) -> JSONResponse:
        return JSONResponse(content={"error": str(exc)}, status_code=status_code)

    return _generate_http_error_json_response


@dataclass
class ExceptionHandler(Generic[E]):
    exception: type[E]
    loglevel: int = logging.ERROR
    response_fn: Callable[[E], Response] = generate_http_error_json_response(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR
    )
    notify: bool = True
    logger_name: ClassVar[str] = "error-handler"

    def __post_init__(self):
        self.logger = logging.getLogger(self.logger_name)

    def handle_exception(self, request: Request, exc: E) -> Response:
        if isinstance(exc, AbstractException):
            self.logger.log(
                level=self.loglevel,
                msg=f"Handled Exception: {exc}",
            )
        else:
            self.logger.log(
                level=self.loglevel,
                msg="An exception occured!",
                exc_info=(type(exc), exc, exc.__traceback__),
            )
        self.notify_error_tracker(exc)

        translated: E = self._translate_exception(exc, request)

        return self.response_fn(translated)

    @staticmethod
    def _translate_exception(exc, request) -> E:
        lang = _get_request_language(request)
        translated: E = translate(exc, lang)
        return translated

    def notify_error_tracker(self, exc):
        sentry_sdk.capture_exception(exc)


def setup_exception_handlers(app: FastAPI, handlers: list[ExceptionHandler]) -> None:
    for exc_handler in handlers:
        app.add_exception_handler(
            exc_class_or_status_code=exc_handler.exception,
            handler=exc_handler.handle_exception,
        )


def _get_request_language(request: Request) -> Language | None:
    try:
        lang: str = request.headers["accept-language"]
        return Language.from_code(lang)
    except (ValueError, KeyError):
        return None
