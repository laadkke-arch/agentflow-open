# Workbench tool decisions

Checked 2026-11-15. These are scoped adoption choices, not rankings of overall product quality.

| Candidate | Evidence inspected | Decision and reason | Execution evidence |
| --- | --- | --- | --- |
| Python unittest | https://docs.python.org/3/library/unittest.html | Adopt existing test discovery, fixtures and assertions; do not write a new test framework. | Used for runtime and both laboratory tasks. |
| urllib.parse | https://docs.python.org/3/library/urllib.parse.html | Adopt component parsing with explicit root-repository constraints. The documentation warns parsing is not validation. | Used in both tasks. Empty credential fields produced a regression and were fixed. |
| w3lib canonicalize_url | https://w3lib.readthedocs.io/en/latest/w3lib.html | Defer for this task: query sorting/fragment removal are generic crawling choices, not repository identity. | Documentation only; no package installation. |
| yarl URL | https://yarl.aio-libs.org/en/stable/api/ | Reference for structured URL handling, not necessary for the current dependency-free runtime. | Optional local comparison used already-installed 1.24.2; see url-comparison.json. |
| Nox | https://nox.thea.codes/en/stable/ | Defer until multi-environment dependency management is needed. The wrapper only ties project context and execution receipts together; it does not replace Nox environments. | Documentation only. |
| uv | https://docs.astral.sh/uv/guides/projects/ | Defer dependency resolution because this prototype has no third-party runtime dependencies. Use frozen lockfiles when product dependencies are introduced. | Documentation only. |
| urllib3's Nox/uv setup | https://github.com/urllib3/urllib3/blob/main/noxfile.py | Reference real upstream usage of frozen dependency sync, explicit environments and separate test sessions. Do not copy the whole configuration. | Read first 150 lines; file blob 1a889bfb2d29ad2dcd52c91ddc9f8a536c74daba. |
| Git bundle | https://git-scm.com/docs/git-bundle | Adopt Git's existing export/verification/restore machinery instead of a custom Git backup format. | Required remote acceptance creates a bundle, verifies it, restores exact commit, runs demo. Not a backup of DB, secrets, issues or LFS. |
| GitHub artifacts | https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts | Adopt bounded retention for run outputs, not permanent Git storage. | CI is configured to upload explicit evidence files with seven-day retention; consult the actual run for confirmation. |

## Failure and correction

The initial implementation used truthiness for parsed username/password. Empty credential fields are empty strings, not None, so https://@github.com/a/b and ssh://git:@github.com/a/b were incorrectly accepted. The first test run reported two failures. Change: check presence with `is not None`. Assertions were unchanged; both acceptance tasks use the corrected helper. A source-record validation test also covers the empty-credential case. An excerpt of the actual local transcript is in initial-failure.txt.

A subsequent review covered tasks deleting declared input files. Previously receipt creation could abort while hashing the missing file. The runtime now emits an inputs-changed failure receipt with a tracking error. A regression test ensures zero process exit does not hide this failure.

## Current execution constraints

The authoring container could not resolve github.com for git clone. No credentials or alternate tunnel were introduced. Files are written through the authorized GitHub connector; local Python checks do not need network; the independent Actions checkout is responsible for the exact-commit and Git-backup checks. This explains the current choice, not a universal preference for connector editing.

## Infinite usage is not a technical design assumption

The supplied community post described continuing conversations and accumulating records. This environment does not make reasoning, tools, storage or compute unlimited and does not continue the assistant after a reply. Each task has a timeout and one attempt. Any future autonomous model worker would be a separate, explicitly authorized service with credentials, budget, stopping conditions and review.

Current official references: https://help.openai.com/en/articles/12003714-chatgpt-business-models-and-limits and https://docs.github.com/en/actions/reference/limits . Do not use an unlimited-use claim as a system guarantee.
