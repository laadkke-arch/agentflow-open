# Decisions

## 001 Use explicit source markers

This lab uses [source:id] rather than attempting to parse all Markdown syntax. GitHub URLs are classified using the tested shared repository_key helper; documentation pages keep their own source ids.

## 002 Reuse only the contract

The shared utility is reused; the other project's fixtures, decisions and state are not imported. A matching source id does not certify a claim, a license, or a live URL.
