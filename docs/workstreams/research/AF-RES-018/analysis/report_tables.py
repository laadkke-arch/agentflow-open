#!/usr/bin/env python3
"""Render required numeric tables from completed observations; never create data."""
import collections,itertools,json
from common import ROOT,load
from build_observations import verdict

HEADERS={
1:['조건','질문 수(011 원문·011 요약·새 질문)','등급2 적중@10','등급≥1 recall@10','첫 관련 후보 순위(중앙값)','N/상위 10','심은 근접 오답 올바른 거절률','관련 후보 잘못 거절률','주장 오류율(분모)','평균 검색·열람 수','미확인'],
2:['층(011·새 질문 × 전체·부분 × I5 유무 × must 유무)','질문 수','A 값','P 값','차이(95% 구간)','판정 출처별 순서 유지 여부','미확인'],
3:['주장 유형','조건','주장 수(분모)','참','거짓','확인 불가','주된 오류 유형','대표 거짓 사례(질문 ID·후보)','미확인'],
4:['사전 기준','관측 값','충족 여부','판정 출처 민감도','이 판정이 틀릴 조건','미확인']}

def clean(v):return str(v).replace('|','\\|').replace('\n',' ')
def table(n,rows):
    h=HEADERS[n];assert all(len(r)==len(h) for r in rows)
    return '\n'.join(['| '+' | '.join(h)+' |','| '+' | '.join(['---']*len(h))+' |']+['| '+' | '.join(clean(x) for x in r)+' |' for r in rows])
def number(v,d=3):return '미확인(분모 확보)' if v is None else f'{v:.{d}f}'
def percent(v):return '미확인(분모 확보)' if v is None else f'{100*v:.1f}%'
def change(r,scale=1):
    if r['difference'] is None:return '미확인(해당 지표 분모 확보)'
    lo,hi=r['ci95'];return f"{scale*r['difference']:+.3f} [{number(None if lo is None else scale*lo)}, {number(None if hi is None else scale*hi)}]"
def rate(r,c):
    den=r.get('denominator_'+c,0);num=r.get('numerator_'+c)
    return f'{percent(r[c])} ({num}/{den})' if den and num is not None else '미확인(해당 역할/주장 분모 확보)'
def main():
    metrics=load('analysis/bootstrap_intervals.json')['rows'];by={(r['group'],r['metric']):r for r in metrics}
    obs=load('analysis/per_question.json');meta=load('questions/metadata.json');claims=load('claims/CLAIMS.json')
    if isinstance(claims,dict):claims=claims['rows']
    orders=load('analysis/judging-source-order.json');h1=load('analysis/H1.json')
    def m(name,g='all'):return by[(g,name)]
    def source(g,left,right):return next(x for x in orders if x['group']==g and x['left_source']==left and x['right_source']==right)
    names={'same_order':'유지','reversed':'반전','both_tie':'양쪽동률','one_tie':'한쪽동률','unscorable':'미확인(공통 판정분모 확보)'}
    def ordering(g):
        out=[]
        for label,right in [('주','primary'),('추가','secondary')]:
            a=source(g,'external_gold',right);b=source(g,'external_gold',right+'_row_valid')
            out.append(f"{label}: 실체풀 {names.get(a['status'],a['status'])} / 행유효 {names.get(b['status'],b['status'])} (공통 {a['common_questions']}문항)")
        return '; '.join(out)
    original=sum(x['cohort']=='011' and x['input_mode']=='original' for x in meta)
    summary=sum(x['cohort']=='011' and x['input_mode']=='summary' for x in meta)
    new=sum(x['cohort']=='new' for x in meta)
    r1=[]
    for c in ['A','P']:
        co=[x for x in obs if x['condition']==c];unknown=sum(x['claims_unknown'] for x in co)
        recall=m('gold_recall_at10_macro');n=m('current_N_per_output');slots=m('current_N_per10slots')
        r1.append([c,f'{len(co)} ({original}·{summary}·{new})',rate(m('grade2_hit_at10'),c),f"{number(recall[c])} (macro, {recall['questions']}문항)",
          f"{number(m('first_related_rank_median')[c],1)} ({len(co)}문항; 무적중=11)",f"{rate(n,c)}; {slots['numerator_'+c]}/{slots['denominator_'+c]} 슬롯",
          rate(m('strict_N_correct_reject'),c),rate(m('positive_false_reject'),c),rate(m('claim_error'),c),
          f"{number(m('queries_mean')[c],2)}·{number(m('normalized_opens_mean')[c],2)} ({len(co)}실행)",
          f"주장 {unknown}/{sum(x['sampled_claims'] for x in co)}; 현재 N 범위 {sum(x['historical_N_scope_unknown'] for x in co)}행; 역사 사실은 별도"])
    r2=[]
    for cohort,scope,i5,must in itertools.product(['011','new'],['whole','part'],['absent','present'],[False,True]):
        g=f'stratum:{cohort}/{scope}/{i5}/{must}';rr=m('gold_recall_at10_macro',g);nr=m('strict_N_correct_reject',g);er=m('claim_error',g)
        def cell(c):return f"R {number(rr[c])} (n={rr['questions']}); N {rate(nr,c)}; E {rate(er,c)}"
        selected=[x for x in obs if x['cohort']==cohort and x['whole_or_part']==scope and x['I5']==i5 and x['must_present']==must]
        u={c:sum(x['claims_unknown'] for x in selected if x['condition']==c) for c in ['A','P']}
        label=f"{'011' if cohort=='011' else '새 질문'} × {'전체' if scope=='whole' else '부분'} × I5 {'유' if i5=='present' else '무'} × must {'유' if must else '무'}"
        r2.append([label,rr['group_questions'],cell('A'),cell('P'),f"R {change(rr)}; N {change(nr)}; E {change(er)}",ordering(g),
          '미확인(빈 층의 질문 확보)' if not rr['group_questions'] else f"확인불가 주장 A {u['A']} / P {u['P']}; "+('n<5, 독립 추가 표본 필요' if rr['group_questions']<5 else '모델 반복·사람 시간 미측정')])
    type_names={'price':'가격','license':'라이선스','offline':'오프라인','self_hosting':'자체 호스팅','platform':'플랫폼','feature':'특정 기능','other':'기타 사실'}
    err_names={'outdated_information':'오래된 정보','product_confusion':'제품 혼동','version_or_plan_scope_omission':'버전·요금제 범위 누락','unsupported_generalization':'근거 없는 일반화'}
    r3=[]
    for typ,tn in type_names.items():
        for c in ['A','P']:
            rows=[x for x in claims if x['condition']==c and x['claim_type']==typ];vc=collections.Counter(verdict(x['verdict']) for x in rows);bad=[x for x in rows if verdict(x['verdict'])=='false']
            errors=collections.Counter(str(x.get('error_type')) for x in bad)
            mainerr='; '.join(f'{err_names.get(k,k)} {v}' for k,v in errors.most_common()) if bad else '관측된 거짓 없음' if rows else '미확인(해당 유형 표집 없음)'
            ex='; '.join(f"{x['qid']}·{x['candidate']} ({x['id']})" for x in bad[:2]) if bad else '해당 없음(거짓 관측 없음)' if rows else '미확인(표집 추가)'
            r3.append([tn,c,len(rows),vc['true'],vc['false'],vc['unknown'],mainerr,ex,'현재 공식 자료 기준; '+(f"{vc['unknown']}건은 범위/접근/실행 확인 필요" if vc['unknown'] else '역사 시점으로 소급하지 않음')])
    criteria={r['criterion']:r for r in h1['criteria']};r4=[]
    definitions=[('C1','strict_N_correct_reject','P−A ≥0.20: 심은 N 올바른 거절률','공식 문서·검사 버전/필수조건의 범위가 틀리거나 이유 감사가 바뀔 때','독립적으로 재확인한 N만 사용한 민감도도 병기'),
      ('C2','gold_recall_at10_macro','P−A ≥−0.05: 알려진 관련 답 macro recall@10','외부 답 목록 누락·후속 조건 변경·실체 매핑이 차등 영향을 줄 때',ordering('all')),
      ('C3','claim_error','P 오류율 < A: 거짓/(참+거짓)','현재 공식 문서의 범위가 잘못 대조되거나 확인불가의 실제 진위가 차등적일 때','확인불가 포함 하한·상한과 현재/역사 구분'),
      ('C4_aux','positive_false_reject','보조: 관련 후보 거절률 P−A ≤0.05','관련/채택 기록이 최초 필수조건 충족을 보장하지 않을 때','변경 채택4문항·절차형 T054 제외 민감도')]
    for key,metric,title,wrong,sensitivity in definitions:
        r=m(metric);v=criteria[key];met='판단불가' if v['met'] is None else '충족(점추정 기준)' if v['met'] else '미충족(점추정 기준)'
        ac=number(r['A']) if metric=='gold_recall_at10_macro' else rate(r,'A');pc=number(r['P']) if metric=='gold_recall_at10_macro' else rate(r,'P')
        r4.append([f'{key}: {title}',f'A {ac}; P {pc}; Δ {change(r)}',met,sensitivity,wrong,'95% 구간은 고정 표본의 질문 대응 재표집; 사람 검토 시간 미확인'])
    text=['## §1 필수 결과 표','',
      '현재 웹 실행·검증의 관측 창은 원 실행/판정 파일의 실제 UTC다. 외부 gold는 실행 전 동결한 실제 답 기록에 작업자가 규칙을 적용한 값이며, 주·추가 판정은 내부 별도 모델 검토다. 원문/요약·분모·역사/현재를 혼합하지 않는다. 아래 Δ는 P−A이고, 95% 구간은 질문 대응 군집 bootstrap10,000회(seed18018)의 조건부 percentile 구간이다.','',
      '### 표 1 — 조건별 지표','',table(1,r1),'',
      'recall은 알려진 외부 정답 회수이며 정답 밖 후보의 무관률이 아니다. N/상위10은 외부 N과 실체가 일치하고 현재 적용 범위가 확인된 행의 보수적 계수다. 새 질문20개에는 원문9개·요약11개가 포함된다. 오류율 분모는 참+거짓, 확인불가는 별도다. 검색·열람은 실제 사용량이며 동일 상한과 실제 동일 지출은 구별한다.','',
      '### 표 2 — 층별 비교','',
      'R=외부 gold macro recall@10, N=심은 엄격N의 이유까지 맞은 거절률, E=현재 확인가능 주장 오류율. Δ와 구간은 비율 척도이며 0.20은20%p다. 판정 출처 순서는 R에 대응하는 외부 known-gold 대 내부 발견후보 풀 recall로 비교한다. 실체풀과 각 조건 자신의 관련 행만 인정한 행유효 민감도를 함께 썼다. 빈 층은 결과0이 아니며 n<5의 좁은/퇴화 구간도 안정된 모집단 효과가 아니다.','',table(2,r2),'',
      '### 표 3 — 주장 정확성','',
      '전수 추출 원장에서 seed18018로 조건별80개를 먼저 동결했다. 모든 값은 표집한 원자적 주장 수이며 동일 질문 안 주장의 독립성을 가정하지 않는다. 오류 유형은 가능한 주된 형태의 분류로, 모델 내부 오류 원인을 직접 관측한 것은 아니다.','',table(3,r3),'',
      '### 표 4 — H1 판정','',table(4,r4),'',
      'C1–C3의 사전 점추정 기준을 그대로 적용한다. C4는 보조 기준이다. 신뢰구간·판정 출처 역전·확인불가 민감도는 강한 해석을 제한하며 사전 임계값을 변경하지 않는다.','']
    (ROOT/'analysis/result-tables.md').write_text('\n'.join(text)+'\n')
    print(json.dumps({'table_rows':{'1':len(r1),'2':len(r2),'3':len(r3),'4':len(r4)},'output':'analysis/result-tables.md'}))

if __name__=='__main__':main()
