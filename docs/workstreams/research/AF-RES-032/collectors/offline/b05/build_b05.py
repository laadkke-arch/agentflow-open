from pathlib import Path
import csv, datetime as dt, hashlib, json
P=Path(__file__).resolve().parent
def jl(path):return [json.loads(s) for s in path.read_text().splitlines()]
def writejl(name,rows):(P/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
def csvout(name,rows):
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
plan=json.loads((P/'PLAN.json').read_text());search=json.loads((P/'search-receipt.json').read_text())
fetch={r['key']:r for r in jl(P/'attempts.jsonl') if r.get('kind')=='direct_original_fetch'}
a=next(c for c in json.loads((P.parent/'followup/cases.json').read_text()) if c['reference_id']=='A-D04')
assert len(plan['queries'])==3

screens=[
 {'source':'https://www.ietf.org/blog/finalizing-ietf-tools-transition/','result':'upstream selected event; not an external consumer'},
 {'source':'https://www.ietf.org/media/documents/2022-09-14-llc-board-minutes.pdf','result':'upstream dated completion report; directly opened; not consumer slot'},
 {'source':'https://datatracker.ietf.org/meeting/112/materials/slides-112-ietf-sessa-all-slides-ietf-112-plenary-02.pdf','result':'upstream planning material; search result only, not counted'},
 {'source':'https://www.postgresql.org/message-id/E1ruWhw-001Rrq-GW%40gemulon.postgresql.org','result':'official consumer commit receipt; PostgreSQL family1, already known A-D04; 15branch source not12publication'},
 {'source':'https://www.ietf.org/participate/tools/','result':'upstream current service listing; not external consumer'},
 {'source':'https://datatracker.ietf.org/','result':'upstream current index; not external consumer'},
 {'source':'https://datatracker.ietf.org/release/about','result':'upstream about/release page; not external consumer'},
 {'source':'https://www.loc.gov/preservation/digital/formats/fdd/fdd000323.shtml','result':'screened current mutable format description; no versioned distribution in hit; not opened/countable, prior LC-case overlap not investigated'},
 {'source':'https://loc.gov/preservation/digital/formats/fdd/fdd000323.shtml','result':'same LC manuscript without www; duplicate search hit, not new family'}]
query_attempts=[dict(kind='consumer_search',reference_id='B05',query_number=i+1,query=q,
    observed_start_utc=search['started_utc'],observed_end_utc=search['completed_utc'],
    outcome='combined search receipt; service does not attribute individual returned hits to each batched query',count_minimum=False) for i,q in enumerate(plan['queries'])]
writejl('screening.jsonl',query_attempts+[dict(kind='search_hit_screen',reference_id='B05',**s,count_minimum=False) for s in screens])

sources=[]
r=fetch['ietf-board-minutes-2022-09-14']
sources.append(dict(source_id='B05-U-BOARD20220914',source_type='official_meeting_report_pdf',publisher='IETF Administration LLC; Executive Director report',
 original_url=r['url'],version='LLC Board meeting 2022-09-14',publication_date='2022-09-14',
 publication_date_role='dated meeting/report observation; PDF first upload time unknown',observed_at_utc=r['observed_at_utc'],
 read_location='PDF page6 (zero-index5), section6 Tools/RPC/RSOC/RSE, Moving off tools.ietf.org; web lines108–110',
 findings='Dated official report states tools.ietf.org decommissioning complete and redirections in place. It strengthens the general transition completion-by observation.',
 limits='Not a per-RFC4180 redirect deployment receipt. No old/new URL instance, exact effective UTC, or reader failure. Cannot substitute for a source-edit/publication clock.',
 questions=['Q3','Q5','Q6'],reference_ids=['B05','A-D04'],duplicate_group='ietf-llc-board-report-2022-09-14',
 count_minimum=True,count_category='upstream',body_sha256=r['sha256'],http_status=r['http_status'],final_url=r['final_url'],
 web_reference='turn743160539view1',cache_path='cache/ietf-board-minutes-2022-09-14'))
r=fetch['pg-commit-mail15']
sources.append(dict(source_id='B05-F-PG15MAIL',source_type='official_commit_notification',publisher='PostgreSQL pgsql-committers; Daniel Gustafsson',
 original_url=r['url'],version='REL_15_STABLE / ef124d0952e18f1c7a7e9f99b2d10e2f0737c24a',
 publication_date='2024-04-10 12:05:41',publication_date_role='mail display date; timezone absent; not release publication',
 observed_at_utc=r['observed_at_utc'],read_location='Date, change rationale, Branch REL_15_STABLE, Details commit and modified psql-ref.sgml',
 findings='Search locates the same multi-branch PostgreSQL link-maintenance change; editor explains avoiding redirect overhead. This hit concerns branch15.',
 limits='Not the12branch source SHA or a built15manual. The known12series distribution evidence is reused from A-D04 with overlap disclosed. Same correction family is not a new minimum-count document.',
 questions=['Q4','Q5','Q6'],reference_ids=['B05','A-D04'],duplicate_group='postgres-rfc-link-fix-2024',
 count_minimum=False,count_category='consumer_followup',body_sha256=r['sha256'],http_status=r['http_status'],final_url=r['final_url']))
writejl('sources.jsonl',sources)

case=dict(reference_id='B05',sample='B',event_key='ietf-tools-final-transition-2022',announcement_date='2022-06-17',
 announcement_date_role='future final-transition plan',announcement_url=plan['announcement'],
 general_transition_complete_by={'date':'2022-09-14','precision':'report day, timezone unspecified','source_id':'B05-U-BOARD20220914'},
 actual_specific_uri_effective='미확인',queries_used=3,queries_limit=3,candidate_document_families_used=1,candidate_document_families_limit=5,
 screened_nonversioned_external_manuscripts=1,new_independent_consumer_families=0,
 consumer_search_result='PostgreSQL psql known family found again; no other eligible versioned consumer family within fixed3queries',
 consumer='PostgreSQL psql',purpose='RFC4180 CSV quoting/escaping rules',consumer_reference='A-D04',
 A_B_duplicate=True,duplicate_event_key_crosswalk={'A_key':a['upstream_event_key'],'B_key':plan['event_key'],
    'level':'same tools-transition project/family; per-URL implementation phase/date still unknown',
    'reason':'Same consumer document and RFC4180 purpose reused. Conservatively excluded from any extra independent numerator; no claim of independent rediscovery.'},
 prior_exposure=True,prior_exposure_note=plan['known_candidate']['reason'],increment_A_numerator=0,
 raw_href=a['raw_href'],original_archive=a['original_archive'],original_member=a['original_member'],
 last_old=a['last_old'],first_observed_new=a['first_observed_new'],source_edit=a['source_edit'],
 publication=a['publication'],current=a['current'],merge=None,build=None,reader_report=None,
 verdict='유지',verdict_actor='researcher judging sealed RFC4180 reading purpose; publisher selected route update',
 actual_consumer_href_changed=True,strict_upstream_to_publication_interval_eligible=False,right_censored=False,
 source_ids=['B-U05','B05-U-BOARD20220914','B05-F-PG15MAIL','PG-U02','PG-U03','PG-U03c','PG-F-SOURCE12','PG-F18-PSQL','PG-F19-PSQL','PG-F-NEWS1219'],
 counterexamples=['2022 announcement future tense is not per-URI implementation date.',
   '2026-10-29 article addition cannot be placed in the2022 evidence.',
   'Search found15branch mail: do not treat its timestamp/SHA as12branch publication.',
   'Old tools URL currently serves the requiredRFC body despite consumer href rewrite.'],
 unknowns=[{'reason':'RFC4180 individual redirect effective date unknown','last_verified':'official2022-09-14 completion report plus2024 PG maintenance observation',
     'next_minimum_source':'dated deployment/config receipt naming /html/rfc4180'},
   {'reason':'no additional independent consumer distribution found within capped search','last_verified':'3 exact queries,1 consumer family, current-only LC hit excluded',
     'next_minimum_source':'in a new authorized sampling round, a versioned consumer archive independently naming old/new tools URLs'},
   {'reason':'reader click/failure, build and exact firstHTML upload unknown','last_verified':'archive12.18/12.19 bytes and official12.19release notice',
     'next_minimum_source':'same-purpose reader report identifying PostgreSQL edition and clickedURI'}])
(P/'cases.json').write_text(json.dumps([case],ensure_ascii=False,indent=2)+'\n')
writejl('references.jsonl',[dict(reference_id='B05',sample='B',consumer='PostgreSQL psql',purpose=case['purpose'],
    raw_href=case['raw_href'],A_duplicate='A-D04',prior_exposure=True,event_key=case['event_key'],
    edition_evidence='../../offline/followup/pg-editions.jsonl',selection_gate_commit=plan['parent_seal_commit'],
    queries_used=3,candidate_families_used=1,new_independent_consumer_families=0)])
editionrows=[]
for role in ['last_old','first_observed_new']:
    r=case[role];m=r['member'];editionrows.append(dict(reference_id='B05',A_duplicate='A-D04',role=role,version=r['version'],
      release_day=r['release_day'],archive_url=r['archive_url'],archive_sha256=r['archive_sha256'],member=m['member_path'],
      member_sha256=m['member_sha256'],href=';'.join(m['target_href']),source_id=r['source_id'],
      publication_time_limit='release day only, timezone/first upload unknown',new_B_read=False))
csvout('editions.csv',editionrows)
csvout('intervals.csv',[dict(reference_id='B05',event_key=case['event_key'],A_duplicate='A-D04',
  start='미확인',start_role='per-RFC4180 effective migration',start_source='B-U05;B05-U-BOARD20220914;PG-U03',
  end='2024-05-09',end_role='12.19 release day, no timezone',end_source='PG-F19-PSQL;PG-F-NEWS1219',
  eligible=False,delta='',right_censored=False,reason='General project completion-by does not establish exact per-URL same-event clock; no extra A numerator')])
checks={'reference_id':'B05','checked_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':0,
   'query_count':3,'query_limit':3,'candidate_families':1,'candidate_limit':5,'A_overlap':True,'increment_A_numerator':0,
   'new_independent_consumer_families':0,'new_counted_upstream_sources':1,'new_counted_consumer_followup_sources':0,
   'scope':'collector only; not whole repository gate','source_facts_rechecked':['PGmail is15branch','PDFpage6 dated completionreport','PG12firstnew proven by A actual archives'],
   'input_sha256':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['PLAN.json','search-receipt.json','sources.jsonl','cases.json','editions.csv','intervals.csv']}}
(P/'self-check-receipt.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(checks,ensure_ascii=False))
