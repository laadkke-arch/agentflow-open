"""Audit recovered GIS evidence, preserve small generated inputs, and replay selected reads.

Only writes below this script's directory. Prior checkout is read-only; binary
environments are reused with bytecode disabled and are not installed or copied.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import urllib.request

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
HIST = BASE / 'streams/gis/historical'
PRIOR = Path('/workspace/scratch/ac46ee61e54a/agentflow-open/docs/workstreams/research/AF-RES-079/streams/gis/historical')
ART = HERE / 'artifacts'
ART.mkdir(exist_ok=True)
RUNS = HERE / 'runs'
RUNS.mkdir(exist_ok=True)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def parse_log(p):
    text = p.read_text()
    return json.JSONDecoder().raw_decode(text[text.index('{'):])[0]


def clean(value):
    import math
    if isinstance(value, float) and not math.isfinite(value):
        return {'non_finite_float': 'NaN' if math.isnan(value) else str(value)}
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items()}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


receipt_checks = []
for p in sorted(HIST.glob('*.json')):
    data = json.loads(p.read_text())
    if not isinstance(data, dict) or not {'output_file', 'output_sha256'} <= data.keys():
        continue
    log = HIST / data['output_file']
    receipt_checks.append({'receipt': p.name, 'exit_code': data.get('exit_code'),
                           'output_exists': log.is_file(),
                           'output_hash_matches': log.is_file() and sha(log) == data['output_sha256']})

artifacts = []
for name in ['g03-old.parquet', 'g03-new.parquet', 'g04-old.parquet',
             'g04-new-same-name.parquet', 'g04-new-alias.parquet', 'new.arg', 'new.json',
             'arg-input/sealed.arg', 'arg-input/sealed.json',
             'arg-input/supplier-int16.arg', 'arg-input/supplier-int16.json']:
    src = PRIOR / 'runs' / name
    dest = ART / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    before = sha(src)
    shutil.copyfile(src, dest)
    assert before == sha(src) == sha(dest)
    artifacts.append({'prior_path': 'streams/gis/historical/runs/' + name,
                      'preserved_path': str(dest.relative_to(BASE)), 'bytes': dest.stat().st_size,
                      'sha256': before, 'source_kind': 'research_generated_fixture_or_output',
                      'additional_natural_events': 0, 'additional_original_works': 0})

writer_checks = []
for label, name in [('g03-old-write', 'g03-old.parquet'), ('g03-new-write', 'g03-new.parquet'),
                    ('g04-old-write', 'g04-old.parquet'), ('g04-new-same-name-write', 'g04-new-same-name.parquet'),
                    ('g04-new-alias-write', 'g04-new-alias.parquet'), ('arg-write-3.8.0', 'new.arg')]:
    raw = parse_log(HIST / (label + '.log'))
    writer_checks.append({'run': label, 'artifact': name,
                          'output_hash_matches': raw['output_sha256'] == sha(ART / name)})

cases = [
    ('g03-read-old', 'gdal37', '3.7.0', 'inspect-vector', 'g03-old.parquet', False, 'g03-p1-old'),
    ('g03-read-new', 'gdal38a10', '3.8.0', 'inspect-vector', 'g03-old.parquet', False, 'g03-p1-new'),
    ('g04-old-reads-struct', 'gdal38', '3.8.0', 'inspect-vector', 'g04-new-same-name.parquet', False, 'g04-old-reads-new-name'),
    ('g04-old-reads-alias', 'gdal38', '3.8.0', 'inspect-vector', 'g04-new-alias.parquet', False, 'g04-old-reads-alias'),
    ('g04-new-reads-struct', 'gdal39', '3.9.0', 'inspect-vector', 'g04-new-same-name.parquet', False, 'g04-new-reads-new-name'),
    ('arg-default', 'gdal38', '3.8.0', 'inspect-raster', 'arg-input/sealed.arg', False, 'arg-default-3.8.0'),
    ('arg-optin', 'gdal38', '3.8.0', 'inspect-raster', 'arg-input/sealed.arg', True, 'arg-opt-in-3.8.0'),
]
replays = []
compared_keys = ['result', 'gdal_version', 'arg_opt_in', 'input_sha256', 'opened_driver',
                 'fields', 'srs_wkt', 'geo_metadata', 'ordered_rows', 'arrow_schema',
                 'shape', 'geotransform', 'dtype', 'nodata', 'checksum', 'ordered_values',
                 'exception_type', 'error', 'exit_code']
for label, envname, version, mode, filename, optin, previous in cases:
    envroot = PRIOR / 'envs' / envname
    command = [str(envroot / 'bin/python'), '-B', str(BASE / 'streams/gis/replay_gis.py'),
               '--expected-version', version]
    if optin:
        command += ['--arg-opt-in']
    command += [mode, '--input', str(ART / filename), '--driver', 'ARG' if mode == 'inspect-raster' else 'Parquet']
    overrides = {'PYTHONDONTWRITEBYTECODE': '1', 'GDAL_DRIVER_PATH': str(envroot / 'lib/gdalplugins'),
                 'GDAL_DATA': str(envroot / 'share/gdal'), 'PROJ_DATA': str(envroot / 'share/proj'),
                 'CPL_TMPDIR': str(RUNS), 'XDG_CACHE_HOME': str(HERE / 'cache')}
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    result = subprocess.run(command, cwd=HERE, env={**os.environ, **overrides},
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = RUNS / (label + '.stdout.json')
    stderr = RUNS / (label + '.stderr.txt')
    stdout.write_bytes(result.stdout)
    stderr.write_bytes(result.stderr)
    current = clean(json.loads(result.stdout))
    earlier = clean(parse_log(HIST / (previous + '.log')))
    differences = [k for k in compared_keys if current.get(k) != earlier.get(k)]
    rec = {'label': label, 'actor': '/root/gis_resume_audit nonblind verification',
           'started_utc': started, 'finished_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
           'command': command, 'cwd': str(HERE), 'environment_overrides': overrides,
           'exit_code': result.returncode, 'stdout': str(stdout.relative_to(BASE)),
           'stdout_sha256': sha(stdout), 'stderr': str(stderr.relative_to(BASE)), 'stderr_sha256': sha(stderr),
           'previous_run': previous, 'semantic_fields_compared': compared_keys,
           'semantic_differences': differences, 'exact_recorded_input_equal': current.get('input_sha256') == earlier.get('input_sha256'),
           'result': current}
    (RUNS / (label + '.receipt.json')).write_text(json.dumps(rec, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
    replays.append(rec)

report = {'task': 'AF-RES-079', 'actor': '/root/gis_resume_audit', 'review_kind': 'nonblind separate-agent recovery audit',
          'checked_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
          'previous_checkout_mutated': False, 'new_installations': False,
          'receipt_checks': receipt_checks, 'artifact_manifest': artifacts, 'writer_hash_checks': writer_checks,
          'targeted_replays': replays,
          'natural_native_event_ids': ['G02', 'G03', 'G04'], 'natural_native_numerator': 3, 'natural_denominator': 4,
          'remaining_native_gap': 'G01 rasdaman server/build; whole full georeferencing/write requirements were originally inapplicable',
          'additional_natural_events': 0, 'additional_original_works': 0,
          'independent_accuracy_or_agreement_rate': None,
          'artifact_mapping_note': 'prior_path and preserved_path are both relative to docs/workstreams/research/AF-RES-079/',
          'source_reread_file': 'streams/resume-gis/source-reread.jsonl',
          'limitations': [
              'Nonblind separate-agent audit; no independent accuracy or agreement rate.',
              'Historical GDAL3.8 and3.9 environments both expose pyarrow14.0.2, but file parquet_created_by reports C++ Arrow14.0.1 and14.0.2 respectively. Binary builds and PROJ differ.',
              'Input and log hash agreement verifies specific evidence continuity; no full standard-conformance or whole-domain compatibility claim.',
              'G01 native rasdaman build/server remains absent.',
          ],
          'findings': [
              {'id': 'RG01', 'severity': 'required_integration', 'finding': 'Update final RESULT/SELF_CHECK/ledgers from GIS native0/4 to observed-event3/4 with bounded judgments; preserve dated initial state.'},
              {'id': 'RG02', 'severity': 'fixed_by_artifact_preservation', 'finding': 'Preserved11 ignored generated inputs/outputs with original-relative-path mapping; root may restore same bytes to historical/runs.'},
              {'id': 'RG03', 'severity': 'required_qualification', 'finding': 'Distinguish Python pyarrow package14.0.2 from differing C++ Arrow writer versions in G04.'},
          ],
          'audit_exit_code': 0 if all(x['output_hash_matches'] for x in receipt_checks + writer_checks)
              and all(not x['semantic_differences'] and x['exact_recorded_input_equal'] for x in replays) else 1}
if (HERE / 'audit.md').is_file():
    report['audit_markdown_sha256'] = sha(HERE / 'audit.md')
(HERE / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
print(json.dumps({'receipt_checks': len(receipt_checks), 'bad_receipts': [x for x in receipt_checks if not x['output_hash_matches']],
                  'preserved_artifacts': len(artifacts), 'preserved_bytes': sum(x['bytes'] for x in artifacts),
                  'replays': len(replays), 'semantic_difference_runs': [(x['label'], x['semantic_differences']) for x in replays if x['semantic_differences']],
                  'exit_code': report['audit_exit_code']}, ensure_ascii=False))
raise SystemExit(report['audit_exit_code'])
