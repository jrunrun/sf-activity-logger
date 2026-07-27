# plan

Think like a senior engineer.

First, inspect the existing code and produce an implementation plan before making changes.

Your plan should:
- summarize the task
- identify the exact existing code involved
- explain the intended approach
- list the files to modify
- note assumptions, unknowns, and risks
- provide a minimal ordered sequence of implementation steps
- define how success will be tested

Constraints:
- Do not code until the plan is complete.
- Do not assume architecture; confirm it from the repo.
- Reuse existing patterns where possible.
- Minimize blast radius.
- Avoid unnecessary refactors unless required.
- If the plan changes after inspection, update the plan before coding.

After producing the plan, sanity-check it for correctness and simplicity, then implement.

This command will be available in chat with /plan
