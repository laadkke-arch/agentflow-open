"""Integrate already-read primary evidence; does not fetch or execute author code."""
import csv
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
E = ROOT / 'evidence'

def readjson(path):
    return json.loads(path.read_text())

def csvrows(path):
    return list(csv.DictReader(path.open()))

def writecsv(name, rows, fields=None):
    fields = fields or list(dict.fromkeys(k for r in rows for k in r))
    with (ROOT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict,list)) else v for k,v in r.items()})

def true(v):
    return v is True or str(v).lower() == 'true'

frames = []
for sub in ['pandas', 'moment']:
    for r in csvrows(E/sub/'frame.csv'):
        rank=r.get('frame_position',r.get('original_rank'))
        frames.append(dict(frame_id=f'N-{sub[0].upper()}-F{int(rank):02}',layer='natural',repository=r['repository'],original_rank=rank,record_id=r.get('issue_number',r.get('number')),title=r['title'],created_utc=r['created_utc'],original_url=r['original_url'],eligible=r['eligible'],selected=r['selected'],case_id=r.get('case_id',''),body_read=True,observed_exists=True,decision=r.get('selection_reason',r.get('decision')),first_body_status=r.get('original_body_restored',r.get('first_body_status')),detail_file=f'evidence/{sub}/frame.csv'))
for r in csvrows(E/'artifacts/frame.csv'):
    frames.append(dict(frame_id=r['frame_id'],layer='execution-first-candidate',repository=r['project'],original_rank=r['original_rank'],record_id=r['record_id'],title=r['title'],created_utc=r['created_at'],original_url=r['original_url'],eligible=r['eligible'],selected=False,case_id=r['frame_id'],body_read='run/job metadata only' if true(r['observed_exists']) else '미확인',observed_exists=r['observed_exists'],decision=r['reason'],first_body_status='해당 없음',detail_file='evidence/artifacts/frame.csv'))
for c in ['E-P1','E-P2','E-M1','E-M2']:
    frames.append(dict(frame_id=c,layer='execution-first-output-slot',repository='pandas-dev/pandas' if c.startswith('E-P') else 'moment/moment-timezone',original_rank=c[-1],record_id='미확인',title='빈자리',created_utc='미확인',original_url='https://github.com/'+('pandas-dev/pandas' if c.startswith('E-P') else 'moment/moment-timezone')+'/actions',eligible='미확인',selected=False,case_id=c,body_read=False,observed_exists=False,decision='날짜 변환 원출력 조건을 충족한 최초 후보 미확보; 뒤 성공례로 교체하지 않음',first_body_status='해당 없음',detail_file='evidence/artifacts/receipts.json'))
writecsv('frame.csv',frames)

receipts=[]
for r in readjson(E/'pandas/receipts.json'):
    receipts.append(dict(receipt_id=r['receipt_id'],case_id=r['case_id'],layer='natural',report_or_run_id=r['event_lineage_id'],publication_utc=r['report_utc'],execution_utc=r['execution_utc'],executor=r['executor'],input_utc=r['input_utc'],input_local=r['input_local'],timezone_id=r['region'],call=r['call'],input_format=r['input_format'],offset_convention=r['offset_convention'],declared_version=r['declared_versions'],installed_or_lock=r['install_or_lock'],loaded_provider=r['loaded_provider'],loaded_edition=r['loaded_tzdb_edition'],loaded_path_or_hash=r['loaded_provider_evidence'],actual_output=r['output'],output_role=r['output_kind'],evidence_level=r['grade'],same_run_key=r['same_run_key'],input_output_join=r['input_output_join'],source_id=r['source_id'],original_url=r['original_url'],locator=r['locator'],traceable=True,date_output_published=r['date_output_published'],provider_label_confirmed=False,loaded_bytes_confirmed=False,same_run_label_output=False,same_run_full_bytes=False,missing='same process loader edition/bytes and original execution timestamp',next_minimum=r['first_additional_archived_observation'],detail_file='evidence/pandas/receipts.json'))
for r in readjson(E/'moment/receipts.json'):
    receipts.append(dict(receipt_id='R-'+r['case_id'],case_id=r['case_id'],layer=r['stratum'],report_or_run_id=r['event_id'],publication_utc=r['posted_utc'],execution_utc=r['execution_utc'],executor=r['author']+' / '+r['role'],input_utc=r['possible_utc'],input_local=r['input_literal'],timezone_id=r['timezone_id'],call=r['call'],input_format=r['input_scale'],offset_convention='ISO east-positive; Zone.utcOffset uses west-positive minutes (see case)' if r['case_id']=='A-M989' else 'ISO east-positive; object utcOffset east-positive minutes',declared_version=r['declaration'],installed_or_lock=r['installation'],loaded_provider=r['loaded_provider'],loaded_edition=r['loaded_edition'],loaded_path_or_hash=r['member_path']+' / '+r['member_sha256'],actual_output=r['output'],output_role=r['output_role'],evidence_level=r['attribution_grade'],same_run_key=r['same_run_key'],input_output_join=r['input_interpretation'],source_id='M-I'+r['original_url'].split('/issues/')[1].split('#')[0],original_url=r['original_url'],locator=r['locator'],traceable=True,date_output_published=r['exact_output_present'],provider_label_confirmed=r['provider_self_report_confirmed'],loaded_bytes_confirmed=False,same_run_label_output=r['case_id']=='A-M967-M',same_run_full_bytes=False,missing=r['execution_time_basis']+'; actual loaded bytes absent',next_minimum=r['next_observation'],detail_file='evidence/moment/receipts.json'))
for r in readjson(E/'artifacts/receipts.json'):
    receipts.append(dict(receipt_id='R-'+r['case_id'],case_id=r['case_id'],layer=r['layer'],report_or_run_id=r.get('report_or_run_id') or '미확인',publication_utc=r.get('publication_utc','미확인'),execution_utc=r.get('execution_utc','미확인'),executor=r.get('actor','미확인'),input_utc=r.get('input_utc','미확인'),input_local='미확인',timezone_id=r.get('timezone_id','미확인'),call=r.get('call','미확인'),input_format='unit=s' if r['case_id']=='A-PW2' else '미확인',offset_convention='미확인',declared_version=r.get('declared_version','미확인'),installed_or_lock=r.get('installed_version','미확인'),loaded_provider=r.get('loaded_provider','미확인'),loaded_edition=r.get('loaded_version','미확인'),loaded_path_or_hash=r.get('loaded_path_or_hash','미확인'),actual_output=r.get('output','미확인'),output_role=r.get('evidence_level','no date output'),evidence_level=r.get('evidence_level','미확인'),same_run_key=r.get('same_run_key','미확인'),input_output_join='same file/cell counters; no original process UUID' if r['case_id'].startswith('A-') else 'run ID metadata exists; input/loader/output unavailable',source_id='E-NB-JV' if r['case_id']=='A-PW2' else ('E-NB-PW' if r['case_id']=='A-PW1' else 'E-CI-P'+r['case_id'].split('C')[-1].zfill(2) if '-C' in r['case_id'] else 'E-AUDIT'),original_url=r['original_url'],locator=r.get('report_or_run_id') or 'evidence/artifacts/notes.md',traceable=r['traceable_record'],date_output_published=r['historical_date_output_confirmed'],provider_label_confirmed=False,loaded_bytes_confirmed=False,same_run_label_output=False,same_run_full_bytes=False,missing=r.get('empty_reason',r.get('output_expiry_reason','same-kernel loaded provider missing')),next_minimum=r['next_minimum'],detail_file='evidence/artifacts/receipts.json'))
for c,doi,author,when,inp,call,out,detail in [
 ('X-D1','10.7910/DVN/XAMFQK','Krzysztof Rybinski et al.','V1 2022-03-16; V2 2022-03-18','observation month 199210; source execution inputs 미확인','미확인; published spreadsheets only','U_Data.xlsx C2=96.71812781026418','dataverse-version-inspection.json'),
 ('X-Z1','10.5281/zenodo.6532252','Mustapha Regragui et al.','2022-05-09','scenario1, FIFO,4workers,seed1,frame0','simulator output; notebook pd.read_csv path code only','duration9378.21 microseconds; 200 raw frame rows','zenodo-package-inspection.json'),
 ('A-XG9','10.7910/DVN/G9QZOU','Iasmin Goes; inherited James R. Vreeland log','2023-03-19 package; 2008-04-18 log local time','Vreeland_2008_IO.dta old local path; 2023 inputs separate','ologit torture party level g population tradegdp war communist if reg==1, robust','N694; party=.5780659; log pseudolikelihood=-893.5787','READING.md')]:
    receipts.append(dict(receipt_id='R-'+c,case_id=c,layer='cross-field' if c.startswith('X-') else 'auxiliary-cross-field',report_or_run_id=doi,publication_utc=when,execution_utc='미확인 (A-XG9 log gives local time only)',executor=author,input_utc='해당 없음',input_local=inp,timezone_id='해당 없음',call=call,input_format='month/scenario/datafile',offset_convention='해당 없음',declared_version=when,installed_or_lock='deposit checksum; no same-run installation receipt',loaded_provider='미확인',loaded_edition='미확인',loaded_path_or_hash='deposited member hashes verified; not original process load',actual_output=out,output_role='author-published numeric output',evidence_level='published bytes + output; same-run input/load linkage incomplete',same_run_key='deposit DOI + file/member; not process UUID',input_output_join='see reading; do not join separate-era files',source_id={'X-D1':'S-XD1','X-Z1':'S-XZ1','A-XG9':'S-XG9'}[c],original_url='https://doi.org/'+doi,locator='evidence/crossfield/'+detail,traceable=True,date_output_published=False,provider_label_confirmed=False,loaded_bytes_confirmed=False,same_run_label_output=False,same_run_full_bytes=False,missing='original execution input digest, timestamp and output linkage',next_minimum='author-published original run receipt matching fixed input digest and output',detail_file='evidence/crossfield/'+detail))
writecsv('receipts.csv',receipts)

# Same work/revisions and mirrors count once. Retain each read row for traceability.
sources=[]; seen=set()
for origin in [E/'pandas/sources.jsonl',E/'moment/sources.jsonl',E/'artifacts/sources.jsonl',E/'root-sources.jsonl']:
    for line in origin.read_text().splitlines():
        r=json.loads(line);r['ledger_origin']=str(origin.relative_to(ROOT));r.setdefault('read_by','web-pro/root' if 'root-' in origin.name else 'web-pro/'+origin.parent.name)
        url=r['original_url']+' '+r['fixed_url']; category=r['category']; original=r['lineage_id']
        if category not in ['issue_report','issue_scope_exclusion','reported_issue','screened_ineligible_issue','ci_metadata_only','executed_notebook','cross_field','cross_field_auxiliary']:
            for fragment,key in [('python/cpython','official-cpython-zoneinfo'),('python/peps','official-pep-495'),('dateutil/dateutil','official-dateutil'),('stub42/pytz','official-pytz'),('pypi.org/pypi/pytz','official-pytz'),('pandas-dev/pandas','official-pandas'),('moment/momentjs.com','official-moment-documentation'),('moment/moment-timezone','official-moment-timezone'),('moment/moment/','official-moment-core'),('eggert/tz','official-new-region-tz-rules')]:
                if fragment in url:
                    r['lineage_id']=key;break
        r['original_lineage_id']=original
        if category in ['issue_scope_exclusion','screened_ineligible_issue']:
            r['count_minimum']=False;r['count_note']='screened original body directly read; conservatively excluded from evidence minimum because it is outside output eligibility'
        if r.get('count_minimum'):
            if r['lineage_id'] in seen: r['count_minimum']=False;r['count_note']='same-work revision/mirror/member already counted in canonical ledger'
            else: seen.add(r['lineage_id'])
        sources.append(r)
(ROOT/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in sources))

# Evidence-specific source IDs in Moment use the ledger's actual stable identifier.
issue_ids={r['original_url'].split('#')[0]:r['source_id'] for r in sources if r['category'] in ['reported_issue','issue_report','screened_ineligible_issue','issue_scope_exclusion']}
for r in receipts:
    if r['original_url'].split('#')[0] in issue_ids: r['source_id']=issue_ids[r['original_url'].split('#')[0]]
writecsv('receipts.csv',receipts)

counted=[r for r in sources if r.get('count_minimum')]
counts={'frame_rows':len(frames),'natural_bodies':sum(r['layer']=='natural' for r in frames),'natural_selected':sum(r['layer']=='natural' and true(r['selected']) for r in frames),'execution_candidate_planned_rows':30,'execution_candidates_observed':15,'execution_output_slots':4,'execution_output_slots_filled':0,'receipt_rows':len(receipts),'source_rows':len(sources),'counted_independent_lineages':len({r['lineage_id'] for r in counted}),'counted_categories':dict(Counter(r['category'] for r in counted)),'natural_date_outputs':sum(r['layer']=='natural' and r['date_output_published'] for r in receipts),'natural_actual_edition_labels':sum(r['layer']=='natural' and r['provider_label_confirmed'] for r in receipts),'natural_same_run_label_output':sum(r['layer']=='natural' and r['same_run_label_output'] for r in receipts),'all_actual_loaded_byte_receipts':sum(r['loaded_bytes_confirmed'] for r in receipts),'cohort_counts_exclude_auxiliaries':True}
(E/'integrated-counts.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(counts,ensure_ascii=False))
