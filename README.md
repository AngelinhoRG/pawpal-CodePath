# PawPal+ (Module 2 Project)

## 📸 Demo

**Owner setup and pet management**

<a href='/Pawpal-Codepath/Screenshot 2026-03-29 at 11.42.23 PM.png' target='_blank'><img src='/Pawpal-Codepath/Screenshot 2026-03-29 at 11.42.23 PM.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

**Adding a pet with species, birthday, and weight**

<a href='/Pawpal-Codepath/Screenshot 2026-03-29 at 11.43.43 PM.png' target='_blank'><img src='/Pawpal-Codepath/Screenshot 2026-03-29 at 11.43.43 PM.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

**Scheduling tasks with duration and priority**

<a href='/Pawpal-Codepath/Screenshot 2026-03-29 at 11.44.46 PM.png' target='_blank'><img src='/Pawpal-Codepath/Screenshot 2026-03-29 at 11.44.46 PM.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

---

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

## Features

- **Pet profiles** — Store each pet's name, type, birthday, and weight. Age is calculated automatically from the birthday so it never goes stale.
- **Task management** — Add, edit, and remove care tasks (walks, feeding, meds, grooming, etc.) with a name, duration, priority, and optional recurrence frequency.
- **Completion tracking** — Mark tasks complete with a timestamp. Each task carries an `is_complete` flag for the current cycle alongside a `last_performed` history.
- **Overdue detection** — Tasks with a set frequency automatically flag themselves as overdue when the interval since `last_performed` is exceeded.
- **Recurring tasks** — Tasks with a frequency auto-schedule their next occurrence the moment they are completed, with no manual input required.
- **Conflict warnings** — The scheduler scans all scheduled task pairs and reports any whose time slots overlap, so clashes are visible before they become a problem.
- **Sort by time** — The daily plan is always displayed in chronological order regardless of the order tasks were added.
- **Priority sorting** — Tasks can be sorted high → medium → low so the most important care items surface first.
- **Filter by pet or status** — Narrow the schedule by pet name, completion status, or both to quickly see what still needs to be done.
- **Availability-aware scheduling** — The owner inputs which time slots are free on a given day; the scheduler only assigns tasks to slots that are long enough to fit them.

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
