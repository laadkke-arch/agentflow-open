#!/usr/bin/env python3
"""Prepare user first windows and link order from frozen local responses only.

No network client, destination fetching, feature editing, or C1/C2 assessment.
Requires the later stage3 SHA and actual case/provider plan before execution.
SC032 is returned as inherited-only without reading its cached README.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

sys.dont_write_bytecode = True
OWN = Path(__file__).resolve().parent
BASE = OWN.parent.parent
FEATURES = OWN.parent / 'features-schema'
STAGE2_SHA = '412192e28356bee13e4c11f20511ab5ec590662c'


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_read(path: Path):
    return json.loads(path.read_text())


def normalized(text: str) -> str:
    return ' '.join(text.split())


def local_renderer():
    path = FEATURES / 'render_windows.py'
    spec = importlib.util.spec_from_file_location('frozen_schema_renderer', path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module, digest(path.read_bytes())


def content_html(raw_path: Path, renderer):
    """Preserve frozen text rendering; select HTML content before windowing."""
    from lxml import html
    rendered = renderer.rendered(raw_path)
    tree = html.fromstring(rendered)
    if raw_path.suffix == '.html':
        candidates = tree.xpath('//main | //article')
        if candidates:
            tree = candidates[0]
            selection = tree.tag
        else:
            bodies = tree.xpath('//body')
            tree = bodies[0] if bodies else tree
            selection = 'body-or-fragment'
    else:
        selection = 'rendered-repository-document'
    # Remove semantic chrome; authored README lists and internal TOC links remain.
    for node in list(tree.iterdescendants()):
        if not isinstance(node.tag, str):
            continue  # lxml comment nodes have no element attributes
        tag = node.tag.lower()
        role = node.get('role', '').lower()
        classes = set(node.get('class', '').lower().split())
        chrome = bool(classes & {'navbar', 'site-nav', 'site-navigation', 'cookie-banner', 'site-footer'})
        hidden = node.get('hidden') is not None or node.get('aria-hidden', '').lower() == 'true'
        if tag in {'script', 'style', 'nav', 'footer'} or role in {'navigation', 'banner', 'contentinfo'} or chrome or hidden:
            if node.getparent() is not None:
                node.drop_tree()
    # GitHub renders Markdown heading IDs. Record derived IDs explicitly.
    slug_counts = {}
    for node in tree.xpath('.//h1 | .//h2 | .//h3 | .//h4 | .//h5 | .//h6'):
        if node.get('id'):
            continue
        title = normalized(''.join(node.itertext())).lower()
        slug = re.sub(r'[^\w\- ]', '', title, flags=re.UNICODE).replace(' ', '-')
        count = slug_counts.get(slug, 0)
        slug_counts[slug] = count + 1
        node.set('id', slug + ('-' + str(count) if count else ''))
        node.set('data-af-derived-id', 'github-style-heading-slug')
    serialized = html.tostring(tree, encoding='unicode', method='html')
    return serialized, selection


BADGE = re.compile(r'(shields\.io|badge|codecov\.io|coveralls\.io|travis-ci|app\.fossa|badgen\.net)', re.I)
CHROME_URL = re.compile(r'/(login|signup|sponsors|stargazers|network|graphs/contributors|actions)(/|[?#]|$)', re.I)
EXCLUDED_LABEL = re.compile(r'^(license|licence|contributors?|contributing|donate|sponsor(?:s|ship)?|build status|code coverage|stars?|forks?|sign in|log in|contents|table of contents|back to top)$', re.I)
INFORMATION_LABEL = re.compile(r'\b(api|documentation|docs?|reference|specification|standard|install(?:ation)?|usage|use|example|samples?|tutorial|guide|manual|unsupported|tests?|test-suite)\b', re.I)
INFORMATION_PATH = re.compile(r'/(docs?|api|examples?|samples?|tutorials?|guides?|manual|reference|tests?)(/|[.#?\-]|$)', re.I)
PACKAGE_HOSTS = {'www.npmjs.com', 'npmjs.com', 'pypi.org', 'rubygems.org', 'packagist.org', 'hex.pm', 'crates.io', 'nuget.org', 'www.nuget.org', 'mvnrepository.com'}


def classify_link(label: str, target: str, context: str, same_document: bool):
    """Same pre-stage3 policy as paths-ld: admit readable body links by default."""
    parsed = urlsplit(target)
    if not label:
        return 'exclude', 'empty text/image-only link'
    if parsed.scheme not in {'http', 'https'}:
        return 'exclude', 'non-document scheme'
    if re.search(r'badge|shields\.io', target, re.I):
        return 'exclude', 'badge'
    if re.search(r'^/(?:login|logout|signup|session|sessions)(?:/|$)', parsed.path, re.I):
        return 'exclude', 'authentication chrome'
    if parsed.hostname in {'github.com','www.github.com'} and re.fullmatch(r'/[^/]+/[^/]+/(?:actions|issues|pulls|discussions|stargazers|watchers|network|fork|forks)/?', parsed.path):
        return 'exclude', 'repository activity chrome'
    if same_document and parsed.fragment:
        return 'include', 'internal document fragment'
    host = parsed.netloc.casefold()
    if host in {'json-schema.org', 'www.json-schema.org'} and not re.search(r'/(tools|implementations|blog|community)', parsed.path):
        return 'include', 'official JSON Schema specification/overview link'
    if (host.endswith('w3.org') and '/TR/' in parsed.path) or host in {'www.rfc-editor.org', 'rfc-editor.org', 'datatracker.ietf.org'}:
        return 'include', 'official specification link'
    if 'json-schema-test-suite' in target.casefold():
        return 'include', 'official conformance/test reference'
    if host in PACKAGE_HOSTS or host.endswith('.readthedocs.io') or host in {'docs.rs', 'hexdocs.pm', 'dev.erldocs.com'}:
        return 'include', 'installation package or official API/documentation host'
    if INFORMATION_PATH.search(parsed.path):
        return 'include', 'usage/API/example/test documentation path'
    if INFORMATION_LABEL.search(label):
        return 'include', 'explicit specification/installation/usage/API/example link label'
    if re.search(r'\b(documentation|api docs?|installation|usage|examples?|tutorials?)\b', context, re.I):
        return 'include', 'adjacent authored heading/paragraph states permitted document purpose'
    return 'include', 'readable authored body link; no usefulness or condition-based exclusion'


def first_window(cid: str, row: dict, original: str, renderer, overrides: dict):
    cache = FEATURES / row['raw_cache']['path']
    raw = cache.read_bytes()
    response_sha = digest(raw)
    if response_sha != row['raw_cache']['sha256']:
        raise ValueError(f'{cid}: cached response SHA differs from frozen feature receipt')
    git_blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if row.get('commit') and git_blob != row['raw_cache']['git_blob']:
        raise ValueError(f'{cid}: cached Git blob differs from frozen receipt')
    markup, selection = content_html(cache, renderer)
    parser = renderer.Visible()
    parser.feed(markup)
    visible = ''.join(parser.parts)
    headings = sorted([x for x in parser.items if x['tag'] in {'h1','h2','h3','h4','h5','h6'}], key=lambda x:x['start'])
    first = headings[0] if headings else None
    start = first['start'] if first else 0
    requested_fragment = unquote(urlsplit(original).fragment)
    fragment_status = 'not_requested'
    if requested_fragment:
        anchor = next((x for x in parser.items if x['attrs'].get('id') == requested_fragment), None)
        if anchor is None:
            return {'catalog_id':cid,'status':'blocked_fragment_unresolved','original_destination_url':original,
                'requested_fragment':requested_fragment,'response_sha256':response_sha,
                'reason':'Do not substitute the first heading for an unresolved requested fragment.'}
        containing = next((h for h in headings if h['start'] <= anchor['start'] <= h['end']), None)
        first = containing
        start = containing['start'] if containing else anchor['start']
        fragment_status = 'derived_heading_id_match' if anchor['attrs'].get('data-af-derived-id') else 'explicit_source_id_match'
    words = list(re.finditer(r'\S+', visible[start:]))
    count = min(500,len(words))
    end = start + words[count-1].end() if count else start
    text_start = start + words[0].start() if count else start
    text = visible[text_start:end]
    base_url = row['fixed_url']
    base_parts = urlsplit(base_url)
    seen = set()
    links=[]
    for item in sorted((x for x in parser.items if x['tag']=='a' and 'href' in x['attrs']),key=lambda x:x['start']):
        if not (start <= item['start'] < end):
            continue
        label = normalized(visible[item['start']:min(item['end'],end)])
        raw_href = item['attrs']['href']
        target = urljoin(base_url,raw_href)
        previous_heading = next((h for h in reversed(headings) if h['start'] <= item['start']),None)
        heading_text=normalized(visible[previous_heading['start']:previous_heading['end']]) if previous_heading else ''
        # Confine context to the paragraph/block containing the anchor.
        left=visible.rfind('\n\n',start,item['start'])
        right=visible.find('\n\n',item['end'],end)
        left=start if left<start else left
        right=end if right<0 else right
        context=heading_text+' / '+normalized(visible[left:right])[:400]
        parts=urlsplit(target)
        same=(parts.scheme,parts.netloc,parts.path,parts.query)==(base_parts.scheme,base_parts.netloc,base_parts.path,base_parts.query)
        decision,reason=classify_link(label,target,context,same)
        if target in seen:
            decision,reason='exclude','exact resolved URL duplicate; query and fragment retained'
        else:
            seen.add(target)
        override=overrides.get(cid,{}).get(target)
        if override:
            if override.get('decision') not in {'include','exclude'} or not override.get('reason'):
                raise ValueError(f'{cid}: override needs include/exclude and observed-text reason')
            if reason.startswith('exact resolved URL duplicate'):
                raise ValueError(f'{cid}: an override cannot undo exact-URL deduplication')
            decision,reason=override['decision'],'manual visible-context classification: '+override['reason']
        links.append({'document_order':len(links)+1,'label':label,'raw_href':raw_href,'resolved_url':target,
            'window_line':visible[text_start:max(text_start,item['start'])].count('\n')+1,
            'label_clipped_by_window':item['end']>end,'context':context,
            'decision':decision,'reason':reason,'override':override})
    eligible=[l for l in links if l['decision']=='include']
    proposed=eligible[:2]
    boundary=proposed[-1]['document_order'] if len(proposed)==2 else len(links)+1
    unresolved=[l for l in links if l['decision']=='review' and l['document_order']<boundary]
    return {'catalog_id':cid,'status':'needs_link_classification' if unresolved else 'prepared',
        'original_destination_url':original,'source_fixed_url':base_url,'commit':row.get('commit'),'version':row.get('version'),
        'cache_file':str(cache.relative_to(BASE)),'response_sha256':response_sha,'source_git_blob':git_blob if row.get('commit') else None,
        'selected_container':selection,'selected_container_sha256':digest(markup.encode()),
        'first_heading':normalized(visible[first['start']:first['end']]) if first else None,
        'requested_fragment':requested_fragment or None,'fragment_status':fragment_status,
        'anchor_character_start':start,'visible_character_range':[text_start,end],'display_word_count':count,'window_sha256':digest(text.encode()),
        'rendered_text':text,'links_in_document_order':links,'first_two_proposed':proposed,
        'first_two_final':proposed if not unresolved else None,
        'unresolved_before_selection':[l['document_order'] for l in unresolved],
        'empty_link_slot_reason':None if len(proposed)==2 else ('review_required' if unresolved else 'fewer_than_two_eligible_links_in_first_window'),
        'read_status':'generated_not_yet_manually_read','judgment_status':'not_performed'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage3-sha',required=True,help='Actual frozen stage3 Git commit, 40 hexadecimal characters')
    ap.add_argument('--plan',type=Path,required=True,help='JSON list of requirement_id/catalog_id pairs')
    ap.add_argument('--link-overrides',type=Path,help='Optional recorded classifications from the visible cached window only')
    ap.add_argument('--output',type=Path,help='New output directory under evidence/paths-schema; default stage3-SHA')
    args=ap.parse_args()
    if not re.fullmatch(r'[0-9a-f]{40}',args.stage3_sha):
        ap.error('--stage3-sha must be the actual 40-character lowercase commit SHA')
    plan_bytes=args.plan.read_bytes()
    plan=json.loads(plan_bytes)
    if not isinstance(plan,list) or any(not isinstance(x,dict) or not x.get('requirement_id') or not re.fullmatch(r'SC-\d{3}',x.get('catalog_id','')) for x in plan):
        ap.error('--plan must be a JSON list of requirement_id/catalog_id objects')
    out=(args.output or OWN/('stage3-'+args.stage3_sha)).resolve()
    if not out.is_relative_to(OWN) or out==OWN:
        ap.error('--output must be a child directory under evidence/paths-schema')
    if out.exists():
        ap.error('output already exists; use a new directory to preserve the earlier prepared plan')
    override_bytes=args.link_overrides.read_bytes() if args.link_overrides else b'{}'
    overrides=json.loads(override_bytes)
    frozen={x['catalog_id']:x for x in json_read(FEATURES/'features.json')}
    catalog={x['catalog_id']:x for x in csv.DictReader((BASE/'inputs/af-res-056/catalog.csv').open())}
    renderer,renderer_sha=local_renderer()
    results=[]
    for cid in sorted({x['catalog_id'] for x in plan}):
        if cid=='SC-032':
            results.append({'catalog_id':cid,'status':'inherit_AF_RES_056_only','source_result_commit':'2f8ec01e6b52bef4fc3cd003b1690383b6496526','reason':'SC032 cached README not read or regenerated; import fixed056 windows/judgments separately.'})
        elif cid not in frozen:
            results.append({'catalog_id':cid,'status':'cache_outside_this_editor_scope','reason':'This adapter owns frozen SC001–031 cache; do not fetch a new destination.'})
        else:
            results.append(first_window(cid,frozen[cid],catalog[cid]['destination_url'],renderer,overrides))
    out.mkdir(parents=True)
    for result in results:
        if 'rendered_text' in result:
            text=result.pop('rendered_text')
            dest=out/(result['catalog_id']+'-P1.txt')
            dest.write_text(text+'\n')
            result['window_file']=str(dest.relative_to(BASE))
    payload={'generated_utc':datetime.now(timezone.utc).isoformat(),'stage2_sha':STAGE2_SHA,
        'stage3_sha':args.stage3_sha,'stage3_sha_verified_remotely_by_this_script':False,
        'plan_file':str(args.plan),'plan_sha256':digest(plan_bytes),'pairs':plan,
        'overrides_sha256':digest(override_bytes),'script_sha256':digest(Path(__file__).read_bytes()),
        'frozen_renderer_sha256':renderer_sha,'frozen_features_sha256':digest((FEATURES/'features.json').read_bytes()),
        'network_requests':0,'destination_judgments':0,'scope':'P1 generation and P2/P3 link selection only',
        'providers':results}
    (out/'prepared-paths.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    counts={state:sum(r['status']==state for r in results) for state in sorted({r['status'] for r in results})}
    print(json.dumps({'output':str(out),'provider_status_counts':counts,'network_requests':0,'manually_read_windows':0},ensure_ascii=False))
    return 2 if any(r['status'] in {'needs_link_classification','blocked_fragment_unresolved','cache_outside_this_editor_scope'} for r in results) else 0


if __name__=='__main__':
    raise SystemExit(main())
