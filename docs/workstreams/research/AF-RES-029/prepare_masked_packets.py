"""After the route seal, make route/rank-free reading packets and a separate key."""
import json, hashlib, re
from pathlib import Path
from urllib.parse import urldefrag
from datetime import datetime, timezone

P=Path(__file__).resolve().parent
def digest(x):return hashlib.sha256(x.encode()).hexdigest()
def doc(u):return urldefrag(u or '')[0]
def main():
 if not (P/'evidence/route-seal.json').exists():raise RuntimeError('Route seal is required first')
 root=P/'judging';root.mkdir(exist_ok=True);(root/'packets').mkdir(exist_ok=True);(root/'evidence').mkdir(exist_ok=True)
 if (root/'key.json').exists():raise RuntimeError('Masked packets already generated; do not replace')
 key={'created_utc':datetime.now(timezone.utc).isoformat(),'packets':{},'evidence':{}}
 fields=['id','ledger','scope','title','caller','input','output','limits','whole_must','partial_must','independent_partial_purpose','independently_useful_next_action','remaining_adapter','preferences','original_named_families','original_named_components','template_named_components','named_component_roles','same_name_wrong_actor_output_failure','initial_url','fixed_version','initial_text_file']
 for q in map(json.loads,(P/'questions.jsonl').read_text().splitlines()):
  qid=q['id']
  for route in ['C','A','B']:
   rd=P/'common'/qid if route=='C' else P/'routes'/route/qid
   ret=json.loads((rd/('baseline-return.json' if route=='C' else 'return.json')).read_text())
   packet_id='P'+digest('AF-RES-029-reader-v1|'+qid+'|'+route)[:12]
   receipts=list((P/'common'/qid).glob('open-*.json'))
   if route!='C':receipts+=list(rd.rglob('*.json'))
   evidence=[]
   for rf in sorted(set(receipts)):
    r=json.loads(rf.read_text())
    if not isinstance(r,dict) or 'request' not in r or 'response' not in r:continue
    req=r['request']
    if 'system2_search_query' in req or 'system1_search_query' in req:continue
    texts=[x.get('text','') for x in r['response'].get('content',[]) if x.get('type')=='text']
    text='\n'.join(texts)
    match=re.search(r'\((https?://[^\n]+)\)\n【',text)
    url=match.group(1) if match else (req.get('open',[{}])[0].get('ref_id','') if req.get('open') else '')
    if not str(url).startswith('http'):url=''
    eid='E'+digest(url+'\n'+text)[:16]
    dest=root/'evidence'/f'{eid}.json'
    if not dest.exists():dest.write_text(json.dumps({'evidence_id':eid,'original_url':url,'delivered_text':text,'scope':'Only the original text delivered in one stored response. Reported total_lines does not mean all lines were delivered.'},ensure_ascii=False,indent=2)+'\n')
    key['evidence'].setdefault(eid,[]).append(str(rf.relative_to(P)))
    evidence.append({'evidence_id':eid,'original_url':url,'file':str(dest.relative_to(P))})
   candidates=[];candidate_key={}
   for c in ret['candidates']:
    token='K'+digest(packet_id+'|'+str(c['rank']))[:10]
    citations=[{'url':z['url'],'section':z['section'],'evidence_ids':[e['evidence_id'] for e in evidence if doc(e['original_url'])==doc(z['url'])]} for z in c['citations']]
    candidates.append({'candidate_token':token,'name':c.get('name',c.get('target_name','')),'proposed_use':c.get('proposed_use',''),'citations':citations})
    candidate_key[token]={'original_rank':c['rank'],'source_ids':[z.get('source_id') for z in c['citations']],'first_document_url':doc(c['citations'][0]['url'])}
   candidates.sort(key=lambda x:digest(x['candidate_token']))
   packet={'packet_id':packet_id,'question':{k:q[k] for k in fields if k in q},'candidates':candidates,'opened_evidence':sorted({e['evidence_id']:e for e in evidence}.values(),key=lambda x:x['evidence_id']),'instructions':'Read ADJUDICATION.md. No route/rank/self-verdict information is included. Do not read key.json or route/search directories. Judge only delivered originals and exact cited sections. Record unknowns; do not invent missing functionality or adapters.'}
   (root/'packets'/f'{packet_id}.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
   key['packets'][packet_id]={'question_id':qid,'route':route,'return_path':str((rd/('baseline-return.json' if route=='C' else 'return.json')).relative_to(P)),'candidates':candidate_key,'first_document_url':doc(ret['candidates'][0]['citations'][0]['url']) if ret['candidates'] else None}
 (root/'key.json').write_text(json.dumps(key,ensure_ascii=False,indent=2)+'\n')
 assignments={}
 for label,ids in [('reader_1',['Q01','Q04','Q07','Q10']),('reader_2',['Q02','Q05','Q08','Q11']),('reader_3',['Q03','Q06','Q09','Q12'])]:
  files=[f'judging/packets/{pid}.json' for pid,v in key['packets'].items() if v['question_id'] in ids];files.sort(key=digest)
  assignments[label]={'question_ids':ids,'packet_files':files,'allowed_reference':'ADJUDICATION.md and the evidence files specifically named by these packets','forbidden':'judging/key.json; routes; route-inputs; common search/start files; other judgments; later proposal drafts; supplementary research'}
  (root/f'{label}-assignment.json').write_text(json.dumps(assignments[label],ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'packets':len(key['packets']),'evidence_responses':len(key['evidence']),'readers':len(assignments)}))

if __name__=='__main__':main()
