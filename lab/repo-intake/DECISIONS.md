# Decisions

## 001 Use the standard parser with a narrow contract

Adopt urllib.parse, not a new general URL parser. Compare w3lib and yarl in RESEARCH.md. Keep the GitHub identity policy in workbench/urls.py for reuse. Exact source pages remain distinct from repository identities.

## 002 Rejection is not absence

An unsupported URL goes to manual review; it is not proof that the source is invalid or nonexistent. Do not fetch URLs or echo credential-bearing values in reports.
