"""Correct nonheading structural anchors without changing frozen source links.

Keep dt class/function destinations in their documented section as instructed.
Footnote, backlink, TOC and GitHub comment targets are structural blocks;
the closest enclosing chapter/main is not their arrival section.
"""
import concurrent.futures
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import urllib.parse
import urllib.request

P = Path(__file__).parent
spec = importlib.util.spec_from_file_location('af044_http_probe', P.parent / 'http_probe.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
SHA = lambda b: hashlib.sha256(b).hexdigest()
load = lambda f: json.loads((P / ('control-second-hop-' + f)).read_text())
def write(f, x):
    (P / ('control-second-hop-' + f)).write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')

arrivals = load('arrivals.json')
temporary = load('windows.tmp.json')
if not (P / 'control-second-hop-arrivals-v1.json').exists():
    write('arrivals-v1.json', arrivals)
else:
    write('arrivals-v2.json', arrivals)
    if (P / 'control-second-hop-scope-corrections.json').exists():
        write('scope-corrections-v2.json', load('scope-corrections.json'))
original_arrivals = {r['url']: r for r in load('arrivals-v1.json')}
selected = [x for x in arrivals if x.get('target_tag') in ('aside', 'a', 'div')]
documents = list(dict.fromkeys(urllib.parse.urldefrag(x['url'])[0] for x in selected))

def fetch(doc):
    with urllib.request.urlopen(doc, timeout=25) as r:
        raw = r.read()
        receipt = dict(requested_url=doc, final_url=r.geturl(), http_status=r.status,
                       sha256=SHA(raw), checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    dom = helper.DOM()
    dom.feed(raw.decode('utf-8', errors='replace'))
    dom.finish()
    return doc, dom, receipt

cache = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    for doc, dom, receipt in executor.map(fetch, documents):
        cache[doc] = (dom, receipt)
corrections = []
for row in selected:
    doc, frag = urllib.parse.urldefrag(row['url'])
    frag = urllib.parse.unquote(frag)
    dom, receipt = cache[doc]
    target = next((n for n in dom.nodes if n.attrs.get('id') == frag or n.attrs.get('name') == frag), None)
    if target is None:
        corrections.append(dict(url=row['url'], correction='revisit fragment missing', receipt=receipt))
        row.update(fragment_exists=False, locator='missing fragment on corrective revisit',
                   read_status='missing_fragment', declared_window_word_count=0)
        continue
    scope = target
    if target.tag == 'div' and target.attrs.get('data-testid') == 'comment-header':
        # GitHub's fragment is on the comment header; its following body is
        # in the same explicit comment-viewer block, not in the header itself.
        if target.parent and str(target.parent.attrs.get('data-testid', '')).startswith('comment-viewer-outer-box-'):
            scope = target.parent
    if target.tag == 'a':
        while scope.parent and scope.tag not in ('aside', 'p', 'li', 'dt', 'dd'):
            scope = scope.parent
        if scope.tag not in ('aside', 'p', 'li', 'dt', 'dd'):
            scope = target
    text = ' '.join(scope.text().split())
    locator = 'structural ' + scope.tag + '#' + str(scope.attrs.get('id', frag))
    original = {k: original_arrivals[row['url']].get(k) for k in ('locator', 'declared_window_word_count', 'declared_window_sha256', 'html_sha256')}
    row.update(locator=locator, declared_window_word_count=len(text.split()),
               declared_window_sha256=SHA(text.encode()), html_sha256=receipt['sha256'],
               checked_utc=receipt['checked_utc'], scope_correction='structural target block; original enclosing section extraction retained in arrivals-v1',
               target_tag=target.tag)
    tmpdoc = next(x for x in temporary if x['document_url'] == doc)
    tmpwin = next(x for x in tmpdoc['windows'] if x['url'] == row['url'])
    tmpwin['window'].update(scope_locator=locator, text=text, links=dom.links(scope))
    corrections.append(dict(url=row['url'], original=original,
                            corrected={k: row[k] for k in ('locator', 'declared_window_word_count', 'declared_window_sha256', 'html_sha256')},
                            reason='A footnote/backlink/TOC/comment structural block is not its entire enclosing chapter or main.',
                            receipt=receipt,
                            atoms_or_source_pool_changed=False))
write('arrivals.json', arrivals)
write('windows.tmp.json', temporary)
write('scope-corrections.json', dict(protocol='dt/class remains its section; only structural anchors corrected',
                                     affected_urls=len(corrections), corrections=corrections))
print(json.dumps(dict(corrected=len(corrections), documents=len(documents)), ensure_ascii=False))
