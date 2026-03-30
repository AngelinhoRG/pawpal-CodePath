from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional


@dataclass
class TimeSlot:
    start: datetime
    end: datetime


@dataclass
class Task:
    name: str
    duration: int           # minutes
    priority: str
    last_performed: Optional[datetime] = None

    def mark_complete(self) -> None:
        pass

    def edit_task(self, field: str, value) -> None:
        pass

    def remove_task(self) -> None:
        pass

    def get_time_since_last_performed(self) -> Optional[timedelta]:
        pass

    def is_overdue(self) -> bool:
        pass


@dataclass
class Pet:
    name: str
    pet_type: str
    birthday: date
    weight: float
    tasks: list[Task] = field(default_factory=list)

    @property
    def num_tasks(self) -> int:
        return len(self.tasks)

    def calculate_age(self) -> int:
        pass

    def update_weight(self, new_weight: float) -> None:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def list_tasks(self) -> list[Task]:
        pass


class Owner:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: list[Pet] = []

    @property
    def num_pets(self) -> int:
        return len(self.pets)

    def add_pet(self, pet: Pet) -> None:
        pass

    def change_email(self, new_email: str) -> None:
        pass

    def change_name(self, new_name: str) -> None:
        pass


class Scheduler:
    def __init__(self):
        self.schedule: dict[TimeSlot, Task] = {}
        self.availability: dict[str, list[TimeSlot]] = {}

    def add_task(self, task: Task, slot: TimeSlot) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def edit_task_time_slot(self, task: Task, new_slot: TimeSlot) -> None:
        pass

    def set_availability(self, day: str, slots: list[TimeSlot]) -> None:
        pass

    def get_schedule_for_day(self, day: str) -> dict[TimeSlot, Task]:
        pass
