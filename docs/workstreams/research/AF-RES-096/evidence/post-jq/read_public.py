import pathlib,json,datetime,html,re,hashlib
P=pathlib.Path(__file__).resolve().parents[2]
items=[x for x in json.loads((P/'evidence/outcomes/public-records.json').read_text()) if x['case_id'] in ['J1','J2','J3','J4']]
records=[]
def read(case,kind,meta,path,url):
 p=P/path;b=p.read_bytes();t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 records.append({'case_id':case,'kind':kind,'checked_utc':t,'url':url,'cache_path':path,'sha256':hashlib.sha256(b).hexdigest(),'metadata':meta,'outside_frozen_route_budget':True})
 text=b.decode();text=re.sub(r'<(?:br\s*/?|/p|/pre|/li|/div)>','\n',text);text=html.unescape(re.sub(r'<[^>]+>','',text))
 print('\n###',case,kind,json.dumps(meta,ensure_ascii=False),'\n',text)
for x in items:
 for a in x['answers']: read(x['case_id'],'first_answer',{'answer_id':a['answer_id'],'accepted_now':a['current_is_accepted'],'created':a['creation_epoch'],'last_edit':a['last_edit_epoch'],'first_guid':a['first_revision_guid']},a['earliest_body_cache'],a['first_revision_url'])
 for c in x['comments']: read(x['case_id'],'comment',{'comment_id':c['comment_id'],'post_id':c['post_id'],'by_asker':c['by_asker'],'within_30d':c['within_30_days'],'created':c['creation_epoch']},c['body_cache'],c['url'])
 for v in sorted(x['question_body_revisions'],key=lambda v:v['creation_epoch']): read(x['case_id'],'question_revision',{'revision_number':v['revision_number'],'guid':v['guid'],'by_asker':v['by_asker'],'within_30d':v['within_30_days'],'created':v['creation_epoch']},v['body_cache'],v['url'])
(P/'evidence/post-jq/public-read-log.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))
