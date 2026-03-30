# PawPal+ Project Reflection

## 1. System Design

- 3 core actions a user should be able to perform:
    - Adding a pet, adding/removing tasks, set times available for walking.

**a. Initial design**

- Briefly describe your initial UML design.
    - The Owner can own many pets, but a pet can only belong to 1 owner
    - The Pet can have many tasks, but a task can be assigned to one pet
    - The Task is scheduled by the scheduler. A scheduler can schedule many tasks, but a task can be assigned to one schedule
- What classes did you include, and what responsibilities did you assign to each?
    - Owner owns a pet and sets the pets attributes. Pet adds and removes tasks and is responsible for calculating the pets age based on the pets birthday. Task class is responsible for editing the tasks contents. It is also responsible for keeping track of which tasks have been completed. The scheduler class is responsible for scheduling tasks throughout the days they are needed.

**b. Design changes**

- Did your design change during implementation?
    - Yes
- If yes, describe at least one change and why you made it.
    - is_overdue() has no frequency/interval to compare against
    is_overdue() can't determine if a task is overdue without knowing how often it should recur (e.g. daily, weekly). Task has no frequency or interval attribute, so this method can never be meaningfully implemented as-is.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - The new detect_conflicts() uses O(n²) pair comparisons instead of a faster sort-then-sweep approach.
- Why is that tradeoff reasonable for this scenario?
    - A pet owner will never have enough daily tasks for the performance difference to matter. Clarity wins over premature optimization at this scale.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - Designing the app through a UML diagram, implementing logic using the UML diagram, debugging, writing tests, UI, and refactoring.
- What kinds of prompts or questions were most helpful?
    - Questions where you get an explanation back.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - N/A
- How did you evaluate or verify what the AI suggested?
    - N/A

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    - Testing of the conflict detector and the sorting of tasks.
- Why were these tests important?
    - It is important that the user recieves accurate information.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    - Very confident. 8/10
- What edge cases would you test next if you had more time?
    - Pets with the same names. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - Understanding how to get the best out of the AI responses.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    - I would improve the UI to make it to where once you create a profile, it takes you to another screen rather than unlocking more things below in the same screen.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    - System design is a lot more complex than I though, as shown by my UML diagrams before and after I was done. The UML diagram was way more complicated after all the AI suggestions.
