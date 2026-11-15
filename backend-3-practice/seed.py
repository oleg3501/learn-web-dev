"""Наполнение базы данных стартовыми мастерами.

Запуск:
    python seed.py
"""

from app.database import Base, SessionLocal, engine
from app.models import Master

STARTER_MASTERS = [
    {"name": "Анна", "specialization": "Парикмахер"},
    {"name": "Мария", "specialization": "Визажист"},
    {"name": "Ольга", "specialization": "Мастер маникюра"},
    {"name": "Ирина", "specialization": "Косметолог"},
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Master).count() > 0:
            print("База уже заполнена, пропускаем.")
            return

        for item in STARTER_MASTERS:
            db.add(Master(**item))
        db.commit()

        print("Добавлены мастера:")
        for master in db.query(Master).order_by(Master.id).all():
            print(" ", master)
    finally:
        db.close()


if __name__ == "__main__":
    seed()
