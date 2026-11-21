"""Read fixed Git objects, recompute assembly audit counts, save only owned output.

This does not rerun earlier retrieval experiments or contact earlier studies' sites.
It reads no AF-RES-017/018/019 content. 011 CASES is used only for structure/counts.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import subprocess, json, csv, io, hashlib, ast, unicodedata

OUT=Path('docs/workstreams/research/AF-RES-020')
FIX=json.loads((OUT/'evidence/fixed-inputs.json').read_text())['fixed']
READ=[]
CACHE={}

def read(t,p):
    key=(t,p)
    if key not in CACHE:
        path=f'docs/workstreams/research/AF-RES-{t}/{p}'
        raw=subprocess.check_output(['git','show',FIX['AF-RES-'+t]+':'+path])
        CACHE[key]=raw.decode()
        READ.append(dict(task='AF-RES-'+t,sha=FIX['AF-RES-'+t],path=path,
                         sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),
                         lines=len(raw.splitlines()),accessed_at_utc=datetime.now(timezone.utc).isoformat(),
                         method='git show'))
    return CACHE[key]

def j(t,p):return json.loads(read(t,p))
def csvrows(t,p,sep=','):
    return [dict(r,_line=n) for n,r in enumerate(csv.DictReader(io.StringIO(read(t,p)),delimiter=sep),2)]
def mean(rows,k):return sum(float(r[k]) for r in rows)/len(rows)
def selected(rows,**kw):return [r for r in rows if all(r[k]==v for k,v in kw.items())]

A=dict(schema=1,task='AF-RES-020',reviewer='GPT-6 Astra Pro 내부 별도 검토',
       description='고정 원 결과의 전달·산술 감사. 원 검색 재실행·외부 서비스 확인·D4 적용 아님.',
       generated_at_utc=datetime.now(timezone.utc).isoformat(),results={})

# 011: never emit question/answer texts or individual profiles.
d=j('011','CASES.json'); cases=d['cases']; part=[c for c in cases if c['whole_or_part']=='part']
adopt={c['id'] for c in part if any(a['outcome'].get('asker_response')=='adopt' for a in c['answers'])}
accepted={c['id'] for c in part if any(a['outcome'].get('accepted') is True for a in c['answers'])}
m=j('011','evidence/metrics.json')['main']
cross=m['cross_domain_answers']
res011=dict(cases=len(cases),scope=dict(Counter(c['whole_or_part'] for c in cases)),
           answers=sum(len(c['answers']) for c in cases),platforms=dict(Counter(c['platform'] for c in cases)),
           partial=dict(n=len(part),adopt=len(adopt),accepted=len(accepted),union=len(adopt|accepted),intersection=len(adopt&accepted)),
           cross_domain=dict(answers=len(cross),threads=len({x.get('case',x.get('case_id')) for x in cross}),
                             responses=dict(Counter(x.get('response') for x in cross))))
assert res011['cases']==61 and res011['answers']==635
assert res011['partial']==dict(n=33,adopt=6,accepted=5,union=10,intersection=1)
assert len(cross)==14
A['results']['011']=res011

# 012: distinguish N per query-condition from N per slot.
r12=csvrows('012','results/metrics.csv')
same=[r for r in r12 if r['corpus']=='full' and r['scope']=='all' and r['query_language']==r['corpus_language']]
base=selected(same,judgments='pooled')
res12=dict(representations={},review={},verification={})
for rep in ['D-a','D-b','D-c']:
    rows=selected(base,representation=rep)
    nq=sum(int(r['near_misses_at10_n']) for r in rows)
    count=round(sum(float(r['near_misses_at10'])*int(r['near_misses_at10_n']) for r in rows))
    res12['representations'][rep]=dict(csv_lines=[r['_line'] for r in rows],cells=len(rows),query_conditions=nq,
        slots=nq*10,N_count=count,N_mean_per_query_condition=mean(rows,'near_misses_at10'),N_per_slot=count/(nq*10),
        recall_macro=mean(rows,'recall_at10'))
for judgment in ['review_pool','review_independent']:
    res12['review'][judgment]={}
    for method in ['M1','M2','M3']:
        rows=selected(same,judgments=judgment,method=method)
        res12['review'][judgment][method]=dict(csv_lines=[r['_line'] for r in rows],cells=len(rows),nDCG=mean(rows,'ndcg_at10'),query_count=sorted({r['queries'] for r in rows}))
v12=j('012','VERIFICATION.json')
res12['verification']={k:v12.get(k) for k in ['pooled_replay','clean_replay','workload','observed_at_utc']}
assert res12['representations']['D-b']['N_count']==85
assert res12['representations']['D-c']['N_count']==163
assert res12['representations']['D-b']['query_conditions']==216
A['results']['012']=res12

# 013: cross-tab the two axes, keep histories and current utility separate.
c13=j('013','cases/CASES.json')['cases']
gold=[dict(x,case_id=c['case_id'] if 'case_id' in c else c.get('id')) for c in c13 for x in c['gold_items']]
a13=j('013','evidence/AGGREGATES.json')
samefield={x['id'] for x in gold if x['role']=='같은 분야의 다른 설계'}
structural={x['id'] for x in gold if x['match_kind']=='structural_design'}
axis_ids=lambda pred:[dict(case_id=x['case_id'],gold_id=x['id']) for x in gold if pred(x)]
res13=dict(cases=len(c13),gold=len(gold),roles=dict(Counter(x['role'] for x in gold)),
           match_kinds=dict(Counter(x['match_kind'] for x in gold)),stances=dict(Counter(x['stance'] for x in gold)),
           role_by_match_kind=[dict(role=a,match_kind=b,n=n) for (a,b),n in Counter((x['role'],x['match_kind']) for x in gold).items()],
           different_axes=dict(same_field_not_structural=axis_ids(lambda x:x['role']=='같은 분야의 다른 설계' and x['match_kind']!='structural_design'),
                               structural_not_same_field=axis_ids(lambda x:x['match_kind']=='structural_design' and x['role']!='같은 분야의 다른 설계')),
           baselines=a13['baseline_totals'],cross_domain=axis_ids(lambda x:x['role']=='다른 분야 원리'))
assert len(gold)==176 and res13['match_kinds']=={'structural_design':146,'external_entity':30}
assert res13['different_axes']['same_field_not_structural'] and res13['different_axes']['structural_not_same_field']
A['results']['013']=res13

# 014: complete pairwise comparisons, not headline-only summary.
r14=csvrows('014','results/metrics.csv')
res14=dict(conditions={},reviews={},query_bridge={},input={},positive_agreement={})
for cond in ['b','c','filter']:
    rows=selected(r14,bridge='terms',condition=cond,judgments='answers',scope='all')
    nq=sum(int(r['near_misses_at10_n']) for r in rows)
    count=sum(int(r['near_miss_count']) for r in rows)
    slots=sum(int(r['slots_at10']) for r in rows)
    res14['conditions'][cond]=dict(csv_lines=[r['_line'] for r in rows],N_count=count,query_conditions=nq,slots=slots,
        N_mean_per_query_condition=mean(rows,'near_misses_at10'),N_per_slot=count/slots,
        by_method={r['method']:{k:r[k] for k in ['recall_at10','recall_at10_n','ndcg_at10','near_miss_count','queries','conflicts']} for r in rows})
for judgment in ['review_answers','review_pool','review_independent']:
    rows=selected(r14,bridge='terms',condition='b',judgments=judgment,scope='all')
    res14['reviews'][judgment]={r['method']:dict(csv_line=r['_line'],nDCG=float(r['ndcg_at10']),n=int(r['queries'])) for r in rows}
for bridge in ['raw','terms']:
    rows=selected(r14,bridge=bridge,method='BM25',condition='b',judgments='answers',scope='all')
    assert len(rows)==1
    r=rows[0]
    res14['query_bridge'][bridge]=dict(csv_line=r['_line'],recall=float(r['recall_at10']),recall_n=int(r['recall_at10_n']),
        queries=int(r['queries']),no_signal=int(r['queries_without_signal']))
qmeta=j('014','queries/metadata.json')
res14['input']=dict(n=len(qmeta),modes=dict(Counter(q['mode'] for q in qmeta)),sources=dict(Counter(q['source'] for q in qmeta)),
                   must=sum(len(q['must']) for q in qmeta),scope=dict(Counter(q['whole_or_part'] for q in qmeta)))
entries14=[json.loads(l) for l in read('014','corpus/entries.jsonl').splitlines() if l.strip()]
per14=selected(csvrows('014','results/per_query.csv'),bridge='terms',method='BM25',condition='filter',judgments='answers')
tree=ast.parse(read('014','src/constraints.py'))
rules={node.targets[0].id:ast.literal_eval(node.value) for node in tree.body
       if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ['NEEDS','BANS']}
normal=lambda value:' '.join(unicodedata.normalize('NFKC',value).casefold().split())
needs={normal(k):v for k,v in rules['NEEDS'].items()};bans={normal(k):v for k,v in rules['BANS'].items()}
mapped=0
for q in qmeta:
    for item in q['must']:
        k=normal(item['target'])
        if (k in needs or k in bans) and item['polarity']==('positive' if needs.get(k) else 'negative'):
            mapped+=1
res14['filter_coverage']=dict(documents_with_exclusions=sum(bool(e['exclusions']) for e in entries14),
                             queries_with_conflicts=sum(int(r['conflicts'])>0 for r in per14),
                             conflicts=sum(int(r['conflicts']) for r in per14),
                             must_items=res14['input']['must'],mapped_items=mapped,
                             limitation_changed=sum(e['D-b']!=e['D-c'] for e in entries14))
assert res14['filter_coverage']==dict(documents_with_exclusions=5,queries_with_conflicts=8,conflicts=9,must_items=68,mapped_items=39,limitation_changed=171)
ind=csvrows('014','qrels/independent.tsv','\t'); pool=csvrows('014','qrels/pooled.tsv','\t')
pk={(r['query_id'],r['doc_id']):r['grade'] for r in pool}
ik={(r['query_id'],r['doc_id']):r['grade'] for r in ind}
ip={k for k,g in ik.items() if g in ['1','2']}
pp={k for k in ik if pk[k] in ['1','2']}
res14['positive_agreement']=dict(pairs=len(ik),all_agree=sum(ik[k]==pk[k] for k in ik),independent_positive=len(ip),pool_positive=len(pp),
                                    relevant_intersection=len(ip&pp),relevant_union=len(ip|pp))
res14['counterexamples']=j('014','results/counterexamples.json')
v14=j('014','VERIFICATION.json')
res14['verification']={k:v14.get(k) for k in ['reproducibility','model_access']}
assert res14['conditions']['b']['N_count']==17 and res14['conditions']['c']['N_count']==11
assert res14['conditions']['b']['query_conditions']==183 and res14['conditions']['b']['slots']==1830
assert res14['positive_agreement']['relevant_union']==12 and res14['positive_agreement']['relevant_intersection']==3
assert res14['positive_agreement']['all_agree']==279 and res14['input']['must']==68
A['results']['014']=res14

# 015: raw reason-level counts, nested cohorts, independent-event warning.
reasons=[json.loads(l) for l in read('015','REASONS.jsonl').splitlines() if l.strip()]
meaningful=[r for r in reasons if r['reason_type']!='이유 없음']
known=lambda r:r['now_verdict'] in ['성립','약화','무너짐']
cohort=[r for r in meaningful if r['then_verdict']=='성립' and known(r)]
dated=[r for r in cohort if r['answer_date']]
linked=[r for r in meaningful if r['url_origin'] is not None]
direct=[r for r in meaningful if r['url_origin'] in ['원문 지정','011 답 직접 링크']]
def status(rows):return dict(n=len(rows),known=sum(known(r) for r in rows),collapsed=sum(r['now_verdict']=='무너짐' for r in rows),now=dict(Counter(r['now_verdict'] for r in rows)))
res15=dict(rows=len(reasons),meaningful=status(meaningful),answers=len({r['answer_ref'] for r in meaningful}),
           no_reason_rows=len(reasons)-len(meaningful),then=dict(Counter(r['then_verdict'] for r in meaningful)),
           historically_valid_current_known=status(cohort),with_answer_date=status(dated),linked=status(linked),direct=status(direct),
           later_collapsed=[dict(reason_id=r['reason_id'],candidate=r['candidate'],direction=r['reason_direction'],dated=bool(r['answer_date'])) for r in cohort if r['now_verdict']=='무너짐'],
           signal_strict={k:{f:v['strict'].get(f) for f in ['n','TP','FN','FP','TN']} for k,v in j('015','results/confusion.json').items()},
           cost=j('015','results/cost.json'),cadence=j('015','results/cadence.json'))
assert res15['meaningful']['n']==500 and res15['meaningful']['known']==195 and res15['meaningful']['collapsed']==14
assert res15['historically_valid_current_known']['n']==83 and res15['historically_valid_current_known']['collapsed']==5
assert res15['with_answer_date']['n']==77 and res15['with_answer_date']['collapsed']==2
assert res15['linked']['n']==275 and res15['linked']['known']==102 and res15['linked']['collapsed']==9
assert res15['direct']['n']==147 and res15['direct']['known']==50 and res15['direct']['collapsed']==2
A['results']['015']=res15

# 016: recompute original coder agreement and the non-independent S3 copy.
ua=j('016','coding/coder-a.json');ub=j('016','coding/coder-b.json')
a={r['unit_id']:r for r in ua['rows']};b={r['unit_id']:r for r in ub['rows']}
units=j('016','sample/units.json')['units'];res16=dict(by_sample={},comparison={},S3_copy={},impact={})
for sample in ['011','012','004']:
    ids=[r['unit_id'] for r in units if r['sample']==sample]
    res16['by_sample'][sample]={scheme:dict(n=len(ids),agree=sum(a[i][scheme]==b[i][scheme] for i in ids)) for scheme in ['S1','S2','S3']}
    res16['comparison'][sample]=dict(A=sum(a[i]['S2']=='comparison' for i in ids),B=sum(b[i]['S2']=='comparison' for i in ids),n=len(ids))
for coder,rows in [('A',a),('B',b)]:
    res16['S3_copy'][coder]=dict(n=len(rows),same=sum(r['S2']==r['S3']['contribution'] for r in rows.values()))
impact=j('016','evidence/impact.json')
res16['impact']=dict(serialization_note=impact['serialization_note'],method=impact['method'],summary=impact['summary'],rows=len(impact['rows']))
res16['reported_agreement']=j('016','evidence/agreement.json')['main']
vocab=j('016','evidence/vocab-map-data.json')
res16['vocab_rows']=len(vocab['rows'])
assert res16['by_sample']['011']==dict(S1=dict(n=120,agree=94),S2=dict(n=120,agree=85),S3=dict(n=120,agree=75))
assert res16['comparison']['011']==dict(A=0,B=14,n=120)
assert res16['vocab_rows']==42 and res16['impact']['rows']==30
A['results']['016']=res16

# Record actual fixed object read hashes for all documented source records as well.
sources=json.loads((OUT/'evidence/sources-late.json').read_text())
for src in sources['sources']:
    t=src['id'][1:4]
    marker=f'docs/workstreams/research/AF-RES-{t}/'
    p=src['access_method'].split(marker,1)[1]
    read(t,p)

A['read_objects']=READ
A['assertions_passed']=True
A['limits']=[
 '기존 판정 파일에 대한 산술 재집계이며 판정 진위의 새 독립 실험이 아니다.',
 '011 CASES는 구조·집계만 사용했다. 최초 탐색에서 outcome dict 전체를 Counter로 직렬화하여 일부 요약 필드가 도구 출력에 부수 노출되었으나 이를 새 단위 분석·출처 주장·산출물에 쓰지 않았다. 이후 허용 필드만 집계했다.',
 '현재 실행은 원문 재조사·E5 실행·사람 적용을 포함하지 않는다.'
]
(OUT/'evidence/audit-numeric-late.json').write_text(json.dumps(A,ensure_ascii=False,indent=2)+'\n')
readmap={(r['task'],r['path']):r for r in READ}
for src in sources['sources']:
    t=src['id'][1:4]; marker=f'docs/workstreams/research/AF-RES-{t}/';p=src['access_method'].split(marker,1)[1]
    r=readmap[('AF-RES-'+t,marker+p)]
    src['accessed_at_utc']=r['accessed_at_utc'];src['content_sha256']=r['sha256'];src['line_count']=r['lines']
(OUT/'evidence/sources-late.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(assertions_passed=True,files=len(READ),summary={
 '011_partial':res011['partial'],'012_N':[res12['representations'][x]['N_count'] for x in ['D-b','D-c']],
 '013_cross_axes':res13['role_by_match_kind'],'014_positive_agreement':res14['positive_agreement'],
 '015_cohorts':{x:res15[x]['n'] for x in ['meaningful','historically_valid_current_known','with_answer_date']},
 '016_comparison':res16['comparison']['011']}),ensure_ascii=False))
