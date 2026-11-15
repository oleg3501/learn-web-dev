"""Данные салона красоты для in-memory версии API (без базы данных)."""

from typing import List

from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str


class Service(BaseModel):
    id: int
    categoryId: int
    title: str
    desc: str
    duration: int
    price: float


class Master(BaseModel):
    id: int
    name: str
    specialization: str


class Appointment(BaseModel):
    id: int
    client_name: str
    master_id: int
    service_id: int
    time: str


CATEGORIES: List[Category] = [
    Category(id=1, name="Стрижки и укладки"),
    Category(id=2, name="Маникюр и педикюр"),
    Category(id=3, name="Брови и ресницы"),
    Category(id=4, name="Спа-процедуры"),
]

SERVICES: List[Service] = [
    # 1. Стрижки и укладки
    Service(id=1, categoryId=1, title="Стрижка женская", desc="Стрижка любой сложности", duration=60, price=2500.0),
    Service(id=2, categoryId=1, title="Стрижка мужская", desc="Классическая мужская стрижка", duration=45, price=1800.0),
    Service(id=3, categoryId=1, title="Укладка", desc="Укладка феном или на брашинг", duration=40, price=1500.0),
    Service(id=4, categoryId=1, title="Окрашивание", desc="Однотонное окрашивание", duration=120, price=6000.0),
    Service(id=5, categoryId=1, title="Детская стрижка", desc="Стрижка для детей до 12 лет", duration=30, price=1200.0),
    # 2. Маникюр и педикюр
    Service(id=6, categoryId=2, title="Маникюр классический", desc="Обработка кутикулы и ногтей", duration=60, price=2000.0),
    Service(id=7, categoryId=2, title="Маникюр аппаратный", desc="Аппаратная обработка", duration=90, price=2800.0),
    Service(id=8, categoryId=2, title="Педикюр", desc="Комплексный уход за стопами", duration=90, price=3200.0),
    Service(id=9, categoryId=2, title="Покрытие гель-лак", desc="Стойкое покрытие", duration=60, price=1900.0),
    Service(id=10, categoryId=2, title="Снятие покрытия", desc="Снятие гель-лака", duration=30, price=700.0),
    # 3. Брови и ресницы
    Service(id=11, categoryId=3, title="Коррекция бровей", desc="Коррекция формы бровей", duration=30, price=1200.0),
    Service(id=12, categoryId=3, title="Окрашивание бровей", desc="Окрашивание краской или хной", duration=40, price=1500.0),
    Service(id=13, categoryId=3, title="Ламинирование ресниц", desc="Уход и завивка ресниц", duration=90, price=3500.0),
    Service(id=14, categoryId=3, title="Наращивание ресниц", desc="Классическое наращивание", duration=120, price=4500.0),
    # 4. Спа-процедуры
    Service(id=15, categoryId=4, title="Спа-уход для лица", desc="Комплексный уход", duration=90, price=4000.0),
    Service(id=16, categoryId=4, title="Массаж лица", desc="Расслабляющий массаж", duration=60, price=3000.0),
    Service(id=17, categoryId=4, title="Обёртывание", desc="Питательное обёртывание", duration=90, price=3500.0),
    Service(id=18, categoryId=4, title="Пилинг", desc="Очищающий пилинг", duration=60, price=2800.0),
]

MASTERS: List[Master] = [
    Master(id=1, name="Анна", specialization="Парикмахер"),
    Master(id=2, name="Мария", specialization="Визажист"),
    Master(id=3, name="Ольга", specialization="Мастер маникюра"),
    Master(id=4, name="Ирина", specialization="Косметолог"),
]

APPOINTMENTS: List[Appointment] = []

OPEN_HOUR = 8
CLOSE_HOUR = 20
