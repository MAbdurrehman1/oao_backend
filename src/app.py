from logging.config import dictConfig
from os.path import join
import logging

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from utils.error_handler import setup_exception_handlers
import services.i18n  # noqa: F401 (register YAMLs & additional translate functions)
from rest import router, endpoints  # noqa: F401 (needed to add all endpoints to router)
from rest.error_handler import exception_handlers
from rest.router import Tags
from settings import configs, StorageType
from settings.constants import (
    ALLOWED_ORIGINS,
    ALLOWED_ORIGIN_REGEX,
    ALLOWED_METHODS,
    ALLOWED_HEADERS,
    EXPOSED_HEADERS,
)
from settings.config import ROOT_DIR, log_config, initiate_sentry

logger = logging.getLogger(configs.app_title)


app = FastAPI(title=configs.app_title, openapi_url="/openapi.json")


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=ALLOWED_ORIGIN_REGEX,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
    expose_headers=EXPOSED_HEADERS,
    allow_credentials=True,
)

if configs.storage_type == StorageType.local_storage:
    app.mount(
        "/media",
        StaticFiles(directory=configs.media_root),
        name="media",
    )

initiate_sentry(sentry_dns=configs.sentry_dsn, environment=configs.environment)

if configs.debug:
    # loading OPEN API (SWAGGER) static files
    app.mount(
        "/static",
        StaticFiles(directory=join(ROOT_DIR, "static")),
        name="static",
    )

    @app.get("/docs/", include_in_schema=False)
    async def custom_swagger_ui_html(request: Request):
        return get_swagger_ui_html(
            openapi_url=str(app.openapi_url),
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        )

    @app.get("/routes/", tags=[Tags.general])
    async def get_routes():
        routes = {route.name: route.path for route in app.routes}  # type: ignore
        routes.update({"static_root": join(ROOT_DIR, "static")})
        return JSONResponse(content=routes)

else:
    app.openapi_url = ""


setup_exception_handlers(app, handlers=exception_handlers)


app.include_router(router)
if configs.logging_on:
    dictConfig(log_config)
if configs.debug and __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=configs.exposed_port, reload=True)
