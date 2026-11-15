"""Модели SQLAlchemy: таблицы базы данных."""

from typing import List

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Category(Base):
    """Категория услуг. Таблица categories."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    services: Mapped[List["Service"]] = relationship(back_populates="category")


class Master(Base):
    """Мастер салона. Таблица masters."""

    __tablename__ = "masters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialization: Mapped[str] = mapped_column(String(100), nullable=False)


class Service(Base):
    """Услуга салона. Таблица services."""

    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    # В API поле называется desc, в базе — description (desc зарезервировано в SQL)
    desc: Mapped[str] = mapped_column("description", String(100), nullable=False)
    duration: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    category: Mapped["Category"] = relationship(back_populates="services")

    def __repr__(self) -> str:
        return "Service(id={id}, title={title!r}, price={price})".format(
            id=self.id, title=self.title, price=self.price
        )
