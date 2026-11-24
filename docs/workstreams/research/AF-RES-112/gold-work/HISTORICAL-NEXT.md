# Historical Godot tests: missing inputs and exact resume steps

This is an unexecuted follow-up procedure. Writing this file did not run commands, fetch sources, install or download binaries, or change sealed gold, existing scripts, or reader results. Run the commands below only in a later authorized execution. They assume the repository root is the working directory.

## 1. Establish the exact available binary before testing

| Case | Required engine | Missing input or verification | Original source input |
| --- | --- | --- | --- |
| G1 | Godot 3.4.2 | An already available exact executable, its full `--version`, file SHA256 and trusted provenance. The reviewed source tag resolves to `45eaa2daf1e3d2571a9f31a3421911262ec82f51`; a different build must be labeled separately. | `StrikeForceZero/godot-path2d-clean-room` at `1a5942e87c2510e6f9fb281ba27f6a257258eb35` |
| G2 | Godot `4.0-dev.20220118` | The date label does not identify a full commit or binary hash. Resolve the precise author-tested build and obtain its existing executable/provenance before claiming a historical replication. | `similar_resource.zip`, SHA256 `e016439485363faaff80376880e71c92b35d7bd390c7da0d5462ca9372f7f9ea` |
| G3 original | Godot 3.4.2 | Same missing exact executable as G1; original project input is available by the fixed ZIP URL/hash. | `test.zip`, SHA256 `7dfda91dcf0440abcc8769d86b884f69e86e681c935d0d2b1d899d8574da5734` |
| G3 claimed second engine | Godot 4.0 alpha 1 | Both a verified exact executable and an alpha-1-compatible input with recorded provenance are missing. The original linked Godot 3 project is not that input. | The later Godot 4 attachment is a different artifact/settings combination and cannot silently fill this slot. |

Set these task-specific variables to executables that are already available from an approved location. Placeholders below are required inputs, not installed paths or permission to download a binary.

```bash
AF112_GOLD=docs/workstreams/research/AF-RES-112/gold-work
AF112_HIST="$AF112_GOLD/examples/historical"
mkdir -p "$AF112_HIST/binary-evidence"

AF112_GODOT_342=/absolute/path/to/verified-godot-3.4.2
AF112_GODOT_40D=/absolute/path/to/verified-godot-4.0-dev-20220118
AF112_GODOT_40A1=/absolute/path/to/verified-godot-4.0-alpha1

test -x "$AF112_GODOT_342"
"$AF112_GODOT_342" --version > "$AF112_HIST/binary-evidence/3.4.2-version.txt" 2>&1
"$AF112_GODOT_342" --help > "$AF112_HIST/binary-evidence/3.4.2-help.txt" 2>&1
sha256sum "$AF112_GODOT_342" > "$AF112_HIST/binary-evidence/3.4.2-binary.sha256"

test -x "$AF112_GODOT_40D"
"$AF112_GODOT_40D" --version > "$AF112_HIST/binary-evidence/4.0-dev-version.txt" 2>&1
"$AF112_GODOT_40D" --help > "$AF112_HIST/binary-evidence/4.0-dev-help.txt" 2>&1
sha256sum "$AF112_GODOT_40D" > "$AF112_HIST/binary-evidence/4.0-dev-binary.sha256"

test -x "$AF112_GODOT_40A1"
"$AF112_GODOT_40A1" --version > "$AF112_HIST/binary-evidence/4.0-alpha1-version.txt" 2>&1
"$AF112_GODOT_40A1" --help > "$AF112_HIST/binary-evidence/4.0-alpha1-help.txt" 2>&1
sha256sum "$AF112_GODOT_40A1" > "$AF112_HIST/binary-evidence/4.0-alpha1-binary.sha256"
```

Inspect these files before continuing. Record where each executable came from and the source/checksum or already trusted artifact establishing its identity. A locally calculated SHA256 identifies the bytes but does not alone prove an official build or the requested historical commit. Do not substitute the observed installed Godot 4.7.2. If an exact binary cannot be identified or is absent, keep that test unexecuted and stop its branch of the procedure.

The launch commands below use only a project path and an explicit scene. Add a display/headless flag only after the corresponding captured historical `--help` confirms it. In particular, do not assume a Godot 4 `--headless` or `--quit-after` option exists in Godot 3. Record any added flag. A graphics/display requirement that the environment cannot satisfy is an execution blocker, not a failed scene/resource test.

Use `timeout` only if it is available in the execution environment. Record its exit code separately: 124 means the time limit ended the process; it does not prove a correctness failure or success. Keep stdout and stderr even when the engine exits zero.

## 2. Materialize the fixed textual source inputs with fresh caches

The existing downloader uses three explicit source-archive URLs and verifies their frozen hashes. It does not fetch engine binaries. It extracts textual project/script/scene/resource files, excluding original editor caches and icons. This extraction difference must remain in the execution record.

```bash
python -B "$AF112_GOLD/fetch_examples.py"

git clone --no-checkout https://github.com/StrikeForceZero/godot-path2d-clean-room.git "$AF112_HIST/G1-source"
git -C "$AF112_HIST/G1-source" checkout --detach 1a5942e87c2510e6f9fb281ba27f6a257258eb35
git -C "$AF112_HIST/G1-source" rev-parse HEAD > "$AF112_HIST/G1-source-commit.txt"
git -C "$AF112_HIST/G1-source" diff --exit-code
```

If `G1-source` already exists, inspect its HEAD and worktree first; do not overwrite it or repeat `clone` into it. The precise original files to inspect are `Scene.gd`, `Scene.tscn`, `Path2D.gd`, `Path2D.tscn`, `LocalPath2D.tscn`, and `project.godot`. The fixed source URL is [the original repository commit](https://github.com/StrikeForceZero/godot-path2d-clean-room/tree/1a5942e87c2510e6f9fb281ba27f6a257258eb35).

The following preparation creates new working copies. It intentionally refuses to overwrite an existing experiment directory. Run it only after the preceding source preparation succeeded. `.tres` and `.tscn` settings are not rewritten for G1; each load treatment changes exactly one call token in the branch being tested.

```bash
python -B - <<'PY'
from pathlib import Path
import hashlib, json, shutil

b = Path('docs/workstreams/research/AF-RES-112/gold-work')
h = b / 'examples/historical'
exclude = shutil.ignore_patterns('.git', '.godot', '.import', '*.gd.uid')
g1 = h / 'G1-source'

for name, needle in [
    ('G1-shared-preload', None),
    ('G1-shared-load', 'preload("res://Path2D.tscn")'),
    ('G1-local-preload', None),
    ('G1-local-load', 'preload("res://LocalPath2D.tscn")'),
]:
    dest = h / name
    shutil.copytree(g1, dest, ignore=exclude)
    if needle is not None:
        script = dest / 'Scene.gd'
        text = script.read_text()
        assert text.count(needle) == 1, 'Unexpected source: stop, do not choose another occurrence'
        script.write_text(text.replace(needle, needle.replace('preload(', 'load(', 1), 1))
    for scene in ('Path2D.tscn', 'LocalPath2D.tscn'):
        assert (dest / scene).read_bytes() == (g1 / scene).read_bytes()

shutil.copytree(b / 'examples/G2/similar_resource', h / 'G2-original', ignore=exclude)
shutil.copytree(b / 'examples/G3/test', h / 'G3-original', ignore=exclude)
shutil.copytree(b / 'examples/G3/test', h / 'G3-print-g3', ignore=exclude)

# Diagnostic print-only variant. The untouched original remains separate.
f = h / 'G3-print-g3/main.gd'
t = f.read_text()
start = t.index("print('second frame')")
end = t.index('yield(get_tree()', start)
block = t[start:end]
needle = 'print(thing.g2())'
assert block.count(needle) == 2, 'Unexpected original diagnostic block'
left, right = block.rsplit(needle, 1)
f.write_text(t[:start] + left + 'print(thing.g3())' + right + t[end:])

files = {}
for project in sorted(h.iterdir()):
    if not project.is_dir() or project.name in {'binary-evidence', 'G1-source'}:
        continue
    for f in sorted(project.rglob('*')):
        if f.is_file():
            files[str(f.relative_to(h))] = hashlib.sha256(f.read_bytes()).hexdigest()
(h / 'prepared-input-sha256.json').write_text(json.dumps(files, indent=2))
PY

git diff --no-index "$AF112_HIST/G1-source/Scene.gd" "$AF112_HIST/G1-shared-load/Scene.gd"
git diff --no-index "$AF112_HIST/G1-source/Scene.gd" "$AF112_HIST/G1-local-load/Scene.gd"
git diff --no-index "$AF112_HIST/G3-original/main.gd" "$AF112_HIST/G3-print-g3/main.gd"
```

`git diff --no-index` returns 1 when the expected difference is present. Inspect the diff rather than treating that code as a failed setup. Record the preparation script and resulting input hashes as a later execution artifact. Do not treat this document as proof those copies have already been created.

## 3. G1: same scene flags, one load/preload call change

Run each pair in separate fresh engine processes. For the shared pair, leave the example's local-to-scene UI toggle off. For the local pair, turn that toggle on before creating a Path2D in both runs. This chooses the original corresponding `.tscn`; it does not change the serialized Curve2D flag. Do not toggle midway through a trial.

```bash
mkdir -p "$AF112_HIST/logs"

timeout --signal=TERM 120s "$AF112_GODOT_342" --path "$AF112_HIST/G1-shared-preload" res://Scene.tscn > "$AF112_HIST/logs/G1-shared-preload.stdout" 2> "$AF112_HIST/logs/G1-shared-preload.stderr"
AF112_EXIT=$?
printf '%s\n' "$AF112_EXIT" > "$AF112_HIST/logs/G1-shared-preload.exit"

timeout --signal=TERM 120s "$AF112_GODOT_342" --path "$AF112_HIST/G1-shared-load" res://Scene.tscn > "$AF112_HIST/logs/G1-shared-load.stdout" 2> "$AF112_HIST/logs/G1-shared-load.stderr"
AF112_EXIT=$?
printf '%s\n' "$AF112_EXIT" > "$AF112_HIST/logs/G1-shared-load.exit"

timeout --signal=TERM 120s "$AF112_GODOT_342" --path "$AF112_HIST/G1-local-preload" res://Scene.tscn > "$AF112_HIST/logs/G1-local-preload.stdout" 2> "$AF112_HIST/logs/G1-local-preload.stderr"
AF112_EXIT=$?
printf '%s\n' "$AF112_EXIT" > "$AF112_HIST/logs/G1-local-preload.exit"

timeout --signal=TERM 120s "$AF112_GODOT_342" --path "$AF112_HIST/G1-local-load" res://Scene.tscn > "$AF112_HIST/logs/G1-local-load.stdout" 2> "$AF112_HIST/logs/G1-local-load.stderr"
AF112_EXIT=$?
printf '%s\n' "$AF112_EXIT" > "$AF112_HIST/logs/G1-local-load.exit"
```

These are launch commands, **not an automated interaction driver**. No historical GUI driver or exact frame/point observer has been supplied. The minimum next action is to launch `G1-shared-preload` with the verified 3.4.2 executable, inspect the live example, and record a reproducible manual sequence: create a path/add a controlled point, invoke the remove button connected to `_on_RemovePath2DButton_pressed`, allow deferred freeing to complete, then create the next path and inspect its curve.

For each run, record actual clicks or equivalent inputs, the local toggle, Curve2D point count before and after removal/reinstantiation, resource identity if observed, surviving PackedScene/script references, and how completion of `queue_free` was observed. A manually estimated wait is not an exact frame trace. If a diagnostic script is needed to observe counts or references, author and identify it as an additional variant; keep the one-call-only comparison intact. Do not claim that the ordinary launcher generates these measurements. Preserve any existing first-point/index errors in stderr rather than silently fixing the example.

The discriminator includes both directions: retaining a reference can defeat a blanket “load always resets” assertion; scene-local resources can defeat a blanket “preload always shares mutable state” assertion. Historical numerical observations remain unexecuted until the above inputs and measurements exist.

## 4. G2: original ZIP, fresh cache, identity and assertion evidence

Original URL: <https://github.com/godotengine/godot/files/7910066/similar_resource.zip>.

The frozen ZIP SHA256 is `e016439485363faaff80376880e71c92b35d7bd390c7da0d5462ca9372f7f9ea`. Use `G2-original` prepared above. Do not start from a current-engine-imported cache. Capture the serialized identities and values before launching:

```bash
rg -n '^\[gd_resource|^\[ext_resource|^value =|^numbers =' "$AF112_HIST/G2-original" -g '*.tres' > "$AF112_HIST/logs/G2-serialized-identities.txt"

timeout --signal=TERM 15s "$AF112_GODOT_40D" --path "$AF112_HIST/G2-original" res://test.tscn > "$AF112_HIST/logs/G2-original.stdout" 2> "$AF112_HIST/logs/G2-original.stderr"
AF112_EXIT=$?
printf '%s\n' "$AF112_EXIT" > "$AF112_HIST/logs/G2-original.exit"
```

Read all three output files. The original `test.gd` expects `1 + 1 + 2 + 3`; a numeric output and an assertion error must be recorded independently of the OS exit code. A successful process exit never substitutes for checking assertion stderr.

The static text dump records **serialized** UIDs and values, not the objects actually resolved at runtime. The additional required observation is each `fibonacci.numbers` entry's runtime value, object identity and resource path/UID mapping before the assertion. Obtain it using the exact build's debugger/inspector, or create a separately labeled instrumentation variant after inspecting that build's supported API. An automated historical per-element logger is not already supplied. Do not invent its command or assume the current engine's UID API/flags exist unchanged.

If direct game launch fails because the historical build needs an editor scan/class registration, preserve that failed attempt. Inspect its captured `--help`, then run the supported editor/import sequence as a separate preparation condition and record every input/cache change. Do not silently resave resources: resaving can alter the identity defect being investigated. Compare a fresh copy to its prepared hashes after the scan.

Only after the original trial is recorded, run the already specified normal input (four equal values) and an explicitly labeled identity treatment in separate fresh copies. Keep `Number`, `Sum`, the array structure and intended values explicit. Regenerating/removing UIDs, author-style resaving, and making resources unique are different operations; record which one was performed. Do not label the existing 4.7.2 result as this historical replay.

## 5. G3: original Godot 3 ZIP and diagnostic print variant

Original URL: <https://github.com/godotengine/godot/files/7944151/test.zip>.

The frozen ZIP SHA256 is `7dfda91dcf0440abcc8769d86b884f69e86e681c935d0d2b1d899d8574da5734`. `G3-original` preserves `A_Thing.gd`, `main.gd`, `main.tscn` and `project.godot`. Launch the explicit scene because the original project configuration does not specify a main-scene path.

```bash
timeout --signal=TERM 15s "$AF112_GODOT_342" --path "$AF112_HIST/G3-original" res://main.tscn > "$AF112_HIST/logs/G3-original.stdout" 2> "$AF112_HIST/logs/G3-original.stderr"
AF112_EXIT=$?
printf '%s\n' "$AF112_EXIT" > "$AF112_HIST/logs/G3-original.exit"

timeout --signal=TERM 15s "$AF112_GODOT_342" --path "$AF112_HIST/G3-print-g3" res://main.tscn > "$AF112_HIST/logs/G3-print-g3.stdout" 2> "$AF112_HIST/logs/G3-print-g3.stderr"
AF112_EXIT=$?
printf '%s\n' "$AF112_EXIT" > "$AF112_HIST/logs/G3-print-g3.exit"
```

Record the first `_ready` values, mutation outputs, second `_ready` values, array/dictionary/string independently, the actual scene-change call, the resource flag, and stop/breakpoint behavior. The original source already has a stop mechanism but may leave the application or debugger running; a time-limited exit must be labeled accordingly.

**Print correction:** in the original second-frame output, `g2()` is printed twice and `g3()` is omitted. The preparation above changes only the last duplicated second-frame print to `g3()` in `G3-print-g3`. It does not change setters, scene reload logic, resource values or flags. Store the diff and distinguish its output from the untouched original. Never state that the untouched original's third second-frame line directly observed the string setter result.

The later Godot 4 attachment is <https://github.com/godotengine/godot/files/10096836/ExportedEmbededResourcePropertyWontResetOnSceneReload.zip>, SHA256 `f93bef24f0439baab957ca975ea74d5b5c774ed05b0f7abd11d3979e5a7ad0ff`. It uses Godot 4 syntax and already sets `resource_local_to_scene=true`, whereas the original Godot 3 ZIP does not. Its previously recorded current-engine execution is a separate artifact/setting test.

### The still-missing Godot 4 alpha 1 input

Do not feed the Godot 3 project into alpha 1 and call syntax failure a resource-behavior result. Do not substitute the later Godot 4 ZIP without labeling the changed input. The next required action is to locate and verify the exact alpha-1-compatible original example, or explicitly construct a syntax-port variant with a complete diff preserving the original resource flag and values. The latter is a constructed follow-up, not recovery of the author's exact old project.

After that missing input has a recorded original URL/provenance, hash and compatible `main.tscn`, the launch is:

```bash
AF112_ALPHA1_PROJECT=/absolute/path/to/verified-alpha1-project
test -f "$AF112_ALPHA1_PROJECT/main.tscn"
timeout --signal=TERM 15s "$AF112_GODOT_40A1" --path "$AF112_ALPHA1_PROJECT" res://main.tscn > "$AF112_HIST/logs/G3-alpha1.stdout" 2> "$AF112_HIST/logs/G3-alpha1.stderr"
AF112_EXIT=$?
printf '%s\n' "$AF112_EXIT" > "$AF112_HIST/logs/G3-alpha1.exit"
```

`AF112_ALPHA1_PROJECT` is unresolved. The command is therefore specified but presently unexecutable as a verified historical trial.

## 6. Evidence required before changing the historical status

Preserve the executable version/hash/provenance and captured help; exact input source commit or archive hash; source/variant hashes and diffs; fresh-cache or editor-scan preparation; actual command, UTC, stdout, stderr and OS exit; observations tied to each field/condition; and unobserved behavior. Copy the selected receipts out of ignored `examples/` into an owned, versioned evidence directory in that later task before committing them. No part of this procedure is currently an execution receipt, and none retroactively changes the sealed gold.
