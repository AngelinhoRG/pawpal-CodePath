# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

PawPal+ includes four algorithms that make the scheduler more intelligent:

- **Sort by time** — `Scheduler.sort_by_time()` orders all scheduled tasks chronologically using each task's `TimeSlot.start`, so the daily plan always displays in the correct sequence regardless of the order tasks were added.
- **Filter by pet or status** — `Scheduler.filter_tasks()` lets you narrow the schedule by pet name, completion status, or both. Useful for quickly seeing what's still left to do for a specific pet.
- **Recurring tasks** — Tasks with a `frequency` (e.g. `timedelta(days=1)` for daily, `timedelta(weeks=1)` for weekly) auto-schedule their next occurrence when completed via `Scheduler.complete_task()`. The next slot is calculated as `last_performed + frequency`.
- **Conflict detection** — `Scheduler.detect_conflicts()` scans all scheduled task pairs and returns any whose time slots overlap. It prints a warning rather than crashing, so the owner can reschedule without losing any data.

## Testing PawPal+

### Run the tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Test | What it verifies |
|---|---|
| `test_mark_complete_changes_status` | `mark_complete()` flips `is_complete` from `False` to `True` |
| `test_add_task_increases_pet_task_count` | `add_task()` correctly grows a pet's task list |
| `test_sort_by_time_returns_chronological_order` | `sort_by_time()` returns tasks ordered by earliest start time, regardless of insertion order |
| `test_complete_daily_task_schedules_next_day` | Completing a recurring task auto-schedules the next occurrence exactly `frequency` time later |
| `test_detect_conflicts_flags_overlapping_tasks` | `detect_conflicts()` identifies two tasks sharing the same time slot as a conflicting pair |

### Confidence level

**3 / 5 stars**

The core behaviors — task completion, recurring scheduling, sort order, and conflict detection — are verified and passing. Confidence is kept at 3 stars because the tests do not yet cover edge cases such as: a pet with no tasks, tasks whose time slots touch but do not overlap (boundary conditions), non-recurring tasks that should not spawn a successor, or the Streamlit UI layer (`app.py`). Expanding coverage to those cases would raise confidence to 4–5 stars.

---

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
