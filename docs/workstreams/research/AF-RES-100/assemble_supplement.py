"""Assemble supplementary source records and the 24 displaced/added positions.

Does not change packet, protocol, judgment, or pair ledgers. The first 22 source
records are the already sealed intake; post-seal evidence remains so labelled.
"""
from pathlib import Path
import argparse, csv, hashlib, io, json

ROOT = Path(__file__).resolve().parent
def jl(p): return [json.loads(x) for x in (ROOT/p).read_text().splitlines() if x.strip()]
def dump(rows): return ''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows)
def output(path, text, check):
    p=ROOT/path
    if check:
        assert p.read_bytes()==text.encode('utf-8'), 'reconstruction mismatch: '+path
    else: p.write_text(text)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args()
    annotations=json.loads((ROOT/'evidence/resume2/supplement_annotations.json').read_text())
    corpus={r['file_id']:r for r in jl('corpus-files.jsonl')}
    accesses=jl('evidence/resume2/postseal-access.jsonl')
    original=[r for r in jl('sources.jsonl') if r['source_id'].startswith('R0-')]
    assert len(original)==22
    sources=original[:]
    for fid,an in annotations.items():
        f=corpus[fid];ev=[e for e in accesses if e['file_id']==fid and e['segments']]
        assert ev, 'not directly read: '+fid
        raw=(ROOT/f['cached_body']).read_bytes();assert hashlib.sha256(raw).hexdigest()==f['sha256']
        spans=[]
        for e in ev:
            for s in e['segments']:
                assert hashlib.sha256(raw[s['byte_start']:s['byte_end']]).hexdigest()==s['sha256']
                if s not in spans:spans.append(s)
        sources.append({'source_id':'AUD-'+fid,'q_numbers':['Q3','Q6'],'case_id':','.join(an['cases']),
          'direct_url':f.get('archive_url') or f['url'],'fixed_url':f['url'],
          'checked_utc':ev[0]['checked_utc'],'last_checked_utc':ev[-1]['checked_utc'],
          'author_publisher':an.get('author',f['repo']+' upstream maintainers'),
          'lineage':f['repo']+'/'+f['path']+'; '+('NetBSD-derived regression script in GNU sed distribution' if fid=='SED-0022' else 'official versioned upstream source'),
          'version':f['version'],'commit':f.get('commit'),
          'exact_section_payload':{'file_id':fid,'path':f['path'],'segments':spans},
          'body_sha256':f['sha256'],'confirmed':an['confirmed'],'supports':an['supports'],
          'limits':[an['limit'],'post-seal2 supplementary audit; no retroactive primary judgment credit'],
          'count_minimum':an.get('count',True),'count_group':an['group'],
          'duplicate_reason':'one count per pinned upstream file; repeated F/S/A/B access and archive are not extra sources',
          'research_phase':'post-seal2 source/displacement audit',
          'access_receipt':'evidence/resume2/postseal-access.jsonl',
          'direct_read_method':'verified upstream download restored to ignored cache, then exact raw source intervals displayed and logged'})
    for rel in ['evidence/resume2/outcomes/sources.jsonl','evidence/resume2/crossdomain/sources.jsonl']:
        if (ROOT/rel).exists():sources.extend(jl(rel))
    if (ROOT/'evidence/resume2/docker-postseal.json').exists():
        sources.append(json.loads((ROOT/'evidence/resume2/docker-postseal.json').read_text()))
    ids=[r['source_id'] for r in sources];assert len(ids)==len(set(ids)),'duplicate source ID'
    output('sources.jsonl',dump(sources),a.check)
    outcome_file=ROOT/'evidence/resume2/outcomes/outcomes.csv'
    if outcome_file.exists():
        outcome_rows=list(csv.DictReader(outcome_file.open()))
        assert len(outcome_rows)==8
        for row in outcome_rows:
            row['evidence_details_file']='evidence/resume2/outcomes/evidence-details.json'
        ob=io.StringIO();ow=csv.DictWriter(ob,fieldnames=list(outcome_rows[0]));ow.writeheader();ow.writerows(outcome_rows)
        output('outcomes.csv',ob.getvalue(),a.check)
    packets=jl('packets.jsonl');judgments={r['packet_id']:r for r in jl('judgments.jsonl')}
    pmap={(p['case_id'],p['policy'],p['mode']):p for p in packets}
    rows=[]
    roles={
      'JQ-0075':('lexical/input plumbing',False,False,False),
      'JQ-0080':('independent upstream corroboration',False,True,False),
      'SED-0001':('adjacent preprocessing constraint',False,False,True),
      'SED-0022':('independent adjacent regression; wrong task',False,True,False),
      'JQ-0070':('partial argv receiver evidence',False,False,True),
      'JQ-0072':('generic shell hint / lexical overlap',False,False,False),
      'WT-0021':('output-consumer schema corroboration',False,False,True),
      'WT-0039':('proposal / lexical overlap',False,False,False),
      'JQ-0045':('low-level object implementation',False,False,False),
      'JQ-0046':('low-level API declarations',False,False,False),
      'AWS-0706':('input schema corroboration',False,False,False),
      'AWS-0248':('wrong AWS service / lexical overlap',False,False,False),
      'PD-0227':('output image type recognition',False,False,False),
      'PD-0005':('wrong output format / lexical overlap',False,False,False),
      'KN-0024':('essential input-function connection under helper interpretation',True,False,True),
      'KN-0013':('extension-printing option is not file selection',False,False,True),
      'PD-0012':('phase/runtime dependency boundary',False,False,True),
      'PD-0018':('architecture navigation only',False,False,False),
      'CE-0001':('library install and test dependency',False,False,True),
      'CE-0004':('WASM plugin dependency, different user version',False,False,True),
      'PD-0022':('main-tool flag boundary only',False,False,True)}
    for case in ['J2','J3','J4','P1','P2','P3']:
      for policy,change in [('A','displaced_main'),('B','added_adjacent')]:
        pf=pmap[(case,policy,'F')];ps=pmap[(case,policy,'S')]
        for slot in [3,4]:
          sf,ss=pf['slots'][slot-1],ps['slots'][slot-1]
          fid=sf.get('file_id')
          citations=[{'condition':c['id'],**z} for c in judgments[pf['packet_id']]['conditions'] for z in c['citations'] if z['slot']==slot]
          role,essential,test,build=roles.get(fid,('unresolved version; charged vacancy',False,False,False))
          full_in_s=[]
          for z in citations:
            full_in_s.append(ss.get('char_start',0)<=z['char_start'] and z['char_end']<=ss.get('char_end',0))
          an=annotations.get(fid,{})
          ev=[e for e in accesses if e['file_id']==fid and e['segments']]
          row={'case_id':case,'change':change,'policy':policy,'slot':slot,'file_id':fid or '',
            'url':sf.get('url',''),'version':sf.get('version',''),'source_sha256':sf.get('sha256',''),
            'F_packet':pf['packet_id'],'S_packet':ps['packet_id'],'F_range':json.dumps([sf.get('char_start'),sf.get('char_end')]),
            'S_range':json.dumps([ss.get('char_start'),ss.get('char_end')]),
            'section_class':role,'essential_for_primary_complete':essential,'independent_upstream_test':test,
            'build_or_input_constraint':build,'F_primary_citations':json.dumps(citations,ensure_ascii=False),
            'F_citations_fully_in_S':json.dumps(full_in_s),'directly_read_source_segments':json.dumps([s for e in ev for s in e['segments']],ensure_ascii=False),
            'confirmed':an.get('confirmed','P3 adjacent latest stable release/source unresolved; two slots retained empty in each reading unit.'),
            'limit':an.get('limit','Exclude P3 pair from strict win/loss denominator; vacancy is not automatic defeat.'),
            'primary_change_after_seal2':False,
            'same_result_failure_condition_removed':'none established; candidate constraints/corroboration are not a verified removed failure condition'}
          rows.append(row)
    assert len(rows)==24
    buf=io.StringIO();w=csv.DictWriter(buf,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    output('displacement.csv',buf.getvalue(),a.check)
    print(json.dumps({'sources':len(sources),'counted':sum(bool(x.get('count_minimum')) for x in sources),'displacement_positions':len(rows),'check':a.check}))

if __name__=='__main__':main()
