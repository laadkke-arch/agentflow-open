"""AF-RES-044 reproducible grouping and evidence arithmetic. No network writes.

Run from repository root with python -B. All outputs stay inside owned_path.
Evidence judgments are explicit inputs, not inferred from grouping keys.
"""
from pathlib import Path
import csv, json, hashlib, datetime, itertools, html, sys
from urllib.parse import urldefrag, urljoin

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'evidence'
def load(p): return json.loads((ROOT/p).read_text())
def dump(p, data): (ROOT/p).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
def lines(p, rows): (ROOT/p).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
def readcsv(p): return list(csv.DictReader((ROOT/p).open(newline='')))
def writecsv(p, rows, fields=None):
    if not rows and not fields: raise ValueError(p)
    fields=fields or list(rows[0]); f=(ROOT/p).open('w',newline='')
    w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader()
    for row in rows:
        w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in row.items()})
    f.close()
def sha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

def build_groups():
    cases=load('evidence/cases.json'); pool=readcsv('pool.csv')
    meta={r['candidate_id']:r for r in load('evidence/display-metadata-freeze.json')['rows']}
    corrections=load('evidence/metadata-audit-corrections.json')['overrides'] if (E/'metadata-audit-corrections.json').exists() else {}
    for cid,change in corrections.items():meta[cid].update(change);meta[cid]['audit_override_source']='evidence/metadata-audit-corrections.json'
    freeze=load('evidence/input-freeze.json')
    for name,digest in freeze['files'].items():
        assert sha(name)==digest,(name,sha(name),digest)
    groups=[];views=[];uviews=[]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    for case in cases:
        cid=case['case_id'];rows=[r for r in pool if r['case_id']==cid]
        assert [int(r['rank']) for r in rows]==list(range(1,7))
        for method in ['A','B','C','C-U']:
            gs=[];lookup={}
            for r in rows:
                if not r['url']:continue
                m=meta[r['candidate_id']]
                if method=='A': key=['url',r['url']]
                elif method=='B':key=['upstream',m['upstream']] if m['upstream']!='미확인' else ['singleton',r['candidate_id']]
                elif not m['identity_key_complete'] and method=='C':key=['singleton',r['candidate_id']]
                else:key=['component',m['upstream'],m['component'],m['purpose'],m['version'],sorted(m['evidence_roles'])]
                ks=json.dumps(key,ensure_ascii=False,sort_keys=True)
                if ks not in lookup:
                    lookup[ks]=len(gs);gs.append({'group_id':f'{cid}-{method}-G{len(gs)+1}','key':key,'representative':r['candidate_id'],'members':[]})
                gs[lookup[ks]]['members'].append(r['candidate_id'])
            byid={r['candidate_id']:r for r in rows}
            cards=[]
            for i in range(3):
                if i<len(gs):
                    g=gs[i];rep=g['representative'];cards.append({'slot':i+1,'candidate_id':rep,'url':byid[rep]['url'],'label':'원문 보기','label_length':5,'description':'','description_length':0,'sibling_label':'관련 링크','sibling_label_length':5,'members':g['members'],'member_urls':[byid[x]['url'] for x in g['members']],'hidden_members':g['members'][1:]})
                else:cards.append({'slot':i+1,'candidate_id':None,'url':None,'label':'','label_length':0,'description':'','description_length':0,'members':[],'member_urls':[],'hidden_members':[],'empty_reason':'unobserved pool' if not case['pool_observed'] else 'fewer than three groups'})
            view={'view_id':cid+'-'+method,'case_id':cid,'layer':case['layer'],'stratum':case['stratum'],'method':method,'computed_utc':now,'pool_sha256':sha('pool.csv'),'metadata_sha256':sha('evidence/display-metadata-freeze.json'),'pool_observed':case['pool_observed'],'cards':cards,'offscreen_groups':[g['members'] for g in gs[3:]],'presentation':'three serialized cards, fixed labels, empty descriptions; no measured human UI response'}
            if method=='C-U':uviews.append(view)
            else:
                groups.append({'case_id':cid,'method':method,'input_candidates':[r['candidate_id'] for r in rows],'groups':gs,'metadata':[meta[r['candidate_id']] for r in rows if r['url']],'gold_used_as_key':False})
                views.append(view)
    lines('groups.jsonl',groups);lines('views.jsonl',views);lines('evidence/views-U.jsonl',uviews)
    panels=[]
    for v in views:
        cards=[]
        for c in v['cards']:
            if c['url']:
                members=''.join('<a href="'+html.escape(u,quote=True)+'">원문 보기</a>' for u in c['member_urls'])
                cards.append('<article><a href="'+html.escape(c['url'],quote=True)+'" target="_blank" rel="noopener">원문 보기</a><details><summary>관련 링크</summary>'+members+'</details></article>')
            else:cards.append('<article aria-label="빈 자리"></article>')
        panels.append('<section id="'+v['view_id']+'"><h2>'+v['view_id']+'</h2><div class="cards">'+''.join(cards)+'</div></section>')
    (E/'screens.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><title>AF-RES-044 three-card fixtures</title><style>body{font:16px sans-serif}section{margin:24px}h2{font-size:14px}.cards{display:grid;grid-template-columns:repeat(3,220px);gap:12px}article{border:1px solid #aaa;min-height:80px;padding:12px}details{margin-top:10px}details a{display:block}</style>'+''.join(panels)+'</html>\n')
    print(json.dumps({'views':len(views),'groups':len(groups),'U_views':len(uviews),'nonempty_cards':sum(bool(c['url']) for v in views for c in v['cards'])}))

def build_candidate_evidence():
    pool=readcsv('pool.csv');cases={c['case_id']:c for c in load('evidence/cases.json')}
    vc={x['candidate_id']:x for x in load('evidence/vega/coding-V.json')['candidate_rows']}
    vw={x['candidate_id']:x for x in load('evidence/vega/windows-V.json')}
    cw={x['candidate_id']:x for x in load('evidence/control/candidate-read-receipts.json')}
    c2={f"C2-{x['slot']}":x for x in load('evidence/crossfield/control-C2.json')['slots']}
    rows=[]
    for p in pool:
        cid=p['case_id'];id=p['candidate_id'];c=cases[cid];atoms=[a['id'] for a in c['required_atoms']]
        r={'case_id':cid,'candidate_id':id,'url':p['url'],'document_url':urldefrag(p['url'])[0],'scope':'strict','supports_by_alternative':{},'full_document_supports_by_alternative':{},'partial_facts':[],'conflicts':[],'unknown_atoms':atoms[:],'evidence_level':'D1_author_statement','runtime_tested':False,'actual_user_response':'미확인','connectivity':'미확인','fragment_confirmed':'미확인','locator':'미확인','limitation':''}
        if not p['url']:
            r.update(evidence_level='D0_no_document',limitation='Acquisition missing, not a zero-candidate pool' if p['empty_kind']=='unobserved' else 'Observed category exhausted; real empty slot')
        elif cid.startswith('V'):
            x=vc[id];w=vw[id]
            r.update(connectivity=x['connectivity_success'],fragment_confirmed=w['fragment_exists'],locator=x['strict_locator'],partial_facts=x.get('subcondition_facts',[]),limitation=x['strict_fact'],atom_verdicts=x['strict_atom_verdicts'],source_record='evidence/vega/coding-V.json')
            if x['supports']:r['supports_by_alternative']['vega-lite']=x['supports']
            if x['full_document_supports']:r['full_document_supports_by_alternative']['vega-lite']=x['full_document_supports']
            override=load('evidence/vega/scope-fact-overrides.json').get(id) if (E/'vega/scope-fact-overrides.json').exists() else None
            if override:r.update(verified_fact=override['strict_fact'],limitation=override['limitation'],locator=override['locator'],source_record='evidence/vega/scope-fact-overrides.json')
        elif cid=='C2':
            x=c2[id];r.update(connectivity=x['status']==200,fragment_confirmed=x.get('fragment_found'),locator=x['candidate_window']['locator'],limitation=x['candidate_window']['limitation'],verified_fact=x['candidate_window']['verified_fact'],source_record='evidence/crossfield/control-C2.json')
            r['supports_by_alternative']={alt:atoms[:] for alt in x.get('complete_alternative_ids',[])}
            r['full_document_supports_by_alternative']=dict(r['supports_by_alternative'])
            if id=='C2-5':r['full_document_supports_by_alternative']={alt:atoms[:] for alt in c2['C2-1']['complete_alternative_ids']}
            if id=='C2-4':r['partial_facts']=['Altair Python visualization; tabular input is not explicit in the first 800-word/home window.'];r['supports_by_alternative']={'C2-altair':['C2.A1']};r['full_document_supports_by_alternative']={'C2-altair':['C2.A1']}
            if id=='C2-6':r['partial_facts']=['Bokeh Python visualization; tabular evidence missing in the first window.'];r['supports_by_alternative']={'C2-bokeh':['C2.A1']};r['full_document_supports_by_alternative']={'C2-bokeh':['C2.A1']}
            if id=='C2-1':r['partial_facts']=['ipyvega and qtpandas are mentioned, but Python condition not independently explicit in this strict section.'];r['conflicts']=['ggplot2 is R, not a Python implementation satisfying this demand.']
        else:
            x=cw[id];scope=x.get('scope',{});r.update(connectivity=x.get('status')==200,fragment_confirmed=scope.get('fragment_found'),locator=scope.get('scope_locator','미확인'),source_record='evidence/control/candidate-read-receipts.json')
            if cid=='C1':
                if id in ['C1-1','C1-2','C1-5']:r['supports_by_alternative']={'http-client:httpx':atoms[:]}
                if id=='C1-3':r['supports_by_alternative']={'http-client:httpx':['C1.A1']};r['partial_facts']=['Client construction and request routing are explicit, but no get/send or Request instance example in strict window.']
                if id=='C1-4':r.update(connectivity='browser confirmed; raw HTTP failed',fragment_confirmed=True,locator='section#prepared-requests (346 words), Requests2.34.2',limitation='Browser independently reached exact section; raw HTTP failures remain failures.');r['supports_by_alternative']={'http-client:requests':atoms[:]}
                if id=='C1-6':r['limitation']='HTTP200 but #client-instances does not exist; do not repair the URL.'
                r['full_document_supports_by_alternative']=dict(r['supports_by_alternative'])
                if id=='C1-3':r['full_document_supports_by_alternative']={'http-client:httpx':atoms[:]}
                if id=='C1-6':r['full_document_supports_by_alternative']={'http-client:httpx':atoms[:]}
            elif cid=='C3':
                if id in ['C3-3','C3-4']:r['supports_by_alternative']={'C3-cpython311':['C3.A1']};r['partial_facts']=['subgroup/split methods are not automatic except* propagation.']
                if id=='C3-5':r['supports_by_alternative']={'C3-cpython311':['C3.A2']}
                if id in ['C3-1','C3-2']:r['partial_facts']=['Introduction/version or motivation, not both full constructor and propagation conditions in strict window.']
                if id=='C3-6':r['conflicts']=['ordinary except catches matching exception types; not equivalent to except* subgroup processing.']
                r['full_document_supports_by_alternative']=dict(r['supports_by_alternative'])
                if id=='C3-2':r['full_document_supports_by_alternative']={'C3-cpython311':atoms[:]}
                if id=='C3-6':r['full_document_supports_by_alternative']={'C3-cpython311':['C3.A2']}
            elif cid=='C4':
                # Frozen A1 includes an explicit gather distinction; preserve both constituents.
                if id=='C4-2':r['partial_facts']=['TaskGroup non-cancellation failure cancels siblings and waits. Gather comparison in frozen A1 is not in this window.'];r['support_fragments']={'C4-cpython311':['C4.A1.taskgroup']}
                if id=='C4-5':r['support_fragments']={'C4-cpython311':['C4.A1.gather']};r['conflicts']=['default gather propagates first child exception without cancelling remaining children; cancelling gather itself is a different condition.']
                if id=='C4-3':r['partial_facts']=['__aenter__/__aexit__ return awaitables; similar synchronous semantics. Complete await and exception-forwarding procedure is in another document, not this strict window.']
                if id=='C4-4':r['partial_facts']=['create_task schedules an individual task; no TaskGroup failure policy.']
                if id=='C4-1':r['partial_facts']=['TaskGroup introduction and exit wait synopsis; full two-atom contract absent.']
                if id=='C4-6':r['partial_facts']=['Maintainer implementation/design decision, not a complete async-with protocol specification.']
                r['limitation']='Planned positive control remains unproved under frozen strict A2; do not silently weaken it.'
                if id in ['C4-2','C4-4','C4-5']:r['full_document_supports_by_alternative']={'C4-cpython311':['C4.A1']}
        if id=='C2-1':
            for alt in ['C2-ipyvega','C2-qtpandas']:
                r['supports_by_alternative'][alt]=['C2.A2'];r['full_document_supports_by_alternative'][alt]=['C2.A2']
        r['unknown_atoms']=[a for a in atoms if not any(a in sup for sup in r['supports_by_alternative'].values())]
        if 'atom_verdicts' not in r:r['atom_verdicts']=[{'atom_id':a,'verdict':'예' if a not in r['unknown_atoms'] else '미확인','direction':c['direction'],'version':c['required_version']} for a in atoms]
        if cid in ['C3','C4'] and (E/'pandoc/control-second-hop-coding.json').exists():
            py=load('evidence/pandoc/control-second-hop-coding.json')
            x=next(z for z in py['destinations'] if z['url']==r['url']);y=next(y for y in x['per_case'] if y['case_id']==cid);alt=cid+'-cpython311'
            r.update(supports_by_alternative={alt:y['supports']},full_document_supports_by_alternative={alt:y['full_document_supports']},atom_verdicts=y['atom_verdicts'],subcondition_facts_by_alternative={alt:y['subcondition_facts']},full_document_subcondition_facts_by_alternative={alt:y['full_document_subcondition_facts']},unknown_atoms=y['unknown'],partial_atoms=y['partial'],locator=x['locator'],verified_fact=x['verified_fact'],source_record='evidence/pandoc/control-second-hop-coding.json')
        rows.append(r)
    lines('evidence/candidate-evidence.jsonl',rows)
    print(json.dumps({'candidate_rows':len(rows),'real_url_rows':sum(bool(r['url']) for r in rows)}))

if __name__=='__main__':
    stage=sys.argv[1] if len(sys.argv)>1 else 'groups'
    if stage=='groups':build_groups()
    elif stage=='coding':build_candidate_evidence()
    else:raise SystemExit('stage must be groups or coding')
