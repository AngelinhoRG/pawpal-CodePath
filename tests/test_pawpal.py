import pytest
from datetime import date
from pawpal_system import Pet, Task


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
