"""Evidence-set arithmetic, always within one alternative and one trial.

Reachable union means each ID has at least one self-contained witness; it never
means a user read the union of all trials. max_in_one_trial is separate.
"""
from pathlib import Path
import json,csv,itertools,hashlib
from urllib.parse import urldefrag,urljoin
from build_study import ROOT,E,load,dump,lines,readcsv,writecsv,sha
def jl(p):return [json.loads(x) for x in (ROOT/p).read_text().splitlines()]

CASES={c['case_id']:c for c in load('evidence/cases.json')}
ATOMS={cid:{a['id'] for a in c['required_atoms']} for cid,c in CASES.items()}
BASE=jl('evidence/candidate-evidence.jsonl'); BYID={r['candidate_id']:r for r in BASE}
BYURL={(r['case_id'],r['url']):r for r in BASE if r['url']}
SUB=load('evidence/pandoc/control-second-hop-coding.json')['subcondition_decomposition']
def python_context_aligned(url):
    return url.startswith('https://docs.python.org/3.11/') or url.startswith('https://peps.python.org/pep-0654/') or url.startswith('https://discuss.python.org/t/accepting-pep-654-exception-groups-and-except/10813')
HOPS={}; EXPECT={}
for r in load('evidence/vega/windows-V.json'):EXPECT[(r['case_id'],r['requested_url'])]=r['html_sha256']
for r in load('evidence/vega/second-hop-arrivals.json'):
    for occ in r['source_occurrences']:
        if r.get('html_sha256'):EXPECT[(occ['case_id'],r['url'])]=r['html_sha256']
for r in load('evidence/control/candidate-read-receipts.json'):
    if r.get('sha256'):EXPECT[(r['candidate_id'][:2],r['requested_url'])]=r['sha256']
for r in load('evidence/crossfield/control-C2.json')['slots']:EXPECT[('C2',r['url'])]=r['sha256']
for name in ['evidence/vega/second-hop-coding.json','evidence/pandoc/control-second-hop-coding.json','evidence/crossfield/control-second-hop-coding.json']:
    for x in load(name)['destinations']:
        for pc in x['per_case']:
            cid=pc['case_id'];r={'case_id':cid,'url':x['url'],'locator':x.get('locator',x.get('scope_locator','미확인')),'supports_by_alternative':{},'full_document_supports_by_alternative':{},'subcondition_facts_by_alternative':{},'full_document_subcondition_facts_by_alternative':{},'source_record':name}
            if cid.startswith('V'):
                r['supports_by_alternative']={'vega-lite':pc['supports']}
                r['full_document_supports_by_alternative']={'vega-lite':pc.get('full_document_supports',[])}
            elif cid in ['C3','C4']:
                alt=cid+'-cpython311';r.update(supports_by_alternative={alt:pc['supports']},full_document_supports_by_alternative={alt:pc['full_document_supports']},subcondition_facts_by_alternative={alt:pc['subcondition_facts']},full_document_subcondition_facts_by_alternative={alt:pc['full_document_subcondition_facts']})
                r.update(version_alignment=pc['version_alignment'],conflicts=pc.get('conflicts',[]),context_aligned=python_context_aligned(x['url']))
            else:
                for a in pc['alternative_atom_support']:
                    r['supports_by_alternative'][a['alternative_id']]=[v['atom_id'] for v in a['atom_verdicts'] if v.get('counts_as_proven')]
                # W is not assumed on an unreviewed destination. The known strict proof remains valid.
                r['full_document_supports_by_alternative']=dict(r['supports_by_alternative'])
            HOPS[(cid,x['url'])]=r
            if (cid,x['url']) not in EXPECT and (x.get('html_sha256') or x.get('document_sha256')):EXPECT[(cid,x['url'])]=x.get('html_sha256',x.get('document_sha256'))

def evidence(cid,url):return BYURL.get((cid,url)) or HOPS.get((cid,url))
def merged(cid,records,scope='strict'):
    afields=['supports_by_alternative'] + (['full_document_supports_by_alternative'] if scope!='strict' else [])
    sfields=['subcondition_facts_by_alternative'] + (['full_document_subcondition_facts_by_alternative'] if scope!='strict' else [])
    atoms={};subs={}
    for r in records:
        if not r:continue
        if cid in ['C3','C4'] and not python_context_aligned(r.get('url','')):continue
        for afield in afields:
            for alt,vals in r.get(afield,{}).items():atoms.setdefault(alt,set()).update(vals)
        for sfield in sfields:
            for alt,amap in r.get(sfield,{}).items():
                for atom,vals in amap.items():subs.setdefault(alt,{}).setdefault(atom,set()).update(vals)
    for alt,amap in subs.items():
        for atom,vals in amap.items():
            if set(SUB.get(atom,[])) and set(SUB[atom])<=vals:atoms.setdefault(alt,set()).add(atom)
    complete=sorted(alt for alt,vals in atoms.items() if ATOMS[cid]<=vals)
    return {'complete_ids':complete,'atoms_by_alternative':{a:sorted(v) for a,v in atoms.items()},'subconditions_by_alternative':{a:{k:sorted(v) for k,v in b.items()} for a,b in subs.items()}}

def gold():
    out=[];summary={}
    for cid,c in CASES.items():
        cand=[r for r in BASE if r['case_id']==cid and r['url']]
        allproof=merged(cid,cand);ids=allproof['complete_ids'];minimal={a:[] for a in ids}
        for k in range(1,len(cand)+1):
            for combo in itertools.combinations(cand,k):
                group={r['candidate_id'] for r in combo}
                for alt in merged(cid,combo)['complete_ids']:
                    if not any(set(old)<=group for old in minimal[alt]):minimal[alt].append(sorted(group))
        summary[cid]={'observed':c['pool_observed'],'eligible_ids':ids if c['pool_observed'] else None,'eligible_count':len(ids) if c['pool_observed'] else None,'minimal_paths':minimal,'unknown':'raw pool unavailable' if not c['pool_observed'] else ('C4.A2 full contract unproved; one intended CPython alternative remains conditional' if cid=='C4' else ('ipyvega/qtpandas Python atom missing in original pool' if cid=='C2' else 'unproved conditions retained in candidate ledger'))}
        for r in [x for x in BASE if x['case_id']==cid]:
            out.append({'row_type':'candidate','case_id':cid,'alternative_id':'','candidate_ids':[r['candidate_id']],'urls':[r['url']] if r['url'] else [],'locators':[r['locator']],'supports':r['supports_by_alternative'],'subconditions':r.get('subcondition_facts_by_alternative',{}),'complete_ids':merged(cid,[r])['complete_ids'],'verdict':'미확인' if not r['url'] else 'see per-alternative atoms','near_miss_or_limitation':r.get('conflicts',[])+r.get('partial_facts',[]),'source_record':r.get('source_record','pool.csv')})
        for alt,paths in minimal.items():
            for ids2 in paths:
                out.append({'row_type':'minimal_complete_pool_path','case_id':cid,'alternative_id':alt,'candidate_ids':ids2,'urls':[BYID[i]['url'] for i in ids2],'locators':[BYID[i]['locator'] for i in ids2],'supports':merged(cid,[BYID[i] for i in ids2])['atoms_by_alternative'],'subconditions':{},'complete_ids':[alt],'verdict':'예','near_miss_or_limitation':'Document statements; no runtime or user adoption observed.','source_record':'evidence/candidate-evidence.jsonl'})
    writecsv('gold-paths.csv',out);dump('evidence/pool-gold-summary.json',summary);return summary

def calculate():
    g=gold();views=jl('views.jsonl');plans=jl('evidence/trial-plan.jsonl');observed=jl('evidence/trial-observations.jsonl') if (E/'trial-observations.jsonl').exists() else []
    obs={o['trial_id']:o for o in observed};rows=[];provisional=len(obs)!=len(plans)
    for t in plans:
        o=obs.get(t['trial_id']);cid=t['case_id'];planned=[evidence(cid,s['url']) for s in t['steps'] if s['url']]
        sem=merged(cid,planned);actual=[];matches=[];arrivals=[];loc=[]
        transition_admissible=True;transition_reason='fixed-card transition'
        if o and t['kind']=='actual_outgoing_href':
            first=next((a for a in o['arrivals'] if a.get('requested_url')),None)
            source_expected=EXPECT.get((cid,t['steps'][0]['url']))
            transition_admissible=bool(first and first.get('success') and source_expected and first.get('html_sha256')==source_expected and urljoin(first.get('final_document_url',''),t['steps'][1]['raw_href'])==t['steps'][1]['url'])
            transition_reason='frozen source bytes match: fixed strict-window href plus current-base resolution verified' if transition_admissible else 'source bytes/arrival/base resolution do not establish this strict-window transition; destination receipt retained but not admitted as a path proof'
        if o:
            for a in o['arrivals']:
                if not a.get('requested_url'):continue
                u=a['requested_url'];r=evidence(cid,u);expected=EXPECT.get((cid,u));match=bool(expected and expected==a.get('html_sha256'))
                matches.append({'url':u,'snapshot_sha_match':match if expected else '미확인'})
                arrivals.append({'url':u,'success':a.get('success',False),'http_status':a.get('http_status'),'fragment_found':a.get('fragment_found'),'transport':a.get('transport'),'reason':a.get('reason','')})
                if r:loc.append({'url':u,'locator':r['locator']})
                # Raw hash mismatch cannot silently borrow a prior reading from another response.
                allowed=transition_admissible or a.get('action')!='follow_actual_href'
                if a.get('success') and match and r and allowed:actual.append(r)
        strict=merged(cid,actual);wide=merged(cid,actual,'W');den=set(g[cid]['eligible_ids'] or [])
        rows.append({'trial_id':t['trial_id'],'case_id':cid,'method':t['method'],'view_id':t['view_id'],'kind':t['kind'],'start_card':t['start_card'],'start_candidate':t['start_candidate'],'planned_cost':sum(s['cost'] for s in t['steps']),'actual_cost':o['cost_used'] if o else '미확인','fresh_start':True,'actions':t['steps'],'arrivals':arrivals,'locators':loc,'connectivity_success':o['connectivity_success'] if o else '미확인','strict_transition_admissible':transition_admissible,'transition_reason':transition_reason,'semantic_snapshot_matches':matches,'semantic_complete_ids':sem['complete_ids'],'confirmed_complete_ids':strict['complete_ids'],'confirmed_original_pool_ids':sorted(set(strict['complete_ids'])&den),'additional_ids_outside_denominator':sorted(set(strict['complete_ids'])-den),'confirmed_atoms':strict['atoms_by_alternative'],'confirmed_subconditions':strict['subconditions_by_alternative'],'W_confirmed_complete_ids':wide['complete_ids'],'actual_user_response':'미확인','receipt':'evidence/trial-observations.jsonl#'+t['trial_id'],'observation_complete':bool(o)})
        rows[-1]['semantic_read_scope_count']=len(actual)
        rows[-1]['applicable_views']=[t['view_id']]
        rows[-1]['observation_population']='main_fixed_plan'
    # Separate observed browser trial: use its own exact DOM reading, never patch failed HTTP trials.
    b=load('evidence/browser-observations.json')['requests']
    valid=bool(b['loaded'] and b['fragment_exists'] and b['fresh_start'] and b['navigation_cost']<=2 and len(b['dom_sha256'])==64)
    r={'url':b['url'],'supports_by_alternative':{b['alternative_id']:b['supports']},'locator':b['locator']}
    proof=merged('C1',[r] if valid else [])
    rows.append({'trial_id':b['trial_id'],'case_id':'C1','method':'B','view_id':'C1-B','kind':'independent_browser_direct','start_card':2,'start_candidate':'C1-4','planned_cost':1,'actual_cost':b['navigation_cost'],'fresh_start':b['fresh_start'],'actions':[{'action':b['action'],'url':b['url'],'cost':b['navigation_cost']}],'arrivals':[{'url':b['url'],'success':valid,'fragment_found':b['fragment_exists'],'transport':'cloud browser fresh tab; DOM snapshot'}],'locators':[{'url':b['url'],'locator':b['locator']}],'connectivity_success':valid,'semantic_snapshot_matches':[{'url':b['url'],'snapshot_sha_match':valid,'hash_kind':b['hash_kind']}],'semantic_complete_ids':proof['complete_ids'],'confirmed_complete_ids':proof['complete_ids'],'confirmed_original_pool_ids':proof['complete_ids'],'additional_ids_outside_denominator':[],'confirmed_atoms':proof['atoms_by_alternative'],'confirmed_subconditions':{},'W_confirmed_complete_ids':proof['complete_ids'],'actual_user_response':'미확인','receipt':'evidence/browser-observations.json#requests','observation_complete':True,'semantic_read_scope_count':int(valid),'applicable_views':['C1-B'],'observation_population':'separate_browser'})
    rows[-1]['strict_transition_admissible']=True;rows[-1]['transition_reason']='independent browser direct arrival: no second-hop inference'
    # Fresh exact-response reread witnesses are appended once, not cloned as three observations.
    extra=load('evidence/crossfield/control-second-hop-revalidated-trials.json')['trials']
    for t in extra:
        cid=t['case_id'];a,z=t['steps'];den=set(g[cid]['eligible_ids'])
        valid=bool(t['fresh_opener'] and t['empty_cookie_jar_at_start'] and t['navigation_cost_used']<=2 and all(s['success'] and s['http_status']==200 for s in t['steps']) and a['raw_sha256']==EXPECT[(cid,a['requested_url'])] and a['fragment_found'] and urljoin(a['final_document_url'],a['chosen_raw_href'])==z['requested_url'] and any(h['raw_href']==a['chosen_raw_href'] and h['dom_index']==a['chosen_dom_index'] for h in a['actual_matching_hrefs']))
        records=[{'url':s['requested_url'],'locator':s['semantic_locator'],'supports_by_alternative':s['supports_by_alternative']} for s in t['steps']]
        proof=merged(cid,records if valid else [])
        assert proof['complete_ids']==t['confirmed_complete_ids']
        applicable=[s.split(':',1)[0] for s in t['applicable_identical_start_cards']]
        assert all(any(c['candidate_id']==t['start_candidate'] and c['slot']==t['start_card'] for c in v['cards']) for v in views if v['view_id'] in applicable)
        rows.append({'trial_id':t['trial_id'],'case_id':cid,'method':'shared A/B/C','view_id':'C2-shared','kind':'independent_exact_response_revalidation','start_card':t['start_card'],'start_candidate':t['start_candidate'],'planned_cost':2,'actual_cost':t['navigation_cost_used'],'fresh_start':t['fresh_opener'] and t['empty_cookie_jar_at_start'],'actions':[{'action':s['action'],'url':s['requested_url'],'cost':s['cost']} for s in t['steps']],'arrivals':[{'url':s['requested_url'],'success':s['success'],'http_status':s['http_status'],'fragment_found':s['fragment_found'],'transport':s['transport'],'raw_sha256':s['raw_sha256']} for s in t['steps']],'locators':[{'url':s['requested_url'],'locator':s['semantic_locator']} for s in t['steps']],'connectivity_success':valid,'strict_transition_admissible':valid,'transition_reason':'Frozen source hash and actual in-window href verified; exact fresh destination response read in this same independent trial. Shared path witness, counted once.','semantic_snapshot_matches':[{'url':s['requested_url'],'snapshot_sha_match':valid,'hash_kind':'raw HTTP response read immediately in this trial','sha256':s['raw_sha256']} for s in t['steps']],'semantic_complete_ids':proof['complete_ids'],'confirmed_complete_ids':proof['complete_ids'],'confirmed_original_pool_ids':sorted(set(proof['complete_ids'])&den),'additional_ids_outside_denominator':sorted(set(proof['complete_ids'])-den),'confirmed_atoms':proof['atoms_by_alternative'],'confirmed_subconditions':{},'W_confirmed_complete_ids':proof['complete_ids'],'actual_user_response':'미확인','receipt':'evidence/crossfield/control-second-hop-revalidated-trials.json#'+t['trial_id'],'observation_complete':True,'semantic_read_scope_count':len(records) if valid else 0,'applicable_views':applicable,'observation_population':'separate_shared_revalidation'})
    for row in rows:
        arrivals=row['arrivals']
        row['source_destination_count']=len(arrivals)
        row['successful_destination_count']=sum(a.get('success') is True for a in arrivals)
        row['http_200_arrival_count']=sum(a.get('http_status')==200 for a in arrivals)
        if not arrivals:row['connectivity_success']='해당 없음'
    writecsv('clicks.csv',rows,list(rows[0]))
    result=[]
    for v in views:
        cid=v['case_id'];reps=[BYID[c['candidate_id']] for c in v['cards'] if c['candidate_id']];direct=merged(cid,reps);wide_direct=merged(cid,reps,'W');eligible=set(g[cid]['eligible_ids'] or [])
        trs=[r for r in rows if v['view_id'] in r['applicable_views']];reach=set().union(*(set(r['confirmed_complete_ids']) for r in trs)) if trs else set();wide_reach=set().union(*(set(r['W_confirmed_complete_ids']) for r in trs)) if trs else set()
        witnesses={a:next(r['trial_id'] for r in sorted(trs,key=lambda r:(r['actual_cost'] if isinstance(r['actual_cost'],int) else 99,r['trial_id'])) if a in r['confirmed_complete_ids']) for a in sorted(reach)}
        docurls=[urldefrag(r['url'])[0] for r in reps]
        result.append({'case_id':cid,'layer':v['layer'],'stratum':v['stratum'],'method':v['method'],'input_pool_observed':v['pool_observed'],'eligible_count':g[cid]['eligible_count'],'eligible_ids':g[cid]['eligible_ids'],'representatives':[c['candidate_id'] for c in v['cards']],'representative_urls':[c['url'] for c in v['cards']],'hidden_members':[i for c in v['cards'] for i in c['hidden_members']],'direct_complete_ids':direct['complete_ids'] if v['pool_observed'] else None,'direct_atoms':direct['atoms_by_alternative'],'direct_subconditions':direct['subconditions_by_alternative'],'reachable_original_pool_ids':sorted(reach&eligible) if v['pool_observed'] else None,'additional_ids_outside_denominator':sorted(reach-eligible),'all_reachable_ids':sorted(reach),'max_complete_original_pool_ids_in_one_trial':max((len(r['confirmed_original_pool_ids']) for r in trs),default=0) if v['pool_observed'] else None,'witnesses':witnesses,'missing_direct_ids':sorted(eligible-set(direct['complete_ids'])),'missing_two_click_ids':sorted(eligible-reach),'duplicate_original_document_card_slots':len(docurls)-len(set(docurls)),'planned_trials':sum(r['observation_population']=='main_fixed_plan' for r in trs),'observed_trials':sum(r['observation_complete'] and r['observation_population']=='main_fixed_plan' for r in trs),'separate_browser_witnesses':sum(r['observation_population']=='separate_browser' for r in trs),'shared_revalidated_witnesses':sum(r['observation_population']=='separate_shared_revalidation' for r in trs),'successful_document_path_trials':sum(r['connectivity_success'] is True for r in trs),'W_direct_complete_ids':wide_direct['complete_ids'] if v['pool_observed'] else None,'W_reachable_original_pool_ids':sorted(wide_reach&eligible) if v['pool_observed'] else None,'actual_user_response':'미확인','provisional':provisional})
    dump('evidence/results-data.json',{'provisional':provisional,'http_trials_planned':len(plans),'http_trials_observed':len(obs),'separate_browser_trials':1,'separate_shared_revalidation_trials':len(extra),'total_unique_observed_trials':len(rows),'views':result,'denominator_note':'original-pool eligible IDs only; per-ID reachable union requires each complete ID in a single trial; max in one trial is separate; unknown pools are not zero'})
    changes=[]
    lookup={(r['case_id'],r['method']):r for r in result}
    for cid in CASES:
        for left,right in [('A','B'),('A','C'),('B','C')]:
            l=lookup[(cid,left)];r=lookup[(cid,right)];known=l['input_pool_observed']
            for metric in ['direct_complete_ids','reachable_original_pool_ids']:
                ls=set(l[metric] or []);rs=set(r[metric] or [])
                changes.append({'row_type':'paired','case_id':cid,'comparison':left+'→'+right,'metric':metric,'before_ids':sorted(ls) if known else '미확인','after_ids':sorted(rs) if known else '미확인','gained_ids':sorted(rs-ls) if known else '미확인','lost_ids':sorted(ls-rs) if known else '미확인','eligible_denominator':l['eligible_count'] if known else '미확인','reason':'Same fixed six-slot pool; pair difference by complete alternative IDs.','evidence':'evidence/results-data.json'})
        for method in ['A','B','C']:
            r=lookup[(cid,method)]
            for m,w in [('direct_complete_ids','W_direct_complete_ids'),('reachable_original_pool_ids','W_reachable_original_pool_ids')]:
                known=r['input_pool_observed'];before=set(r[m] or []);after=set(r[w] or [])
                changes.append({'row_type':'W_same_document_scope','case_id':cid,'comparison':method+' strict→W','metric':m,'before_ids':sorted(before) if known else '미확인','after_ids':sorted(after) if known else '미확인','gained_ids':sorted(after-before) if known else '미확인','lost_ids':sorted(before-after) if known else '미확인','eligible_denominator':r['eligible_count'] if known else '미확인','reason':'Only read scope of actually reached documents changes; frozen cards, strict transition graph and cost unchanged. Unreviewed whole-document parts stay unknown. Missing fragments not repaired.','evidence':'evidence/candidate-evidence.jsonl; hop coding full_document fields'})
    for u in jl('evidence/views-U.jsonl'):
        v=next(v for v in views if v['case_id']==u['case_id'] and v['method']=='C')
        assert [c['candidate_id'] for c in u['cards']]==[c['candidate_id'] for c in v['cards']]
        known=v['pool_observed']
        changes.append({'row_type':'U_unknown_key_merge','case_id':u['case_id'],'comparison':'C→C-U','metric':'representatives','before_ids':[c['candidate_id'] for c in v['cards']] if known else '미확인','after_ids':[c['candidate_id'] for c in u['cards']] if known else '미확인','gained_ids':[] if known else '미확인','lost_ids':[] if known else '미확인','eligible_denominator':lookup[(u['case_id'],'C')]['eligible_count'] if known else '미확인','reason':'Otherwise-known key fields never match, so this relaxation merges no observed groups.' if known else 'Unobserved pool: equality of blank fixtures is not empirical evidence of no change.','evidence':'evidence/views-U.jsonl'})
    for t in extra:
        changes.append({'row_type':'new_evidence_outside_original_pool','case_id':'C2','comparison':'same C2-1 card shared by A/B/C','metric':'independent exact-response path','before_ids':[],'after_ids':t['additional_ids_outside_denominator'],'gained_ids':t['additional_ids_outside_denominator'],'lost_ids':[],'eligible_denominator':g['C2']['eligible_count'],'reason':'Newly confirmed Python atom via a second document, not restoration of an original-pool complete alternative. Two actual shared trials are not six method observations.','evidence':'evidence/crossfield/control-second-hop-revalidated-trials.json#'+t['trial_id']})
    writecsv('changes.csv',changes)
    print(json.dumps({'provisional':provisional,'observed_http':len(obs),'planned_http':len(plans),'pool_eligible':{c:x['eligible_count'] for c,x in g.items()},'control_views':[{k:r[k] for k in ['case_id','method','direct_complete_ids','reachable_original_pool_ids','max_complete_original_pool_ids_in_one_trial']} for r in result if r['layer']=='control']},ensure_ascii=False))

if __name__=='__main__':calculate()
