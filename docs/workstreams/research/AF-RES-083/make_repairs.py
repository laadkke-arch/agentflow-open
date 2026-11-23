"""Apply and reverse research-only annotations while retaining sealed citations."""
from pathlib import Path
import csv,json,difflib,hashlib,subprocess,datetime,shutil
P=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda x:(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
records=[json.loads(l)for l in(P/'records.jsonl').read_text().splitlines()]
proposals=list(csv.DictReader((P/'proposals.csv').open()))
plan=json.loads((P/'streams/gis/postseal/research-repair-plan.json').read_text())
fp=json.loads((P/'streams/gis/postseal/record-fingerprints.json').read_text())
out=P/'patches';out.mkdir(exist_ok=True)
before=P/'evidence/repairs/before';after=P/'evidence/repairs/after'
before.mkdir(parents=True,exist_ok=True);after.mkdir(parents=True,exist_ok=True)
work=P/'evidence/repairs/.workbench';work.mkdir(parents=True,exist_ok=True)
locations=[];receipts=[]
for r in records:
 if r.get('stratum')!='core'or r.get('status')!='SELECTED':continue
 rid=r['record_id']; pid='RESEARCH-'+rid
 initial={'record_id':rid,'original_record_from_seal':r,'sealed_assessments':[q for q in proposals if q['record_id']==rid],'seal_commit':'35d7e18024cced8cc81f9397b65e90e0e74bb907'}
 old=dump(initial)
 oldscope=('GeoPandas0.14.4의 지원 WKB 파일에 대한 원 왕복 지시 유지. GN04–07은 다른 caller/입력이다.' if rid=='G04-1'else '0.14.4의 지원 write schema:0.1.0/0.4.0/1.0.0-beta.1/1.0.0. reader는WKB범위. 당시 any-version문구는미래encoding보증으로해석하지않는다.')
 latestscope='1.0.0의 별도 native GeoArrow 지원과1.1 schema선택은 고정 구현·공급자 시험의 정적 근거로 확인했다. 1.2.0 안내의 현재 문구도 읽었다. 구0.14.4의 WKB-only제약을 새 판 전체에 소급하지 않는다. 실제consumer build/실행은미확인.'
 views=[]
 for tag,commit,key in [('v0.14.4',r['old_commit'],'geopandas'),('v1.0.0',r['first_followup_commit'],'first'),('v1.2.0',r['latest_commit'],'latest')]:
  loc=fp[key][rid];lo,hi=loc['lines'].split('-')
  views.append({'consumer_tag':tag,'consumer_commit':commit,'source_url':f'https://github.com/geopandas/geopandas/blob/{commit}/{r["path"]}#L{lo}-L{hi}','source_span_sha256':loc['sha256'],'reading_scope':oldscope if key=='geopandas'else latestscope,'historical_original_is_preserved':True})
 updated={**initial,'research_revision':{'id':pid,'action':plan[rid]['action'],'is_publisher_merged_patch':False,'correction_necessity':'정정 필요 확정 없음; 판 한정 설명 또는 유지 주석','reason':plan[rid]['append_annotation'],'publisher_change_id':'PUBLISHER-GEO-3391'if rid=='G04-1'else'PUBLISHER-GEO-3348','views':views}}
 new=dump(updated);(before/(rid+'.json')).write_bytes(old);(after/(rid+'.json')).write_bytes(new)
 rel='records/'+rid+'.json'
 forward=''.join(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile='a/'+rel,tofile='b/'+rel))
 reverse=''.join(difflib.unified_diff(new.decode().splitlines(True),old.decode().splitlines(True),fromfile='a/'+rel,tofile='b/'+rel))
 fwd=out/(pid+'.forward.diff');rev=out/(pid+'.reverse.diff');fwd.write_text(forward);rev.write_text(reverse)
 target=work/rid; (target/'records').mkdir(parents=True,exist_ok=True);tf=target/rel;tf.write_bytes(old)
 steps=[]
 for direction,diff,expected in [('forward',fwd,new),('reverse',rev,old)]:
  argv=['patch','--batch','--forward','-p1','--input',str(diff)]
  start=datetime.datetime.now(datetime.timezone.utc).isoformat();run=subprocess.run(argv,cwd=target,capture_output=True,text=True)
  actual=tf.read_bytes()
  steps.append({'direction':direction,'argv':argv,'cwd':str(target),'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'actual_sha256':sha(actual),'expected_sha256':sha(expected),'byte_equal':actual==expected})
  if run.returncode or actual!=expected:raise SystemExit(json.dumps(steps,ensure_ascii=False))
 preserved=(json.loads(new)['original_record_from_seal']==r and json.loads(new)['sealed_assessments']==initial['sealed_assessments'])
 receipts.append({'research_patch_id':pid,'record_id':rid,'before_sha256':sha(old),'after_sha256':sha(new),'original_and_old_assessment_preserved':preserved,'steps':steps,'reversed_to_identical_bytes':tf.read_bytes()==old,'tested_unit':'research JSON record, not consumer documentation bytes or executable behavior','bidirectional_tag_views':views})
 locations.append({'research_patch_id':pid,'record_id':rid,'actual_original_url':r['original_source_url'],'actual_release_views':[{k:v[k]for k in ['consumer_tag','consumer_commit','source_url','source_span_sha256']}for v in views],'forward_diff':fwd.name,'reverse_diff':rev.name,'publisher_patch_id':updated['research_revision']['publisher_change_id'],'publisher_diff_is_separate':True})
(out/'locations.json').write_text(json.dumps(locations,ensure_ascii=False,indent=2)+'\n')
result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip(),'research_records':len(receipts),'forward_pass':sum(r['steps'][0]['byte_equal']for r in receipts),'reverse_pass':sum(r['reversed_to_identical_bytes']for r in receipts),'vacancy_patches':0,'publisher_repositories_modified':False,'functional_execution':False,'records':receipts}
(P/'evidence/rollback-receipt.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k!='records'},ensure_ascii=False,indent=2))
