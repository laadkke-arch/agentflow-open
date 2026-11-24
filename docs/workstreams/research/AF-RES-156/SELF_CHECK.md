# AF-RES-156 SELF_CHECK — 자기 검토, PARTIAL

검토자는 본 작성자뿐. 다른 모델/독립 코더, 실제 web-pro 세션 설정 확인, 체크아웃/실행, CI 로그 검증 없음. 작업 문맥: 배정 brief, AGENTS/STATE/운영·연구·제품 brief, AF-RES-147 고정 HANDOFF와 RESULT·oracle/costs의 관련 부분. 147 전체 행 수나 새 oracle 값을 독립 재계산하지 않음. 외부 자료 전 사전 지식(시간대 일반) 및 초기 릴리스 조사 있음. 새로운 독립 실험으로 주장하지 않는다.

## 재집계 및 반증
- sources.jsonl 원판 57행, 보정 후 77행. 고유 counted work_id 29: Django decision 6 / pandas decision 4 / 소비자 변경·당사자 사건 10 / provider 5 / 교통기관 실제 시간표 2 / 아카이브 실제 catalog 2. 요구 20, 세부 3+3+6+4+2+2 개수 기준은 충족. 중복/코드·릴리스 재확인/지침 등의 미산입 39, 실패 또는 본문 충분하지 않은 9. 검색 snippet은 count하지 않음. 교통 시간표는 원 게시 표로 실제 운행 아님; 아카이브는 실제 date 레코드이나 offset 없는 시분초는 미달.
- timeline 27행, changes 16행, downstream 3행, effort 12행, release_refs 15행, merge_parents 8행(D0 미병합 포함). 16+3+1=20 사건 ID는 분모 고유 사건군과 다르다. 본문 P3/P4 issue/PR, X1 issue/PR, X3 issue/PR, D1/백포트 등을 두 번 세지 않음. D0는 실제 배포가 아니고 P5 proposed PR 미병합.
- 엄격 Q4 목표 6/6 두 프로젝트: Django #32365에서 첫 6 직접 commit D1–D6 관측; 5.0 D6 배포 창 외, D3/D4 tag ancestry 후보; 보수적 확정 배포 3(D1,D2,D5), 2 후보, 1 외부. pandas 직접 사건군 5(P1,P2,P3/P4,P5,P8), merge 확인 4, P5 제안. P6/P7은 인접 사례. 2.0/2.1/4.2 전체 변경기록을 전수 코딩 못 함. 후속 두 번째 pandas feature 판은 right-censored. 그 결과 모집완료라고 할 수 없음.
- 비용: 12 effort 행 모두 실제 person-hour 결측; matched counterfactual 0건, runtime report P3/P8 2건, author fuzz P7 1건. 0은 관측 수, 총 사람시간 0이 아니다. diff는 selected file counts, PR 전체가 아님. 예시 숫자 119/11.3 ms, 3/106 ms, 28704 cases 서로 합산하지 않음.
- 반증 경로: D0 #13073 처음 shim 의존 제안 미병합; #14848 gap/ambiguous 논의; D4 같은 객체 alias; X2/X3 자동 변경 오류; P3 explicit pytz 성능 대안; P5 제안 미병합과 2100 cutoff; P8 from_file wrong data 및 probe 기각; P6 overflow vs gap, P7 Series 차이; S31 Dublin negative DST. 이로부터 순절감 주장을 유지하지 않는다. 사용자 실제 두 대안의 대응 시간기록/사용판/같은 입력 회귀 실행 결과가 나오면 철회/수정한다.

## Q→근거 위치→원장→한계
| Q | 원전/위치 (sources.jsonl ID의 URL과 section) | 원장/실행 | 한계와 역방향 |
|---|---|---|---|
| Q1 | S01–S05, S14–S18, S26, S52–S58, S60–S68, release_refs tag | timeline D-T0..9/P-T0..16, SCOPE_CORRECTION | 3.1.8/3.2.10 동일일·v1.5 earliest generic 경로·tag ancestry 미확인; P default +2 결측. 해당 baseline 자료는 count 제외. |
| Q2 | S06–S13, S15/S17/S20, S49–S51 각 diff/PR body | changes D1–D8/P1/P2/P4, merge_parents 8 | 자기 구현 계획 자료 없음. first visible != 작업 최초. D0는 미병합, D4 rename. P2 PR base vs parent 보정. |
| Q3 | S27–S31 계약, S06,S07,S08,S17,S18,S23–S25,S26,S59 | 표2, D1/D2/D3/P2/P6/P7/P8/X3 | test source vs actual CI vs author report 구분; P6/P7 causality 미확인. |
| Q4 | S01 #32365 comments 3–12; S19–S26; S43–S47,S59 | changes + downstream + merge_parents | 6/6 엄격 미달, P3/P4 합침; D6 배포 외, P5 proposed; X1/2/3 원 티켓 역방향 직접 참조 아님. |
| Q5 | S14 초기 estimate, S19/S25 runtime, S24 author fuzz, S06–S13 selected diffs, S43/S46 actual user report | effort E01–E12 | 인건비/대안 결측. 단위 변환 금지, phase 분리. |
| Q6 | S03/S05 opt-out removal, S18 explicit pytz, S49/S51 proposal, S19/S21/S22/S25 alternative, S44–S47/S59 | D0,D2,D6,P3–P5,P8,X1–X3 | 실제 Django opt-out 사용자 미확인; explicit pytz 실행 보고 ≠ 운영 유지. 상류·하류 연결은 X1→S05, X2→S04, X3→X2. |
| Q7 | S32–S42,S48 (T1/T2 official tables, A1/A2 catalog; GTFS/NARA/EDTF) | RESULT Q7 and table3; S35 secondary excluded | no use of Django/pandas inferred. planned vs actual; date vs time; MBTA original rows/offset-less clock data missing. F01–F04 blocked/not fetched. |
| Q8 | S03/S05/S18/S25/S46, S27–S31 | RESULT Q8 examples | conditional design explanation; not run. comparison source and remaining labor both required. |

역방향 검토: counted sources는 최소 하나의 Q/사건과 연결. S01–S18, S49–S58 등 동일 사건 release/diff는 중복 산입하지 않았고, S26은 여러 후속 결정을 포함하는 별개 릴리스 원저작. S32/S35–38/S41/S42/S48은 도메인 규약/가이드로 실제 레코드 하한 제외. 실패 F07–09는 API 성공 S44–46의 대체 경로이며 중복 count 없음. SCOPE_CORRECTION에서 P4 P5/P7 오기→P5/P8, X3 diff 보정. 출처 확인 UTC 일자만 기록, 분·초 없음. release_refs annotated tag ref 확인했으나 peel 불가/미실시를 별도 기록.

## 중간 원격 검증
- ① 6b27d5a329cfe78cf5de4ccd2972b9f6bf7476de — SCOPE.md fetch fixed SHA, match true.
- ② 3387248581df67fecc3e4d5db4ff0d02fa2bd2e9 — timeline.csv fetch fixed SHA match true, 4848 chars.
- ③ 06220b96ac3a4d6623dfdd8ca846d173ddd82b8a — changes.csv match true, 7905 chars.
- ④ 56ecc979948e009e6ae3205520ee329ac11ecd90 — sources.jsonl 43596, effort.csv 3001, downstream.csv 1079 chars; all match.
- 보정 e68281ad1a38fc300748f540f36e4ad9bd9c4f1d — SCOPE_CORRECTION.md 1628, release_refs.csv 1355, merge_parents.csv 2606, sources.jsonl 58727 chars; match true, 77/29 checked by JSON parsing.
- ⑤ 이 파일과 RESULT.md의 실제 원격 SHA·검증은 마지막 HANDOFF에서 기록(자기 SHA 순환 방지).

## 재개 검증
로컬 checkout/테스트/공통 검사 미실행; 실행 명령은 HANDOFF. PR 파일 pagination, merge ancestry, Django/Pandas tagged test 실행, CI log/artifact 확인은 미실행. 전체 외부 원전의 링크 최신화는 범위 밖. 통합 base와 result commit의 changed path 대조 및 정형 원장 읽기는 마지막 인계 직전 수행 예정. 현 단계 결론: 출처 수는 통과, 채택 완전성/재현/기간/비용 조건 불충족 → PARTIAL.
