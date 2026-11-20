#!/usr/bin/env python3
"""Merge preserved reading logs and conservatively audit the per-site cap."""
from collections import Counter
import json
from pathlib import Path
from urllib.parse import urlsplit

BASE=Path(__file__).resolve().parents[1]

def site(url):
    host=urlsplit(url).hostname or ''
    if host.endswith('github.io') or host in {'github.com','raw.githubusercontent.com'}:
        return 'github-platform-including-pages'
    if host.endswith('upenn.edu'):
        return 'upenn.edu'
    if host.endswith('eric.ed.gov'):
        return 'eric.ed.gov'
    return host.removeprefix('www.')

def main():
    sources=[]; excluded=[]; supplementary=[]
    names=['schemes-sources.json','reliability-sources.json','vocab-sources.json']
    if (BASE/'evidence/impact-sources.json').exists(): names.append('impact-sources.json')
    for name in names:
        obj=json.loads((BASE/'evidence'/name).read_text())
        for row in obj['sources']:
            r=dict(row)
            r['reading_log']='evidence/'+name
            r['external_method_or_scheme']=r['id'].startswith(('S','M'))
            r['conservative_site_key']=site(r['url'])
            if len(r['accessed_at_utc'])==10:
                r['access_time_precision']='UTC date only; exact clock time was not logged'
            sources.append(r)
        excluded.extend([{'reading_log':'evidence/'+name,**r} for r in obj.get('excluded',[])])
        supplementary.extend([{'reading_log':'evidence/'+name,**r} for r in obj.get('supplementary_not_counted',[])])
    supplement=BASE/'evidence/reliability-supplement.json'
    if supplement.exists():
        obj=json.loads(supplement.read_text())
        for row in obj.get('sources',[])+obj.get('supporting_reads',[]):
            r=dict(row);r['reading_log']='evidence/reliability-supplement.json'
            r['external_method_or_scheme']=True;r['conservative_site_key']=site(r['url'])
            sources.append(r)
        excluded.extend([{'reading_log':'evidence/reliability-supplement.json',**r} for r in obj.get('excluded',[])])
    assert len({r['id'] for r in sources})==len(sources)
    fields={'id','url','accessed_at_utc','source_type','title','version_or_date','sections_read','confirmed','limits','level','used_in'}
    for r in sources:
        assert fields<=set(r),(r['id'],fields-set(r))
    counts=Counter()
    # Preserve one primary SPDX source, Libraries.io code, and ecosyste.ms README
    # even if all GitHub Pages/raw/GitHub are treated as a single hosting site.
    github_preferred={'S01','S08','S09'}
    for r in sources:
        key=r['conservative_site_key']
        counted=r['external_method_or_scheme'] and r['level'] in ('D1','D2') and r.get('counted_for_minimum',True)
        if key=='github-platform-including-pages':
            counted=counted and r['id'] in github_preferred
        counted=counted and counts[key]<3
        r['counts_toward_external_minimum']=counted
        r['counting_reason']='direct body/fixed code read, within conservative site cap' if counted else (
            'fixed prior research input, not new external literature' if r['id'].startswith('V')
            else 'post-freeze candidate verification, not methods/schemes literature' if r['id'].startswith('I')
            else 'supplemental tracing read excluded from minimum by the preserved reading log' if not r.get('counted_for_minimum',True)
            else 'read and usable, excluded from minimum only by conservative shared-site cap')
        if counted: counts[key]+=1
    counted=[r for r in sources if r['counts_toward_external_minimum']]
    audit={'directly_read_external_n':sum(r['external_method_or_scheme'] for r in sources),
        'core_method_scheme_sources_n':sum(r['external_method_or_scheme'] and r.get('counted_for_minimum',True) for r in sources),
        'counted_after_site_cap_n':len(counted),'counted_ids':[r['id'] for r in counted],
        'by_conservative_site':dict(sorted(counts.items())),
        'indexing_empirical_ids':[r['id'] for r in counted if r['source_type']=='색인 실증 연구'],
        'software_empirical_ids':[r['id'] for r in counted if r['source_type']=='소프트웨어 분류 실증 연구'],
        'metric_method_ids':[r['id'] for r in counted if r['source_type'].startswith('일치도 지표')],
        'software_scheme_families':{'SPDX':['S01','S02'],'CycloneDX':['S03'],'PyPI':['S04','S05'],'Debian':['S06'],'Libraries.io':['S07','S08'],'ecosyste.ms':['S09','S10'],'Wikidata':['S11','S12'],'CPE':['S13']},
        'other_field_principles':{'patent':['S14','S15','S16'],'library':['S17'],'clinical research':['S18'],'design patterns':['S19','S20','S21']},
        'prior_input_sources_n':sum(r['id'].startswith('V') for r in sources),
        'impact_verification_sources_n':sum(r['id'].startswith('I') for r in sources),
        'all_directly_read_external_n':sum(not r['id'].startswith('V') for r in sources),
        'excluded_attempt_records_n':len(excluded)}
    assert len(counted)>=25
    assert max(counts.values())<=3
    assert len(audit['indexing_empirical_ids'])>=4
    assert len(audit['metric_method_ids'])>=3
    obj={'study':'AF-RES-016','counting_rule':'Only directly read external bodies/fixed code count. All GitHub Pages/raw/GitHub conservatively share one site; max three per site. Prior AF-RES and coding units do not count.',
        'sources':sources,'excluded':excluded,'supplementary_not_counted':supplementary,'audit':audit}
    (BASE/'sources.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    (BASE/'evidence/source-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(audit,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
