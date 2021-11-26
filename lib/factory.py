import os
import importlib
import redis
from loguru import logger
from fastapi import FastAPI, APIRouter

from app.config import (
    PROJECT_NAME,
    API_PREFIX,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
)


def import_mods(mod_name: str, sub_apps=None, app_dir="app"):
    app_path = app_dir.replace("/", ".")

    if not sub_apps:
        sub_apps = [a for a in os.listdir(app_dir) if not a.startswith((".", "_"))]

    for sub_app in sub_apps:
        exists = os.path.exists(os.path.join(app_dir, sub_app, f"{mod_name}.py"))
        if exists:
            path = f"{app_path}.{sub_app}.{mod_name}"
            yield (sub_app, importlib.import_module(path))
        else:
            logger.debug(
                "No mod:{mod} in app:{path}.{app}",
                mod=mod_name,
                app=sub_app,
                path=app_path,
            )


def import_models():
    res = [m for _, m in import_mods(mod_name="models")]
    return res


def register_routes(app):
    api_router = APIRouter()

    for name, views in import_mods(mod_name="views"):
        logger.debug("Register route:{name}", name=name)
        api_router.include_router(views.router, tags=[name])

    app.include_router(api_router, prefix=API_PREFIX)


def create_app(name=PROJECT_NAME):
    app = FastAPI(title=name, openapi_url=f"{API_PREFIX}/openapi.json")
    register_routes(app)
    return app


def get_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)