#!/usr/bin/env python3
"""Bounded, offline document reader for AF-RES-116.

No network, model calls, hidden-URL navigation, or correctness judgement.
The output of open/choose is exactly one <=1500-codepoint document display.
The append-only hash-chained log records the display and all accepted actions.
This is procedural blinding on a shared filesystem, not an access-control sandbox.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import fcntl
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
import time
from urllib.parse import urlsplit, urlunsplit

OWNED = Path(__file__).resolve().parent.parent
DEFAULT_SESSIONS = OWNED / 'readers'
LIMIT = 1500
MAX_OPENS = 3
SAFE_ID = re.compile(r'[A-Za-z0-9_-]{1,48}\Z')
RESERVED = {'open', 'next', 'again', 'back'}


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def owned_path(value):
    p = Path(value).resolve()
    if not p.is_relative_to(OWNED):
        raise ValueError('output must remain within the AF-RES-116 owned path')
    return p


@dataclass(frozen=True)
class Corpus:
    path: Path
    sha256: str
    documents: dict
    links: dict

    @classmethod
    def load(cls, path):
        path = Path(path).resolve()
        raw = path.read_bytes()
        data = json.loads(gzip.decompress(raw) if path.suffix=='.gz' or raw.startswith(b'\x1f\x8b') else raw)
        if data.get('schema') != 1 or not isinstance(data.get('documents'), list):
            raise ValueError('expected corpus schema=1 and documents list')
        docs, links = {}, {}
        for doc in data['documents']:
            did = doc.get('id', '')
            if not SAFE_ID.fullmatch(did) or did in docs:
                raise ValueError('document IDs must be unique short ASCII identifiers')
            if not all(isinstance(doc.get(k), str) and doc[k] for k in ('url', 'version', 'source_sha')):
                raise ValueError('document requires url, version, source_sha strings')
            if not isinstance(doc.get('text'), str):
                raise ValueError('document text must be a string')
            if not isinstance(doc.get('links', []), list):
                raise ValueError('links must be a list')
            if not isinstance(doc.get('navigation_spans', []), list):
                raise ValueError('navigation_spans must be a list')
            for span in doc.get('navigation_spans', []):
                a, b = span.get('start'), span.get('end')
                if type(a) is not int or type(b) is not int or not 0 <= a < b <= len(doc['text']):
                    raise ValueError('invalid document navigation interval')
            docs[did] = doc
        if not docs:
            raise ValueError('empty corpus')
        for did, doc in docs.items():
            previous_end = -1
            for link in sorted(doc.get('links', []), key=lambda x: (x.get('start', -1), x.get('end', -1))):
                lid = link.get('id', '')
                if not SAFE_ID.fullmatch(lid) or lid in RESERVED or lid in links:
                    raise ValueError('link IDs must be globally unique and not reserved')
                a, b = link.get('start'), link.get('end')
                if type(a) is not int or type(b) is not int or not 0 <= a < b <= len(doc['text']):
                    raise ValueError('invalid link interval')
                if a < previous_end:
                    raise ValueError('overlapping link display intervals')
                previous_end = b
                if not isinstance(link.get('label'), str) or not link['label']:
                    raise ValueError('link requires upstream label')
                token = doc['text'][a:b]
                if lid not in token or link['label'] not in token:
                    raise ValueError('link display interval must contain its ID and full label')
                target = link.get('target_doc')
                offset = link.get('target_offset')
                if target not in docs or type(offset) is not int or not 0 <= offset <= len(docs[target]['text']):
                    raise ValueError('link target must be a fixed allowed document and valid offset')
                if 'display' in link and token != link['display']:
                    raise ValueError('explicit link display does not match document text')
                links[lid] = {**link, 'source_doc': did}
        return cls(path, digest(raw), docs, links)

    def render(self, doc_id, offset):
        """A pure document page. Every history sees the same page at an offset.

        Header/footer reserve is 150 codepoints. Actual unused reserve stays blank
        (it is not filled with extra text), making pagination independent of EOF.
        Link tokens crossing the cut move intact to the next page when possible.
        Footer back/again always shows, but back is actionable only with history.
        """
        if doc_id not in self.documents:
            raise ValueError('document is not in the fixed corpus')
        doc = self.documents[doc_id]
        if type(offset) is not int or not 0 <= offset <= len(doc['text']):
            raise ValueError('invalid document offset')
        header = f'[{doc_id} {doc["version"]} offset={offset}]\n'
        reserve = 150
        if len(header) > 100:
            raise ValueError('header exceeds fixed navigation reserve')
        end = min(len(doc['text']), offset + LIMIT - reserve)
        deferred = []
        for link in doc.get('links', []):
            if offset < link['start'] < end < link['end']:
                end = link['start']
                deferred.append(link['id'])
        body = doc['text'][offset:end]
        has_next = end < len(doc['text'])
        footer = '\n' + ('[next] 다음 구간' if has_next else '[end] 문서 끝')
        footer += ' | [again] 재열람 | [back] 직전 열람(있으면)\n'
        display = header + body + footer
        if len(display) > LIMIT:
            raise ValueError('display exceeds budget')
        visible = [link['id'] for link in doc.get('links', []) if offset <= link['start'] and link['end'] <= end]
        partial = [link['id'] for link in doc.get('links', []) if link['start'] < end and link['end'] > offset and link['id'] not in visible]
        nav_ranges = sorted((max(offset,x['start']),min(end,x['end'])) for x in doc.get('navigation_spans',[]) if x['start']<end and x['end']>offset)
        merged=[]
        for a,b in nav_ranges:
            if merged and a<=merged[-1][1]:merged[-1][1]=max(merged[-1][1],b)
            else:merged.append([a,b])
        doc_nav=''.join(doc['text'][a:b] for a,b in merged)
        content=[];cursor=offset
        for a,b in merged:
            content.append(doc['text'][cursor:a]);cursor=b
        content.append(doc['text'][cursor:end]);content=''.join(content)
        fragment = ''
        anchors = doc.get('anchors', {})
        if isinstance(anchors, dict):
            candidates = [(int(pos), name) for name, pos in anchors.items() if type(pos) is int and pos <= offset]
            if candidates:
                fragment = sorted(candidates)[-1][1]
        url = doc['url']
        if fragment:
            parts = urlsplit(url)
            url = urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, fragment))
        return {
            'doc_id': doc_id, 'offset_start': offset, 'offset_end': end,
            'requested_document_url': doc['url'], 'arrival_url': url,
            'arrival_url_kind': 'canonical_source_locator_reconstructed_for_offline_view; not_observed_HTTP_arrival',
            'fragment': fragment, 'fragment_basis': 'nearest_preceding_fixed_anchor' if fragment else 'none',
            'document_version': doc['version'], 'source_sha': doc['source_sha'],
            'corpus_sha256': self.sha256, 'body_text': body, 'navigation_text': header + footer,
            'display_text': display, 'display_sha256': digest(display), 'body_sha256': digest(body),
            'body_codepoints': len(body), 'body_utf8_bytes': len(body.encode()),
            'navigation_codepoints': len(header) + len(footer),
            'navigation_utf8_bytes': len((header + footer).encode()),
            'source_slice_codepoints': len(body), 'source_slice_utf8_bytes': len(body.encode()),
            'content_codepoints': len(content), 'content_utf8_bytes': len(content.encode()),
            'document_navigation_codepoints': len(doc_nav), 'document_navigation_utf8_bytes': len(doc_nav.encode()),
            'total_navigation_codepoints': len(header)+len(footer)+len(doc_nav),
            'total_navigation_utf8_bytes':len((header+footer).encode())+len(doc_nav.encode()),
            'document_navigation_intervals':merged,
            'navigation_classification_supplied': 'navigation_spans' in doc,
            'body_metric_definition':'body_* is full source slice including document navigation; use content_* and total_navigation_* for disjoint semantic cost accounting',
            'display_codepoints': len(display), 'display_utf8_bytes': len(display.encode()),
            'visible_link_ids': visible, 'partial_link_ids': partial, 'deferred_link_ids': deferred,
            'next_offset': end if has_next else None,
            'transport': 'offline_fixed_document_viewer', 'http_request_performed': False,
            'render_reserve_codepoints': reserve,
        }


def actions_for(corpus, history, known_links):
    """Every allowed continuation, including previously visible links."""
    if not history:
        return {}
    current = history[-1]
    actions = {}
    for lid in sorted(known_links):
        link = corpus.links[lid]
        actions[lid] = {'doc_id': link['target_doc'], 'offset': link['target_offset'], 'kind': 'link', 'source_doc': link['source_doc'], 'link_display_start': link['start'], 'link_display_end': link['end'], 'label': link['label'], 'fragment': link.get('fragment', '')}
    if current['next_offset'] is not None:
        actions['next'] = {'doc_id': current['doc_id'], 'offset': current['next_offset'], 'kind': 'next'}
    actions['again'] = {'doc_id': current['doc_id'], 'offset': current['offset_start'], 'kind': 'reopen'}
    if len(history) > 1:
        previous = history[-2]
        actions['back'] = {'doc_id': previous['doc_id'], 'offset': previous['offset_start'], 'kind': 'back'}
    return actions


def read_events(stream):
    stream.seek(0)
    events = []
    previous = None
    for number, line in enumerate(stream, 1):
        if not line.endswith('\n'):
            raise ValueError('incomplete last log record; preserve and repair separately')
        record = json.loads(line)
        actual = record.pop('event_sha256', None)
        if record.get('seq') != number or record.get('previous_event_sha256') != previous or actual != digest(canonical(record)):
            raise ValueError('event chain changed')
        record['event_sha256'] = actual
        events.append(record)
        previous = actual
    return events


def append_event(stream, events, item):
    item = {'seq': len(events) + 1, 'previous_event_sha256': events[-1]['event_sha256'] if events else None, 'at_utc': utc(), **item}
    item['event_sha256'] = digest(canonical(item))
    stream.seek(0, 2)
    stream.write(canonical(item) + '\n')
    stream.flush()
    events.append(item)
    return item


def derive(events):
    exposures = [x for x in events if x['event'] == 'exposure']
    answers = [x for x in events if x['event'] == 'answer']
    known = {lid for event in exposures for lid in event['view']['visible_link_ids']}
    return exposures, answers, known, any(x['event'] == 'finish' for x in events)


def run(args):
    started = time.perf_counter()
    if not SAFE_ID.fullmatch(args.session):
        raise ValueError('invalid session ID')
    root = owned_path(args.sessions)
    directory = root / args.session
    if args.command == 'init':
        if directory.exists():
            raise ValueError('session already exists; never overwrite an observed session')
        corpus = Corpus.load(args.corpus)
        if args.start_doc not in corpus.documents:
            raise ValueError('start document is not in corpus')
        corpus.render(args.start_doc, args.start_offset)
        directory.mkdir(parents=True)
        with (directory/'events.jsonl').open('x+', encoding='utf-8') as stream:
            append_event(stream, [], {
                'event': 'init', 'session': args.session, 'reader_id': args.reader_id,
                'corpus_path': str(corpus.path), 'corpus_sha256': corpus.sha256,
                'engine_sha256': digest(Path(__file__).read_bytes()),
                'start_doc': args.start_doc, 'start_offset': args.start_offset,
                'max_opens': MAX_OPENS, 'max_display_codepoints': LIMIT,
                'method': 'fresh_AI_context_if_caller_supplied_it; engine_does_not_prove_context_independence',
                'os_isolation': False, 'prepared_at_utc': utc(),
            })
        return 'Session ready. Open the supplied starting document.\n'
    logfile = directory/'events.jsonl'
    if not logfile.is_file():
        raise ValueError('session has not been initialized')
    with logfile.open('r+', encoding='utf-8') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        events = read_events(stream)
        init = events[0]
        if init['event'] != 'init':
            raise ValueError('missing initialization event')
        corpus = Corpus.load(init['corpus_path'])
        if corpus.sha256 != init['corpus_sha256']:
            raise ValueError('fixed corpus changed after session initialization')
        if digest(Path(__file__).read_bytes()) != init['engine_sha256']:
            raise ValueError('reader engine changed after session initialization')
        exposures, answers, known, finished = derive(events)
        step = len(exposures)
        def reject(message):
            append_event(stream, events, {'event': 'rejected_action', 'session': args.session, 'command': args.command, 'action': getattr(args, 'action', None), 'step_before': step, 'reason': message})
            raise ValueError(message)
        if finished:
            reject('session is finished')
        if args.command in ('open', 'choose'):
            if step >= MAX_OPENS:
                reject('three-opening budget exhausted')
            if step and (not answers or answers[-1]['step'] != step):
                reject('record the current stage answer before the next opening')
            if args.command == 'open':
                if step:
                    reject('initial open is allowed only once; use a visible action')
                action = 'open'
                target = {'doc_id': init['start_doc'], 'offset': init['start_offset'], 'kind': 'initial_open'}
            else:
                if not step:
                    reject('first action must open the supplied starting document')
                action = args.action
                allowed = actions_for(corpus, [x['view'] for x in exposures], known)
                if action not in allowed:
                    reject('action has not been fully shown or is not currently available')
                target = allowed[action]
            if not args.reason.strip():
                reject('a selection reason must precede the exposure')
            choice = append_event(stream, events, {'event': 'choice', 'session': args.session, 'next_step': step+1, 'action': action, 'target': target, 'selection_reason': args.reason, 'previous_answer_event_sha256': answers[-1]['event_sha256'] if answers else None, 'elapsed_since_previous_answer_seconds':(datetime.now(timezone.utc)-datetime.fromisoformat(answers[-1]['at_utc'])).total_seconds() if answers else None})
            view = corpus.render(target['doc_id'], target['offset'])
            history = [x['view'] for x in exposures] + [view]
            new_known = known | set(view['visible_link_ids'])
            possible = actions_for(corpus, history, new_known) if step+1 < MAX_OPENS else {}
            append_event(stream, events, {
                'event': 'exposure', 'session': args.session, 'step': step+1,
                'action': action, 'choice_event_sha256': choice['event_sha256'], 'view': view,
                'known_link_ids_after': sorted(new_known), 'allowed_actions_after': possible,
                'cumulative_display_codepoints': sum(x['view']['display_codepoints'] for x in exposures)+view['display_codepoints'],
                'cumulative_display_utf8_bytes': sum(x['view']['display_utf8_bytes'] for x in exposures)+view['display_utf8_bytes'],
                'command_wall_seconds': time.perf_counter()-started,
                'reader_active_seconds': None,
            })
            return view['display_text']
        if args.command == 'answer':
            if not step:
                reject('cannot answer before first exposure')
            if answers and answers[-1]['step'] == step:
                reject('stage answer is already sealed; do not overwrite it')
            if args.json:
                answer = json.loads(args.json)
            else:
                answer = {'operation':args.operation,'preservation':args.preservation,'exceptions':args.exceptions,'disposition':args.disposition,'citations':json.loads(args.citations_json),'notes':args.notes}
            for key in ('operation','preservation','exceptions','disposition'):
                if not isinstance(answer.get(key), str) or not answer[key].strip():
                    reject('answer requires nonempty operation, preservation, exceptions, disposition')
            if not isinstance(answer.get('citations', []), list):
                reject('citations must be a list')
            for citation in answer.get('citations', []):
                if not isinstance(citation, dict) or not isinstance(citation.get('quote'), str):
                    reject('each citation needs an exact quote string')
            append_event(stream, events, {'event':'answer','session':args.session,'step':step,'answer':answer,'exposure_event_sha256':exposures[-1]['event_sha256'],'recorded_before_next_open':True,'command_wall_seconds':time.perf_counter()-started,'elapsed_since_exposure_seconds':(datetime.now(timezone.utc)-datetime.fromisoformat(exposures[-1]['at_utc'])).total_seconds(),'elapsed_is_wall_not_human_active_time':True})
            return 'Stage answer recorded.\n'
        if args.command == 'finish':
            if not step or not answers or answers[-1]['step'] != step:
                reject('answer the current exposure before finishing')
            if step < MAX_OPENS and not args.stop:
                reject('finishing before three openings requires explicit --stop')
            append_event(stream, events, {'event':'finish','session':args.session,'observed_steps':step,'early_stop':step<MAX_OPENS,'unobserved_early_stop_positions':MAX_OPENS-step,'summary':args.summary,'final_answer_event_sha256':answers[-1]['event_sha256'],'measured_session_wall_seconds':(datetime.now(timezone.utc)-datetime.fromisoformat(init['at_utc'])).total_seconds(),'human_time_saving_inferred':False})
            return 'Session finished.\n'
    raise ValueError('unknown command')


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sessions', default=str(DEFAULT_SESSIONS))
    p.add_argument('--session', required=True)
    sub = p.add_subparsers(dest='command', required=True)
    x = sub.add_parser('init')
    x.add_argument('--corpus', required=True)
    x.add_argument('--start-doc', required=True)
    x.add_argument('--start-offset', type=int, default=0)
    x.add_argument('--reader-id', default='unspecified')
    x = sub.add_parser('open'); x.add_argument('--reason', required=True)
    x = sub.add_parser('choose'); x.add_argument('--action', required=True); x.add_argument('--reason', required=True)
    x = sub.add_parser('answer')
    x.add_argument('--json')
    for name in ('operation','preservation','exceptions','disposition','notes'):
        x.add_argument('--'+name, default='')
    x.add_argument('--citations-json', default='[]')
    x = sub.add_parser('finish'); x.add_argument('--stop', action='store_true'); x.add_argument('--summary', required=True)
    return p


def main():
    try:
        sys.stdout.write(run(parser().parse_args()))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print('Reader error: '+str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
