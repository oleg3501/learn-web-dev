"""Задание 2. От Python-программы к Web API.

Учебный backend салона красоты на FastAPI. Данные пока хранятся в памяти
(списки в data.py), база данных появится в следующей практике.

Запуск:
    uvicorn main:app --reload

Документация (Swagger UI):
    http://127.0.0.1:8000/docs
"""

from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

import data

app = FastAPI(
    title="Салон красоты — API",
    description="Учебный API: категории, услуги, мастера и записи клиентов.",
    version="1.0.0",
)


class CategoryOut(BaseModel):
    id: int
    name: str
    servicesCount: int


class AppointmentCreate(BaseModel):
    client_name: str
    master_id: int
    service_id: int
    time: str


@app.get("/")
def root() -> dict:
    """Короткая информация о сервисе."""
    return {
        "service": "Салон красоты — API",
        "docs": "/docs",
        "endpoints": ["/categories", "/categories/{category_id}", "/services", "/masters", "/appointments"],
    }


@app.get("/categories", response_model=List[CategoryOut])
def get_categories() -> List[CategoryOut]:
    """Список всех категорий услуг с количеством услуг в каждой."""
    result: List[CategoryOut] = []
    for category in data.CATEGORIES:
        services_count = len([s for s in data.SERVICES if s.categoryId == category.id])
        result.append(
            CategoryOut(id=category.id, name=category.name, servicesCount=services_count)
        )
    return result


@app.get("/categories/{category_id}", response_model=CategoryOut)
def get_category(category_id: int) -> CategoryOut:
    """Информация о конкретной категории услуг."""
    for category in data.CATEGORIES:
        if category.id == category_id:
            services_count = len([s for s in data.SERVICES if s.categoryId == category.id])
            return CategoryOut(
                id=category.id,
                name=category.name,
                servicesCount=services_count,
            )
    raise HTTPException(status_code=404, detail="Category not found")


@app.get("/services", response_model=List[data.Service])
def get_services(category_id: Optional[int] = Query(default=None)) -> List[data.Service]:
    """Список услуг. Можно отфильтровать по категории: /services?category_id=1."""
    if category_id is None:
        return data.SERVICES
    return [service for service in data.SERVICES if service.categoryId == category_id]


@app.get("/masters", response_model=List[data.Master])
def get_masters(specialization: Optional[str] = Query(default=None)) -> List[data.Master]:
    """Список мастеров. Можно отфильтровать по специализации."""
    if specialization is None:
        return data.MASTERS
    return [master for master in data.MASTERS if master.specialization == specialization]


@app.get("/masters/{master_id}", response_model=data.Master)
def get_master(master_id: int) -> data.Master:
    """Один мастер по id."""
    for master in data.MASTERS:
        if master.id == master_id:
            return master
    raise HTTPException(status_code=404, detail="Master not found")


@app.get("/appointments", response_model=List[data.Appointment])
def get_appointments() -> List[data.Appointment]:
    """Все записи клиентов."""
    return data.APPOINTMENTS


@app.post("/appointments", response_model=data.Appointment, status_code=201)
def create_appointment(payload: AppointmentCreate) -> data.Appointment:
    """Создаёт запись клиента.

    Сервер сам проверяет, что клиент заполнил все поля, мастер и услуга
    существуют, а время входит в часы работы салона (08:00–20:00).
    """
    if not payload.client_name.strip():
        raise HTTPException(status_code=422, detail="client_name не может быть пустым")

    master = next((m for m in data.MASTERS if m.id == payload.master_id), None)
    if master is None:
        raise HTTPException(status_code=404, detail="Master not found")

    service = next((s for s in data.SERVICES if s.id == payload.service_id), None)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    if not _is_working_hours(payload.time):
        raise HTTPException(
            status_code=422,
            detail="Записаться можно только в часы работы салона: с 08:00 до 20:00",
        )

    appointment = data.Appointment(
        id=len(data.APPOINTMENTS) + 1,
        client_name=payload.client_name.strip(),
        master_id=payload.master_id,
        service_id=payload.service_id,
        time=payload.time,
    )
    data.APPOINTMENTS.append(appointment)
    return appointment


def _is_working_hours(time: str) -> bool:
    """Проверяет формат "HH:MM" и часы работы салона."""
    if not isinstance(time, str) or len(time) != 5 or time[2] != ":":
        return False

    hours, minutes = time[:2], time[3:]
    if not (hours.isdigit() and minutes.isdigit()):
        return False

    hour, minute = int(hours), int(minutes)
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return False

    return data.OPEN_HOUR <= hour <= data.CLOSE_HOUR
