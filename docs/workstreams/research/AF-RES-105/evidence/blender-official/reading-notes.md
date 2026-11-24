# Blender official behavior and upstream tests — stage 3

All reads and executions here occurred after the confirmed stage-2 remote seal. No official page or test is used as evidence that an original requester performed an operation or acquired knowledge.

## Distinct required works

| Source ID | Work/version | Read location and contribution | Mandatory category/count |
|---|---|---|---|
| BL-O1 | Blender Manual 4.0, Accumulate Field | Inputs/domain/type, Leading/Trailing/Total, and the actual numeric example table; explains grouped local edge index and weighted accumulation | Official / 1 |
| BL-O2 | Blender Manual 4.0, Sample Curve | Factor/length and value interpolation; explains the linked weighted-interval mapping | Official / 1 |
| BL-O3 | Blender Manual 4.0, Link Data | Active source and Copy Modifiers; target modifier stacks are replaced | Official / 1 |
| BL-O4 | Blender Manual 4.0, Extrude Mesh | Selection, edge/face/individual mode, offset, and topology/attribute semantics | Official / 1 |
| BL-U1 | Blender upstream `BLI_math_rotation_test.cc`, v4.0.2, blob `8a04184532faadcf673a3ba4f386f0ec1be0deed` | Explicit direction rotation, quaternion angle/vector/tracking input-and-expected assertions | Upstream test / 1 |
| BL-U2 | Blender upstream `BLI_math_vector_test.cc`, v4.0.2, blob `0e99619d2105b6fa99e8d690d41fae48fd63333e` | Entire file; concrete interpolation, square-root, and reciprocal expected values | Upstream test / 1 |

The official pages were fetched directly and their relevant textual sections were read. The source files were fetched through the official repository contents API, base64-decoded, and their Git blob hashes recomputed successfully. The public HTML and immutable blob URLs are identifiers returned in that API response; they are not claimed as additional opens. No complete source copies are committed.

The upstream tests are two distinct low-level works with actual input/expected values, not generic build smoke tests. Rotation tests include rotating X around Z by pi/2 to Y and pi to negative X. Vector interpolation tests include `(40,-100,50)` and `(20,100,100)` at factor 0.5 producing `(30,0,75)`. These behaviors are relevant to direction/pivot semantics and the value interpolation documented for Sample Curve. They do **not** test the complete proposal node graphs, establish matching code paths for every node, or verify original-user execution. The C++ tests were read, not compiled here.

## Additional reads and explicit gaps

BL-O5 is Manual 4.0 Apply / Visual Geometry as Mesh. BL-O6 and BL-O7 are Manual 3.6 Align Euler to Vector and Compare. The latter two were also read at version 4.0, without counting the version mirror as another work. They distinguish Euler rotation from target direction, Pivot Auto from axis-constrained pivots, and Direction Greater Than 90 degrees from Direction Not Equal 0. These three supporting documents count zero toward the four already-filled required official slots.

Two original GN fixture downloads, `accumulate_field_column_grid.blend` and `sample_curves.blend`, were attempted at test-data commit `221f67d71e370f251d39ea7d863b9e08a18094ed`. Both returned HTTP 403. Their bytes, inputs, and expected geometry were not read, and neither counts as a source. The 17-line geometry-node test harness was read and identifies `test_object` and `expected_object` with tolerance 1e-4, but it contains neither actual input nor expected geometry and also counts zero. These gaps are separate from the successfully read mathematical test works.

## Independent native probes

`controlled_probes.py` ran in Blender 4.3.2 with automatic scripts disabled and `--python-exit-code 1`. All three probes passed; the receipt includes the command, script/output hashes, timestamps, and exit 0.

- A disconnected triangle and quad produce local indices 0–2 and 0–3. The initial predicate selects the first edge of each island. The random-index predicate at seed 0 selects local edges 2 and 1, preserving exactly one per island. This is a cardinality check for one seed, not a distribution test.
- Copying a Geometry Nodes translation modifier from an active triangle to another triangle replaces that target's prior Bevel. Conversion produces two static meshes at Z=2 with zero modifiers. This checks the concrete replacement/baking scope, not hundreds of original scene objects.
- For direction angles 0, 45, 90, 180 degrees, Greater Than 90 yields `[false,false,false,true]`, while Not Equal 0 yields `[false,true,true,true]`. Aligning X toward `(0,1,1)` gives normalized `(0,1,1)` with Pivot Auto and `(0,1,0)` with Pivot Z. These are distinct outcomes on controlled inputs, not a replay of the auxiliary user's scene or Blender 3.6 environment.

Native probes are researcher-created D3 evidence and count zero upstream works. The author release, proposer stated release, artifact format, manual release, test-source tag, and researcher runtime are recorded separately.
