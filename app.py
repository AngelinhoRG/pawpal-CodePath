import streamlit as st
from datetime import date, datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler, TimeSlot

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Session state ────────────────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None

# ── Owner setup ──────────────────────────────────────────────────────────────
st.subheader("Owner")
with st.form("owner_form"):
    owner_name = st.text_input("Your name", value="Jordan")
    owner_email = st.text_input("Email", value="")
    if st.form_submit_button("Set Owner"):
        st.session_state.owner = Owner(owner_name, owner_email)

if st.session_state.owner is None:
    st.info("Enter your name above to get started.")
    st.stop()

owner: Owner = st.session_state.owner
st.success(f"Owner: {owner.name}")

st.divider()

# ── Add a Pet ────────────────────────────────────────────────────────────────
st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    birthday = st.date_input("Birthday", value=date(2020, 1, 1))
    weight = st.number_input("Weight (lbs)", min_value=0.1, value=10.0)
    if st.form_submit_button("Add Pet"):
        # Owner.add_pet() is the method that handles this data.
        # It appends the new Pet to owner.pets so every downstream widget
        # that reads owner.pets will reflect the addition on the next rerun.
        new_pet = Pet(pet_name, species, birthday, weight)
        owner.add_pet(new_pet)
        st.success(f"Added {new_pet.name} to {owner.name}'s pets.")

if not owner.pets:
    st.info("No pets yet. Add one above.")
    st.stop()

# ── Select active pet ────────────────────────────────────────────────────────
pet_names = [p.name for p in owner.pets]
chosen = st.selectbox(
    f"Active pet ({owner.num_pets} total)",
    options=range(len(owner.pets)),
    format_func=lambda i: owner.pets[i].name,
)
active_pet: Pet = owner.pets[chosen]
st.caption(
    f"{active_pet.name} | {active_pet.pet_type} | "
    f"Age: {active_pet.calculate_age()} yr | {active_pet.weight} lbs"
)

st.divider()

# ── Schedule a Task ──────────────────────────────────────────────────────────
st.subheader("Schedule a Task")
with st.form("add_task_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    if st.form_submit_button("Add Task"):
        # Pet.add_task() appends the Task to active_pet.tasks.
        # Setting task.pet enables task.remove_task() to work correctly.
        task = Task(name=task_title, duration=int(duration), priority=priority)
        task.pet = active_pet
        active_pet.add_task(task)

incomplete = active_pet.get_incomplete_tasks()
if incomplete:
    st.write(f"Tasks for {active_pet.name}:")
    st.table(
        [
            {"name": t.name, "duration (min)": t.duration, "priority": t.priority}
            for t in incomplete
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Generate schedule ────────────────────────────────────────────────────────
st.subheader("Build Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(owner)

    # Assign back-to-back slots starting at 08:00 for every unscheduled task.
    cursor = datetime.combine(date.today(), datetime.min.time()).replace(hour=8)
    for task in scheduler.get_unscheduled_tasks():
        slot = TimeSlot(start=cursor, end=cursor + timedelta(minutes=task.duration))
        scheduler.add_task(task, slot)
        cursor = slot.end

    ordered = scheduler.sort_tasks_by_priority()
    if ordered:
        st.success("Schedule generated (high → medium → low priority):")
        st.table(
            [
                {"task": t.name, "duration (min)": t.duration, "priority": t.priority}
                for t in ordered
            ]
        )
    else:
        st.warning("No tasks to schedule. Add some tasks first.")
