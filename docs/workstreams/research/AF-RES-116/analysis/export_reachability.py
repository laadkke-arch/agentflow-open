#!/usr/bin/env python3
"""Export exact frozen coverage rows and witness view locations, not reader data."""
from pathlib import Path
import argparse,json
OWN=Path(__file__).resolve().parent.parent

def render():
    data=json.loads((OWN/'reachability/coverage-v1/coverage-summary.json').read_text());rows=[]
    for r in data['results']:
        r={**r,'source_requirement_file':'gold-intervals.json','frozen_graph_archive':'reachability/raw-enumeration.tar.gz','source_reference_seal':'8b57d241d88cb6c5ddf3454d2b28fa3fb46fd473'}
        if r.get('witness'):
            views={v['view_id']:v for v in map(json.loads,(OWN/'reachability/raw'/r['case_id']/'views.jsonl').read_text().splitlines())}
            r['witness_views']=[{k:v for k,v in views[vid].items() if k not in ['display_text','body_text','navigation_text']} for vid in r['witness']['view_ids']]
        rows.append(r)
    return ''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args();value=render();p=OWN/'reachability.jsonl'
    if a.check:
        assert p.read_text()==value,'reachability export differs'
    else:p.write_text(value)
    print(json.dumps({'rows':len(value.splitlines()),'check':a.check,'match':True}))
