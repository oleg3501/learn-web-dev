# Backend 3. SQLAlchemy и Alembic

Практика по module Backend: мастера салона теперь хранятся не в Python-списке,
а в базе данных SQLite. Доступ к данным — через SQLAlchemy, структуру таблиц
описывают миграции Alembic.

## Задание

1. Создать SQLAlchemy-модель `Master` и таблицу `masters` с полями
   `id`, `name`, `specialization`.
2. Реализовать API для работы с мастерами из базы данных:
   - `GET /masters` — список всех мастеров;
   - `GET /masters?specialization=Парикмахер` — фильтр по специализации;
   - `GET /masters/{master_id}` — один мастер, `404 Not Found`, если его нет.

## Структура

```
backend-3-practice/
├── app/
│   ├── main.py            # приложение FastAPI, подключение роутеров
│   ├── database.py        # подключение к SQLite, сессия, Base
│   ├── models.py          # модель Master (таблица masters)
│   ├── schemas.py         # Pydantic-схемы
│   └── routers/
│       └── masters.py     # маршруты /masters
├── alembic/
│   ├── env.py
│   └── versions/
│       └── 0001_create_masters.py
├── alembic.ini
├── seed.py                # заполнение базы стартовыми мастерами
└── requirements.txt
```

## Запуск

```bash
pip install -r requirements.txt
alembic upgrade head        # создать таблицу миграцией
python seed.py              # добавить мастеров
uvicorn app.main:app --reload
```

Если миграции не запускались, таблица всё равно создастся при старте приложения
(`Base.metadata.create_all`), но в учебном проекте правильнее использовать Alembic.

Swagger UI: http://127.0.0.1:8000/docs

## Примеры запросов

```bash
curl http://127.0.0.1:8000/masters
curl "http://127.0.0.1:8000/masters?specialization=Парикмахер"
curl http://127.0.0.1:8000/masters/1
```

Ответ `GET /masters`:

```json
[
  { "id": 1, "name": "Анна", "specialization": "Парикмахер" },
  { "id": 2, "name": "Мария", "specialization": "Визажист" }
]
```
