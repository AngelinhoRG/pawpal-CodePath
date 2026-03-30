import pytest
from datetime import date, datetime, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task, TimeSlot


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def dog():
    return Pet(name="Star", pet_type="Dog", birthday=date(2021, 4, 10), weight=18.5)


@pytest.fixture
def task(dog):
    return Task(name="Morning Walk", duration=30, priority="high", pet=dog)


# ── Task Completion ──────────────────────────────────────────────────────────

def test_mark_complete_changes_status(task):
    """mark_complete() should set is_complete to True."""
    assert task.is_complete is False
    task.mark_complete()
    assert task.is_complete is True


# ── Task Addition ────────────────────────────────────────────────────────────

def test_add_task_increases_pet_task_count(dog):
    """add_task() should increase the pet's task count by one."""
    initial_count = dog.num_tasks
    new_task = Task(name="Feeding", duration=10, priority="medium", pet=dog)
    dog.add_task(new_task)
    assert dog.num_tasks == initial_count + 1


# ── Sorting ──────────────────────────────────────────────────────────────────

def test_sort_by_time_returns_chronological_order():
    """sort_by_time() should return tasks ordered earliest start time first."""
    owner = Owner(name="Alex", email="alex@example.com")
    dog = Pet(name="Buddy", pet_type="Dog", birthday=date(2020, 1, 1), weight=10.0)
    owner.add_pet(dog)
    scheduler = Scheduler(owner)

    base = datetime(2024, 1, 1, 8, 0)
    task_late  = Task(name="Bath",       duration=20, priority="low",    pet=dog)
    task_early = Task(name="Walk",       duration=30, priority="high",   pet=dog)
    task_mid   = Task(name="Medication", duration=10, priority="medium", pet=dog)

    scheduler.add_task(task_late,  TimeSlot(start=base + timedelta(hours=2), end=base + timedelta(hours=2, minutes=20)))
    scheduler.add_task(task_early, TimeSlot(start=base,                      end=base + timedelta(minutes=30)))
    scheduler.add_task(task_mid,   TimeSlot(start=base + timedelta(hours=1), end=base + timedelta(hours=1, minutes=10)))

    ordered = [task for _, task in scheduler.sort_by_time()]
    assert ordered == [task_early, task_mid, task_late]


# ── Recurrence ───────────────────────────────────────────────────────────────

def test_complete_daily_task_schedules_next_day():
    """Completing a daily recurring task should create a new task 24 hours later."""
    owner = Owner(name="Alex", email="alex@example.com")
    dog = Pet(name="Buddy", pet_type="Dog", birthday=date(2020, 1, 1), weight=10.0)
    owner.add_pet(dog)
    scheduler = Scheduler(owner)

    base = datetime(2024, 1, 1, 7, 0)
    walk = Task(name="Morning Walk", duration=30, priority="high", frequency=timedelta(days=1), pet=dog)
    dog.add_task(walk)
    scheduler.add_task(walk, TimeSlot(start=base, end=base + timedelta(minutes=30)))

    next_task = scheduler.complete_task(walk)

    assert next_task is not None
    # The new slot should start exactly one day after last_performed
    next_slot = next(slot for slot, task in scheduler.schedule.items() if task is next_task)
    assert next_slot.start == walk.last_performed + timedelta(days=1)


# ── Conflict Detection ───────────────────────────────────────────────────────

def test_detect_conflicts_flags_overlapping_tasks():
    """detect_conflicts() should return a pair for tasks scheduled at the same time."""
    owner = Owner(name="Alex", email="alex@example.com")
    dog = Pet(name="Buddy", pet_type="Dog", birthday=date(2020, 1, 1), weight=10.0)
    owner.add_pet(dog)
    scheduler = Scheduler(owner)

    base = datetime(2024, 1, 1, 9, 0)
    task_a = Task(name="Bath",       duration=20, priority="low",  pet=dog)
    task_b = Task(name="Vet Checkup",duration=60, priority="high", pet=dog)

    # Both start at 09:00 — fully overlapping
    scheduler.add_task(task_a, TimeSlot(start=base, end=base + timedelta(minutes=20)))
    scheduler.add_task(task_b, TimeSlot(start=base, end=base + timedelta(minutes=60)))

    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert task_a in conflicts[0] and task_b in conflicts[0]
