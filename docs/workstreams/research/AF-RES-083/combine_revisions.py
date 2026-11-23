"""Join post-seal observations without altering the frozen sampling files."""
from pathlib import Path
import csv,json
P=Path(__file__).resolve().parent
records={r['record_id']:r for r in map(json.loads,(P/'records.jsonl').read_text().splitlines())}
props={(r['record_id'],r['policy']):r for r in csv.DictReader((P/'proposals.csv').open())}
out=[]
for stream in ['gis','oss']:
 for r in csv.DictReader((P/f'streams/{stream}/revisions.csv').open()):
  rid=r['record_id'];orig=records[rid]
  out.append({'record_id':rid,'stratum':orig['stratum'],'original_status':orig['status'],
   'old_release':orig.get('old_tag',orig.get('old_release','')),'original_source_url':orig.get('original_source_url',''),
   'first_followup':r.get('first_followup',''),'latest_followup':r.get('latest_followup',''),
   'first_location':r.get('first_location',''),'latest_location':r.get('latest_location',''),
   'publisher_diff_ids':r.get('publisher_diff_id',r.get('publisher_diff_ids','')),
   'publisher_diff_url':r.get('publisher_diff_url',''),
   'observed_revision':r.get('actual_change',r.get('observed_revision','')),
   'publisher_reason':r.get('publisher_reason','미확인 또는 stream publisher-events 참조'),
   'correction_necessity':r.get('correction_necessity','정오 분모 제외; 보조 원기록의 source-level 판단만 기록'),
   'A_sealed_repair':props[(rid,'A')]['proposed_repair'],'B_sealed_repair':props[(rid,'B')]['proposed_repair'],
   'A_evaluation':r.get('score_A',r.get('A_evaluation','')),'B_evaluation':r.get('score_B',r.get('B_evaluation','')),
   'independent_criterion':r.get('independent_criterion',''),'correctness_denominator_eligible':False,
   'denominator_note':r.get('score_denominator','0; 원안내 공석 또는 보조층, 핵심 정오 비교에 합산하지 않음'),
   'mismatch_or_unknown':r.get('mismatch',r.get('unknowns','')),'next_check':r.get('next_check','REPRODUCE.md 및 stream POSTSEAL.md 참조'),
   'source_ids':r.get('source_ids',''),'observation_file':f'streams/{stream}/revisions.csv',
   'preseal_commit':'35d7e18024cced8cc81f9397b65e90e0e74bb907'})
fields=list(out[0])
with(P/'revisions.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(out)
print(json.dumps({'revision_rows':len(out),'core_rows':sum(r['stratum']=='core'for r in out),'correctness_denominator':0}))
