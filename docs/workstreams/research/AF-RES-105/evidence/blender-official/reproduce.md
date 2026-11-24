# Blender stage-3 reproduction and unexecuted commands

This document is a command recipe, written from the already recorded URLs, hashes, scripts, and source readings. Writing it performed **no new download, build, or test**. The recorded successful executions are the four artifact inspections and three controlled probes in Blender **4.3.2**. The two C++ test works were read but **미실시** as compiled tests. The two GN fixture downloads returned **HTTP 403**; their contents and test results remain **미확인 / 미실시**.

Run the commands from a clean checkout containing this evidence package. They place new downloads, copied scripts, logs, and results below the ignored workstream cache; they do not overwrite the committed evidence results. Use a new empty reproduction directory for another attempt.

## 1. Required inputs and tools

- Python 3 with its standard library, Git, and the `zstd` command for the one Zstandard-compressed original attachment. The other three original attachments use gzip.
- `/usr/bin/blender` reporting **Blender 4.3.2** for repetition of the recorded native work. This is a researcher runtime, not a recovered original-user runtime. Its recorded build hash was `Unknown`; a particular upstream binary build is not pinned.
- Public read access to the observed Blend Exchange metadata/download endpoints and the official Blender repository URLs listed below.
- For the unrun C++ tests: the **v4.0.2** Blender source tree, a supported C/C++ compiler and CMake build toolchain, and a complete Blender-4.0.2-compatible dependency library bundle. The dependency bundle was not acquired or built in this investigation. Set `AF105_BLENDER_LIBDIR` to its absolute path before attempting the build recipe.
- For the unrun GN fixtures: the two actual `.blend` assets at test-data commit `221f67d71e370f251d39ea7d863b9e08a18094ed`, plus the Python harness and its sibling `tests/python/modules` from the Blender source tree. Their matching Blender build is not established: the test-data commit is from 2025, while the read harness is v4.0.2. A cross-version trial must not be reported as the matched upstream regression result.

```bash
export AF105_REPO="$(git rev-parse --show-toplevel)"
export AF105_ROOT="$AF105_REPO/docs/workstreams/research/AF-RES-105"
export AF105_REPRO="$AF105_ROOT/.cache/blender-reproduce"
mkdir -p "$AF105_REPRO/evidence/blender-followup"
mkdir -p "$AF105_REPRO/evidence/blender-official"
mkdir -p "$AF105_REPRO/.cache/blender-followup"
cp "$AF105_ROOT/evidence/blender-followup/inspect_originals.py" "$AF105_REPRO/evidence/blender-followup/inspect_originals.py"
cp "$AF105_ROOT/evidence/blender-official/controlled_probes.py" "$AF105_REPRO/evidence/blender-official/controlled_probes.py"
command -v python3
command -v zstd
/usr/bin/blender --version
```

The copied scripts derive their root from their own path. Preserving `evidence/<package>/<script>` inside `AF105_REPRO` redirects their outputs into this new reproduction tree. Do not run the tracked `controlled_probes.py` directly if you intend to preserve the committed result JSON unchanged.

## 2. Fetch and verify the four originally linked files

The observed public client uses `GET /api/blends/{id}`, then `/d/{id}/{fileName}`. The script below verifies the returned filename, raw-download SHA-256, decompressed SHA-256, and header before producing the four filenames expected by `inspect_originals.py`. It uses the metadata endpoint rather than treating the `/b/` JavaScript shell as file content.

| Key | Original link | Observed metadata URL | Observed download URL |
|---|---|---|---|
| initial1 | https://blend-exchange.com/b/kvl5pe59/ | https://blend-exchange.com/api/blends/kvl5pe59 | https://blend-exchange.com/d/kvl5pe59/q8.blend |
| initial2 | https://blend-exchange.com/b/7YRW52yV/ | https://blend-exchange.com/api/blends/7YRW52yV | https://blend-exchange.com/d/7YRW52yV/q9.blend |
| proposal1 | https://blend-exchange.com/b/QdbbOY4b/ | https://blend-exchange.com/api/blends/QdbbOY4b | https://blend-exchange.com/d/QdbbOY4b/A309037_geometry-nodes-selecting-random-edge.blend |
| linked2 | https://blend-exchange.com/b/pBJmoznb/ | https://blend-exchange.com/api/blends/pBJmoznb | https://blend-exchange.com/d/pBJmoznb/randomize%20materials.blend |

```bash
python3 - <<'PY'
from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, json, os, subprocess
from urllib.parse import quote
from urllib.request import Request, urlopen

root = Path(os.environ['AF105_REPRO'])
cache = root / '.cache/blender-followup'
specs = [
    ('initial1', 'kvl5pe59', 'q8.blend',
     '9d9216ea1551dbbf1841ba8426e4eb8a3b0a46d481e14b96d39674535a804a42',
     '379f3b69cda7cfc34727f1c15d0471f73bfc183db339e83f62a5ad7a97162a54',
     'BLENDER-v401'),
    ('initial2', '7YRW52yV', 'q9.blend',
     'bcd74497f7664948913ed1b65bd6ac90a5f03ae3c849a6f497a20f1fba17c281',
     'ce0545b4c930b6ed753f46d7c257f16fae8a03c0af1c6cada646afbc32718b7b',
     'BLENDER-v401'),
    ('proposal1', 'QdbbOY4b', 'A309037_geometry-nodes-selecting-random-edge.blend',
     '386e2923ff1a65e34acccfab76aad8f591e773c1a4bbe348b276f2c4eaef2ede',
     '9e682eea5bb59698bcdcdb995c1d6f9fd8d194ff999a9805c0fc2dddcb2cb20d',
     'BLENDER-v400'),
    ('linked2', 'pBJmoznb', 'randomize materials.blend',
     '2d772917ab2456ed8705d58563c0e84790e3bb6750dddad7996a77ea1346ab22',
     '66490bdf537eb6eb33a3286da1593e84ba109c3f3ae8af2952864c01c80e713f',
     'BLENDER-v306'),
]

def fetch(url):
    request = Request(url, headers={'User-Agent': 'AF-RES-105-public-reproduction'})
    with urlopen(request, timeout=60) as response:
        return response.read()

def sha(data):
    return hashlib.sha256(data).hexdigest()

receipts = []
for key, blend_id, filename, raw_sha, decoded_sha, header in specs:
    opened = datetime.now(timezone.utc).isoformat()
    metadata_url = f'https://blend-exchange.com/api/blends/{blend_id}'
    metadata_bytes = fetch(metadata_url)
    (cache / f'blend-api-{key}.json').write_bytes(metadata_bytes)
    metadata = json.loads(metadata_bytes)['data']
    assert metadata['id'] == blend_id
    assert metadata['fileName'] == filename, 'Attachment filename changed'
    download_url = f'https://blend-exchange.com/d/{blend_id}/{quote(filename, safe="")}'
    raw = fetch(download_url)
    (cache / f'original-{key}.bin').write_bytes(raw)
    assert sha(raw) == raw_sha, f'{key}: raw bytes differ from recorded input'
    if raw.startswith(b'\x1f\x8b'):
        decoded = gzip.decompress(raw)
    elif raw.startswith(b'\x28\xb5\x2f\xfd'):
        decoded = subprocess.run(
            ['zstd', '--decompress', '--stdout'], input=raw,
            capture_output=True, check=True).stdout
    else:
        raise RuntimeError(f'{key}: unexpected compression/header')
    assert sha(decoded) == decoded_sha, f'{key}: decompressed hash mismatch'
    assert decoded[:12].decode('ascii') == header
    (cache / f'original-{key}.blend').write_bytes(decoded)
    receipts.append({'key': key, 'opened_utc': opened,
                     'metadata_url': metadata_url, 'download_url': download_url,
                     'download_sha256': sha(raw), 'decompressed_sha256': sha(decoded),
                     'header_ascii': header})
(root / 'input-download-receipt.json').write_text(
    json.dumps(receipts, indent=2) + '\n')
print('Four recorded inputs verified')
PY
```

A hash mismatch is a changed/unreproduced input, not permission to replace the expected hash. The current public bytes may change or disappear. File headers describe a format major/minor, and `bpy.data.version` adds an internal subversion; neither establishes the original author's release patch or historical file immutability.

## 3. Repeat the recorded native inspections and controlled probes

This wrapper verifies the copied script hashes, checks that the executable reports 4.3.2, and records exact commands, return codes, timestamps, and output hashes. It adds `--python-exit-code 1` for both scripts. The original inspection receipt did not use that flag, so the wrapper also checks per-file and per-object errors explicitly instead of relying on process exit alone.

```bash
python3 - <<'PY'
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess

root = Path(os.environ['AF105_REPRO'])
binary = '/usr/bin/blender'
version = subprocess.run([binary, '--version'], capture_output=True,
                         text=True, check=True).stdout.splitlines()[0]
assert version == 'Blender 4.3.2', version
specs = [
    ('originals', 'evidence/blender-followup/inspect_originals.py',
     'da4346b0875e74c69725094cda4b492fe99799b374e430753b964a135ad8ff0e'),
    ('controlled', 'evidence/blender-official/controlled_probes.py',
     '071701488382fbe45fbe6f77b5224ae5ee3af9253ef110076619a2b4968fe4bf'),
]
receipts = []
for key, relative, expected_sha in specs:
    script = root / relative
    actual_sha = hashlib.sha256(script.read_bytes()).hexdigest()
    assert actual_sha == expected_sha, f'{key}: script differs from recorded version'
    command = [binary, '--background', '--factory-startup', '--disable-autoexec',
               '--python-exit-code', '1', '--python', str(script)]
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(command, capture_output=True, timeout=180)
    (root / f'{key}.stdout.log').write_bytes(result.stdout)
    (root / f'{key}.stderr.log').write_bytes(result.stderr)
    receipts.append({'command': command, 'started_utc': started,
                     'ended_utc': datetime.now(timezone.utc).isoformat(),
                     'runtime': version, 'exit_code': result.returncode,
                     'script_sha256': actual_sha,
                     'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
                     'stderr_sha256': hashlib.sha256(result.stderr).hexdigest()})
    (root / 'native-reproduction-receipts.json').write_text(
        json.dumps(receipts, indent=2) + '\n')
    assert result.returncode == 0, f'{key}: inspect saved logs'

originals = json.loads((root / '.cache/blender-followup/original-inspection-raw.json').read_text())
assert len(originals) == 4
for item in originals:
    assert 'error' not in item, item
    assert item['auto_execute_enabled'] is False
    assert all('evaluation_error' not in obj for obj in item['objects'])
controlled = json.loads((root / 'evidence/blender-official/controlled-probes-result.json').read_text())
assert controlled['all_passed']
assert len(controlled['probes']) == 3
print('Four file inspections and three controlled probes completed; inspect new receipts/results')
PY
```

Compare the new results with the committed `artifact-inspection.json` and `controlled-probes-result.json`. The recorded object counts were 30/34/8 vertices/edges/faces for initial1, 260060/260060/65015 for initial2, 144/168/48 for proposal1, and 2500/4900/2401 for linked2. The controlled probe assertions cover one selected edge per island, stack replacement plus conversion, and the two operator/pivot distinctions. Timestamps and output-log hashes will differ across reruns; equality of log hashes is not an expectation.

## 4. Two C++ upstream test works — concrete unrun recipe

**Status: 미실시.** No Blender source build, dependency installation, GTest binary, or CTest discovery was performed for this investigation. The commands below describe the intended retry, not a verified build transcript. The `blender_test` target/location and dependency configuration must be confirmed by the actual v4.0.2 configure/build output; an absent target or failed configure is a build gap, not a passing or failing mathematical test.

The exact sources already read are available through these public contents URLs:

- https://projects.blender.org/api/v1/repos/blender/blender/contents/source/blender/blenlib/tests/BLI_math_rotation_test.cc?ref=v4.0.2
- https://projects.blender.org/api/v1/repos/blender/blender/contents/source/blender/blenlib/tests/BLI_math_vector_test.cc?ref=v4.0.2

Their immutable Git blob locators are:

- https://projects.blender.org/api/v1/repos/blender/blender/git/blobs/8a04184532faadcf673a3ba4f386f0ec1be0deed
- https://projects.blender.org/api/v1/repos/blender/blender/git/blobs/0e99619d2105b6fa99e8d690d41fae48fd63333e

The source clone below supplies the complete build tree and Python harness dependencies. It does not acquire the required platform library bundle. Configure only after that required asset is supplied; no successful library installation is implied here.

```bash
export AF105_BLENDER_SOURCE="$AF105_REPRO/blender-v4.0.2"
export AF105_BLENDER_BUILD="$AF105_REPRO/blender-build-v4.0.2"
git clone --depth 1 --branch v4.0.2 https://projects.blender.org/blender/blender.git "$AF105_BLENDER_SOURCE"
test "$(git -C "$AF105_BLENDER_SOURCE" rev-parse HEAD:source/blender/blenlib/tests/BLI_math_rotation_test.cc)" = 8a04184532faadcf673a3ba4f386f0ec1be0deed
test "$(git -C "$AF105_BLENDER_SOURCE" rev-parse HEAD:source/blender/blenlib/tests/BLI_math_vector_test.cc)" = 0e99619d2105b6fa99e8d690d41fae48fd63333e
test "$(git -C "$AF105_BLENDER_SOURCE" rev-parse HEAD:tests/python/geo_node_test.py)" = bec1be0ce96f5fbc16afd350b617c8d721217272
: "${AF105_BLENDER_LIBDIR:?Set the absolute path to a complete Blender-4.0.2-compatible dependency library bundle}"
cmake -S "$AF105_BLENDER_SOURCE" -B "$AF105_BLENDER_BUILD" -DWITH_GTESTS=ON -DWITH_TESTS_BATCHED=ON -DLIBDIR="$AF105_BLENDER_LIBDIR"
cmake --build "$AF105_BLENDER_BUILD" --target blender_test --parallel 4
"$AF105_BLENDER_BUILD/bin/blender_test" --gtest_list_tests
"$AF105_BLENDER_BUILD/bin/blender_test" --gtest_filter='math_rotation.RotateDirectionAroundAxis:math_rotation.QuaternionAngleBetween:math_rotation.QuaternionFromVector:math_rotation.QuaternionFromTracking' --gtest_output="xml:$AF105_REPRO/rotation-tests.xml"
"$AF105_BLENDER_BUILD/bin/blender_test" --gtest_filter='math_vector.InterpolateInt:math_vector.InterpolateFloat:math_vector.sqrt:math_vector.safe_sqrt:math_vector.rcp:math_vector.safe_rcp' --gtest_output="xml:$AF105_REPRO/vector-tests.xml"
```

Do not accept a GTest invocation that selects zero tests. Preserve configure/build logs, the discovered test names, executed test counts, XML, executable version/build information, and return codes. The actual inputs and expected values are compiled into the two pinned source files; they require no external scene assets:

| Source/test | Concrete input | Expected assertion |
|---|---|---|
| BL-U1 `RotateDirectionAroundAxis` | `(1,0,0)`, axis `(0,0,1)`, angle pi/2 | `(0,1,0)` within `FLT_EPSILON` |
| BL-U1 same test | `(1,0,0)`, Z axis, angle pi | `(-1,0,0)` within `FLT_EPSILON` |
| BL-U1 `QuaternionFromVector` selected case | Vector `(0.927091,0.211322,-0.124857)`, track X positive, up Z | Quaternion `(0.111583,-0.0648251,-0.00729451,-0.991612)`, tolerance 1e-5 |
| BL-U2 `InterpolateFloat` | A `(40,-100,50)`, B `(20,100,100)`, factor 0.5 | `(30,0,75)` |
| BL-U2 `InterpolateInt` | A `(0,-100,50)`, B `(0,100,100)`, factor 0.75 | `(0,50,87)` |
| BL-U2 `sqrt` | `(1,4,9)` | `(1,2,3)`, tolerance 1e-6 |
| BL-U2 `rcp` | `(1,2,4)` | `(1,0.5,0.25)`, tolerance 1e-6 |
| BL-U2 `safe_rcp` | `(1,0,4)` | `(1,0,0.25)`, tolerance 1e-6 |

Even a successful run would test these mathematical assertions. It would not prove GN Pivot Auto code-path identity, the complete weighted-curve graph, or any original author's execution.

## 5. The two inaccessible GN fixtures — retry inputs and unrun harness commands

**Recorded status: both downloads HTTP 403; bytes not read; tests 미실시.** The exact pinned public read URLs are below. A subsequent retry may still fail. Preserve that failure; do not count an HTML error body, directory listing, or Git LFS pointer as a fixture read.

```bash
mkdir -p "$AF105_REPRO/node-fixtures"
curl --fail --location --proto '=https' --max-time 60 --output "$AF105_REPRO/node-fixtures/accumulate_field_column_grid.blend" 'https://projects.blender.org/blender/blender-test-data/raw/commit/221f67d71e370f251d39ea7d863b9e08a18094ed/modeling/geometry_nodes/utilities/accumulate_field_column_grid.blend'
curl --fail --location --proto '=https' --max-time 60 --output "$AF105_REPRO/node-fixtures/sample_curves.blend" 'https://projects.blender.org/blender/blender-test-data/raw/commit/221f67d71e370f251d39ea7d863b9e08a18094ed/modeling/geometry_nodes/curves/sample_curves.blend'
```

Only after a successful `.blend` retrieval, record its byte hash, decompressed header, and actual contained objects. These acquisition facts have no known expected values in this investigation. The read harness's contract is to compare the file's `test_object` with `expected_object` at threshold **1e-4**; the inaccessible assets were not inspected to confirm that contract is present in either file.

The exact harness read was v4.0.2 `tests/python/geo_node_test.py`, blob `bec1be0ce96f5fbc16afd350b617c8d721217272`:

https://projects.blender.org/api/v1/repos/blender/blender/contents/tests/python/geo_node_test.py?ref=v4.0.2

With the complete v4.0.2 source checkout from section 4, the following are concrete **unrun cross-version trial commands** using the recorded native 4.3.2 runtime. They are intentionally labelled a trial: neither fixture compatibility nor a matched upstream Blender/test-data pair has been established.

```bash
/usr/bin/blender --background --factory-startup --disable-autoexec "$AF105_REPRO/node-fixtures/accumulate_field_column_grid.blend" --python-exit-code 1 --python "$AF105_BLENDER_SOURCE/tests/python/geo_node_test.py"
/usr/bin/blender --background --factory-startup --disable-autoexec "$AF105_REPRO/node-fixtures/sample_curves.blend" --python-exit-code 1 --python "$AF105_BLENDER_SOURCE/tests/python/geo_node_test.py"
```

A full upstream regression reproduction additionally requires identifying and recording the Blender source/build paired with test-data commit `221f67d71e370f251d39ea7d863b9e08a18094ed`, then rerunning with that binary and its matching harness. That pairing, both asset inspections, and both node-level executions remain **미확인 / 미실시**. The successful independent native probes do not fill this gap.

## Recorded versus still unexecuted

| Work | Investigation status |
|---|---|
| Four original attachment downloads, byte/header checks, structural inspection, native evaluation | Performed; recorded fingerprints and receipts in `blender-followup` |
| Three researcher-created native semantic probes | Performed in Blender 4.3.2; all assertions passed, exit 0 |
| Two pinned C++ test works | Source and explicit input/expected assertions read; configure/build/test execution 미실시 |
| Two pinned GN `.blend` fixtures | Retrieval attempted and returned 403; bytes and expected geometry 미확인; execution 미실시 |
| Clean-checkout recipes in this document | Newly documented; not rerun while writing this file |
| Original-user historical environment | Not reconstructed |
