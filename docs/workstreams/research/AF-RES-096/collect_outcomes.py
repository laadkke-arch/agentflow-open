"""Open public outcomes ONLY after the remote A/B judgment seal.

Raw public bodies remain in ignored cache. The analyst publishes short excerpts,
attributed findings, original URLs, times, hashes, and the missing observations.
"""
from pathlib import Path
import datetime, hashlib, json, urllib.parse, urllib.request

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'evidence/outcomes'

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def dump(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def fetch(endpoint, label, extra=None):
    params = {'site':'stackoverflow','filter':'withbody','pagesize':100}
    if extra:
        params.update(extra)
    items, pages = [], []
    for page in range(1, 11):
        params['page'] = page
        url = 'https://api.stackexchange.com/2.3/' + endpoint + '?' + urllib.parse.urlencode(params)
        start = now()
        request = urllib.request.Request(url, headers={'User-Agent':'AF-RES-096-public-research'})
        try:
            with urllib.request.urlopen(request,timeout=40) as response:
                raw = response.read(); status=response.status
            obj=json.loads(raw)
            receipt={'label':label,'page':page,'url':url,'started_utc':start,
                     'finished_utc':now(),'http_status':status,'sha256':hashlib.sha256(raw).hexdigest(),
                     'items':len(obj.get('items',[])),'has_more':obj.get('has_more'),
                     'quota_remaining':obj.get('quota_remaining'),'backoff':obj.get('backoff')}
            dump(OUT/'_cache'/f'{label}-{page}.json',obj)
            items.extend(obj.get('items',[]));pages.append(receipt)
            with (OUT/'receipts.jsonl').open('a') as f:f.write(json.dumps(receipt)+'\n')
            if 'error_id' in obj:raise RuntimeError(str(obj))
            if obj.get('backoff'):raise RuntimeError('API backoff; resume only after specified interval')
            if not obj.get('has_more'):break
        except Exception as exc:
            with (OUT/'receipts.jsonl').open('a') as f:
                f.write(json.dumps({'label':label,'page':page,'url':url,'started_utc':start,
                                    'finished_utc':now(),'error':f'{type(exc).__name__}: {exc}'})+'\n')
            raise
    else:
        raise RuntimeError('Pagination exceeds bounded10 pages; preserve missing tail')
    return items,pages

def main():
    seal=json.loads((ROOT/'evidence/seal2-receipt.json').read_text())
    assert len(seal['remote_sha'])==40 and seal.get('confirmed_remote') is True
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'first-open.json').exists():raise ValueError('Outcomes already opened; do not overwrite original first time')
    dump(OUT/'first-open.json',{'first_open_utc':now(),'seal2_remote_sha':seal['remote_sha'],
                               'seal2_confirmed_utc':seal['verified_utc'],
                               'first_access_purpose':'public outcomes after both-route remote seal'})
    cases=json.loads((ROOT/'protocol.json').read_text())['cases']
    qids=';'.join(str(c['question_id']) for c in cases)
    questions,_=fetch('questions/'+qids,'questions-current')
    answers,_=fetch('questions/'+qids+'/answers','answers-current',{'sort':'creation','order':'asc'})
    qcomments,_=fetch('questions/'+qids+'/comments','question-comments',{'sort':'creation','order':'asc'})
    qrevisions,_=fetch('posts/'+qids+'/revisions','question-revisions')
    aids=';'.join(str(a['answer_id']) for a in answers)
    arevisions,acomments=[],[]
    if aids:
        arevisions,_=fetch('posts/'+aids+'/revisions','answer-revisions')
        acomments,_=fetch('answers/'+aids+'/comments','answer-comments',{'sort':'creation','order':'asc'})
    records=[]
    for case in cases:
        qid=case['question_id'];q=next((x for x in questions if x['question_id']==qid),{})
        asker=q.get('owner',{}).get('user_id')
        created=q.get('creation_date');deadline=created+30*86400 if created else None
        ars=[]
        for answer in [a for a in answers if a['question_id']==qid]:
            aid=answer['answer_id']
            revisions=[r for r in arevisions if r.get('post_id')==aid and r.get('body')]
            revisions.sort(key=lambda r:(r.get('creation_date',0),r.get('revision_number',0),r.get('revision_guid','')))
            first=revisions[0] if revisions else None
            body=(first or {}).get('body','')
            cache=OUT/'_cache'/f'answer-{aid}-earliest.html';cache.write_text(body)
            ars.append({'answer_id':aid,'url':f'https://stackoverflow.com/a/{aid}',
                        'creation_epoch':answer.get('creation_date'),'last_edit_epoch':answer.get('last_edit_date'),
                        'current_is_accepted':answer.get('is_accepted'),
                        'owner_id':answer.get('owner',{}).get('user_id'),
                        'within_30_days':answer.get('creation_date',0)<=deadline if deadline else None,
                        'first_revision_guid':(first or {}).get('revision_guid'),
                        'first_revision_number':(first or {}).get('revision_number'),
                        'first_revision_epoch':(first or {}).get('creation_date'),
                        'first_revision_url':f'https://stackoverflow.com/revisions/{first["revision_guid"]}/view-source' if first else None,
                        'earliest_body_sha256':hashlib.sha256(body.encode()).hexdigest(),
                        'earliest_body_cache':str(cache.relative_to(ROOT)),
                        'body_revision_count':len(revisions)})
        answer_ids={a['answer_id'] for a in ars}
        comments=[c for c in qcomments+acomments if c.get('post_id')==qid or c.get('post_id') in answer_ids]
        commentmeta=[]
        for comment in comments:
            cid=comment['comment_id'];body=comment.get('body','');cache=OUT/'_cache'/f'comment-{cid}.html';cache.write_text(body)
            commentmeta.append({'comment_id':cid,'post_id':comment.get('post_id'),
                                'url':f'https://stackoverflow.com/questions/{qid}#comment{cid}_{comment.get("post_id")}',
                                'creation_epoch':comment.get('creation_date'),
                                'within_30_days':comment.get('creation_date',0)<=deadline if deadline else None,
                                'by_asker':asker is not None and comment.get('owner',{}).get('user_id')==asker,
                                'owner_id':comment.get('owner',{}).get('user_id'),
                                'body_cache':str(cache.relative_to(ROOT)),
                                'body_sha256':hashlib.sha256(body.encode()).hexdigest()})
        qr=[r for r in qrevisions if r.get('post_id')==qid and r.get('body')]
        qmeta=[]
        for revision in qr:
            guid=revision['revision_guid'];body=revision['body'];cache=OUT/'_cache'/f'question-{qid}-{guid}.html';cache.write_text(body)
            qmeta.append({'guid':guid,'revision_number':revision.get('revision_number'),
                          'creation_epoch':revision.get('creation_date'),
                          'within_30_days':revision.get('creation_date',0)<=deadline if deadline else None,
                          'by_asker':asker is not None and revision.get('user',{}).get('user_id')==asker,
                          'url':f'https://stackoverflow.com/revisions/{guid}/view-source',
                          'body_cache':str(cache.relative_to(ROOT)),
                          'body_sha256':hashlib.sha256(body.encode()).hexdigest()})
        records.append({'case_id':case['case_id'],'question_id':qid,'asker_id':asker,
                        'question_creation_epoch':created,'deadline_30d_epoch':deadline,
                        'current_accepted_answer_id':q.get('accepted_answer_id'),
                        'answers':ars,'comments':commentmeta,'question_body_revisions':qmeta,
                        'runtime_success':'not inferred; manual attributed evaluation required'})
    dump(OUT/'public-records.json',records)
    print(json.dumps({'cases':len(records),'answers':len(answers),'comments':len(qcomments)+len(acomments),
                      'first_open_record':'evidence/outcomes/first-open.json'}))

if __name__=='__main__':main()
