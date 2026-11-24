# AF-RES-207 자체점검

**자체 판정 DONE.** 실제 단일행 2건, 합계 2건, 보류 2건으로 양안을 실행했다. 전이 판별의 각 수치 유형에 최소 한 건 이상이 있다. 12개 주표본 셀과 네 통제를 모두 정산했다. 고유 직접 열람은 유형별 하한을 충족했다. 피험 입력과 코드를 작성한 같은 세션이 검토했다. 새 GitHub checkout 재생과 별도 검증 스크립트를 실행했으며 별도 세션·사람의 독립 검토는 미실시다.

## 질문별 근거와 역검사

| 질문 | 근거 및 판정 | 반증을 확인한 원자료·결과 | 아직 미확인 |
| --- | --- | --- | --- |
| Q1 입력 자격 | 195 중앙 DONE·자체 PARTIAL와 raw 분절 적격. 196 중앙·자체 DONE 및 실제 O2 C가 1,083 B로 최소. D03 [물리 입력 L1–11](https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/segments.csv#L1-L11) · R03 [합격행 L7–25](https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/matrix.csv#L7-L25) | H195의 미충족 HF와 R03의 저비용 A/B를 확인했다. HF 정확판이 필요한 관측은 자격을 넘어서고, A/B 저비용은 실제 오프라인 단독 원문 재열람에서 보류였다. [195 인계와 HF 제한](https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/HANDOFF.md) · [196 O2 A/B L20–23](https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/matrix.csv#L20-L23) | 정확한 HF 원바이트 및 QA |
| Q2 정답 | D01의 30/31, 35/36, 46/47 여섯 위치와 D03의 실제 시간·단어. 골드 커밋을 검사기보다 앞에 고정했다. [195 결과](https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/RESULT.md#L28-L53) · [gold](gold.json) | 분모에 백업을 더하는 경우와 시간열이 다른 경우를 탐색했다. D07 B06은 미완료 동일 작업의 시간 공백. D01 L73의 95,011/77,334 ms 차이로 editing 대체 가정은 기각했다. [D07 B06](https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/bounds.csv#L7) · [D01 시간 L73](https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/RESULT.md#L73) | 로그 내 긴 간격의 실제 활동 및 독립 검수 분모 |
| Q3 전이 | 196 C와 같은 여덟 필드, B에서 다섯 정보만 추가. A/B가 같은 로컬 자료에 접근한다. [R01 L67–79](https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/make_bundles.py#L67-L79) · [판독 로그](receipts/core.jsonl#L1-L12) | 완전한 원행 좌표가 없어야만 집계를 되찾을 수 없다는 조건을 거꾸로 확인했다. 연속 좌표로 두 합계가 A에 충분해 표본에서 항상 B가 필요하다는 가설은 기각했다. [D03 L2–11](https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/segments.csv#L2-L11) · [M1/M2 실측 L5–8](receipts/core.jsonl#L5-L8) | 비연속·복수 그룹 인용, 일반 자연어 판독 |
| Q4 네 통제 | C1 같은 값 다른 행, C2 ms/초, C3 생성 0, C4 동일 참여자의 관측 별칭. A 오승인 2, B 보류 4. [통제 원출력 L1–8](receipts/controls.jsonl#L1-L8) | C1에서 분절 수·단어·사람 수까지 같지만 행이 다르다. C2/C3는 A도 검출했다. 실제 함께 더할 수 있는 건 다른 생산자 둘의 조건창이라는 반례를 D02 및 D03에서 확인했다. METR 원 CSV의 실제 0/결측도 대조했다. [D02 L2–3](https://github.com/laadkke-arch/agentflow-open/blob/a674c67aaf2c4f1a6aaef4b1ac278dabf44188c0/docs/workstreams/research/AF-RES-195/assignments.csv#L2-L3) · [O07 L3–27](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv#L3-L27) · [실제 분모 대조](receipts/context.stdout.json) | 각각의 오승인 유형에 대한 일반 발생률과 각 필드의 단독 필요성 |
| Q5 격리·판정 | 20회 모두 staging 목록 일치, 새 열린 경로/소켓 EPERM, 종료 0. 판독기의 단위·행·분모·보류 사유와 채점이 분리된다. [검산 원출력](receipts/verify.stdout) · [새 checkout 재생](receipts/replay-compare.stdout) | 동시 변조된 196 발췌와 자체 해시가 통과한 반례를 재판독했다. 207 C1은 바른 외부 코호트가 있는 조건에서만 B가 보류함을 확인했다. [R03 동시 변경 L42](https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/matrix.csv#L42) · [통제 L1–2](receipts/controls.jsonl#L1-L2) | 잘못된 코호트가 함께 제공되는 경우와 독립 리뷰 |
| Q6 타 분야 | E01 PROV entity/activity/usage, E02 Data Cube 차원·측정·단위·중복, E03 SDMX DSD, E05 지역·기간·모집 참조. E06의 두 행씩으로 같은 404의 다른 통계량을 계산했다. [E01 §5](https://www.w3.org/TR/prov-dm/) · [E02 §5.2/IC-12](https://www.w3.org/TR/vocab-data-cube/) · [E03 p.87–90](https://sdmx.org/wp-content/uploads/SDMx_3-1-0_SECTION_2_FINAL.pdf#page=87) · [E05 §3–4](https://ec.europa.eu/eurostat/cache/metadata/en/rail_pa_esms.htm) | 같은 공식 데이터의 2024 단위 문자열과 결측 상태 위치를 직접 열었다. DK/PT 및 LT/RO의 실제 두 합으로 숫자만 같은 관측, BE 결측과 EE의 0, 공식 발표에서 국가별 두 지표가 반대로 움직일 수 있음을 확인했다. [E06 고정 위치 원API](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/rail_pa_typepas?lang=en&time=2024) · [E08 지표 방향](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Railway_passenger_transport_statistics_-_quarterly_and_annual_data) · [비교 원출력](receipts/context.stdout.json) | 원 HTTP 바이트 지문, 유럽 합계의 교차 국경 중복 제거 |
| Q7 비용 | 주표본 두 안 동일. B 순증 2,335 B를 다섯 필드별로 합계와 재대조했다. [비용표](costs.csv) · [종합 채점](receipts/score.json) | 0 B 추가로 충분한 S1/S2/M1/M2와 B로도 합계를 만들 수 없는 W1/W2를 확인했다. 196의 저장안별 비용은 단일 영수증의 값이다. 공유 규칙 직렬화로 중복 저장 설명을 점검했다. [실재 표본](matrix.csv) · [R04 O2 비용 L20–25](https://github.com/laadkke-arch/agentflow-open/blob/6147197ee77016a096412353bd9c3a9f4cd61b1e/docs/workstreams/research/AF-RES-196/costs.csv#L20-L25) · [공유 규칙](receipts/rule-registry.json) | 필드 제거 실험, 운영 조회 비용과 정확도-용량의 일반 곡선 |

## 고유 자료와 계보

| 자료 유형 | 실제 | 최소 | 부족 | 위치 |
| --- | ---: | ---: | ---: | --- |
| 195 고정 배정·분절·집계·메타데이터·영수증 | 8 | 6 | 0 | D01–D08 |
| 196 실제 정답·명세·판정·비용·판독 | 7 | 6 | 0 | R01–R07 |
| 두 선행이 인용한 원출전 | 7 | 4 | 0 | O01–O07 |
| PROV·Data Cube·SDMX·Eurostat 실제 자료와 단위 메타데이터 | 8 | 4 | 0 | E01–E08 |
| 합계 | 30 | 20 | 0 | [출처 원장](sources.jsonl) |

39개 등록 중 고유 직접 열람 30개에 계보 ID 14개가 있다. 9개 제외는 진행표·인계·SDMX 입구 4개, Eurostat 전송 403 두 건, UI 미열람 1개, 필터 요청 미열람 1개, 선행 HF 정확판 미확보 1개다. R06은 196에서 실제 판독에 사용된 고정 원표현이다. 이를 산입하지 않아도 196 직접 원자료 6개가 남는다. 본 작업에서 만든 A/B와 통제·출력·웹의 같은 자료 재열람은 산입하지 않았다. E06 소스는 사전 범위에 있었고 404를 만드는 숫자 조합은 사후 선택했다. E08과 O07은 사후 보강이다.

같은 사건을 여러 파일에서 확인한 경우 사건군을 합치면 6개다. DivEMT 원작업, 196 오프라인 판독 실험, 186 새 O2 영수증, 과거 EARL H1 제출, METR 작업시간, Eurostat 철도 통계 계열이다. 본 표본 수치를 지지하는 DivEMT의 고유 관측은 12개 조건 분절이다. 두 보류의 QA 보조 근거 24행 중 10행은 같은 분절을 재사용해 총 26개 고유 행을 사용했다. 분절행은 방문별 이벤트 여러 개를 합친 관측 단위다. 철도 비교의 6좌표는 숫자 5개와 기밀 결측 1개를 포함하며 물리적 개별 탑승 사건 수는 미확인이다. 이 작업의 20개 판독과 생성된 통제는 원자료 사건 수에 더하지 않았다.

## 실행 점검

- GitHub 고정 tree의 지문 17건, 6개 모집 자리와 원행 합, 결과 16행, 모든 보호된 판독, 실제·생성 행 구분, 추가 바이트와 출처 하한을 별도 코드로 다시 확인했다. 종료 0. [검증기](receipts/verify.py) · [검증 원출력](receipts/verify.stdout)
- GitHub의 깨끗한 `375058d11904e5f446306b8be175f33f241b623a`에서 주표본 12회와 통제 8회, 차원·생산자 산식 및 채점을 재실행했다. 판정·비용·판독 원출력 등 파일 10개 일치. 환경은 Linux, Python 3.12.14, libseccomp2 2.6.0-2, strace 6.13, Git 2.52.0이다. [SHA-256 및 파일](receipts/replay-compare.stdout) · [실행 환경](receipts/core-run.json)
- 같은 판의 `workbench.session check --fetch`는 최신 통합판 `bb146773bbffba5e724e8c842951e2c25198c2da`에서 통과했다. 시작부터의 추가 차이는 진행표 한 파일이었다. 공통 클라우드 검사도 종료 0이었다. 작업 계약의 합격은 위 별도 세션 검사로 확인했다. [계약 영수증](receipts/replay-session.json) · [공통 검사](receipts/replay-cloud.json)
- 미실시는 독립 검토, 195 원 ZIP/고정 HF 검사의 재실행, 196 세 안×두 접근 검사의 재실행, Eurostat raw HTTP 원바이트 재대조다. 마지막 항목은 curl 403으로 막혔고, 보존된 API 판독 수치와 상태의 정규화 지문 및 재계산은 확인했다. [명령과 남은 입력](receipts/04.md)
