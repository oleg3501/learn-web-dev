"""Наполнение базы данных категориями, услугами и мастерами.

Запуск:
    python seed.py
"""

from app.database import Base, SessionLocal, engine
from app.models import Category, Master, Service

STARTER_CATEGORIES = [
    "Стрижки и укладки",
    "Маникюр и педикюр",
    "Брови и ресницы",
    "Спа-процедуры",
]

# (category_id, title, desc, duration, price)
STARTER_SERVICES = [
    (1, "Стрижка женская", "Стрижка любой сложности", 60, 2500.0),
    (1, "Стрижка мужская", "Классическая мужская стрижка", 45, 1800.0),
    (1, "Укладка", "Укладка феном или на брашинг", 40, 1500.0),
    (1, "Окрашивание", "Однотонное окрашивание", 120, 6000.0),
    (1, "Детская стрижка", "Стрижка для детей до 12 лет", 30, 1200.0),
    (2, "Маникюр классический", "Обработка кутикулы и ногтей", 60, 2000.0),
    (2, "Маникюр аппаратный", "Аппаратная обработка", 90, 2800.0),
    (2, "Педикюр", "Комплексный уход за стопами", 90, 3200.0),
    (2, "Покрытие гель-лак", "Стойкое покрытие", 60, 1900.0),
    (2, "Снятие покрытия", "Снятие гель-лака", 30, 700.0),
    (3, "Коррекция бровей", "Коррекция формы бровей", 30, 1200.0),
    (3, "Окрашивание бровей", "Окрашивание краской или хной", 40, 1500.0),
    (3, "Ламинирование ресниц", "Уход и завивка ресниц", 90, 3500.0),
    (3, "Наращивание ресниц", "Классическое наращивание", 120, 4500.0),
    (4, "Спа-уход для лица", "Комплексный уход", 90, 4000.0),
    (4, "Массаж лица", "Расслабляющий массаж", 60, 3000.0),
    (4, "Обёртывание", "Питательное обёртывание", 90, 3500.0),
    (4, "Пилинг", "Очищающий пилинг", 60, 2800.0),
]

STARTER_MASTERS = [
    ("Анна", "Парикмахер"),
    ("Мария", "Визажист"),
    ("Ольга", "Мастер маникюра"),
    ("Ирина", "Косметолог"),
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Category).count() > 0:
            print("База уже заполнена, пропускаем.")
            return

        for name in STARTER_CATEGORIES:
            db.add(Category(name=name))
        db.flush()

        for category_id, title, desc, duration, price in STARTER_SERVICES:
            db.add(
                Service(
                    category_id=category_id,
                    title=title,
                    desc=desc,
                    duration=duration,
                    price=price,
                )
            )

        for name, specialization in STARTER_MASTERS:
            db.add(Master(name=name, specialization=specialization))

        db.commit()

        print("Добавлено категорий:", db.query(Category).count())
        print("Добавлено услуг:", db.query(Service).count())
        print("Добавлено мастеров:", db.query(Master).count())
    finally:
        db.close()


if __name__ == "__main__":
    seed()
