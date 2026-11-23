"""Normalize pre-observation frame/vocabulary without reading catalogs."""
from pathlib import Path
from datetime import datetime, timezone
import csv, json, re

P=Path(__file__).resolve().parent
def readcsv(p):
    return list(csv.DictReader((P/p).open()))
def writecsv(p,rows):
    with (P/p).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def norm(s):
    return re.sub(r'\s+',' ',s.casefold().replace('-',' ')).strip()

schema=json.loads((P/'evidence/schema-pre/requirements.json').read_text())
ld=json.loads((P/'evidence/ld-pre/requirements.json').read_text())
req=[]
for r in schema:
    req.append({'case_id':r['case_id'],'domain':'JSON Schema','rank':r['screen_rank'],'question_id':r['question_id'],'url':r['url'],'C1':r['c1'],'C2':r['c2'],'language':r['language'],'version':r['product_version'],'dialect':r['draft'],'guard':r['extra_constraints'],'L_terms':r['l_terms'],'definition_file':'evidence/schema-pre/requirements.json'})
for r in ld:
    req.append({'case_id':r['case_id'],'domain':'JSON-LD','rank':r['rank'],'question_id':r['question_id'],'url':r['question_url'],'C1':r['C1'],'C2':r['C2'],'language':r['language'],'version':r['version'],'dialect':r['version'],'guard':r['condition_caveat'],'L_terms':r['L_phrases'],'definition_file':'evidence/ld-pre/requirements.json'})
(P/'requirements.json').write_text(json.dumps(req,ensure_ascii=False,indent=2)+'\n')
frame=[]
for r in readcsv('evidence/schema-pre/frame.csv'):
    frame.append({'frame_id':r['frame_id'],'domain':r['domain'],'screen_rank':r['screen_rank'],'question_id':r['question_id'],'created_utc':r['creation_utc'],'url':r['question_url'],'revision':r['original_revision'],'revision_guid':r['revision_guid'],'body_sha256':r['original_body_sha256'],'original_tags':r['original_tags_json'],'current_tags':r['current_tags_json'],'tag_at_creation':r['original_domain_tag_present'],'case_id':r['case_id'],'status':r['status'],'reason':r['reason'],'source_id':r['source_id'],'details_file':'evidence/schema-pre/revision-audit.json'})
for r in readcsv('evidence/ld-pre/frame.csv'):
    frame.append({'frame_id':'LD-F'+str(r['cohort_rank']).zfill(2),'domain':'JSON-LD','screen_rank':r['cohort_rank'],'question_id':r['question_id'],'created_utc':r['created_utc'],'url':r['question_url'],'revision':r['earliest_revision'],'revision_guid':r['revision_guid'],'body_sha256':r['original_body_sha256'],'original_tags':r['original_tags'],'current_tags':r['current_tags'],'tag_at_creation':r['jsonld_at_creation'],'case_id':r['case_id'],'status':r['selection'],'reason':r['reason'],'source_id':'LDQ-'+str(r['cohort_rank']).zfill(2),'details_file':'evidence/ld-pre/revision-audit.json'})
writecsv('frame.csv',frame)
v=[]
for r in schema:
    for n,term in enumerate(r['l_terms'],1):
        v.append({'mapping_id':r['case_id']+'-L'+str(n),'case_id':r['case_id'],'raw_function_phrase':term,'normalized':norm(term),'target_term':term,'relation':'literal','direction':'original -> same normalized phrase','method':'L,V','definition_uri':r['url'],'section':'original revision1; see requirement location','reason':'case/whitespace/hyphen only','phase':'pre_catalog_ranking'})
for r in readcsv('evidence/schema-pre/vocabulary.csv'):
    v.append({'mapping_id':r['mapping_id'],'case_id':r['case_id'],'raw_function_phrase':r['raw_function_phrase'],'normalized':r['normalized'],'target_term':r['target_term'],'relation':r['relation'],'direction':r['direction'],'method':'V' if r['allowed_V']=='True' else 'withhold','definition_uri':r['definition_uri'],'section':r['section'],'reason':r['reason']+' Preserved: '+r['condition_preserved'],'phase':'pre_catalog_ranking'})
for r in readcsv('evidence/ld-pre/vocabulary.csv'):
    v.append({'mapping_id':r['vocab_id'],'case_id':r['case_id'],'raw_function_phrase':r['original_function_phrase'],'normalized':r['normalized_phrase'],'target_term':r['target_term'],'relation':r['relation'],'direction':r['direction'],'method':{'L and V':'L,V','allow V':'V','withhold':'withhold'}[r['decision']],'definition_uri':r['target_URI'],'section':'see evidence/ld-pre/standard-notes.md','reason':r['reason'],'phase':'pre_catalog_ranking'})
writecsv('vocabulary.csv',v)
sources=[]
for file in ['evidence/schema-pre/sources.jsonl','evidence/schema-pre/standard-sources.jsonl','evidence/ld-pre/sources.jsonl']:
    sources.extend(json.loads(s) for s in (P/file).read_text().splitlines() if s)
(P/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
print(json.dumps({'frame':len(frame),'cases':len(req),'vocabulary_rows':len(v),'V_allow_rows':sum(x['method']=='V' for x in v),'source_rows':len(sources)},ensure_ascii=False))
