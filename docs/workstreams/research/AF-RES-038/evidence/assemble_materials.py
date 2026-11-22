"""Assemble owned research materials; no network, participants, or effect estimates."""
from pathlib import Path
import csv
import json
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[1]

def write_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

all_sources = []
for stream in ('pandas', 'numpy', 'methods'):
    for line in (BASE / 'streams' / stream / 'sources.jsonl').read_text().splitlines():
        if line.strip():
            row = json.loads(line)
            row['reading_stream'] = stream
            if row['source_id'] == 'P-S14':
                row['stream_original_counted'] = row['counted']
                row['counted'] = False
                row['count_exclusion'] = '보수적 통합: 같은 PDEP 및 날짜 테스트 개정이 포함된 merge를 별도 고유 원문 최소수에 다시 넣지 않는다. 후속 결정의 내용 근거는 보존한다.'
            all_sources.append(row)
for line in (BASE / 'evidence/root-rereads.jsonl').read_text().splitlines():
    old = json.loads(line)
    matching = next((s for s in all_sources if old['url'] in (s.get('original_url'), s.get('pinned_url_or_version'))), None)
    row = {'source_id': old['event_id'], 'original_url': old['url'], 'pinned_url_or_version': old['url'],
           'publisher': matching['publisher'] if matching else 'pandas official website (failed path)',
           'published_or_event_date': matching['published_or_event_date'] if matching else '미확인',
           'checked_utc': old['checked_utc'], 'recorded_utc': old['recorded_utc'], 'time_precision': old['time_precision'],
           'locator': old['locator'], 'source_kind': 'duplicate_root_reread' if matching else 'access_failure',
           'verified_fact': old['verified_fact'], 'limitation': old['limitation'], 'question_ids': ['Q1','Q3','Q4'],
           'case_ids': [old['event_id'].split('-')[1] if '-' in old['event_id'] else 'P02'],
           'duplicate_group': matching['duplicate_group'] if matching else old['event_id'],
           'counted': False, 'reading_stream': 'root', 'method': old['method']}
    all_sources.append(row)
(BASE / 'sources.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in all_sources))

frame_rows = []
fieldnames = ['frame_id', 'registry', 'order']
for stream in ('pandas', 'numpy'):
    with (BASE / 'streams' / stream / 'frame.csv').open(newline='') as f:
        reader = csv.DictReader(f)
        for field in reader.fieldnames:
            if field not in fieldnames:
                fieldnames.append(field)
        frame_rows.extend(list(reader))
for field in ('stream_eligibility','root_disposition','strict_readiness_limit'):
    fieldnames.append(field)
for row in frame_rows:
    cid = row['frame_id']
    if cid in ('P02','P04','P06','N08'):
        row['stream_eligibility'] = row['eligibility']
        row['case_id'] = cid
        row['eligibility'] = 'selected_document_task_conditional'
        row['root_disposition'] = '최초 복구 요구·당대 기전 근거 둘로 내용 과제 선정. 실행·사람 검증 미실시.'
        limits = {'P02':'POC 실제 build와 transitive @main 의존 closure 미확인',
                  'P04':'역사적 API 실행 미실시; infer-once strict도 허용',
                  'P06':'native guard는 공식 내부기전 기반 구성 설계; 공식 완성 소비자 recipe 아님',
                  'N08':'formal 본문 절대 최초 공개시각 미확인. 작은 집계흐름으로만 전체 분류'}
        row['strict_readiness_limit'] = limits[cid]
with (BASE / 'frame.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    writer.writerows(frame_rows)

pandas = json.loads((BASE / 'streams/pandas/cases.json').read_text())
drafts = json.loads((BASE / 'streams/pandas/packet-drafts.json').read_text())['cases']
numpy = json.loads((BASE / 'streams/numpy/cases.json').read_text())
write_json(BASE / 'casebook.json', {'audience': 'RESEARCHER_ONLY_RAW_STREAM_DESIGNS', 'snapshot_note':'stream 최초 설계와 예상 판독을 보존한다. 조정 뒤 권위 있는 요구 판정은 rubric.csv 및 examples.jsonl의 original/observed/adjudication을 함께 읽는다.', 'pandas': pandas, 'numpy': numpy})

common = '''공개 인터넷 검색, 실행 도구, 도움 요청 규칙, 교육과 작업 예산은 모든 보기에서 같습니다. 진행자가 사전에 공통 공지한 예산·재검 간격·도구 정책을 적용하세요. 첫 채택을 선언할 때 결정 ID와 제출판을 고정하세요. 찾은 자료와 사전 인지를 기록하고, 실행하지 않은 결과는 미확인으로 적으세요. 후대 자료를 발견했다면 URL·판·첫 노출을 기록하세요. 이 과제는 문서·의사코드의 요구 합치성을 판독하며, 실행하지 않은 성공을 요구하지 않습니다.'''
arm_intro = '# 자료\n\n이 파일은 배정된 보기의 추가 자료입니다. 공통 과제와 환경은 t0 문서를 따릅니다.\n\n'
arm_a = arm_intro + '공개 인터넷에서 자유롭게 검색하세요. 추가 선별 링크는 제공되지 않습니다.\n'
distribution = {'status': 'CONTENT_REVIEW_KIT_NOT_A_HUMAN_RUN', 'public_repository_is_not_participant_delivery': True,
                'release_gate': 'forms/run-config.json의 미합의 값과 독립 사람 채점 검토를 후속에서 확정',
                't0_delivery': {}, 't1_delivery': {},
                'forbidden_to_bundle': ['sources.jsonl', 'frame.csv', 'casebook.json', 'rubric.csv', 'examples.jsonl', 'RESULT.md', 'SELF_CHECK.md', 'evidence/', 'streams/'],
                'access_rule': '개별 파일만 전달. t1은 공통 예약시점에 모든 동의 유지 배정자에게 제공. A/B/C 검색·실행·교육·지원·예산은 동일.'}

for case_id, draft in drafts.items():
    p = BASE / 'packets' / case_id
    p.mkdir(parents=True, exist_ok=True)
    paragraphs = draft['t0'].split('\n\n')
    paragraphs[1] = common
    t0_text = '\n\n'.join(paragraphs).rstrip() + '\n'
    t1_text = draft['t1'].rstrip() + '\n'
    if case_id == 'P02':
        t0_text = t0_text.replace('컴파일 graph의 관리와 Python metadata/배포 산출 책임을 구분하는 구조를 제안하세요.', '컴파일 대상·의존·생성 규칙을 명시적인 빌드 graph 또는 동등한 구조로 분리하고, Python metadata/배포 산출 책임과의 경계를 제안하세요. 파일 이름이나 파일 개수 자체는 평가 기준이 아닙니다.')
        t1_text = t1_text.replace('선언 graph에 native target과 dependency가 하나 더 생긴다고 할 때 어느 책임 영역을 바꾸나요? 컴파일 로직을 단일 setup 스크립트에 계속 쌓는 구조인지 확인하세요.', 't0 구조에서 native target과 dependency를 표현하는 책임 영역을 추적하세요. target 하나를 더 선언한다고 가정해 그 경계를 설명하되 실제 새 기능을 구현할 필요는 없습니다. 컴파일 graph의 관리와 packaging 책임이 분리되는지 확인하세요. 파일 이름이나 파일 수는 합격 기준이 아닙니다.')
    if case_id == 'P06':
        t0_text = t0_text.replace('이 literal 집합 밖의 NA/NaN, overflow, bool, vector/slice 대입과 전체 API는 별도 범위입니다.', '검사 범위는 작은 수의 scalar 정수·정수값 float·fractional float와 부적합 text입니다. NA/NaN, overflow, bool, vector/slice 대입과 전체 API는 별도 범위입니다.')
    (p / 't0.md').write_text(t0_text)
    (p / 't1.md').write_text(t1_text)
    (p / 'arm-A.md').write_text(arm_a)
    for arm in ('B', 'C'):
        text = draft['arm_' + arm].replace('# 선별 자료', '# 자료', 1)
        if case_id == 'P04' and arm == 'C':
            text = text.replace('날짜 순서 선호나 추론 옵션과 명시 format의 보증은 같지 않으며', '이 판의 dayfirst 또는 infer_datetime_format 옵션과 명시 format의 보증은 같지 않으며')
        (p / f'arm-{arm}.md').write_text(text.rstrip() + '\n')

def record_table(rows):
    cols = ['row_id','year','month','day','time','store','SKU','number']
    return '\n'.join(['| ' + ' | '.join(cols) + ' |', '| ' + ' | '.join(['---']*len(cols)) + ' |'] +
                     ['| ' + ' | '.join(str(r[c]) for c in cols) + ' |' for r in rows])

p = BASE / 'packets/N08'
p.mkdir(parents=True, exist_ok=True)
reqs = '\n'.join('- ' + r['id'] + ': ' + r['requirement'] for r in numpy['requirements'])
t0 = f'''# N08 · 구매기록 집계 흐름 · t0

{common}

## 상황과 최초 요구

{numpy['participant_common']}

계획 기준은 2010-04-27 작성, 2010-04-29 저장소에 추가된 공개 문서판입니다. 이 과제는 작은 집계 흐름을 설계하며 새 API 도입 정책 전체를 결정하지 않습니다.

{reqs}

{numpy['input_contract']}

## 입력

{record_table(numpy['t0']['records'])}

## 제출

선택한 처리 흐름과 대안 하나, 세 grouping의 키, 원행 배정 방법, 네 통계를 내는 의사코드 또는 동등한 설명, 세 결과표를 제출하세요. 원문 URL·절과 적용 한계, 실행 여부를 함께 적으세요. 첫 채택 선언과 제출판을 고정하고 D-N08-KEY / D-N08-MEMBERSHIP / D-N08-REDUCTION 결정 ID로 연결하세요. 분수 평균 표기도 허용합니다.
'''
(p / 't0.md').write_text(t0)
(p / 't1.md').write_text(f'''# N08 · 동일 요구 재검 · t1

{numpy['t1']['prompt']}

N08-R1은 세 grouping의 키와 결과 라벨, N08-R2는 각 관측 그룹의 네 통계, N08-R3은 원행의 키와 수량 대응을 확인합니다. 원래 단일년·비결측·관측 그룹 범위는 그대로입니다.

## 재검 입력

{record_table(numpy['t1']['records'])}

각 요구에 유지 / 수정 필요 / 미확인과 근거를 적으세요. 수정하면 D-N08-KEY / D-N08-MEMBERSHIP / D-N08-REDUCTION 중 되돌린 결정과 같은 원래 요구 ID, 새 제출판, 수정 활동을 연결하세요. 첫 제출판을 덮어쓰지 마세요. 새로운 빈 그룹·결측·연도경계 조건은 별도 제안으로 표시하며 이번 원요구 재작업에 넣지 않습니다.
''')
(p / 'arm-A.md').write_text(arm_a)
for arm in ('B', 'C'):
    text = arm_intro
    for card in numpy['cards']:
        text += f"{card['rank']}. [{card['title']}]({card['url']})\n\n"
        if arm == 'C':
            text += '   ' + card['explanation'] + '\n\n'
    (p / f'arm-{arm}.md').write_text(text.rstrip() + '\n')

for case_id in ('P02', 'P04', 'P06', 'N08'):
    distribution['t0_delivery'][case_id] = {a: [f'packets/{case_id}/t0.md', f'packets/{case_id}/arm-{a}.md'] for a in ('A', 'B', 'C')}
    distribution['t1_delivery'][case_id] = [f'packets/{case_id}/t1.md']
write_json(BASE / 'distribution.json', distribution)
print(json.dumps({'sources_rows': len(all_sources), 'counted_rows': sum(r['counted'] for r in all_sources),
                  'counted_unique_groups': len({r['duplicate_group'] for r in all_sources if r['counted']}),
                  'frame_rows': len(frame_rows), 'participant_files': len(list((BASE/'packets').glob('*/*.md')))}, ensure_ascii=False))
