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
        self.is_complete = True

    def edit_task(self, field: str, value) -> None:
        setattr(self, field, value)

    def remove_task(self) -> None:
        # uses self.pet back-reference to remove itself from the pet's task list
        if self.pet is not None:
            self.pet.remove_task(self)

    def get_time_since_last_performed(self) -> Optional[timedelta]:
        if self.last_performed is None:
            return None
        return datetime.now() - self.last_performed

    def is_overdue(self) -> bool:
        # requires self.frequency to be set to determine overdue status
        if self.frequency is None or self.last_performed is None:
            return False
        return datetime.now() - self.last_performed > self.frequency


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
        today = date.today()
        age = today.year - self.birthday.year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            age -= 1
        return age

    def update_weight(self, new_weight: float) -> None:
        self.weight = new_weight

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        self.tasks.remove(task)

    def list_tasks(self) -> list[Task]:
        return list(self.tasks)

    def get_incomplete_tasks(self) -> list[Task]:
        return [t for t in self.tasks if not t.is_complete]

    def get_overdue_tasks(self) -> list[Task]:
        return [t for t in self.tasks if t.is_overdue()]


class Owner:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: list[Pet] = []

    @property
    def num_pets(self) -> int:
        return len(self.pets)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def change_email(self, new_email: str) -> None:
        self.email = new_email

    def change_name(self, new_name: str) -> None:
        self.name = new_name

    def get_all_tasks(self) -> list[Task]:
        # aggregates tasks across all pets in self.pets
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.schedule: dict[TimeSlot, Task] = {}
        self.availability: dict[date, list[TimeSlot]] = {}

    def add_task(self, task: Task, slot: TimeSlot) -> None:
        # validate: slot.duration >= timedelta(minutes=task.duration) before scheduling
        if slot.duration >= timedelta(minutes=task.duration):
            self.schedule[slot] = task

    def remove_task(self, task: Task) -> None:
        slot = next((s for s, t in self.schedule.items() if t is task), None)
        if slot is not None:
            del self.schedule[slot]

    def edit_task_time_slot(self, task: Task, new_slot: TimeSlot) -> None:
        self.remove_task(task)
        self.add_task(task, new_slot)

    def set_availability(self, day: date, slots: list[TimeSlot]) -> None:
        self.availability[day] = slots

    def get_schedule_for_day(self, day: date) -> dict[TimeSlot, Task]:
        return {slot: task for slot, task in self.schedule.items() if slot.start.date() == day}

    def get_unscheduled_tasks(self) -> list[Task]:
        # returns tasks on owner's pets that have not been placed in any slot
        scheduled = set(self.schedule.values())
        return [task for pet in self.owner.pets for task in pet.tasks if task not in scheduled]

    def get_tasks_by_priority(self, priority: str) -> list[Task]:
        return [task for task in self.schedule.values() if task.priority == priority]

    def sort_tasks_by_priority(self) -> list[Task]:
        order = {"high": 0, "medium": 1, "low": 2}
        return sorted(self.schedule.values(), key=lambda t: order.get(t.priority, 99))
