"""Read-only C3/C4 second destinations. No downloaded code is executed.

Inputs are frozen source scopes. Parent's window helper is used unchanged;
scope ambiguities are exposed in the receipt and reviewed separately.
Full extracted text is temporary, never a final source deliverable.
"""
import concurrent.futures
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

P = Path(__file__).parent
E = P.parent
spec = importlib.util.spec_from_file_location('af044_http_probe', E / 'http_probe.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
INPUT = E / 'control' / 'candidate-read-receipts.json'
SHA = lambda b: hashlib.sha256(b).hexdigest()

def write(suffix, value):
    (P / ('control-second-hop-' + suffix)).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + '\n')

rows = [r for r in json.loads(INPUT.read_text())
        if r.get('candidate_id', '').startswith(('C3', 'C4'))]
targets = {}
for row in rows:
    for link in row['scope']['links']:
        url = urllib.parse.urljoin(row['requested_url'], link['raw_href'])
        occurrence = dict(candidate_id=row['candidate_id'],
                          case_id=row['candidate_id'].split('-')[0],
                          start_requested_url=row['requested_url'],
                          source_html_sha256=row['sha256'],
                          source_scope=row['scope']['scope_locator'], **link)
        targets.setdefault(url, []).append(occurrence)
target_manifest = dict(
    protocol='SCOPE v1 strict source scopes; frozen atoms; no A/B/C computation',
    bundle2_remote_sha='b36cc513ccbc1616168401ec9564866038e880a3',
    input_file='evidence/control/candidate-read-receipts.json',
    input_sha256=SHA(INPUT.read_bytes()),
    helper_sha256=SHA((E / 'http_probe.py').read_bytes()),
    strict_outgoing_occurrences=sum(map(len, targets.values())),
    unique_url_count=len(targets),
    unique_document_count=len({urllib.parse.urldefrag(u)[0] for u in targets}),
    targets=[dict(url=u, source_occurrences=occ) for u, occ in targets.items()])
write('targets.json', target_manifest)
docs = {}
for url in targets:
    docs.setdefault(urllib.parse.urldefrag(url)[0], []).append(url)

def fetch_document(item):
    url, destinations = item
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    rec = dict(document_url=url, checked_utc=now, http_status='미확인',
               access_success=False, requested_destinations=len(destinations))
    arrivals, windows = [], []
    try:
        with urllib.request.urlopen(url, timeout=25) as response:
            raw = response.read()
            rec.update(http_status=response.status, access_success=True,
                       final_url=response.geturl(),
                       content_type=response.headers.get('content-type'),
                       byte_count=len(raw), sha256=SHA(raw))
        dom = helper.DOM()
        dom.feed(raw.decode('utf-8', errors='replace'))
        dom.finish()
        title = next((n.text() for n in dom.nodes if n.tag == 'title'), '')
        rec['title'] = ' '.join(title.split())
        rec['published_version_display'] = (
            (re.search(r'Python ([0-9.]+) documentation', title) or [None, '미확인'])[1])
        full = ' '.join(dom.main().text().split())
        document_windows = []
        for dest in destinations:
            window = dom.window(dest)
            fragment = urllib.parse.unquote(urllib.parse.urldefrag(dest)[1])
            target = next((n for n in dom.nodes
                           if n.attrs.get('id') == fragment or n.attrs.get('name') == fragment), None) if fragment else None
            confirmed = window.get('fragment_found') is not False
            receipt = dict(url=dest, source_occurrences=targets[dest],
                           http_status=rec['http_status'], access_success=True,
                           checked_utc=now, final_document_url=rec['final_url'],
                           html_sha256=rec['sha256'], title=rec['title'],
                           published_version_display=rec['published_version_display'],
                           fragment_exists=window.get('fragment_found') if fragment else True,
                           requested_fragment=fragment,
                           target_tag=target.tag if target else None,
                           locator=window.get('scope_locator'),
                           declared_window_word_count=len(window['text'].split()),
                           declared_window_sha256=SHA(window['text'].encode()),
                           read_status='window_extracted_pending_semantic_review' if confirmed else 'missing_fragment',
                           actual_user_response='미확인')
            arrivals.append(receipt)
            document_windows.append(dict(url=dest, window=window))
        windows = dict(document_url=url, sha256=rec['sha256'], title=rec['title'],
                       full_text=full, windows=document_windows)
    except urllib.error.HTTPError as exc:
        rec.update(http_status=exc.code, error_type=type(exc).__name__, error=str(exc))
    except Exception as exc:
        rec.update(error_type=type(exc).__name__, error=str(exc))
    if not arrivals:
        for dest in destinations:
            arrivals.append(dict(url=dest, source_occurrences=targets[dest],
                                 http_status=rec['http_status'], access_success=False,
                                 checked_utc=now, fragment_exists='미확인',
                                 locator='접속 실패' if not rec['access_success'] else '추출 실패',
                                 read_status='failed', actual_user_response='미확인'))
    return rec, arrivals, windows

access, arrivals, temporary = [], [], []
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    for rec, dests, win in executor.map(fetch_document, docs.items()):
        access.append(rec)
        arrivals.extend(dests)
        if win:
            temporary.append(win)
write('access.json', access)
write('arrivals.json', arrivals)
write('windows.tmp.json', temporary)
print(json.dumps(dict(documents=len(access), urls=len(arrivals),
                      http200_documents=sum(x['http_status'] == 200 for x in access),
                      failed_documents=[dict(url=x['document_url'], status=x['http_status'], error=x.get('error'))
                                        for x in access if not x['access_success']]), ensure_ascii=False), flush=True)

def fresh_step(url):
    result = helper.fetch(url)
    meta = {k: v for k, v in result.items() if k not in ('window', 'all_links', 'full_text')}
    win = result.get('window', {})
    meta['scope'] = {k: v for k, v in win.items() if k != 'text'}
    meta['window_sha256'] = SHA(win.get('text', '').encode())
    meta['window_word_count'] = len(win.get('text', '').split())
    return meta, win

trials = []
for trial_id, cid, raw_href, dom_index in [
    ('C3-PEP-SPEC-independent', 'C3-2', '#specification', 11),
    ('C4-DATAMODEL-ASYNCWITH-independent', 'C4-3', 'compound_stmts.html#async-with', 956),
]:
    source = next(r for r in rows if r['candidate_id'] == cid)
    first, first_window = fresh_step(source['requested_url'])
    actual = next((a for a in first_window.get('links', [])
                   if a['raw_href'] == raw_href and a['dom_index'] == dom_index), None)
    trial = dict(trial_id=trial_id, case_id=cid.split('-')[0], source_candidate_id=cid,
                 independent_start_state=True,
                 start_state_description='No evidence from another trial is carried into this fresh pair of requests.',
                 first_step=dict(action='open_candidate_direct', cost=1, receipt=first),
                 actual_source_href_confirmed=actual is not None,
                 actual_source_href=actual,
                 total_click_cost=1,
                 actual_user_response='미확인',
                 semantic_review_status='pending; only the two scoped windows may be combined')
    if actual:
        dest = urllib.parse.urljoin(source['requested_url'], raw_href)
        second, second_window = fresh_step(dest)
        trial['second_step'] = dict(action='follow_actual_href_in_first_scope', cost=1,
                                   raw_href=raw_href, destination_url=dest, receipt=second)
        trial['total_click_cost'] = 2
        trial['destination_scope_confirmed'] = second.get('status') == 200 and second_window.get('fragment_found') is not False
    trials.append(trial)
write('independent-trials.json', trials)
print(json.dumps(dict(independent_trials=[dict(id=x['trial_id'], href_confirmed=x['actual_source_href_confirmed'],
                                               arrived=x.get('destination_scope_confirmed'), cost=x['total_click_cost'])
                                         for x in trials]), ensure_ascii=False), flush=True)
