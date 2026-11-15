"""Задание 3. SQLAlchemy и Alembic.

Хранение мастеров перенесено из Python-списка в базу данных SQLite,
доступ к данным — через SQLAlchemy. Таблицу создаёт миграция Alembic
(или Base.metadata.create_all при старте приложения, если миграции не запускались).

Запуск:
    uvicorn app.main:app --reload

Документация (Swagger UI):
    http://127.0.0.1:8000/docs
"""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app import models  # noqa: F401  (нужно, чтобы SQLAlchemy знала о моделях)
from app.database import Base, engine
from app.routers import masters


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Создаёт таблицы при первом запуске, если их ещё нет."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Салон красоты — API (SQLite + SQLAlchemy)",
    description="Учебный API: мастера салона хранятся в базе данных.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(masters.router)


@app.get("/")
def root() -> dict:
    """Короткая информация о сервисе."""
    return {
        "service": "Салон красоты — API",
        "storage": "SQLite + SQLAlchemy",
        "docs": "/docs",
        "endpoints": ["/masters", "/masters/{master_id}"],
    }
