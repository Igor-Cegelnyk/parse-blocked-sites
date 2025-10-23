import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.config import settings
from backend.database import db_helper
from backend.routers import router

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

templates = Jinja2Templates(directory=TEMPLATE_DIR)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # Clean up the ML models and release the resources
    db_helper.dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
)

main_app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

main_app.include_router(router)

main_app.state.templates = templates


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
