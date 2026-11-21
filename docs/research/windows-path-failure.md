# Windows path identity correction

The first independent CI run tested commit 1c185a6a296dec5bac49f4c35786db9c064cd5fa. Ubuntu passed, while Windows reported 14 errors among 38 common tests before project acceptance could run.

Run: https://github.com/laadkke-arch/agentflow-open/actions/runs/43703805460
Windows job: 132780441458

The actual error compared resolved files under `C:\Users\runneradmin\...` with the unnormalized temporary root `C:\Users\RUNNER~1\...`. Those denote the same underlying location, but relative_to compares path components. The files had been resolved while the supplied root had not.

Correction: resolve the workspace root at the context, project, run, receipt, tracked-input and export boundaries, and resolve the receipt path before calculating its relative name. Existing path-escape and symlink-escape assertions remain unchanged. A new regression exercises context, execution, receipt verification and export through a directory alias. This does not weaken directory confinement.

Primary reference: https://docs.python.org/3.12/library/pathlib.html . The pathlib documentation distinguishes lexical relative-path operations from filesystem resolution.

Local canonical-root checks passed. The correction still requires a new independent Windows and Linux run; the old Ubuntu success is not evidence that the corrected revision passed.
