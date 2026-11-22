from pathlib import Path
import datetime as dt, hashlib, json
P=Path(__file__).resolve().parent
def rows(name):return [json.loads(s) for s in (P/name).read_text().splitlines()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pg=rows('pg-editions.jsonl')
assert [r['version'] for r in pg]==['12.'+str(i) for i in range(3,23)]
for r in pg:
    for m in r['members']:
        assert sha(P/m['relevant_copy'])==m['relevant_bytes_sha256']
        if m['member_path'].endswith('app-psql.html'):
            expected='https://tools.ietf.org/html/rfc4180' if int(r['version'].split('.')[1])<19 else 'https://datatracker.ietf.org/doc/html/rfc4180'
            assert m['target_href']==[expected]
a=(P/'excerpts/pg-12.18-app-psql.html.fragment.html').read_text()
b=(P/'excerpts/pg-12.19-app-psql.html.fragment.html').read_text()
assert a.replace('https://tools.ietf.org/html/rfc4180','https://datatracker.ietf.org/doc/html/rfc4180')==b
for r in rows('sqlite-editions.jsonl'):
    for m in r['members']:assert sha(P/m['relevant_copy'])==m['relevant_bytes_sha256']
ss=rows('sources.jsonl');assert len({s['source_id'] for s in ss})==len(ss)
counted=[s for s in ss if s['count_minimum']]
assert len({s['duplicate_group'] for s in counted})==len(counted)
assert (dt.date(2024,5,9)-dt.date(2024,4,10)).days==29
receipt={'collector':'same researcher, not independent blind reviewer',
 'observed_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
 'command':'python docs/workstreams/research/AF-RES-032/collectors/offline/followup/check_followup.py',
 'target_commit':'A seal 168d90b8519bcb4f673acc659bbaae895f79fca5; followup files not yet committed by collector',
 'input_sha256':{n:sha(P/n) for n in ['cases.json','sources.jsonl','editions.csv','intervals.csv','pg-editions.jsonl','sqlite-editions.jsonl']},
 'exit_code':0,'checks':['PG12.3–12.22 sequence complete; all40 relevant bytes hashes correct',
 'PG12.18→12.19 relevant paragraph differs only by same-RFC href',
 'SQLite4 followup archives8 relevant bytes hashes correct',
 'unique source IDs and counted duplicate groups','calendar date arithmetic29'],
 'source_rows':len(ss),'counted_source_groups':len(counted),'remaining_gaps':['SQLite46 intermediate archives unread','RFC4180 individual redirect effective timestamp unknown','release timezone and first HTML publication unknown','no reader failure established']}
(P/'self-check-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,ensure_ascii=False))
