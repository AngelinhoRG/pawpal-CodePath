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
        """Mark this task as completed and record the time it was performed."""
        self.is_complete = True
        self.last_performed = datetime.now()

    def next_occurrence(self) -> Optional[Task]:
        """Return a new Task instance for the next recurrence, or None if not recurring."""
        if self.frequency is None:
            return None
        return Task(
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            frequency=self.frequency,
            pet=self.pet,
        )

    def edit_task(self, field: str, value) -> None:
        """Update a task field by name."""
        setattr(self, field, value)

    def remove_task(self) -> None:
        """Remove this task from its associated pet's task list."""
        if self.pet is not None:
            self.pet.remove_task(self)

    def get_time_since_last_performed(self) -> Optional[timedelta]:
        """Return elapsed time since the task was last performed, or None if never."""
        if self.last_performed is None:
            return None
        return datetime.now() - self.last_performed

    def is_overdue(self) -> bool:
        """Return True if the task is past its scheduled frequency."""
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
        """Return the pet's age in whole years."""
        today = date.today()
        age = today.year - self.birthday.year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            age -= 1
        return age

    def update_weight(self, new_weight: float) -> None:
        """Update the pet's recorded weight."""
        self.weight = new_weight

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)

    def list_tasks(self) -> list[Task]:
        """Return a copy of this pet's task list."""
        return list(self.tasks)

    def get_incomplete_tasks(self) -> list[Task]:
        """Return all tasks that have not been marked complete."""
        return [t for t in self.tasks if not t.is_complete]

    def get_overdue_tasks(self) -> list[Task]:
        """Return all tasks whose frequency interval has been exceeded."""
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
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def change_email(self, new_email: str) -> None:
        """Update the owner's email address."""
        self.email = new_email

    def change_name(self, new_name: str) -> None:
        """Update the owner's display name."""
        self.name = new_name

    def get_all_tasks(self) -> list[Task]:
        """Return a flat list of every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.schedule: dict[TimeSlot, Task] = {}
        self.availability: dict[date, list[TimeSlot]] = {}

    def add_task(self, task: Task, slot: TimeSlot) -> None:
        """Schedule a task into a time slot if the slot is long enough."""
        if slot.duration >= timedelta(minutes=task.duration):
            self.schedule[slot] = task

    def remove_task(self, task: Task) -> None:
        """Remove a task and its time slot from the schedule."""
        slot = next((s for s, t in self.schedule.items() if t is task), None)
        if slot is not None:
            del self.schedule[slot]

    def edit_task_time_slot(self, task: Task, new_slot: TimeSlot) -> None:
        """Reschedule a task to a new time slot."""
        self.remove_task(task)
        self.add_task(task, new_slot)

    def set_availability(self, day: date, slots: list[TimeSlot]) -> None:
        """Record the available time slots for a given day."""
        self.availability[day] = slots

    def get_schedule_for_day(self, day: date) -> dict[TimeSlot, Task]:
        """Return all scheduled tasks occurring on a specific date."""
        return {slot: task for slot, task in self.schedule.items() if slot.start.date() == day}

    def get_unscheduled_tasks(self) -> list[Task]:
        """Return tasks belonging to the owner's pets that have no scheduled slot."""
        scheduled = set(self.schedule.values())
        return [task for pet in self.owner.pets for task in pet.tasks if task not in scheduled]

    def get_tasks_by_priority(self, priority: str) -> list[Task]:
        """Return all scheduled tasks matching the given priority level."""
        return [task for task in self.schedule.values() if task.priority == priority]

    def sort_tasks_by_priority(self) -> list[Task]:
        """Return all scheduled tasks sorted high → medium → low priority."""
        order = {"high": 0, "medium": 1, "low": 2}
        return sorted(self.schedule.values(), key=lambda t: order.get(t.priority, 99))

    def sort_by_time(self) -> list[tuple[TimeSlot, Task]]:
        """Return all scheduled (slot, task) pairs sorted by start time."""
        return sorted(self.schedule.items(), key=lambda item: item[0].start)

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs of tasks whose time slots overlap.

        Two slots conflict when one starts before the other ends:
            a.start < b.end  AND  a.end > b.start
        """
        pairs = list(self.schedule.items())
        conflicts = []
        for i in range(len(pairs)):
            slot_a, task_a = pairs[i]
            for j in range(i + 1, len(pairs)):
                slot_b, task_b = pairs[j]
                if slot_a.start < slot_b.end and slot_a.end > slot_b.start:
                    conflicts.append((task_a, task_b))
        return conflicts

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete and, if recurring, schedule the next occurrence.

        Returns the new Task if one was created, otherwise None.
        """
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is None:
            return None
        next_start = task.last_performed + task.frequency
        next_slot = TimeSlot(
            start=next_start,
            end=next_start + timedelta(minutes=next_task.duration),
        )
        self.add_task(next_task, next_slot)
        if next_task.pet is not None:
            next_task.pet.add_task(next_task)
        return next_task

    def filter_tasks(
        self,
        *,
        pet_name: Optional[str] = None,
        is_complete: Optional[bool] = None,
    ) -> list[Task]:
        """Return scheduled tasks filtered by pet name and/or completion status."""
        tasks = list(self.schedule.values())
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet is not None and t.pet.name == pet_name]
        if is_complete is not None:
            tasks = [t for t in tasks if t.is_complete == is_complete]
        return tasks
