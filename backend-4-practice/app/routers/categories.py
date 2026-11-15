"""Маршруты для работы с категориями услуг."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=List[schemas.CategoryOut])
def get_categories(db: Session = Depends(get_db)) -> List[schemas.CategoryOut]:
    """Список всех категорий услуг с количеством услуг в каждой."""
    categories = db.query(models.Category).order_by(models.Category.id).all()
    return [
        schemas.CategoryOut(
            id=category.id,
            name=category.name,
            servicesCount=len(category.services),
        )
        for category in categories
    ]


@router.get("/{category_id}", response_model=schemas.CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)) -> schemas.CategoryOut:
    """Информация о конкретной категории услуг."""
    category = db.get(models.Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return schemas.CategoryOut(
        id=category.id,
        name=category.name,
        servicesCount=len(category.services),
    )
