"""Reproducible public corpus projection; phase2 never prints OP follow-up.

Run only after remote verification of the initial-selection commit. Cached raw
responses are ignored; public locators, hashes and adjudications are committed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import unicodedata
from research_io import ROOT, se, utc

FILTER='RXBclA_iTvr1Vkp7e4w7BNj)RNrc4avJuy-XQ*WKgptGK(hfFWaiTNFAhTF)br7Q*arP'
KNOWN=['already tried','already knew','already know','had already tried','have already tried','i tried that','i knew that']
NEW=["didn't know",'did not know',"wasn't aware",'was not aware','never knew','was unaware']

def normalize(text):
    return unicodedata.normalize('NFKC',text).lower().replace('\u2019',"'").replace('\u2018',"'")

def hits(text):
    value=normalize(text)
    found=[]
    for family,phrases in [('known',KNOWN),('new',NEW)]:
        for phrase in phrases:
            m=re.search(r'(?<!\w)'+re.escape(phrase)+r'(?!\w)',value)
            if m: found.append({'family':family,'phrase':phrase,'offset':m.start()})
    return sorted(found,key=lambda x:x['offset'])

def pages(path,params,reader,key):
    result=[]
    page=1
    while True:
        cache=ROOT/'.cache'/reader/f'{key}-p{page}.json'
        if cache.exists(): obj=json.loads(cache.read_text())
        else: obj,_=se(path,{**params,'page':page,'pagesize':100,'filter':FILTER},reader,f'{key}-p{page}')
        if 'error_id' in obj or 'backoff' in obj:raise RuntimeError(obj)
        result.extend(obj['items'])
        if not obj.get('has_more'):break
        page+=1
        if page>25:raise RuntimeError('Unexpected paging >25; mark incomplete')
    return result

def collect(site,questions,selected_ids,reader,phase='frame'):
    questions={str(q['question_id']):q for q in questions}
    ids=list(questions)
    allanswers=[];comments=[]
    for chunk in range(0,len(ids),100):
        allanswers+=pages('questions/'+';'.join(ids[chunk:chunk+100])+'/answers',
                         {'site':site,'fromdate':1704067200,'todate':1735689599,'sort':'creation','order':'asc'},reader,f'{phase}-answers-{chunk//100}')
    posts=ids+[str(a['answer_id']) for a in allanswers]
    for chunk in range(0,len(posts),100):
        comments+=pages('posts/'+';'.join(posts[chunk:chunk+100])+'/comments',
                        {'site':site,'fromdate':1704067200,'todate':1735689599,'sort':'creation','order':'asc'},reader,f'{phase}-comments-{chunk//100}')
    amap={str(a['answer_id']):a for a in allanswers}
    events=[]
    for a in allanswers:
        events.append({**a,'kind':'answer','event_id':a['answer_id'],'question_id':a['question_id']})
    for c in comments:
        qid=c['post_id'] if str(c['post_id']) in questions else amap.get(str(c['post_id']),{}).get('question_id')
        if qid is None:raise RuntimeError('Cannot resolve comment parent')
        events.append({**c,'kind':'question_comment' if str(c['post_id']) in questions else 'answer_comment','event_id':c['comment_id'],'question_id':qid})
    events.sort(key=lambda x:(x['creation_date'],x['event_id']))
    reader_cache=ROOT/'.cache'/reader;reader_cache.mkdir(parents=True,exist_ok=True)
    (reader_cache/f'{phase}-events-all-unread.json').write_text(json.dumps(events,ensure_ascii=False,indent=2))
    nonop=[];aux=[];masked_count=0
    for e in events:
        q=questions[str(e['question_id'])]
        qowner=q.get('owner',{}).get('user_id')
        eowner=e.get('owner',{}).get('user_id')
        own=(qowner is not None and eowner==qowner)
        possible_own=own or (qowner is None and (eowner is None or e.get('owner',{}).get('display_name')==q.get('owner',{}).get('display_name')))
        if e['question_id'] in selected_ids:
            if possible_own:masked_count+=1;continue
            if e['kind'] in ['answer','question_comment'] and q['creation_date']<=e['creation_date']<=q['creation_date']+30*86400:
                nonop.append({**e,'question_owner_user_id':qowner,'speaker_user_id':eowner,'different_public_account':qowner is not None and eowner is not None and qowner!=eowner,'identity_limit':'미확인: original owner ID absent' if qowner is None else ''})
        else:
            match=hits(e.get('body',''))
            if match:
                aux.append({**e,'lexicon_hits':match,'question_owner_user_id':qowner,'speaker_user_id':eowner,'author_matches':own})
    (reader_cache/f'{phase}-nonop-proposals-current-unread.json').write_text(json.dumps(nonop,ensure_ascii=False,indent=2))
    (reader_cache/f'{phase}-aux-matches.json').write_text(json.dumps(aux,ensure_ascii=False,indent=2))
    note={'site':site,'phase':phase,'created_utc':utc(),'question_count':len(questions),'answer_count':len(allanswers),'comment_count':len(comments),'events':len(events),'chronological_op_events_not_exposed':masked_count,'nonop_proposal_event_count':len(nonop),'aux_lexicon_match_count':len(aux),'aux_author_match_count':sum(a['author_matches'] for a in aux),'selected_questions_excluded_from_aux':sorted(selected_ids),'body_sha256':{str(e['event_id']):hashlib.sha256(e.get('body','').encode()).hexdigest() for e in events},'limits':['Raw current answer bodies not eligible as historical first proposal until revision read','Only currently surviving public records','No body printed by acquisition script']}
    evidence=ROOT/'evidence'/reader;evidence.mkdir(parents=True,exist_ok=True)
    (evidence/f'{phase}-corpus-receipt.json').write_text(json.dumps(note,ensure_ascii=False,indent=2))
    return note

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('site',choices=['blender','gis']);parser.add_argument('--seal-sha',required=True)
    args=parser.parse_args()
    prefix='blender' if args.site=='blender' else 'qgis'
    initial=json.loads((ROOT/'evidence'/f'{prefix}-initial'/'initial-part.json').read_text())
    cases=initial if isinstance(initial,list) else initial.get('cases',initial.get('selected',[]))
    selected={int(c['question_id']) for c in cases}
    frame=json.loads((ROOT/'.cache'/f'{prefix}-initial'/'frame-h1-masked.json').read_text())
    note=collect(args.site,frame,selected,f'{prefix}-episodes')
    print(json.dumps({k:v for k,v in note.items() if k!='body_sha256'},ensure_ascii=False))
