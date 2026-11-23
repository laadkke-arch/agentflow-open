# Graph release metadata — before scope seal

- d3-force many-body: component release **v3.0.0**, published 2021-06-05T19:12:11Z, source commit `156712c8c3285d77cb487e1685c5adafcd0394a4`. v3.0.1 is after cutoff and excluded. Node >=12, ESM; UMD bundle export exists. Browser ES2015 boundary follows v2 release note, not a separately measured compatibility result.
- Graphviz sfdp: bundled engine in stable Graphviz **14.1.1**, published 2025-12-13T20:42:20.852Z, source commit `a74b50c20fc624f46f72e24f981b261f6e5edf71`. No independently versioned sfdp release was observed. `with_sfdp` is ON in the tagged build configuration and `lib/sfdpgen` exists. Next stable 14.1.2 is 2026-01-24, outside cutoff.
- Tagged Graphviz release assets: Windows 10 32/64, Fedora 41/42, Darwin 23.6.0/arm64, Rocky 8.9/9.3, Ubuntu 22.04/24.04/25.04/25.10, MSYS2/Cygwin and source. These are asset names, not runtime certification for every platform. Build metadata: CMake >=3.21, C17/C++17.

## Exposure

Search snippets and earlier d3 release notes exposed unit timestep/mass and deterministic coincident-node jiggling. The helper did not open d3 implementation, assertions, full examples or donor papers before the scope seal. Graphviz radius example in a search result is unrelated to sfdp and not counted. Source read timestamps are bracketed UTC intervals between actual clock observations; no exact per-request second is asserted.

## Source counting

G001-G004 are one d3-force work; G005-G010 are one Graphviz work. Metadata alone does not fulfill the later implementation/fixture reading requirement. Query snippets and failed HTML rendering are excluded.
