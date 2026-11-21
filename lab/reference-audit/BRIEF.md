# Research reference audit laboratory

Purpose: detect unresolved [source:id] citations in a research note, and redundant repository-root source identities. This is a separate project exercising the shared workbench.

Project-only marker: AUDIT_ONLY_9E52. No repository-intake project state belongs here.

Acceptance: missing and duplicate source ids fail; unused references are reported; a documentation subpage never collapses into its repository root. Reuse workbench/urls.py rather than copying it. This is reference integrity, not claim verification.
