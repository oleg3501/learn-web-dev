"""Маршруты для работы с мастерами."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/masters", tags=["masters"])


@router.get("", response_model=List[schemas.MasterOut])
def get_masters(
    specialization: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[models.Master]:
    """Список мастеров, при необходимости — по специализации."""
    query = db.query(models.Master)
    if specialization:
        query = query.filter(models.Master.specialization == specialization)
    return query.order_by(models.Master.id).all()
