#!/usr/bin/env python3
"""Resolve only citations actually present in a frozen response, never invent links."""
import argparse, collections, re
from common import load, save

REF = re.compile(r'turn\d+[a-z]+\d+')

def citation_links(run, source_file, resolution_rows):
    refs = set(REF.findall(run['raw_response']))
    candidates = collections.defaultdict(set)
    methods = collections.defaultdict(set)
    for doc in run.get('opened_documents', []):
        for ref in REF.findall(str(doc.get('source_ref', ''))):
            if ref in refs:
                candidates[ref].add(doc['url']); methods[ref].add('preserved source_ref in run document log')
    for row in resolution_rows:
        ref = row['original_ref']
        if row['source_file'] == source_file and ref in refs:
            candidates[ref].add(row['url']); methods[ref].add('metadata of actual emitted citation re-opened by root')
    links = [{'source_ref': ref, 'url': next(iter(candidates[ref])), 'methods': sorted(methods[ref])}
             for ref in sorted(refs) if len(candidates[ref]) == 1]
    unresolved = [{'source_ref': ref, 'possible_urls': sorted(candidates[ref]),
                   'reason': 'No unique preserved or observed URL mapping'}
                  for ref in sorted(refs) if len(candidates[ref]) != 1]
    return links, unresolved

def main(partial, write):
    resolution = load('evidence/citation-resolution.json', {'rows': []})['rows']
    rows = []
    for dispatch in load('questions/dispatch.json')['order']:
        run = load(dispatch['output'])
        if not run or len(run.get('checks', [])) != 3:
            if partial: continue
            raise AssertionError(('Incomplete run', dispatch['output']))
        links, unresolved = citation_links(run, dispatch['output'], resolution)
        rows.append({'source_file': dispatch['output'], 'citation_links': links,
                     'unresolved_citations': unresolved})
    result = {'rows': rows, 'runs': len(rows), 'resolved_refs': sum(len(r['citation_links']) for r in rows),
              'unresolved_refs': sum(len(r['unresolved_citations']) for r in rows),
              'limits': 'Only source references actually printed in raw_response are mapped. Opened-document logs without a matching printed reference do not create supplied citations. Link presence does not establish factual support.'}
    if write: save('analysis/citation-audit.json', result)
    print({k: result[k] for k in ['runs', 'resolved_refs', 'unresolved_refs']})

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--partial', action='store_true'); p.add_argument('--write', action='store_true')
    a = p.parse_args(); main(a.partial, a.write)
