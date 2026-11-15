# Backend 1. Python-основы языка

Практика по module Backend: переводим запись клиента из обычного словаря
в класс и добавляем бизнес-правило салона.

## Задания

### Задание 1. Класс Appointment (запись клиента)

Функция `create_appointment` раньше возвращала словарь. Нужно перевести запись
в класс `Appointment`. Функция должна возвращать объект класса, а объект записи
создаётся только в том случае, если заполнены все поля.

Ожидаемая проверка:

```python
first_appointment = create_appointment("Иванова А.А.", 1, 1, '10:00')
second_appointment = create_appointment("Петрова А.А.", 1, 1, '11:00')
print("Список записей:")
for appointment in appointments:
    print(appointment.client_name, appointment.time)
```

```
Список записей:
Иванова А.А. 10:00
Петрова А.А. 11:00
```

Запись с незаполненными полями не создаётся:

```python
no_correct_appointment = create_appointment("", 1, 1, '12:00')
print(len(appointments))
```

```
2
```

### Задание 2. Новое бизнес-правило

Записаться к мастеру можно только в часы работы салона: **с 08:00 до 20:00**.

```python
night_appointment = create_appointment("Сидорова А.А.", 1, 1, '00:00')
print(len(appointments))
```

```
2
```

## Структура

```
backend-1-practice/
└── main.py    # классы Master, Service, Appointment, create_appointment и демонстрация
```

## Запуск

```bash
python main.py
```

Скрипт последовательно выполняет все проверки из задания и печатает результат.
Дополнительных библиотек не требуется — только стандартный Python 3.9+.
