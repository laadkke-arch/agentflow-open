#!/usr/bin/env python3
"""Compute public timestamp intervals; these are not measured reading/work times."""
import csv,json
from pathlib import Path
from datetime import datetime,timedelta
P=Path(__file__).resolve().parent
def dt(v):return datetime.fromisoformat(v.replace('Z','+00:00')) if v else None
def updated(e):return e.get('updated_at') or e.get('updated_utc') or e.get('last_edited_utc') or e['utc']
def h(v):return round(v.total_seconds()/3600,6)
out=[]
for r in map(json.loads,(P/'chains.jsonl').read_text().splitlines()):
 for q in r['questions']:
  if not q['is_information_request_to_original_author']:continue
  aa=[a for a in r['answers'] if a['question_id']==q['question_id'] and a['is_original_author']]
  aa.sort(key=lambda a:a['utc'])
  q0=dt(q['utc']);q1=dt(updated(q));qend=q0+timedelta(days=30)
  a=next((a for a in aa if q0<=dt(a['utc'])<=qend),None)
  row={'case_id':r['case_id'],'sample':r['sample'],'question_id':q['question_id'],'episode_id':q['episode_id'],
       'root30_question':q['root30'],'question_url':q['url'],'question_created_utc':q['utc'],'question_latest_utc':updated(q),
       'answer_url':a['url'] if a else '', 'answer_created_utc':a['utc'] if a else '',
       'answer_latest_utc':updated(a) if a else '',
       'answer_class':a['answer_class'] if a else 'no_author_reply_in_observed_question30',
       'strict_direct_answer':a['strict_same_variable_existing_answer'] if a else False,
       'reply_wait_creation_hours':h(dt(a['utc'])-q0) if a else '',
       'reply_latest_from_question_creation_hours':h(dt(updated(a))-q0) if a else '',
       'possible_min_hours_given_known_edits':max(0,h(dt(a['utc'])-q1)) if a else '',
       'root30_no_reply_censor_hours':max(0,h(dt(r['windows']['root30_end'])-q0)) if not a and q['root30'] else '',
       'question30_no_reply_censor_hours':720 if not a else '',
       'wording_after_answer_edit':bool(a and q1>dt(a['utc'])),
       'episode_elapsed_hours':a.get('episode_elapsed_hours') if a else '',
       'limit':'현재 댓글 생성/수정 시각의 관측 간격; 원판 미복원으로 해당 문자열 공개시각은 확정하지 않음. 클릭/읽기/대신할 노동 미확인.'}
  if r['case_id']=='X02':row['limit']+=' traceback 문구는 답 이후 편집 가능; error 요청과 별도 미확인.'
  out.append(row)
with (P/'wait-audit.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]),lineterminator='\n');w.writeheader();w.writerows(out)
print(json.dumps({'question_utterance_rows':len(out),'primary_rows':sum(r['root30_question'] for r in out),'wording_edited_after_answer':[r['question_id'] for r in out if r['wording_after_answer_edit']]}))
