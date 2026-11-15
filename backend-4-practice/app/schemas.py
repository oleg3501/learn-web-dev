"""Pydantic-схемы с валидацией входных данных."""

from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryOut(BaseModel):
    id: int
    name: str
    servicesCount: int


class MasterOut(BaseModel):
    id: int
    name: str
    specialization: str

    model_config = ConfigDict(from_attributes=True)


class ServiceOut(BaseModel):
    id: int
    # В модели БД атрибут называется category_id, в JSON — categoryId
    categoryId: int = Field(validation_alias="category_id")
    title: str
    desc: str
    duration: int
    price: float

    model_config = ConfigDict(from_attributes=True)


class ServiceCreate(BaseModel):
    """Тело запроса POST /services.

    Ограничения:
      * title и desc не могут быть пустыми, максимум 100 символов;
      * duration — от 30 минут до 3 часов (180 минут);
      * price — больше 0.
    """

    categoryId: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=100)
    desc: str = Field(min_length=1, max_length=100)
    duration: int = Field(ge=30, le=180)
    price: float = Field(gt=0)

    @field_validator("title", "desc")
    @classmethod
    def not_blank(cls, value: str) -> str:
        """Строка из одних пробелов тоже считается пустой."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("Поле не может быть пустым")
        return stripped
