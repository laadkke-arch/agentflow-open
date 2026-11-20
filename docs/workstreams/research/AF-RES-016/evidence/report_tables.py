"""Render tables from frozen numerical and manually reviewed result artifacts."""
import json
from pathlib import Path
from collections import Counter
BASE=Path(__file__).resolve().parents[1]
def read(name):return json.loads((BASE/name).read_text())
def esc(s):return str(s).replace('|','\\|').replace('\n',' ')
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(map(esc,headers))+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(esc,r))+' |' for r in rows])
def pct(v):return f'{100*v:.2f}%'
def interval(v,digits=3):return '['+', '.join(f'{x:.{digits}f}' for x in v)+']'
def metrics_row(r):return [r.get('sample',r.get('stratum','')),r['scheme'],f"{r['agree']}/{r['n']}",pct(r['po']),interval([100*x for x in r['po_ci95']],2)+'%',f"{r['kappa']:.3f} {interval(r['kappa_ci95'])}",str(r['undefined_kappa_replicates'])]
T1_HEADERS=['분류안','표본(011·012·004)','단위 수','단순 일치율','kappa 또는 alpha(95% 구간)','주 불일치 유형','011 원래 값과 비교','미확인']
T2_HEADERS=['불일치 쌍 ID','역할 A','역할 B','A일 때 판정','B일 때 판정','판정 변화 여부','근거 위치','미확인']
T3_HEADERS=['작업','어휘','답하는 질문','대응 어휘(다른 작업)','같은 것으로 읽으면 안 되는 이유','근거 위치','미확인']
T4_HEADERS=['주장','근거 자료 주소','확인한 내용','반증 시도','미확인']
def t1_rows():
    g=read('evidence/agreement.json');d=read('coding/adjudication.json')['rows'];out=[]
    for scheme in ('S1','S2','S3'):
        for sample in ('011','012','004'):
            r=next(x for x in g['main'] if x['sample']==sample and x['scheme']==scheme)
            counts=Counter(x['primary_type'] for x in d if x['sample']==sample and scheme in x['different_axes'])
            desc='; '.join(f'{k} {v}/{r["n"]-r["agree"]}' for k,v in counts.most_common()) if counts else '불일치 0/18'
            cmp=(f"동일120 원66/120=55.00% 대비 {(r['po']-.55)*100:+.2f}pp; 원149는50.34%" if sample=='011' else '다른 표본; 011과 직접 차이 추정 안 함')
            missing={'011':'미확인(새 사람·새 스레드 재코딩)','012':'미확인(무작위 질의 연결36개를 실제 제안 문맥으로 재측정)','004':'미확인(새 문제에서 반복; 현 표본4문제의 구간은 탐색적)'}[sample]
            out.append([scheme+{'S1':' 후보 속성형','S2':' 문제 상대형','S3':' 두 축 결합'}[scheme],sample,r['n'],f"{r['agree']}/{r['n']} = {pct(r['po'])}",f"κ={r['kappa']:.3f} {interval(r['kappa_ci95'])}",desc,cmp,missing])
    return out
def role_string(x):return f"{x['S1']}; {x['S3']['form']} × {x['S2']}"
def judgment_string(x):
    hs='; '.join(f"{h['condition']}={h['status']}" for h in x['H']) or 'H: must 미제공/unclear'
    label=x['overall_004_label'] or '전체 판정 라벨 미부여'
    near={'known':'알려진 근접 오답','not_established':'N 미입증','not_claimed':'전체 충족 주장 없음'}[x['near_miss']]
    return f"{hs}; T={x['T']}; {label}; {near}"
def t2_rows():
    return [[r['unit_id'],role_string(r['role_a']),role_string(r['role_b']),judgment_string(r['judgment_a']),judgment_string(r['judgment_b']),'없음(고정 사용·같은 근거)',f"[impact.json](evidence/impact.json) rows {r['unit_id']}; [표본](sample/units.json); "+', '.join(x for x in r['evidence_locations'][3:]),'미확인('+r['minimum_next_check']+')'] for r in read('evidence/impact.json')['rows']]
def t1():return table(T1_HEADERS,t1_rows())
def t2():return table(T2_HEADERS,t2_rows())
