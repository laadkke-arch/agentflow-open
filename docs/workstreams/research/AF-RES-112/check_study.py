"""Task-specific ledger and traceability checks; no claim of semantic fact truth."""
import hashlib
import json
import re
from pathlib import Path
from compile_observations import build as build_main
from compile_control import build as build_control
from build_results import build as build_results

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def read_field(value, field):
    for name in field.split('.'):
        value = value[name]
    return value


def check():
    generated = {}
    for builder in (build_main, build_control, build_results):
        for name, content in builder().items():
            assert (ROOT / name).read_text() == content, ('generated output drift', name)
            generated[name] = hashlib.sha256(content.encode()).hexdigest()
    refs_checked = 0
    for name in ['assessments.json', 'control-assessment.json']:
        doc = json.loads((ROOT / 'adjudication' / name).read_text())
        for ref in walk(doc):
            if 'file' not in ref or 'json_lines' not in ref:
                continue
            path = REPO / ref['file']
            assert path.is_file(), ref
            assert path.is_relative_to(ROOT), ref
            lines = path.read_text().splitlines()
            first, last = ref['json_lines']
            assert 1 <= first <= last <= len(lines), ref
            if 'field' in ref:
                event = json.loads(path.read_text())
                value = read_field(event, ref['field'])
                if 'field_codepoint_range' in ref:
                    a, b = ref['field_codepoint_range']
                    assert isinstance(value, str) and 0 <= a <= b <= len(value), ref
                if 'decoded_source_lines' in ref:
                    a, b = ref['decoded_source_lines']
                    assert 1 <= a <= b <= len(value.splitlines()), ref
                if 'capture_codepoint_range' in ref and 'field_codepoint_range' in ref:
                    a, b = ref['field_codepoint_range']
                    start = event.get('capture_codepoint_start', 0)
                    assert ref['capture_codepoint_range'] == [start + a, start + b], ref
            refs_checked += 1
    context = json.loads((ROOT / 'evidence/reader-contexts.json').read_text())
    assert len(context['contexts']) == 7
    assert len({c['task_name'] for c in context['contexts']}) == 7
    runtime_hash = hashlib.sha256((ROOT / 'reader_runtime.js').read_bytes()).hexdigest()
    for c in context['contexts']:
        assert c['fork_turns'] == 'none' and c['runtime_sha256'] == runtime_hash
        assert hashlib.sha256((ROOT / c['input']).read_bytes()).hexdigest() == c['input_sha256']
    invariance = json.loads((ROOT / 'evidence/exposure-invariance.json').read_text())
    assert len(invariance['events']) == 18
    for row in invariance['events']:
        event = json.loads((ROOT / row['event_file']).read_text())
        assert hashlib.sha256(event['exposed_text'].encode()).hexdigest() == row['exposed_sha256']
    local_links = 0
    pending_receipts = {'evidence/final-verification.json', 'HANDOFF.md'}
    for name in ['RESULT.md', 'analysis.md', 'SELF_CHECK.md', 'reproduce.md', 'INDEX_PROPOSAL.md']:
        path = ROOT / name
        assert path.is_file(), name
        text = path.read_text()
        for dest in re.findall(r'\]\(([^)]+)\)', text):
            if dest.startswith(('http://', 'https://', '#')):
                continue
            target = dest.split('#')[0]
            if target in pending_receipts:
                continue
            assert (path.parent / target).exists(), (name, target)
            local_links += 1
    result = (ROOT / 'RESULT.md').read_text()
    assert result.startswith('## 표 1.')
    assert result.index('## 표 1.') < result.index('## 표 2.') < result.index('## 표 3.') < result.index('## 판정과 사용 범위')
    tail = result.split('## 가장 중요한 불일치·약점과 다음 조사 — 정확히 3건\n\n')[-1].strip().splitlines()
    assert len(tail) == 5 and all(x.startswith('|') for x in tail)
    metrics = json.loads((ROOT / 'metrics.json').read_text())
    assert metrics['status'] == 'PARTIAL'
    assert metrics['costs']['B']['hint_codepoints'] == 86 + 74 + 73 == 233
    assert metrics['costs']['B']['hint_utf8_bytes'] == 503
    assert metrics['main']['historical_accuracy'] is None
    return {'status': 'passed', 'scope': 'ledger equality, budgets, source allocation, reference bounds, local links, required table ordering; not semantic truth or completed research acceptance',
            'generated_files': generated, 'adjudication_reference_bounds_checked': refs_checked,
            'local_links_checked': local_links, 'main_contexts': 6, 'control_contexts': 1,
            'research_status': 'PARTIAL'}


if __name__ == '__main__':
    print(json.dumps(check(), ensure_ascii=False, indent=2))
