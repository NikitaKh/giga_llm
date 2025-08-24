import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers.llm import router
from app.settings import settings

logger = logging.getLogger(__name__)

CORS_ORIGINS = ["*"]

app = FastAPI(
    title=settings.service_name,
    description=settings.service_description,
    version=settings.api_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

logger.info(f"Приложение {settings.service_name} инициализировано")
