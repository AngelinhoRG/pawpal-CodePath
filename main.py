from datetime import date, datetime
from pawpal_system import Owner, Pet, Task, TimeSlot, Scheduler

# --- Setup ---
owner = Owner(name="Angel Ramirez", email="angel@example.com")

dog = Pet(name="Star", pet_type="Dog", birthday=date(2021, 4, 10), weight=18.5)
cat = Pet(name="Rob", pet_type="Cat", birthday=date(2022, 9, 1), weight=4.2)

owner.pets.extend([dog, cat])

# --- Tasks ---
today = date.today()

morning_walk = Task(name="Morning Walk", duration=30, priority="high", pet=dog)
vet_checkup  = Task(name="Vet Checkup",  duration=60, priority="high", pet=dog)
feeding      = Task(name="Feeding",      duration=10, priority="medium", pet=cat)
grooming     = Task(name="Grooming",     duration=20, priority="low", pet=cat)

dog.tasks.extend([morning_walk, vet_checkup])
cat.tasks.extend([feeding, grooming])

# --- Schedule ---
scheduler = Scheduler(owner=owner)

def make_slot(hour: int, minute: int, duration_minutes: int) -> TimeSlot:
    start = datetime(today.year, today.month, today.day, hour, minute)
    from datetime import timedelta
    return TimeSlot(start=start, end=start + timedelta(minutes=duration_minutes))

scheduler.schedule[make_slot(7, 0, 30)]  = morning_walk
scheduler.schedule[make_slot(9, 0, 60)]  = vet_checkup
scheduler.schedule[make_slot(8, 0, 10)]  = feeding
scheduler.schedule[make_slot(11, 0, 20)] = grooming

# --- Print Today's Schedule ---
print(f"=== Today's Schedule ({today.strftime('%A, %B %d %Y')}) ===\n")
print(f"Owner: {owner.name}  |  Pets: {', '.join(p.name for p in owner.pets)}\n")
print(f"{'Time':<22} {'Task':<20} {'Pet':<10} {'Duration':>10}  Priority")
print("-" * 72)

sorted_slots = sorted(scheduler.schedule.items(), key=lambda item: item[0].start)
for slot, task in sorted_slots:
    time_str = f"{slot.start.strftime('%I:%M %p')} – {slot.end.strftime('%I:%M %p')}"
    pet_name = task.pet.name if task.pet else "N/A"
    print(f"{time_str:<22} {task.name:<20} {pet_name:<10} {task.duration:>8} min  {task.priority}")

print()
