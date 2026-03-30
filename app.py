import streamlit as st
from datetime import date, datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler, TimeSlot

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")
st.title("🐾 PawPal+")

# ── Session state ────────────────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

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

col_gen, col_reset = st.columns([1, 1])
with col_gen:
    if st.button("Generate schedule", use_container_width=True):
        scheduler = Scheduler(owner)
        # Assign back-to-back slots starting at 08:00 for every unscheduled task.
        cursor = datetime.combine(date.today(), datetime.min.time()).replace(hour=8)
        for task in scheduler.get_unscheduled_tasks():
            slot = TimeSlot(start=cursor, end=cursor + timedelta(minutes=task.duration))
            scheduler.add_task(task, slot)
            cursor = slot.end
        st.session_state.scheduler = scheduler

with col_reset:
    if st.button("Clear schedule", use_container_width=True):
        st.session_state.scheduler = None

scheduler: Scheduler | None = st.session_state.scheduler

if scheduler is None:
    st.info("Click 'Generate schedule' to build today's plan.")
else:
    # ── Conflict detection ───────────────────────────────────────────────────
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.warning(f"**{len(conflicts)} scheduling conflict(s) detected!** Resolve by removing or rescheduling overlapping tasks.")
        with st.expander("See conflicting tasks"):
            for task_a, task_b in conflicts:
                st.write(f"- **{task_a.name}** overlaps with **{task_b.name}**")
    else:
        st.success("No scheduling conflicts — your day is conflict-free!")

    st.divider()

    # ── Filter controls ──────────────────────────────────────────────────────
    st.subheader("Filter & View Schedule")
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        all_pet_names = [p.name for p in owner.pets]
        filter_pet = st.selectbox(
            "Filter by pet",
            options=["All pets"] + all_pet_names,
        )
    with filter_col2:
        filter_status = st.selectbox(
            "Filter by status",
            options=["All", "Incomplete only", "Complete only"],
        )
    with filter_col3:
        sort_mode = st.selectbox(
            "Sort by",
            options=["Time (chronological)", "Priority (high first)"],
        )

    # Resolve filter args
    pet_name_arg = None if filter_pet == "All pets" else filter_pet
    complete_arg = None
    if filter_status == "Incomplete only":
        complete_arg = False
    elif filter_status == "Complete only":
        complete_arg = True

    # Get filtered tasks
    filtered_tasks = scheduler.filter_tasks(pet_name=pet_name_arg, is_complete=complete_arg)
    filtered_slots = {s: t for s, t in scheduler.schedule.items() if t in filtered_tasks}

    # Sort the filtered results
    if sort_mode == "Time (chronological)":
        # sort_by_time returns (slot, task) pairs for the whole schedule; filter afterwards
        sorted_pairs = [(s, t) for s, t in scheduler.sort_by_time() if t in filtered_tasks]
    else:
        priority_order = {"high": 0, "medium": 1, "low": 2}
        slot_map = {t: s for s, t in scheduler.schedule.items()}
        priority_sorted = sorted(filtered_tasks, key=lambda t: priority_order.get(t.priority, 99))
        sorted_pairs = [(slot_map[t], t) for t in priority_sorted if t in slot_map]

    if not sorted_pairs:
        st.info("No tasks match the current filters.")
    else:
        priority_colors = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        table_rows = []
        for slot, task in sorted_pairs:
            table_rows.append({
                "Time": f"{slot.start.strftime('%H:%M')} – {slot.end.strftime('%H:%M')}",
                "Task": task.name,
                "Pet": task.pet.name if task.pet else "—",
                "Duration (min)": task.duration,
                "Priority": f"{priority_colors.get(task.priority, '')} {task.priority}",
                "Status": "✅ Done" if task.is_complete else "⏳ Pending",
            })
        st.table(table_rows)

    st.divider()

    # ── Mark tasks complete ──────────────────────────────────────────────────
    st.subheader("Mark Tasks Complete")
    incomplete_scheduled = [(s, t) for s, t in scheduler.sort_by_time() if not t.is_complete]
    if not incomplete_scheduled:
        st.success("All scheduled tasks are complete — great work!")
    else:
        for slot, task in incomplete_scheduled:
            pet_label = f" ({task.pet.name})" if task.pet else ""
            time_label = f"{slot.start.strftime('%H:%M')}–{slot.end.strftime('%H:%M')}"
            btn_label = f"Complete: {task.name}{pet_label} @ {time_label}"
            if st.button(btn_label, key=f"complete_{id(task)}"):
                next_task = scheduler.complete_task(task)
                if next_task:
                    st.success(f"Done! Next '{next_task.name}' auto-scheduled.")
                else:
                    st.success(f"'{task.name}' marked complete!")
                st.rerun()
