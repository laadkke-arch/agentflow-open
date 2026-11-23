"""Read-only independent checks of the assembled AF-RES-070 ledgers.

Run from the repository root. Only this audit's JSON report is written; no
source ledger, sealed A record, Git ref, or investigated program is changed.
"""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import csv
import hashlib
import io
import json
import re
import sys

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[3]
INPUTS = ['tools/build_ledgers.py', 'ENROLLMENT.csv', 'EVENTS.csv', 'VIEWS.csv',
          'OUTCOMES.csv', 'PINS.csv', 'CASES.json']
snapshots = {name: (BASE / name).read_bytes() for name in INPUTS}
checks = []

def check(key, description, failures, inspected=None, severity='error'):
    checks.append(dict(check_id=key, description=description, passed=not failures,
                       inspected=inspected, severity=severity, findings=failures))

def rows(name):
    content = snapshots[name].decode('utf-8')
    raw = list(csv.reader(io.StringIO(content)))
    check('width-' + name, 'CSV header/row column counts',
          [dict(row=i + 1, expected=len(raw[0]), actual=len(r))
           for i, r in enumerate(raw[1:], 1) if len(r) != len(raw[0])], len(raw) - 1)
    return list(csv.DictReader(io.StringIO(content)))

def array(path):
    value = json.loads(path.read_text())
    return value.get('rows', []) if isinstance(value, dict) else value

def list_value(value):
    if value in ('', None):
        return []
    if isinstance(value, list):
        return value
    try:
        value = json.loads(value)
    except (ValueError, TypeError):
        pass
    return value if isinstance(value, list) else [value]

def time(value):
    return datetime.fromisoformat(value.replace(' UTC', 'Z').replace(' ', 'T').replace('Z', '+00:00'))

enroll = rows('ENROLLMENT.csv')
events = rows('EVENTS.csv')
views = rows('VIEWS.csv')
outcomes = rows('OUTCOMES.csv')
pins = rows('PINS.csv')
cases = json.loads(snapshots['CASES.json'])
case_map = {r['issue_id']: r for r in cases}
event_map = {r['event_id']: r for r in events}
sources = {}
for path in sorted((BASE / 'streams').glob('*/*source*.jsonl')):
    for line in path.read_text().splitlines():
        if line.strip():
            row = json.loads(line)
            if 'source_id' in row:
                sources[row['source_id']] = row

for name, data, key in [('ENROLLMENT', enroll, 'enrollment_id'), ('EVENTS', events, 'event_id'),
                        ('VIEWS', views, 'view_id'), ('OUTCOMES', outcomes, 'outcome_id'),
                        ('PINS', pins, 'pin_id'), ('CASES', cases, 'issue_id')]:
    count = Counter(r[key] for r in data)
    check('unique-' + name, 'Unique primary keys', [k for k, n in count.items() if n != 1], len(data))

enroll_map = {r['issue_id']: r for r in enroll}
check('case-enrollment-join', 'Each case joins one enrollment row',
      [r['issue_id'] for r in cases if r['issue_id'] not in enroll_map], len(cases))
for name, data in [('EVENTS', events), ('VIEWS', views), ('OUTCOMES', outcomes), ('PINS', pins)]:
    check('issue-join-' + name, 'Each ledger row joins an enrolled A/B case',
          [r for r in data if r['issue_id'] not in case_map], len(data))

bad = []
for iid, case in case_map.items():
    vv = [r for r in views if r['issue_id'] == iid]
    oo = [r for r in outcomes if r['issue_id'] == iid and r['row_type'] == 'case']
    ee = [r for r in events if r['issue_id'] == iid and r['event_type'] == 'original_body']
    if Counter(r['view'] for r in vv) != Counter({'A': 1, 'B': 1}) or len(oo) != 1 or len(ee) != 1:
        bad.append(dict(issue_id=iid, views=len(vv), case_outcomes=len(oo), opening_events=len(ee)))
check('one-case-two-views-one-opening', 'Exactly A/B, one primary outcome, and one opening event per case', bad, len(cases))

bad = []
for stream in ['rclone', 'ripgrep', 'pandoc', 'jq']:
    rr = [r for r in enroll if r['stream'] == stream]
    if [int(r['sequence']) for r in rr] != list(range(1, 17)):
        bad.append(dict(stream=stream, sequences=[r['sequence'] for r in rr]))
    if len({r['issue_id'] for r in rr}) != len(rr):
        bad.append(dict(stream=stream, duplicate_issue=True))
    main = [r for r in rr if r['selected_main'] == 'true']
    if len(main) != 3:
        bad.append(dict(stream=stream, main_count=len(main)))
check('enrollment-order-and-slots', 'Each alternating stream preserves 1..16 and three primary slots', bad, len(enroll))

bad = []
for iid in case_map:
    ee = [r for r in events if r['issue_id'] == iid]
    ordered = sorted(ee, key=lambda r: (time(r['created_utc']), int(re.findall(r'\d+', r['event_id'])[-1])))
    if [r['event_id'] for r in ee] != [r['event_id'] for r in ordered]:
        bad.append(iid)
check('event-chronology', 'Within-issue events are ordered by creation UTC and numeric tie break', bad, len(events))

bad = []
for c in cases:
    a, b = next(r for r in views if r['issue_id'] == c['issue_id'] and r['view'] == 'A'), next(r for r in views if r['issue_id'] == c['issue_id'] and r['view'] == 'B')
    for k in ['candidate_ids', 'candidate_1', 'candidate_2', 'evidence_sections', 'version', 'selected_field', 'context', 'goal', 'prohibitions']:
        if a[k] != b[k]:
            bad.append(dict(issue_id=c['issue_id'], changed_column=k))
    if int(b['values_copied_into_B']) not in (0, 1):
        bad.append(dict(issue_id=c['issue_id'], copied_fields=b['values_copied_into_B']))
check('A-B-fixed-packet', 'A/B preserve context, candidates, field, version and evidence; at most one B value', bad, len(cases))

missing_B = [c for c in cases if c['B_value'] is None]
bad = [c['issue_id'] for c in missing_B if c['recommendation_direction_change'] != 'unobservable' or c['strict_accuracy_change'] != 'unobservable' or c['strict_effect_denominator']]
check('missing-B-not-zero-effect', 'Missing or ambiguous B never becomes same/improved/worsened or an effect denominator', bad, len(missing_B))
bad = []
for c in cases:
    if c['B_value'] is None:
        continue
    e = event_map.get(c['B_event_id'])
    if not e or e['issue_id'] != c['issue_id'] or str(e['actor_id']) != str(c['author_id']):
        bad.append(dict(issue_id=c['issue_id'], B_event=c['B_event_id'], author_id=c['author_id']))
check('B-event-author-join', 'Every observed B joins the same issue and numeric original author', bad, len(cases) - len(missing_B))

bad = []
for row in outcomes:
    for eid in list_value(row['actual_followup_events']):
        if eid not in event_map:
            bad.append(dict(outcome_id=row['outcome_id'], reference=eid, reference_type='source_id' if eid in sources else 'unresolved'))
        elif event_map[eid]['issue_id'] != row['issue_id']:
            bad.append(dict(outcome_id=row['outcome_id'], cross_issue_event=eid))
check('followup-event-join', 'Actual followup columns contain event IDs, not document IDs', bad, len(outcomes))

bad = []
groups = defaultdict(list)
for pin in pins:
    groups[(pin['issue_id'], pin['candidate_id'])].append(pin)
    if pin['source_id'] not in sources:
        bad.append(dict(pin_id=pin['pin_id'], missing_source=pin['source_id']))
    if not re.search(r'/blob/[0-9a-f]{40}/', pin['pinned_url']):
        bad.append(dict(pin_id=pin['pin_id'], non_SHA_pin=pin['pinned_url']))
check('pin-source-and-SHA', 'Every candidate evidence reference resolves to a source and immutable code/doc SHA URL', bad, len(pins))
bad = []
for (iid, candidate), pp in groups.items():
    by_document = defaultdict(set)
    for pin in pp:
        by_document[pin['pinned_url'].split('#')[0]].add(pin['section'])
    if len(by_document) > 2 or any(len(s) > 1 for s in by_document.values()):
        bad.append(dict(issue_id=iid, candidate_id=candidate, sections_by_document={d: sorted(s) for d, s in by_document.items()}))
check('candidate-packet-budget', 'At most two documents per candidate and one designated section per document', bad, len(groups))

check('unknown-A-not-present', 'RG-1778 missing cwd and RG-1840 unknown exclusion cause are not actual A field values',
      [iid for iid in ['RG-1778', 'RG-1840'] if case_map[iid]['field_in_A']], 2)
bad = []
for c in cases:
    if not c['author_id']:
        extra = {}
        opened = BASE / 'private' / c['stream'] / ('opened-' + str(c['number']) + '.json')
        if opened.exists():
            raw = json.loads(opened.read_text())
            extra['recoverable_numeric_id'] = raw.get('payload', {}).get('issue', {}).get('user', {}).get('id')
        bad.append(dict(issue_id=c['issue_id'], **extra))
check('original-author-ID-completeness', 'Opening author numeric ID survives even without OP followup', bad, len(cases))

bad = []
for r in enroll:
    raw = next(x for x in array(BASE / r['origin_ledger']) if x['issue_id'] == r['issue_id'])
    if raw.get('original_body_status') == 'unknown_current_body_only' and r['initial_body_verified'] == 'true':
        bad.append(dict(issue_id=r['issue_id'], raw_original_status=raw['original_body_status'], assembled_verified=r['initial_body_verified']))
check('opening-proof-not-hardcoded', 'Unrecovered current-only diagnostic openings are not declared verified', bad, len(enroll))

bad = []
for c in cases:
    raw = next(r for r in array(BASE / c['A_origin']) if r['issue_id'] == c['issue_id'])
    if c['stream'] == 'rclone':
        # This stream used preread=True for prior exposure, the reverse of the
        # other streams. RCL-4914's current text added the core/command manual
        # link before original-body recovery; apply the same conservative rule
        # used for Pandoc-7057's added documentation link.
        exposed = raw.get('preread') is True or c['issue_id'] == 'RCL-4914'
    else:
        exposed = raw.get('preread') is False or 'exposed' in raw.get('analysis_layer', '')
    if exposed and c['clean_packet']:
        bad.append(dict(issue_id=c['issue_id'], raw_layer=raw.get('analysis_layer'), raw_preread=raw.get('preread')))
check('exposure-layer-preserved', 'Pre-exposed cases never enter clean packet layer', bad, len(cases))
bad = []
for iid in ['RG-1808', 'RG-1778']:
    c = case_map[iid]
    pp = [r for r in pins if r['issue_id'] == iid]
    if c['strict_budget_compliant'] or any(r['strict_actual_budget_compliant'] == 'true' for r in pp):
        bad.append(dict(issue_id=iid, raw_note='extra_prior_exposure explicitly excludes strict exposure-controlled analysis', assembled_flag=c['strict_budget_compliant']))
check('actual-budget-vs-packet-budget', 'Sealed packet size is distinct from acknowledged extra prior document reading', bad, 2)

bad = []
expected_pairs = {'pandoc-7006': 'OP pair in A', 'pandoc-7039': 'maintainer pair, not OP', 'pandoc-7113': 'OP pair in another field'}
for iid, reason in expected_pairs.items():
    pair_rows = [r for r in outcomes if r['issue_id'] == iid and 'observed_pair' in r['row_type']]
    if not pair_rows:
        bad.append(dict(issue_id=iid, missing_classification=reason))
    for r in pair_rows:
        if r['strict_effect_denominator'] == 'true' or r['slot_denominator'] == 'true':
            bad.append(dict(issue_id=iid, pair_in_AB_denominator=r['outcome_id']))
        if iid == 'pandoc-7039' and r['actual_or_reconstructed'] == 'author_reported_intervention':
            bad.append(dict(issue_id=iid, third_party_wrongly_called_OP=True))
check('pandoc-observed-pairs-preserved', 'Known OP/maintainer setting contrasts remain separate from missing selected B', bad, 3)

bad = []
for c in cases:
    if time(c['first_comment_read_utc']) <= time(c['cutoff_A_utc']):
        bad.append(dict(issue_id=c['issue_id'], cutoff=c['cutoff_A_utc'], first_comment_read=c['first_comment_read_utc']))
check('A-cutoff-before-comment-read', 'Recorded A cutoff precedes recorded first comment read', bad, len(cases))
check('input-snapshot-stable', 'Audited top-level files did not change during this run',
      [name for name, content in snapshots.items() if (BASE / name).read_bytes() != content], len(snapshots))

warnings = [dict(issue_id=r['issue_id'], missing=[k for k in ['archive_url', 'archive_event_id', 'archive_line'] if not r[k]])
            for r in enroll if r['initial_body_verified'] == 'true' and any(not r[k] for k in ['archive_url', 'archive_event_id', 'archive_line'])]
check('archive-locator-completeness', 'Verified openings retain URL, event ID and archive line in aggregate enrollment', warnings, len(enroll), 'warning')

finding_history = [
    ('unknown-A-not-present', 'RG-1778/RG-1840 unknown descriptions were inferred to mean field_in_A=true; explicit false required.'),
    ('opening-proof-not-hardcoded', 'Eight ripgrep extension rows were declared recovered despite raw current-only/unknown status; original recovery total is 56, direct issue reads 64.'),
    ('original-author-ID-completeness', 'Four ripgrep original author IDs were dropped when no OP comment existed; numeric IDs recovered from opened-event payloads.'),
    ('pandoc-observed-pairs-preserved', 'Pandoc 7006/7039/7113 separate observed setting contrasts were omitted by the initial generic outcome mapper.'),
    ('actual-budget-vs-packet-budget', 'RG-1808/1778 extra prior reading was not retained by the strict actual budget flag; packet size and actual exposure are separate.'),
    ('followup-event-join', 'RCL-4911-CF1 used source ID RCL-D1 in actual_followup_events; document evidence must use its own source-key field.'),
    ('exposure-layer-preserved', 'rclone preread polarity differs from other streams; audit corrected its normalization. RCL-4914 added documentation-link exposure remains analogous to Pandoc-7057.'),
    ('archive-locator-completeness', 'All sixteen rclone archive line locators were omitted by the aggregate mapper; private opening-meta jsonl_line provides recoverable values.')
]
by_check = {c['check_id']: c for c in checks}
history = [dict(check_id=k, finding=message,
                current_status='resolved_in_current_snapshot' if by_check[k]['passed'] else 'still_present_in_current_snapshot')
           for k, message in finding_history]
execution_history = []
for previous_name in ['ledger-independent-audit-first.json', 'ledger-independent-audit.json']:
    previous_path = BASE / 'evidence' / previous_name
    if previous_path.exists():
        previous = json.loads(previous_path.read_text())
        execution_history.extend(previous.get('execution_history', []))
        execution_history.append(dict(checked_utc=previous['checked_utc'],
                                      exit_code=previous['execution']['exit_code'],
                                      failed_checks=[c['check_id'] for c in previous['checks'] if not c['passed']],
                                      input_sha256=previous['input_sha256']))
execution_history = list({r['checked_utc']: r for r in execution_history}.values())

report = dict(
    audit_id='AF-RES-070-independent-ledger-audit', auditor='pandoc subagent, independent of build_ledgers.py author',
    checked_utc=datetime.now(timezone.utc).isoformat(),
    execution=dict(command='python -B docs/workstreams/research/AF-RES-070/evidence/ledger_independent_audit.py',
                   cwd=str(Path.cwd()), target='materialized draft snapshot; exact SHA256 per input below',
                   inspected_A_seal_SHAs=sorted({c['A_seal_sha'] for c in cases}),
                   no_git_operations=True, no_target_program_execution=True,
                   exit_code=1 if any(not c['passed'] and c['severity'] == 'error' for c in checks) else 0),
    input_sha256={name: hashlib.sha256(content).hexdigest() for name, content in snapshots.items()},
    counts=dict(enrollment=len(enroll), main_slots=sum(c['scope'] == 'main' for c in cases),
                diagnostic_cases=sum(c['scope'] == 'diagnostic' for c in cases), events=len(events),
                views=len(views), outcomes=len(outcomes), pins=len(pins), candidates=len(groups),
                B_absent_or_ambiguous=len(missing_B), B_observed=len(cases)-len(missing_B),
                B_new=sum(c['B_is_new'] for c in cases),
                strict_effect_denominator=sum(c['strict_effect_denominator'] for c in cases)),
    reported_findings=history,
    execution_history=execution_history,
    previous_execution_record='evidence/ledger-independent-audit-first.json; first run exit 1; generic preread polarity normalized, RCL-4912 false alarm removed, RCL-4914 independently retained for added-link exposure',
    checks=checks,
    limits=['No remote commit reread in this independent audit; parent performs required result-SHA GitHub reread.',
            'No new original-source interpretations were introduced; checks compare preserved ledgers and fixed packets.',
            'This checks manuscript/dataset transformations, not causal question efficacy or investigated software execution.',
            'Candidate packet budget pass does not erase prior-exposure or actual reading-budget deviations.',
            'rclone preread=True denotes prior exposure; other streams use preread=False for that condition. Normalization uses accompanying provenance.',
            'RCL-4914 current-vs-opening diff adds the core/command documentation link before recovery; conservative exposure rule matches Pandoc-7057.'])
(BASE / 'evidence/ledger-independent-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(exit_code=report['execution']['exit_code'], counts=report['counts'],
                     failed_checks=[c['check_id'] for c in checks if not c['passed']]), ensure_ascii=False))
sys.exit(report['execution']['exit_code'])
