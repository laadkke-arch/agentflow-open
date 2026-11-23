"""Regenerate the two required tables from audited ledgers; preserve narrative."""
from pathlib import Path
import json
import sys

B = Path(__file__).resolve().parent
MARK = "<!-- END_REQUIRED_TABLES -->"
sources = {r['source_id']: r for r in map(json.loads, (B/'sources.jsonl').read_text().splitlines())}
out = json.loads((B/'evidence/outcome-ledger.json').read_text())
con = json.loads((B/'evidence/contrast-ledger.json').read_text())
def cell(v):
    return str(v).replace('|', '\\|').replace('\n', ' ')
def row(vs): return '| ' + ' | '.join(cell(v) for v in vs) + ' |'
def link(sid):
    s=sources[sid];return f"[{sid}]({s.get('fixed_version_url') or s['original_url']})"
def refs(r):
    return ' '.join(link(s) for s in r['source_ids']) + f"; {r.get('source_file') or '통합 정의'} / {r.get('source_row') or r.get('contrast_id')}"

first = [
 ['A01 · A · Ramos 등, SIGIR2020 · 사람 간, 무작위 절차 미보고',
  '항공 문서 검색·선택 후 quiz; T/TA/TAB 각 완료자50, 최초 배정 N 미확인',
  '같은 BM25 방법진술. Fig1(TAB)/Fig5(TA)의 query·첫2제목은 같음; Fig4(T)는 query·둘째 결과 다름. 실제 impression ID·순위 미확인(EU/예시 한정 관측)',
  'T 제목 / TA 초록 / TAB 초록+단어 기여 막대·hover 숫자. '+link('SW-S24')+' Fig1/4/5; '+link('SW-S31')+' SearchBar.js',
  'Cranfield query002 qrel25행 회수; −1·이진 relevance 기준 미확인. quiz키는 문서 권고 참값과 다름. '+link('SW-S34'),
  '고정 패키지 bookmark559/quiz459/exit67행. 같은 batch 익명 exit ID67 연결; 조건·150완료자 대응·최종 문서 노출 D 미확인. '+link('SW-S32'),
  'J3/JU: 신뢰·quiz 성과를 정오별 수락으로 전환 불가. HEAD의 지시/재시도/길이 차이가 당시 개입인지는 미확인'],
 ['A02 · A · Search Result Presentation for Non-Native Language Documents, IUI Companion2024 · 사람 안 과제/화면(정확 배정 미확인)',
  '비모국어 문서10개 중 관련 문서 선택; A–F 여섯 화면, N 미확인',
  '같은 예시 제목·저자·URL의 A–F를 실제 확인. 전체 후보10·순위·과제별 권고 대응표 미확인(EU)',
  'A 기본; B 번역 snippet; C/D 오른쪽 원어/번역 keyphrase; E/F 아래 원어/번역 keyphrase. '+link('SW-S28')+' 여섯 화면',
  '관련 문서 하나를 찾도록 요청; 유일한 정답인지·전문가/사전 key·복수정답 규칙 미확인',
  '저자 poster의 평균/요약만, 정식 본문403; 최종 선택 원행·결측 미확보',
  'J3/JU: 번역·정보량·배치가 함께 바뀜. poster를 정식 원논문 직접 읽음으로 계산하지 않음'],
 ['A03 · A · 미충원', '미실시 — 선정 연구 없음', '해당 없음 — 연구 없음', '해당 없음 — 연구 없음', '해당 없음 — 연구 없음', '미실시 — 연구 없음', '앞선 방법 접근 미확인 때문에 최초4개 복원 미완료; 음성 결과0이 아님'],
 ['A04 · A · 미충원', '미실시 — 선정 연구 없음', '해당 없음 — 연구 없음', '해당 없음 — 연구 없음', '해당 없음 — 연구 없음', '미실시 — 연구 없음', '다른 층/진단 연구로 빈자리를 메우지 않음'],
 ['B01 · B · Panigutti 등, CHI2022 · 사람 안 2과제, 순서 배정',
  '미래 MI 확률 초기/최종 추정; Dr.AI/Dr.XAI; 모집31−주의1−초기100 두 명=분석28',
  '권고 A=100은 모두 동일·맞음이라는 방법(E2). 서로 다른 유사 환자2명, item 동일성 EU; 연속 응답이라 후보 순위 해당 없음',
  '진단 dot·반사실 조건 강조·요약 규칙·hover. '+link('AD-M12')+' §3.3–3.5/Fig1–2; 캡션·본문만 판독, 픽셀 미확인',
  '두 환자 미래 MI 양성은 저자 진술; 독립 환자key 미확인. 위험확률 답의 이산 정답 규약 부재',
  'WOA 중앙값 .31 vs0만; 최종 F=100 정수 횟수 미확인. 오권고는 설계상0',
  'J3/J4: 절댓값 WOA/판단 변경 크기와 최종 수락은 다름. 오권고 거절 효과는 해당 없음; 다른 환자·hover 동시 변화'],
 ['B02 · B · Schemmer 등, IUI2023 · 사람 간 무작위',
  '호텔 리뷰 fake/genuine: 초기 답→AI→최종 답. 모집200−1=199; Control100/Feature99, 16시행/인',
  '32 pool에서 16개, TP/FP/TN/FN 각4라는 방법(E2); 조건별 itemID·완전 자극 쌍 미확인',
  'LIME 단어 강조와 같은 AI권고. '+link('RT-SCH-P')+' Fig5(PDF11): 초기/지원후 화면 쌍, control/feature 렌더쌍 아님',
  'Ott2011/2013: 고용된 허위 리뷰와 사이트에서 채집한 실제로 간주한 리뷰; 숙박 진위 독립검증 아님. '+link('RT-OTT11-P')+' '+link('RT-OTT13-P'),
  'Table3 RAIR/RSR·정확도 평균; 원응답 공동표 미확보. §6.3 no missing은 SEM 맥락',
  'J3: 초기 불일치 부분분모를 전체 정오수락 분모로 쓸 수 없음. v3 확인; 정정 VoR 전문 미확인'],
 ['B03 · B · Schoeffer 등, CHI2024 · 사람 간3군 무작위',
  'bio 직업 professor/teacher; N600 동수배정→계획200/군. baseline/task-relevant/gendered, 14판단/인',
  '같은14 bio·같은 binary 예측은 방법(E2); Fig1 두 설명의 같은 bio/권고만 관측. 실제로 서로 다른543/214특징 모델, F1 .87/.77',
  '단어 강조·색 있는 권고; baseline은 강조/색 없음. '+link('AD-M26')+' Fig1(PDF5), AppendixA/B; 모델확률은 화면 미표시',
  'BIOS 첫문장 직업명 추출·정규화, 이후 첫문장 제거. 선택14개 원ID 미확인; 실제 자격 검증 아님. '+link('AD-BIOS-P'),
  'Fig3/5 비율만. Table1 정8/오6과 그림 정권고 몫50%가 불일치; 포함/가중 규칙·원행 미확보',
  'J3: 분모를12로 추정하지 않음. EAAMO2023/arXiv 개정은 같은 계보이며 독립 연구로 추가 안 함'],
 ['B04 · B · Kayser 등, EMNLP2024 · 사람 안4블록, 순서 배정',
  'Xray finding: Not/Maybe/Definitely present; 포함85, 조건별20, None/SM/NLE/Combined',
  '같은80이미지·모델 권고, 조건별 균등 빈도/70% 정답은 방법(E2). 할당ID 미확인; 같은 모델을4개 모델처럼 표기',
  'GradCAM / 자연어 이유 / 둘 다 / 없음. '+link('AD-M30')+' Fig2·Fig15 화면 확인; 같은 None/Combined 쌍은 미확인',
  '3방사선 전문의가160사례 사전 채점, 그중80선정; Maybe+Definitely 양성. Not/Definitely 충돌 제외; 설명7점은 별도 변수',
  'Fig6 GLMM 예측률; 응답·배정·전문가 key 원행 미확보. 연결 GitHub는 README1개뿐',
  'J3-model: 계획1190/510을 관측 D로 쓰지 않음. NLE−None 오수락+6.3pp는 모형 기술차; 실제 읽기/원문 링크 효과 아님']
]

h1=['연구·층·배정 단위','원과제·조건 N','같은 후보·순위·권고의 증거','설명의 차이·원 자극 주소','정답 원천','최종 응답 원천·연결 수','가능한 해석·미확인']
h2=['연구·조건·대비','맞는/틀린 권고','배정·판정 가능·결측 분모','권고 수락 수/분모','최종 정답 수/분모','조건 간 차이·가능 범위','원행/저자 집계/미확인','근거 주소·표·열']
lines=['# AF-RES-058 · 같은 권고의 설명과 정오별 최종 선택 — PARTIAL','', '## 표 1. 여덟 고정 연구 자리','',row(h1),row(['---']*7)]
lines.extend(row(r) for r in first)
lines.extend(['','## 표 2. 조건별 정오층·대비·결측 원장','',row(h2),row(['---']*8)])
primary_out=[r for r in out if r['stratum'] in 'AB']
primary_con=[r for r in con if r['stratum'] in 'AB']
for case in ('A01','A02','A03','A04','B01','B02','B03','B04'):
    rows=[r for r in primary_out if r['case_id']==case]
    for r in rows:
        if r['row_type']!='outcome': continue
        g=r['advice_truth'];gl='맞는 권고' if g=='correct' else '틀린 권고'
        if case in ('A03','A04'):
            lines.append(row([f"{case} · 미실시 ({r['record_id']})",gl,'해당 없음 — 연구 없음','해당 없음','해당 없음','해당 없음','미실시','[frame.csv](frame.csv); SCOPE §2']))
            continue
        people = '완료50/군; 배정N 미확인' if case=='A01' else '사람N 미확인' if case=='A02' else '모집31/분석28, 사람 안' if case=='B01' else f"분석{r['analyzed_people']}명" if case=='B02' else '계획200/군; 실제군N 미확인' if case=='B03' else '포함85, 사람 안'
        plan = f"계획D={r['planned_D']}; " if r['planned_D'] is not None else ''
        den=f"{people}; {plan}판정D·결측m 미확인"
        ac='미확인/미확인';fc='미확인/미확인';delta='미확인 — 자료가 주는 범위 없음'
        if case=='B01' and g=='wrong':
            den='설계상 오권고0; 관측응답 분모라는 뜻 아님';ac=fc='해당 없음 — 설계상0';delta='해당 없음 — 비교할 오권고 없음'
        elif case=='B01':
            fc='원 이산 정답 종점 부재';delta='WOA 중앙값은 수락 비율 아님'
        elif case=='B02': delta='RAIR/RSR 부분분모와 구별; 조건차 미확인'
        elif case=='B03': delta='그림 분모 충돌; 원개수·범위 미확인'
        elif case=='B04':
            delta=f"참고 모형 수락{r['model_acceptance_percent']}%, 정확도{r['model_accuracy_percent']}%; 원개수 아님"
        lines.append(row([f"{case} · {r['condition']} ({r['record_id']})",gl,den,ac,fc,delta,r['grade']+'; 원분자/분모 미확인',refs(r)]))
    for r in [x for x in primary_con if x['case_id']==case]:
        g=r['advice_truth'];gl='맞는 권고' if g=='correct' else '틀린 권고' if g=='wrong' else '맞는 권고만·별도 WOA'
        sub=' / 높은 설명품질 하위군' if r.get('subgroup') else ''
        d='미확인 — 공통 판정 분모 미확인';delta='미확인 — 원개수 차이·자료 기반 범위 없음'
        if r['delta_accept_pp_model'] is not None:delta=f"모형 기술차 {r['delta_accept_pp_model']:+g}pp; 원개수 차이 아님"+('; 분할 기준 다름·동일 항목 구성 미확인/BH 유의표시 소실' if r.get('subgroup') else '; 새 유의성 주장 없음')
        ac='미확인 (양 조건 A/D)';fc='미확인 (양 조건 C/D)'
        if case=='B01' and g=='wrong':d='해당 없음 — 설계상 오권고0';delta='해당 없음';ac=fc='해당 없음 — 설계상0'
        if r.get('alternate_metric'):delta='WOA 중앙값 .31−0=.31; 수락률 차이 아님'
        lines.append(row([f"{case} · {r['intervention']}−{r['control']}{sub} ({r['contrast_id']})",gl,d,ac,fc,delta,str(r['grade']),refs(r)]))
    for r in rows:
        if r['row_type']!='missingness':continue
        if case in ('A03','A04'):
            lines.append(row([f"{case} · 결측 ({r['record_id']})",'미실시','해당 없음 — 연구 없음','해당 없음','해당 없음','해당 없음','미실시','[frame.csv](frame.csv)']))
            continue
        d='원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함'
        if case=='A01':d+=';150−67을 결측으로 계산 안 함'
        if case=='B01':d='저자 사람 제외3(주의1/초기일치2); 원시행 결측·정오별 배분 미확인'
        if case=='B02':d='Feature 사람 제외1; SEM자료 결측0 저자진술과 원배정 응답 결측 미확인을 구별'
        if case=='B04':d+='; 시간분석만 제외5.1%를 여기 전용 안 함'
        lines.append(row([f"{case} · {r['condition']} 결측 ({r['record_id']})",'정오 미배분',d,'미확인','미확인','m 미확인으로 보완 범위 미계산','결측 원행 미확보',refs(r)]))

path=B/'RESULT.md'
text=path.read_text() if path.exists() else MARK+'\n'
assert MARK in text
narrative=text.split(MARK,1)[1]
expected='\n'.join(lines)+'\n\n'+MARK+narrative
if '--check' in sys.argv:
    assert path.read_text()==expected, 'RESULT required tables differ from current ledgers/generator'
else:
    path.write_text(expected)
print(json.dumps({'table1_rows':len(first),'table2_outcomes':sum(r['row_type']=='outcome' for r in primary_out),'table2_contrasts':len(primary_con),'table2_missing':sum(r['row_type']=='missingness' for r in primary_out)},ensure_ascii=False))
