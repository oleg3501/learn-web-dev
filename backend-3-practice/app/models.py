"""Модели SQLAlchemy: таблицы базы данных."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Master(Base):
    """Мастер салона. Таблица masters."""

    __tablename__ = "masters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialization: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self) -> str:
        return "Master(id={id}, name={name!r}, specialization={spec!r})".format(
            id=self.id, name=self.name, spec=self.specialization
        )
