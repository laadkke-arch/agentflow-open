# Evidence-first work procedure

Use this procedure for a bounded research/implementation task. It is not an installed ChatGPT skill or an autonomous service.

1. Read the selected project BRIEF, STATE and DECISIONS, not another project's state.
2. Compare at least two existing approaches against the acceptance cases. Record URL, date, claim, evidence level, decision and reason in sources.json. A third-party README is evidence of what its author says, not proof of our execution.
3. Choose a small implementation surface. Reuse standard tools and tested shared utilities; do not copy another project's state or private data.
4. Run the manifest-declared test and demo tasks. Inspect stdout/stderr and the receipt, including return code, exact inputs and source revision. Do not lower assertions just to obtain a pass.
5. Correct real failures and retain the cause, regression test and limitation. Promote an observation to a shared rule only when its scope is understood and a second task has exercised it.
6. Update project STATE with current choice, completed checks and next action. Keep rejected alternatives in DECISIONS; do not present old choices as current.
7. Export to a new directory when checking portability; run there with no original PYTHONPATH. This tests filesystem/process handover, not a fresh model conversation.

## Boundaries

Only reviewed repository tasks may execute. Python processes inherit the account's OS authority: this wrapper is not a sandbox. Do not place secrets in context files or stdout. Network lookups, installing third-party agents, deploying, changing permissions, and paid resources require their own authorized step. No daemon, schedule, account-limit workaround, or infinite retry is supplied.

## Reproduction

`python -m workbench context PROJECT --query contract`

`python -m workbench run PROJECT test`

`python -m workbench run PROJECT demo`

`python -m workbench verify-receipt PROJECT .workbench/runs/PROJECT/RUN/receipt.json`

The receipt proves only consistency with the declared inputs and log files. It is not a signature or proof of complete tests.
