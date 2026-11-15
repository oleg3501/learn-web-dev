"""Маршруты для работы с мастерами."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/masters", tags=["masters"])


@router.get("", response_model=List[schemas.MasterOut])
def get_masters(
    specialization: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[models.Master]:
    """Список всех мастеров из таблицы базы данных.

    Фильтр по специализации: /masters?specialization=Парикмахер
    """
    query = db.query(models.Master)
    if specialization:
        query = query.filter(models.Master.specialization == specialization)
    return query.order_by(models.Master.id).all()


@router.get("/{master_id}", response_model=schemas.MasterOut)
def get_master(master_id: int, db: Session = Depends(get_db)) -> models.Master:
    """Один мастер по id. Если мастера нет — 404 Not Found."""
    master = db.get(models.Master, master_id)
    if master is None:
        raise HTTPException(status_code=404, detail="Master not found")
    return master


@router.post("", response_model=schemas.MasterOut, status_code=201)
def create_master(payload: schemas.MasterCreate, db: Session = Depends(get_db)) -> models.Master:
    """Добавляет мастера в базу данных."""
    master = models.Master(name=payload.name.strip(), specialization=payload.specialization.strip())
    db.add(master)
    db.commit()
    db.refresh(master)
    return master
