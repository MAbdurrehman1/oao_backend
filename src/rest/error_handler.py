import logging
from typing import List

from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_503_SERVICE_UNAVAILABLE,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_403_FORBIDDEN,
)

from utils.error_handler import generate_http_error_json_response
from cexceptions import (
    AbstractException,
    UniqueException,
    ValidationException,
    CredentialValidationException,
    ExpireException,
    ExternalSourceException,
    MissingEntityException,
    NotFoundException,
    UnauthorizedException,
    EntityProcessException,
    MissingValuesException,
    LessThanOrEqualException,
    GreaterThanOrEqualException,
    DoesNotBelongException,
    EmptyResultException,
    AlreadyBelongException,
    UniquePerEntityException,
)
from utils.error_handler import (
    ExceptionHandler,
)
from settings import configs

ExceptionHandler.logger_name = configs.app_title


# Add exception handlers
base_exception_Handler = ExceptionHandler(exception=AbstractException)
unique_exception_Handler = ExceptionHandler(
    exception=UniqueException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_400_BAD_REQUEST,
    ),
)
validation_exception_Handler = ExceptionHandler(
    exception=ValidationException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_400_BAD_REQUEST,
    ),
)
credential_validation_exception_Handler = ExceptionHandler(
    exception=CredentialValidationException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_403_FORBIDDEN,
    ),
)

expire_exception_Handler = ExceptionHandler(
    exception=ExpireException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_401_UNAUTHORIZED,
    ),
)

external_source_exception_Handler = ExceptionHandler(
    exception=ExternalSourceException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_503_SERVICE_UNAVAILABLE,
    ),
)

missing_entity_exception_Handler = ExceptionHandler(
    exception=MissingEntityException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_400_BAD_REQUEST,
    ),
)

missing_values_exception_Handler = ExceptionHandler(
    exception=MissingValuesException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_400_BAD_REQUEST,
    ),
)

not_found_exception_Handler = ExceptionHandler(
    exception=NotFoundException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_404_NOT_FOUND,
    ),
)

unauthorized_exception_Handler = ExceptionHandler(
    exception=UnauthorizedException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_403_FORBIDDEN,
    ),
)

entity_process_exception_Handler = ExceptionHandler(
    exception=EntityProcessException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    ),
)


less_than_or_equal_exception_Handler = ExceptionHandler(
    exception=LessThanOrEqualException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_400_BAD_REQUEST,
    ),
)


greater_than_or_equal_exception_Handler = ExceptionHandler(
    exception=GreaterThanOrEqualException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_400_BAD_REQUEST,
    ),
)

does_not_belong_exception_Handler = ExceptionHandler(
    exception=DoesNotBelongException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_400_BAD_REQUEST,
    ),
)


empty_result_exception_Handler = ExceptionHandler(
    exception=EmptyResultException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    ),
)


already_belong_exception_Handler = ExceptionHandler(
    exception=AlreadyBelongException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_400_BAD_REQUEST,
    ),
)

unique_per_entity_exception_Handler = ExceptionHandler(
    exception=UniquePerEntityException,
    loglevel=logging.ERROR,
    notify=True,
    response_fn=generate_http_error_json_response(
        status_code=HTTP_400_BAD_REQUEST,
    ),
)

exception_handlers: List[ExceptionHandler] = [
    base_exception_Handler,
    unique_exception_Handler,
    validation_exception_Handler,
    credential_validation_exception_Handler,
    expire_exception_Handler,
    external_source_exception_Handler,
    missing_entity_exception_Handler,
    missing_values_exception_Handler,
    not_found_exception_Handler,
    unauthorized_exception_Handler,
    entity_process_exception_Handler,
    less_than_or_equal_exception_Handler,
    greater_than_or_equal_exception_Handler,
    empty_result_exception_Handler,
    does_not_belong_exception_Handler,
    already_belong_exception_Handler,
    unique_per_entity_exception_Handler,
]
