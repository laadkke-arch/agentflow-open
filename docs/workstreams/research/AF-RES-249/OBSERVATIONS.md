| 과제·조건 | 링크 공개 전 산출물 | 공개·사용·교체 근거 | 독립 품질·인수 기준 | 분모·결측 | 설계 근거 URL |
|---|---|---|---|---|---|
| A-E | 중립 자유회상, runs 설계/코드, t0 seal | 0분 A1/A2, viewport/open/explain/try/same actor diff, t12−·t24 | A0–A6, 원본 불변, 독립 검수·인수 hash | 예정 12, 1기6; 실제0; 결측 아직 적용 전 | https://docs.python.org/3.12/library/itertools.html#itertools.groupby ; https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf |
| A-L | 동일 요구·seal | 12분 직전 동결 후 동일 카드; 자력 검색·스니펫 별도; 동일 actor diff | 동일 A 벡터/인수 | 예정12, 1기6; 실제0 | https://docs.python.org/3.12/library/collections.html#collections.Counter ; https://pmc.ncbi.nlm.nih.gov/articles/PMC6667942/ |
| B-E | 중립 회상, insertion_index 설계/코드 t0 seal | 0분 B1/B2 제공; 동일 페이지에서 두 후보 보일 수 있음; t12−·t24 | B0–B7, 동률 뒤, 빈 입력, no mutation; 독립 인수 | 예정12, 1기6; 실제0 | https://docs.python.org/3.12/library/bisect.html ; https://web.cs.ucla.edu/~miryung/Publications/icse2019-examplestack.pdf |
| B-L | 동일 | 12분 직전 freeze, 카드 제공; 오염/자력 검색 유지 | 동일 B 벡터/인수 | 예정12, 1기6; 실제0 | https://github.com/python/cpython/blob/v3.12.0/Lib/test/test_bisect.py ; https://pmc.ncbi.nlm.nih.gov/articles/PMC2844943/ |

표 1: 한 행=과제×정책 조건, 총 4행. 예정 48 배정, 24명(1기 24, 각 cell 6). 배정 전이라 예정 좌석 미배정, 실제 로그 0. 실제 결측률은 정의 불가. 두 과제의 결과를 합친 후보 행 수가 사람 분모가 아니다.

| 행동기록 사례 | 사전 인지 근거 | 관측 행동·대안 설명 | 허용할 주장 | 뒤집는 추가 증거 |
|---|---|---|---|---|
| K (합성) A1 | 자유회상에서 이전 사용 명시, 같은 groupby 코드 seal | 0 제공, 1 open; 같은 hash; 상기 가능 | 알려진 방법 유지; 인수는 합성 통과, 교체 N | actor provenance 누락이면 사용 귀속 보류 |
| N (합성) B1 | <=x 수동 구현, 명시 API 모름; 효과는 이미 앎 | 0 제공, 2 open, 5 저장, count→right; 다른 경로 미관측 | 특정 API 첫 접함과 일치, 구현 교체 Y, 합성 품질 통과; 개인 인과/새 개념 확정 아님 | 이전 right 코드·자력 선행 노출→known/독립; 타인 수정→교체 U |
| R (합성) A2 | 수동 방식, Counter 사전 지식 U | 12 제공, 13 열람, 비연속 반례 이유로 거절; 동일 hash | 열람·거절, 교체 N; 기존 코드 합성 인수 | 새 Counter 보조 도입 저장 증거→변경 재판정 |
| F (합성) B2 | 수동 count, 명시 API 낯섦; 적합 조건 U | 12 제공, 13 열람, 16 left로 교체; no-tie 예시만 테스트; B2/B3/B6/B7 실패 | 교체 Y, 이름 발견과 일치, 이해 불충분, 인수 N | 이후 right로 수정→별도 버전; rollback→최종 비채택 |

표 2: 한 행=합성 candidate×동일 artifact 계보, 4행, 실제 관측·실험 분모 0. 원행 worked-traces.csv K/N/R/F; trace-artifacts.jsonl 각 3 checkpoint. 시간/인수는 가정. 독립 검토 실제 미실시.

## ③ 주관측과 선행 판정(정정 전)
- 236 chain M1 링크 제공 이후 유용성 언급은 교체 아님; M2 사전 지식; M3 기대 표현과 제3자 종료; S1 실패 및 권고자 zip은 동일 작성자 산출물 아님. 237 cohort의 동일 작성자 두 단계 시간은 독립 reviewer 비용 없음. 서로 다른 연구의 결손을 한 사건으로 보완하지 않는다.
- 원문 관측 D01, D02, D03, D05, D06, D10은 제공·실제 검색·미리보기·과제 순서·코드 편집/응답을 서로 다르게 남긴다. D06은 adaptation count 및 설명, 실제 실행 없음. D10은 실제 feature 완료지만 URL+prior+hash 결합 없음. D11은 위치→선택→통합 사이 실패.
- 사전 예측에 대해 네 합성 사건을 손으로 적용. K no replacement, N implementation replacement, R reject, F replacement but failed. 인과적 효과량 아님. N의 prior dimension을 이름/효과로 분리해야 하고 F는 이름 인지와 이해 실패가 양립. 후속 정정 기록은 다음 커밋.
