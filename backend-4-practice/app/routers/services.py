"""Маршруты для работы с услугами."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/services", tags=["services"])


@router.get("", response_model=List[schemas.ServiceOut])
def get_services(
    category_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[models.Service]:
    """Список услуг. Фильтр по категории: /services?category_id=3"""
    query = db.query(models.Service)
    if category_id is not None:
        query = query.filter(models.Service.category_id == category_id)
    return query.order_by(models.Service.id).all()


@router.post("", response_model=schemas.ServiceOut, status_code=201)
def create_service(payload: schemas.ServiceCreate, db: Session = Depends(get_db)) -> models.Service:
    """Создаёт услугу.

    Тело запроса проверяет Pydantic (некорректные данные → 422).
    Категория должна существовать в базе, иначе 404.
    """
    category = db.get(models.Category, payload.categoryId)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    service = models.Service(
        category_id=payload.categoryId,
        title=payload.title,
        desc=payload.desc,
        duration=payload.duration,
        price=payload.price,
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service
