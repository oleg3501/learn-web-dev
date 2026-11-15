# Backend 4. Pydantic

Практика по module Backend: услуги и категории салона теперь хранятся в базе
данных, а входные данные проверяет Pydantic-модель `ServiceCreate`.

## Задания

### Задание 1. Pydantic-модель

Модель `ServiceCreate` содержит пять полей и ограничения:

| Поле         | Тип     | Ограничения                                  |
|--------------|---------|----------------------------------------------|
| `categoryId` | `int`   | идентификатор существующей категории         |
| `title`      | `str`   | не пустое, максимум 100 символов             |
| `desc`       | `str`   | не пустое, максимум 100 символов             |
| `duration`   | `int`   | от 30 до 180 минут                           |
| `price`      | `float` | больше 0                                     |

Строка из одних пробелов тоже считается пустой — это проверяет `field_validator`.

### Задание 2. Эндпоинт POST /services

`POST /services` добавляет услугу в базу данных.

* `201` — услуга создана;
* `422` — данные не прошли валидацию Pydantic;
* `404` — категории с таким `categoryId` нет в базе.

Пример запроса:

```json
{
  "categoryId": 3,
  "title": "Наращивание ресниц",
  "desc": "Огромные ресницы уже через 30 минут",
  "duration": 30,
  "price": 1500.00
}
```

Ответ с кодом `201`:

```json
{
  "id": 19,
  "categoryId": 3,
  "title": "Наращивание ресниц",
  "desc": "Огромные ресницы уже через 30 минут",
  "duration": 30,
  "price": 1500.0
}
```

Некорректные данные (`"price": "бесплатно"`, пустой `desc`, `duration: 0`,
`price: -1500`) возвращают `422`.

## Дополнительные эндпоинты

* `GET /categories` — категории с количеством услуг (`servicesCount`);
* `GET /categories/{category_id}` — одна категория, `404` если нет;
* `GET /services`, `GET /services?category_id=3` — список услуг;
* `GET /masters`, `GET /masters?specialization=Парикмахер` — мастера.

## Структура

```
backend-4-practice/
├── app/
│   ├── main.py            # приложение FastAPI, подключение роутеров
│   ├── database.py        # подключение к SQLite, сессия, Base
│   ├── models.py          # Category, Master, Service
│   ├── schemas.py         # Pydantic-схемы и ServiceCreate
│   └── routers/
│       ├── categories.py
│       ├── masters.py
│       └── services.py
├── alembic/
│   ├── env.py
│   └── versions/
│       └── 0001_create_tables.py
├── alembic.ini
├── seed.py                # категории, 18 услуг и мастера
└── requirements.txt
```

В базе поле `desc` хранится в колонке `description` (`desc` — зарезервированное
слово в SQL), а `categoryId` в JSON соответствует атрибуту `category_id` модели.

## Запуск

```bash
pip install -r requirements.txt
alembic upgrade head        # создать таблицы миграцией
python seed.py              # наполнить базу данными
uvicorn app.main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs

## Примеры запросов

```bash
curl http://127.0.0.1:8000/categories
curl "http://127.0.0.1:8000/services?category_id=3"

curl -X POST http://127.0.0.1:8000/services \
  -H "Content-Type: application/json" \
  -d "{\"categoryId\": 3, \"title\": \"Наращивание ресниц\", \"desc\": \"Огромные ресницы уже через 30 минут\", \"duration\": 30, \"price\": 1500.00}"
```
