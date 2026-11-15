"""Задание 1. Python-основы языка + Задание 2. Новое бизнес-правило.

Практика по module Backend:
  1. Запись клиента (appointment) переводится из обычного словаря в класс Appointment.
  2. Добавляется бизнес-правило: записаться к мастеру можно только в часы работы салона
     с 08:00 до 20:00.

Запуск:
    python main.py
"""

from typing import Dict, List, Optional


class Master:
    """Мастер салона."""

    def __init__(self, master_id: int, name: str, specialization: str) -> None:
        self.master_id = master_id
        self.name = name
        self.specialization = specialization


class Service:
    """Услуга салона."""

    def __init__(self, service_id: int, title: str, duration: int, price: float) -> None:
        self.service_id = service_id
        self.title = title
        self.duration = duration
        self.price = price


class Appointment:
    """Запись клиента к мастеру.

    Объект записи создаётся только в том случае, если заполнены все поля,
    мастер и услуга существуют, а время попадает в часы работы салона.
    """

    OPEN_HOUR = 8
    CLOSE_HOUR = 20

    def __init__(
        self,
        appointment_id: int,
        client_name: str,
        master: Master,
        service: Service,
        time: str,
    ) -> None:
        self.id = appointment_id
        self.client_name = client_name
        self.master = master
        self.service = service
        self.time = time

    @property
    def master_id(self) -> int:
        return self.master.master_id

    @property
    def service_id(self) -> int:
        return self.service.service_id

    def __repr__(self) -> str:
        return (
            "Appointment(id={id}, client_name={client_name!r}, master_id={master_id}, "
            "service_id={service_id}, time={time!r})"
        ).format(
            id=self.id,
            client_name=self.client_name,
            master_id=self.master_id,
            service_id=self.service_id,
            time=self.time,
        )


masters: List[Master] = [
    Master(1, "Анна", "Парикмахер"),
    Master(2, "Мария", "Визажист"),
    Master(3, "Ольга", "Мастер маникюра"),
]

services: List[Service] = [
    Service(1, "Стрижка женская", 60, 2500.0),
    Service(2, "Стрижка мужская", 45, 1800.0),
    Service(3, "Маникюр классический", 60, 2000.0),
]

appointments: List[Appointment] = []


def get_master(master_id: int) -> Optional[Master]:
    for master in masters:
        if master.master_id == master_id:
            return master
    return None


def get_service(service_id: int) -> Optional[Service]:
    for service in services:
        if service.service_id == service_id:
            return service
    return None


def is_working_hours(time: str) -> bool:
    """Проверяет, что время вида "10:00" попадает в часы работы салона."""
    if not isinstance(time, str) or len(time) != 5 or time[2] != ":":
        return False

    hours, minutes = time[:2], time[3:]
    if not (hours.isdigit() and minutes.isdigit()):
        return False

    hour, minute = int(hours), int(minutes)
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return False

    return Appointment.OPEN_HOUR <= hour <= Appointment.CLOSE_HOUR


def create_appointment(
    client_name: str,
    master_id: int,
    service_id: int,
    time: str,
) -> Optional[Appointment]:
    """Создаёт запись клиента.

    Возвращает объект Appointment либо None, если:
      * не заполнено хотя бы одно поле;
      * мастер или услуга не найдены;
      * время не входит в часы работы салона (08:00–20:00).
    """
    if not isinstance(client_name, str) or not client_name.strip():
        return None

    master = get_master(master_id)
    service = get_service(service_id)

    if master is None or service is None:
        return None

    if not is_working_hours(time):
        return None

    appointment = Appointment(
        appointment_id=len(appointments) + 1,
        client_name=client_name.strip(),
        master=master,
        service=service,
        time=time,
    )
    appointments.append(appointment)
    return appointment


def print_appointments() -> None:
    print("Список записей:")
    for appointment in appointments:
        print(appointment.client_name, appointment.time)


def demo() -> None:
    print("=== Проверка 1: две корректные записи ===")
    create_appointment("Иванова А.А.", 1, 1, "10:00")
    create_appointment("Петрова А.А.", 1, 1, "11:00")
    print_appointments()

    print()
    print("=== Проверка 2: пустое имя клиента ===")
    no_correct_appointment = create_appointment("", 1, 1, "12:00")
    print("Создана запись:", no_correct_appointment)
    print("Всего записей:", len(appointments))

    print()
    print("=== Проверка 3: время вне часов работы салона (08:00–20:00) ===")
    night_appointment = create_appointment("Сидорова А.А.", 1, 1, "00:00")
    print("Создана запись:", night_appointment)
    late_appointment = create_appointment("Кузнецова А.А.", 1, 1, "21:30")
    print("Создана запись:", late_appointment)
    print("Всего записей:", len(appointments))

    print()
    print("=== Проверка 4: мастер и услуга должны существовать ===")
    unknown_master = create_appointment("Орлова А.А.", 99, 1, "15:00")
    unknown_service = create_appointment("Орлова А.А.", 1, 99, "15:00")
    print("Несуществующий мастер:", unknown_master)
    print("Несуществующая услуга:", unknown_service)
    print("Всего записей:", len(appointments))


if __name__ == "__main__":
    demo()
