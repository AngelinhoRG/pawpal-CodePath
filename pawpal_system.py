from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional


@dataclass(frozen=True)
class TimeSlot:
    start: datetime
    end: datetime

    @property
    def duration(self) -> timedelta:
        return self.end - self.start


@dataclass
class Task:
    name: str
    duration: int                       # minutes
    priority: str
    frequency: Optional[timedelta] = None
    last_performed: Optional[datetime] = None
    is_complete: bool = False
    pet: Optional[Pet] = None           # back-reference to owning pet

    def mark_complete(self) -> None:
        pass

    def edit_task(self, field: str, value) -> None:
        pass

    def remove_task(self) -> None:
        # uses self.pet back-reference to remove itself from the pet's task list
        pass

    def get_time_since_last_performed(self) -> Optional[timedelta]:
        pass

    def is_overdue(self) -> bool:
        # requires self.frequency to be set to determine overdue status
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

    def get_incomplete_tasks(self) -> list[Task]:
        pass

    def get_overdue_tasks(self) -> list[Task]:
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

    def get_all_tasks(self) -> list[Task]:
        # aggregates tasks across all pets in self.pets
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.schedule: dict[TimeSlot, Task] = {}
        self.availability: dict[date, list[TimeSlot]] = {}

    def add_task(self, task: Task, slot: TimeSlot) -> None:
        # validate: slot.duration >= timedelta(minutes=task.duration) before scheduling
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def edit_task_time_slot(self, task: Task, new_slot: TimeSlot) -> None:
        pass

    def set_availability(self, day: date, slots: list[TimeSlot]) -> None:
        pass

    def get_schedule_for_day(self, day: date) -> dict[TimeSlot, Task]:
        pass

    def get_unscheduled_tasks(self) -> list[Task]:
        # returns tasks on owner's pets that have not been placed in any slot
        pass

    def get_tasks_by_priority(self, priority: str) -> list[Task]:
        pass

    def sort_tasks_by_priority(self) -> list[Task]:
        pass
