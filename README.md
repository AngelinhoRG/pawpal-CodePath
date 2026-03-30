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
