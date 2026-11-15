"""Задание 4. Pydantic.

Продолжение работы над API салона: услуги хранятся в базе данных,
а входные данные проверяет Pydantic-модель ServiceCreate.

Запуск:
    uvicorn app.main:app --reload

Документация (Swagger UI):
    http://127.0.0.1:8000/docs
"""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app import models  # noqa: F401  (регистрирует модели в Base.metadata)
from app.database import Base, engine
from app.routers import categories, masters, services


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Создаёт таблицы при первом запуске, если их ещё нет."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Салон красоты — API (Pydantic)",
    description="Учебный API: категории, услуги и мастера салона в SQLite.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(categories.router)
app.include_router(masters.router)
app.include_router(services.router)


@app.get("/")
def root() -> dict:
    """Короткая информация о сервисе."""
    return {
        "service": "Салон красоты — API",
        "storage": "SQLite + SQLAlchemy",
        "validation": "Pydantic",
        "docs": "/docs",
        "endpoints": ["/categories", "/categories/{category_id}", "/services", "/masters"],
    }
