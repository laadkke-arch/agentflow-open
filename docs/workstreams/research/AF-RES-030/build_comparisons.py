#!/usr/bin/env python3
"""Add outcomes to presealed pairs in a separate CSV; never rewrite comparisons.csv."""
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parent
initial={r['case_id']:r for r in map(json.loads,(P/'initial.jsonl').read_text().splitlines())}
chains={r['case_id']:r for r in map(json.loads,(P/'chains.jsonl').read_text().splitlines())}
notes={
 'M01':('M-P01/M-P02; NumPy1.24의 범위밖 정수변환 경고는 기술 가설을 지지. wx 사용 성공의 판별 근거는 공급자 PR24869뿐.', 'NumPy colormap 경고 대 wx toolbar 배치. 정보5/4; 같은 bug 층이지만 입력/사용/난도가 다름.', 'M01: 지원자가 재현 가능으로 바뀜, 원작성자 새 실행 없음. M02: 공급자 구현, 원작성자 후속 없음.', '누락된 원작성자 재실행·질문 없이 같은 버전을 진단한 동등 사례가 나오면 관측 해석이 달라짐. 전략 효과 미확인.'),
 'M03':('M-P03 및 M-P03-SOURCE: 수동 addfont 등록의 세션 간 영속성은 보장되지 않음; cache 구조는 공식판 소스로 제한 확인.', '동일 분기·종류·정보차<=1의 즉답/조건부 사례가 없음.', '후보 fit 거절 뒤 다른 지원자의 cache 설명과 작성자 삭제 실행. 부분목표 성공.', '정보질문과 후보평가를 합치면 분모가 달라진다. 같은 지원자 연결·매 새 세션 영속성 미확인.'),
 'M07':('M-P07/M-P09/M-P10: seaborn 범례 생성과 move_legend; ncols setter 존재만으로 live 재배치를 보장할 수 없음.', '동일 분기·종류의 적합한 즉답/조건부 대조 없음.', '원작성자 질문 답0. 후발 Seaborn 공급자 설명은 별도 주체.', '원작성자 실제 범례 조정 코드/출력이 확보되면 사용 판정을 바꿀 수 있음.'),
 'M08':('M-P08: GUI 이벤트루프/툴킷 통합 원칙. M-P06: pandas.clear 정적 코드.', '같은 bug·정보5/5이나 Tk/macOS 혼합과 pandas 순서 문제. M06 root EDIT 미래정보 노출.', 'M08 새 축소코드도 실패. M06 예제 편집과 pandas 신고 계획; 성공 실행 없음.', '정확한 macOS/backend 재현시험·M06 원판이 필요. 실패 대 미보고를 전략 우열로 볼 수 없음.'),
 'X04':('XD01/XD02: 당시 Dataset→dask DataFrame 계약. XD05: backend 안내는 뒤판 자료이므로 1월 설치 보장에 쓰지 않음.', '같은 feature·정보3/3. GeoTIFF metadata/intake 대 DataArray→Series라는 다른 목적, 실제 설치판 일부 미확인.', 'X04 rasterio 직접 열기 부분성공 후 같은 후보 설명 추가. X03 문서 안내 후 목적 보충, 실행 없음.', 'X04 성공은 답에 포함된 새 실행이며 기존값 직접답 아님. 전체 metadata 보존·동일 데이터 X03 실행 없으면 효과 비교 불가.'),
 'X07':('XD04: 좌표가 있지만 index가 없는 조건의 기존 오류분기를 확인.', '같은 층 즉답/조건부 대조 없음. 유지관리자 requester에게 초보 기여자가 뜻을 물은 역할 역전.', '유지관리자가 pure-xarray 최소 예제 목적을 설명. 원작성자 새 실행 없음.', '유지관리자 제외시 이 직접답이 빠진다. 이후 제3자 repro를 작성자 실행으로 옮기면 오류.'),
 'D02':('DP05: 신고자가 지정한 BufferManager 판의 예약/퇴거/롤백 경로. DP06: lambda 미지원 예외 공급자 결정.', '같은 bug 층·정보5/4이나 동시 메모리 처리 대 binder lambda. D01은 이미 미래정보 노출.', 'D02 실제 OOM+추가 다중 query 논거에 설명 수정, 첫 구체 설계 제안. D01 공급자 미지원 처리; 작성자 재실행 없음.', '물은 경험값과 자발적인 다중 query 논거의 기여를 분리할 자료 없음. 전 제안 부재이므로 엄격 변경0.'),
 'D05':('DP02: ICU 수정 코드/기대시험은 공급자 변경. D07 당시 NumPy 변환 계약은 미확인.', '같은 bug·정보5/5이지만 SQL 시간대/interval 대 Python NaN/MaskedArray. 대조 후보 D08은 더 멀어 선정하지 않음.', 'D05 작성자 시간대 답0, 공급자 추정. D07 첫 설명 뒤 작성자 후속0.', '관측 무응답과 만족을 혼동할 수 없음. 다른 후보 D08의 성공을 보고 대조를 교체하면 결과선정 편향.')
}
rows=[]
for pair in csv.DictReader((P/'comparisons.csv').open()):
 cid=pair['question_case']; control=pair['comparison_case']; x=chains[cid]; y=chains.get(control)
 official,difference,follow,limit=notes[cid]
 r={**pair,'provider_support':official,'version_goal_information_difference':difference,
    'actual_followup':follow,'overturning_condition_or_unknown':limit,
    'question_root30_direct_answer':x['root30']['same_variable_answer'],
    'question_root30_success':x['root30']['new_execution_success'],
    'question_root30_failure':x['root30']['new_execution_failure'],
    'control_root30_success':y['root30']['new_execution_success'] if y else '해당 없음',
    'control_root30_failure':y['root30']['new_execution_failure'] if y else '해당 없음',
    'question_strict_roundtrips':x['root30']['strict_answer_roundtrips'],
    'question_reply_roundtrips':x['root30']['any_author_reply_roundtrips'],
    'question_wait_hours':json.dumps(x['root30']['strict_wait_hours']),
    'click_reading_counterfactual_labor':'미확인: 독립 로그 없음',
    'post_outcome_fields_start':'provider_support; frozen selection fields retained unchanged'}
 r['outcomes']='post-seal observed reports only'
 rows.append(r)
with (P/'comparison-results.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
print(json.dumps({'pairs':len(rows),'matched':sum(r['comparison_case']!='해당 없음' for r in rows),'unmatched':sum(r['comparison_case']=='해당 없음' for r in rows)}))
