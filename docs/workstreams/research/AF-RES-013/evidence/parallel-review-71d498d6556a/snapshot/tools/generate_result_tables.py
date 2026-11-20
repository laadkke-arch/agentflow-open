"""Render the required tables from frozen cases and explicit judgments.

Only replaces RESULT section 1. Narrative conclusions in sections 2–5 remain
human-readable researcher synthesis and are not inferred from keyword matches.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ROLES=['같은 목적 완성품','재사용 부품','같은 분야의 다른 설계','다른 언어·생태계','다른 분야 원리','표준·논문']
T1=['사례 ID','계열','원문 주소(고정 판)','결정일','정답 항목 수(완성품·부품·같은 분야 설계·다른 생태계·다른 분야·표준논문)','기준선 A 적중','기준선 B 적중','놓친 정답 항목','정답원 밖 유용 후보','근접 오답','깨진·가짜 링크','누설·사후 자료','미확인']
T2=['역할','정답 항목 수(분모)','기준선 A 적중(비율)','기준선 B 적중(비율)','대표 놓침 사례 ID','미확인']
T3=['주장','근거 자료 주소','확인한 내용','반증 시도','미확인']

def read(name): return json.loads((ROOT/name).read_text())
def cell(x): return str(x).replace('|','&#124;').replace('\n',' ')
def table(cols,rows):
    return '\n'.join(['| '+' | '.join(cols)+' |','| '+' | '.join(['---']*len(cols))+' |']+['| '+' | '.join(cell(x) for x in row)+' |' for row in rows])
def rate(n,d): return f'{n}/{d} ({n/d:.1%})' if d else '0/0 (정의 불가)'

def main():
    agg=read('evidence/AGGREGATES.json'); cases=read('cases/CASES.json')['cases']
    assert not agg['pending'] and all(x['complete_all_cases'] for x in agg['baselines'].values())
    cm={c['id']:c for c in cases}; rows=[]
    for x in agg['cases']:
        c=cm[x['case_id']]; a=x['baselines']['A'];b=x['baselines']['B'];n=x['gold_count']
        ma=set(a['missed_identity']);mb=set(b['missed_identity']); names={g['id']:g['name'] for g in c['gold_items']}
        def misses(ids): return '; '.join(g.rsplit('-',1)[-1]+' '+names[g] for g in sorted(ids)) or '없음'
        missing='공통: '+misses(ma&mb)+' / A만: '+misses(ma-mb)+' / B만: '+misses(mb-ma)
        uncertainty=f"미확인(날짜 A{a['candidate_dates'].get('unknown',0)}·B{b['candidate_dates'].get('unknown',0)}행은 결정 전 고정 판 확인; 판정 불충분 A{a['insufficient']}·B{b['insufficient']}행은 JUDGMENTS가 연결한 상세 remaining_check 수행; 실제 사용효과는 대상 구현·설계자 평가)"
        label=c.get('canonical_id',c['id']); url=c.get('display_url',c['url'])
        rows.append([c['id'],c['family'],f'[{label}]({url})',c['decision_date'], '·'.join(str(x['roles'].get(r,0)) for r in ROLES),
            f"동일 {len(a['identity_hits'])}/{n}; 이전 {len(a['historical_hits'])}/{n}",
            f"동일 {len(b['identity_hits'])}/{n}; 이전 {len(b['historical_hits'])}/{n}", missing,
            f"A {a['nongold_useful']}/{a['nongold_count']} (이전 {a['nongold_historical_useful']}); B {b['nongold_useful']}/{b['nongold_count']} (이전 {b['nongold_historical_useful']})",
            f"A {a['near_miss']}/{a['candidate_count']}; B {b['near_miss']}/{b['candidate_count']}",
            f"A {a['broken_or_fake']}/{a['candidate_count']}; B {b['broken_or_fake']}/{b['candidate_count']}",
            f"노출기록 A{a['exposure_records']}·B{b['exposure_records']}; 사후 후보 A{a['candidate_dates'].get('post_decision',0)}·B{b['candidate_dates'].get('post_decision',0)}",
            uncertainty])
    role_rows=[]
    for role in ROLES:
        x=agg['roles'][role]; n=x['gold_count'];a=x['baselines']['A'];b=x['baselines']['B']
        role_rows.append([role,n,'동일 '+rate(a['identity_hits'],n)+'; 이전 '+rate(a['historical_hits'],n),
            '동일 '+rate(b['identity_hits'],n)+'; 이전 '+rate(b['historical_hits'],n),
            'A '+(', '.join(a['missed_identity_case_ids'][:5]) or '해당 없음')+'; B '+(', '.join(b['missed_identity_case_ids'][:5]) or '해당 없음'),
            '미확인(이 역할의 모집단 성능은 역할별 외부 표본을 추가하여 확인)' if n else '미확인(분모가 있는 별도 표본으로 해당 역할의 회수율 확인)'])
    A=agg['baselines']['A'];B=agg['baselines']['B'];U=agg['union'];D=agg['gold_items']
    prior='https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md'
    claims=[
      ['Q4: 고정 규칙에 따른 역할 정정 후 다른 분야 원리·구조 항목은 1/176(0.57%)이다.',
       '[사례와 최초 값](cases/CASES.json), [정정 근거](evidence/ROLE_CORRECTIONS.json), [내부 별도 검토](evidence/judgments/SECOND_REVIEW.json), [작동 원리 반례](https://www.rfc-editor.org/rfc/rfc8289.html)',
       'KEP 1/34, Python 0/73, Rust 0/39, Swift 0/30. C05의 문법 역할→event field 구조 차용이며 별도 언어학 문헌 인용은 없다. 해당 항목 A/B 회수는 모두0/1.',
       '최초0/176은 외부 인용을 필요조건처럼 본 과도한 코딩을 원문·변경 없는 규칙으로 정정한 값이다. 최초0/0 회수율은 정의 불가, PySizer까지 넓히면2/176·회수0/2. CoDel은 표본 밖, P433 sterile/C22 Atom은 용어 차용으로 분리한다.',
       '미확인(이 목적 표본 밖 빈도는 시기·분야별 층화 표본과 경계 재판정으로 확인)'],
      ['Q8: 반대 가설 A의 공식 기각 조건은 이번 결과만으로 판정할 수 없다.',
       f'[009 GAP §2·§3·§5]({prior}), [A 원 응답](runs/A/), [채점](JUDGMENTS.json)',
       f"A의 항목 동일성 {rate(A['identity_hit_count'],D)}, 결정 이전 근거 {rate(A['historical_hit_count'],D)}. 사전 지정한 새 절차·허용 오류·검토 시간과의 비교는 이번 실험에 없다.",
       '낮은 gold 회수가 별도 제품 필요라는 해석을 정답 밖 후보, 본문 내부 설계 비중, 코드검색 가용성, 노출 없는 부분집합으로 반박했다.',
       '미확인(실제 설계자가 새 절차와 기존 조합을 같은 과제·오류·시간 기준으로 비교)'],
      ['Q8: 반대 가설 B도 공식 기각 또는 채택의 대상 비교가 부족하다.',
       f'[009 GAP §3]({prior}), [B 원 응답](runs/B/), [집계](evidence/AGGREGATES.json)',
       f"B의 항목 동일성 {rate(B['identity_hit_count'],D)}, 결정 이전 근거 {rate(B['historical_hit_count'],D)}. 번역자는 새 문맥 내부 모델이며 사람 개발자 번역 실험이 아니다.",
       f"사후 A+B pool union은 동일 {U['identity_hits']}/{D}, 이전 {U['historical_hits']}/{D}이나 실제 통합 검색 실행이나 새 절차와의 대조로 취급하지 않는다.",
       '미확인(동일 목적·허용 오류·시간을 고정한 사람 번역 카탈로그와 새 절차 비교)'],
      ['정답원은 불완전하나, 더 나은 설계의 발견 건수로 환산할 수 없다.',
       '[C22 리뷰](https://github.com/rust-lang/rfcs/pull/123), [C28 결정 토론](https://forums.swift.org/t/accepted-se-0022-referencing-the-objective-c-selector-of-a-method/1194/1), [후보별 판정](JUDGMENTS.json)',
       f"본문 밖 리뷰 7항목 중 alias 1개를 빼면 2/31사례에서 6개 신규 항목, 확대 pool 182개다. 정답 밖 문서상 유용 후보는 A {A['nongold_useful']}/{A['nongold_candidates_judged']}, B {B['nongold_useful']}/{B['nongold_candidates_judged']}행이며 실제 우월성 입증은 0건이다.",
       'C23의 실제 bit/pointer 원문처럼 유용하지만 gold의 내부 선택과 다른 후보를 보존했다. H unknown·위반 후보는 유용 수에서 제외했다.',
       '미확인(남은 리뷰 전체와 풀 밖 후보를 확장 평가하고 설계자가 유용성·우월성을 확인)'],
      ['링크 검증 후 제출한 후보에서는 가짜·다른 대상 링크를 관측하지 않았다.',
       '[원 열람 기록](runs/), [URL 감사](evidence/RUN_AUDIT.json), [검증 보완](evidence/judgments/VERIFICATION.json)',
       f"A {A['broken_or_fake']}/{A['candidate_count']}, B {B['broken_or_fake']}/{B['candidate_count']}행. 실패·차단은 따로 보존했으며 403/timeout을 가짜로 세지 않는다.",
       'fragment·redirect·HTTP/HTTPS 차이를 실제 열람과 대조했다. 검색 단계에서 탈락한 링크와 최종 후보의 분모를 분리했다.',
       '미확인(검증 없는 생성 결과의 가짜율은 별도 조건의 반복 실험으로 확인)']]
    text='# AF-RES-013 — 설계 문서의 선행 사례·대안 기준선\n\n## §1 필수 결과 표\n\n### 표 1 — 사례별 결과\n\n'+table(T1,rows)+'\n\n### 표 2 — 역할별 집계\n\n'+table(T2,role_rows)+'\n\n### 표 3 — 주장 표\n\n'+table(T3,claims)+'\n\n'
    text+='''**읽는 법과 판정자.** 표의 정답 분절·역할은 작업자 코딩이다. 후보 판정은 작업자와 내부 별도 검토이며, `JUDGMENTS.json`의 각 행에 판정자를 적었다. 사람 또는 다른 모델 검토가 아니다. 모든 B 실행은 gold를 주지 않은 새 문맥의 내부 모델이 카탈로그를 번역한 조건이다. 실제 개발자의 번역 성능으로 부르지 않는다.

`동일`은 날짜와 별개로 특정 대상 또는 핵심 설계 선택을 회수한 서로 다른 정답 항목 수, `이전`은 그중 결정일 이전 근거가 확인된 항목 수다. `놓친`은 동일성 기준이며 공통·A만·B만으로 나눈다. G번호는 해당 사례의 gold ID 끝부분으로 `CASES.json`에 전체 이름·원문 위치가 있다. `정답원 밖 유용 후보`의 분모는 비정답 후보 행, `근접 오답`·`깨진·가짜 링크`의 분모는 제출 후보 행이다. 여러 후보가 한 정답을 가리켜도 한 번만 센다. 유용성은 문서로 뒷받침되는 제한된 참고 용도이며 실제 채택·실행 성공을 뜻하지 않는다.

노출기록은 원문·snippet·일반 기억 인식 등 실행자가 보존한 사건 수다. 모든 사건을 확정적인 정답 누설이라고 단정하지 않는다. 사후 후보와 날짜 미확인을 별도로 두며, 날짜 미확인을 역사적 실패 또는 사후 자료로 바꾸지 않는다. 표의 날짜는 사례마다 수락·병합·거절·초안 교체 중 해당 결정 사건이며 구현 출시일과 다를 수 있다. 관측 창은 2026-11-20 UTC의 원 실행 로그, 사례당 상위 최대 15개 후보이며 실제 개수는 §2에 제시한다.

'''
    old=(ROOT/'RESULT.md').read_text() if (ROOT/'RESULT.md').exists() else ''
    marker='## §2 세부 질문별 답'
    if marker in old: text+=old[old.index(marker):]
    (ROOT/'RESULT.md').write_text(text)
    print(json.dumps({'case_rows':len(rows),'role_rows':len(role_rows),'claim_rows':len(claims),'narrative_preserved':marker in old}))

if __name__=='__main__':main()
