# Backend 2. От Python-программы к Web API

Практика по module Backend: функции салона красоты становятся HTTP-эндпоинтами.
Сервер на FastAPI принимает запросы от браузера, а данные пока хранятся в памяти
(списки в `data.py`) — база данных появится в следующей практике.

## Задания

### Задание 1. Список категорий

`GET /categories` — список всех категорий услуг с количеством услуг в каждой.

```json
[
  { "id": 1, "name": "Стрижки и укладки", "servicesCount": 5 },
  { "id": 2, "name": "Маникюр и педикюр", "servicesCount": 5 },
  { "id": 3, "name": "Брови и ресницы", "servicesCount": 4 },
  { "id": 4, "name": "Спа-процедуры", "servicesCount": 4 }
]
```

### Задание 2. Информация по категории

`GET /categories/{category_id}` — одна категория.

* `200` — `{ "id": 1, "name": "Стрижки и укладки", "servicesCount": 5 }`
* `404` — `Category not found`

### Дополнительно

Чтобы приложение было похоже на настоящий backend салона, добавлены ещё методы:

* `GET /services`, `GET /services?category_id=1` — услуги (с фильтром по категории);
* `GET /masters`, `GET /masters?specialization=Парикмахер` — мастера;
* `GET /masters/{master_id}` — один мастер (`404`, если не найден);
* `GET /appointments` — все записи клиентов;
* `POST /appointments` — создание записи; сервер сам проверяет, что все поля
  заполнены, мастер и услуга существуют, а время попадает в часы работы
  салона (08:00–20:00).

## Структура

```
backend-2-practice/
├── main.py            # приложение FastAPI и маршруты
├── data.py            # данные салона: категории, услуги, мастера, записи
└── requirements.txt
```

## Запуск

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs

## Примеры запросов

```bash
curl http://127.0.0.1:8000/categories
curl http://127.0.0.1:8000/categories/1
curl http://127.0.0.1:8000/categories/99    # 404 Category not found
curl "http://127.0.0.1:8000/masters?specialization=Парикмахер"
```

Создание записи клиента:

```bash
curl -X POST http://127.0.0.1:8000/appointments \
  -H "Content-Type: application/json" \
  -d "{\"client_name\": \"Иванова А.А.\", \"master_id\": 1, \"service_id\": 1, \"time\": \"10:00\"}"
```

Ответ с кодом `201`:

```json
{ "id": 1, "client_name": "Иванова А.А.", "master_id": 1, "service_id": 1, "time": "10:00" }
```

Запись на `00:00` или `21:30` вернёт `422`: записаться можно только с 08:00 до 20:00.
