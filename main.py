from datetime import date, datetime, timedelta
from pawpal_system import Owner, Pet, Task, TimeSlot, Scheduler

# --- Setup ---
owner = Owner(name="Angel Ramirez", email="angel@example.com")

dog = Pet(name="Star", pet_type="Dog", birthday=date(2021, 4, 10), weight=18.5)
cat = Pet(name="Rob", pet_type="Cat", birthday=date(2022, 9, 1), weight=4.2)

owner.pets.extend([dog, cat])

# --- Tasks ---
today = date.today()

morning_walk = Task(name="Morning Walk", duration=30, priority="high",   pet=dog, frequency=timedelta(days=1))
vet_checkup  = Task(name="Vet Checkup",  duration=60, priority="high",   pet=dog, frequency=timedelta(weeks=1))
feeding      = Task(name="Feeding",      duration=10, priority="medium",  pet=cat, frequency=timedelta(days=1))
grooming     = Task(name="Grooming",     duration=20, priority="low",     pet=cat)

dog.tasks.extend([morning_walk, vet_checkup])
cat.tasks.extend([feeding, grooming])

# --- Schedule (intentionally out of order) ---
scheduler = Scheduler(owner=owner)

def make_slot(hour: int, minute: int, duration_minutes: int) -> TimeSlot:
    start = datetime(today.year, today.month, today.day, hour, minute)
    return TimeSlot(start=start, end=start + timedelta(minutes=duration_minutes))

scheduler.schedule[make_slot(11, 0, 20)] = grooming       # added first
scheduler.schedule[make_slot(9,  0, 60)] = vet_checkup    # added second — overlaps grooming (9:00–10:00 vs 9:30 start below)
scheduler.schedule[make_slot(8,  0, 10)] = feeding        # added third
scheduler.schedule[make_slot(7,  0, 30)] = morning_walk   # added last

# Intentional conflict: bath starts at exactly 9:00, same as vet_checkup
bath = Task(name="Bath", duration=20, priority="medium", pet=dog)
dog.tasks.append(bath)
scheduler.schedule[make_slot(9, 0, 20)] = bath

# Complete recurring tasks — should auto-schedule next occurrences
print("=== Completing Recurring Tasks ===\n")
for task in [morning_walk, vet_checkup, feeding]:
    next_task = scheduler.complete_task(task)
    if next_task:
        freq_label = "daily" if task.frequency == timedelta(days=1) else "weekly"
        print(f"  '{task.name}' marked complete ({freq_label}) → next occurrence scheduled")
    else:
        print(f"  '{task.name}' marked complete (no recurrence)")
print()

# --- Print: Sorted by Time ---
print(f"=== Sorted by Time ({today.strftime('%A, %B %d %Y')}) ===\n")
print(f"Owner: {owner.name}  |  Pets: {', '.join(p.name for p in owner.pets)}\n")
print(f"{'Time':<22} {'Task':<20} {'Pet':<10} {'Duration':>10}  Priority   Complete")
print("-" * 80)

for slot, task in scheduler.sort_by_time():
    time_str = f"{slot.start.strftime('%I:%M %p')} – {slot.end.strftime('%I:%M %p')}"
    pet_name = task.pet.name if task.pet else "N/A"
    print(f"{time_str:<22} {task.name:<20} {pet_name:<10} {task.duration:>8} min  {task.priority:<10} {task.is_complete}")

# --- Print: Filter — incomplete tasks only ---
print(f"\n=== Filter: Incomplete Tasks Only ===\n")
for task in scheduler.filter_tasks(is_complete=False):
    pet_name = task.pet.name if task.pet else "N/A"
    print(f"  {task.name:<20} {pet_name:<10} {task.priority}")

# --- Print: Filter — tasks for Star (dog) ---
print(f"\n=== Filter: Tasks for Star ===\n")
for task in scheduler.filter_tasks(pet_name="Star"):
    pet_name = task.pet.name if task.pet else "N/A"
    print(f"  {task.name:<20} complete={task.is_complete}  priority={task.priority}")

# --- Print: Filter — incomplete tasks for Rob (cat) ---
print(f"\n=== Filter: Incomplete Tasks for Rob ===\n")
for task in scheduler.filter_tasks(pet_name="Rob", is_complete=False):
    print(f"  {task.name:<20} {task.duration} min  {task.priority}")

# --- Print: Conflict Detection ---
print(f"\n=== Conflict Detection ===\n")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for task_a, task_b in conflicts:
        pet_a = task_a.pet.name if task_a.pet else "N/A"
        pet_b = task_b.pet.name if task_b.pet else "N/A"
        print(f"  WARNING: '{task_a.name}' ({pet_a}) and '{task_b.name}' ({pet_b}) overlap — please reschedule one.")
else:
    print("  No conflicts detected. Schedule looks good!")
