"""Pydantic-схемы для API мастеров."""

from pydantic import BaseModel, ConfigDict, Field


class MasterBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    specialization: str = Field(min_length=1, max_length=100)


class MasterCreate(MasterBase):
    """Тело запроса на создание мастера."""


class MasterOut(MasterBase):
    """Мастер в ответе API."""

    id: int

    model_config = ConfigDict(from_attributes=True)
