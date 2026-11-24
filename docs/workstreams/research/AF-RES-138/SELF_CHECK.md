# AF-RES-138 자가검사

| 주장 | 직접 읽은 원문 URL·위치 | 확인 범위 | 가장 강한 반례·찾은 곳 | 남은 미확인·다음 확인 |
| --- | --- | --- | --- | --- |
| Q1 창 43슬롯·고유 첫 글 41개. 층간 겹침 0. | [실제 검색 p1–3, 결과 배열](evidence/search.jsonl) · [첫 글 bodyVersion](evidence/opening-receipts.jsonl) | 6질의, 첫 20 또는 배열 끝, 경계 다음 시각. 41개 재요청에서도 Markdown 모두 일치. | P1/P2의 두 동일 이슈는 검색 단위로만 세면 중복. 조회 기법에서 숫자 문자열과 본문의 정수 ID를 대조해 수정했다. | 이전 열람 뒤 쓰기 이력 전체 미확인. 새 시각 검색은 새 관측으로 분리. |
| Q2 적격 목적 1·중립 4저자. 목적 형태는 시도. | [P1-07 L2–4](https://github.com/Beomi/KcELECTRA/issues/5) · [N1-06 L1–11](https://github.com/yskim0/NYU-DEEP-LEARNING/issues/2) · [위치·해시](requests.jsonl) | 답글·점수 없는 초기 판독. 134 URL·본문 지문 대조 및 새 글 계보를 기록했다. | P1-06 L48은 실제 표본 확률의 형태지만 본문은 과제 정리. N1-06은 공개 코드 설명을 자기 보존 조작으로 오인할 수 있다. [과제 정리](https://github.com/Boostcamp-AI-Tech-2th-level01-04/TWL/issues/13) | 독립 판독자 및 삭제 계정의 원저자 미확인. 과거 행을 효과 분모에 다시 넣지 않는다. |
| Q3 표면이 같아도 입력·출력이 다르다. | [Sampler L228–290](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/sampler.py#L228-L290) · [Tensor API·시험](sources.jsonl#L57) · [온라인가나다의 인용+조사](sources.jsonl#L82) | 파라미터/확률, 복사/이력, 축/stride, 샘플/인덱스 구별. 금지와 명시 요구가 빠진 경우를 기록했다. | P1-07의 리뷰 속 뷰 2번과 N2-01의 로그 단어. strided 전치의 공유를 sparse로 확장하면 틀린다. [어절 감사](evidence/alias-audit.csv) | 적격 복사·전치·데이터로더 형태의 자연 원문 추가 필요. PyTorch 런타임 미설치로 공식 회귀 코드 판독 범위. |
| Q4 먼저 표시 80, 별도 기준 80. | [두 봉인](display.csv) · [전수 기준](truth.csv) · [P1-07 후속](https://github.com/Beomi/KcELECTRA/issues/5#issuecomment-977563439) | 같은 판독자, 고정 카드 16개. 댓글 13개는 이후 열람했다. | 배치 재사용이 첫 목표의 일부인지 두 해석이 가능하다. 나중 forward 호출은 D01·D03·D04의 일부→미확인 해석을 지지한다. | 첫 시각의 정확한 사용자 의도, 독립 판독, 회신자의 실행 결과 미확인. |
| Q5 조사 8/표시 3 유지. B→C에서 D08의 조사 신규 1. | [정확한 가중치 원절](https://github.com/Beomi/KcELECTRA/issues/5) · [조사·표시 320행](ranks.csv) · [두 재생](evidence/replays.json) | 전체 480전이, 표시 15자리×4 및 조사 40자리×4. 기준판 이전 해시는 보존했다. | P1-07 D04는 조사 한 칸 하락하고 D02는 예산 밖으로 갔다. 세 표시는 그대로다. 민감도 산식은 현재 표본의 관측이 아니다. [전이](transitions.csv) | 신규 조건부 후보를 배정할 적격 원문 부재. 1장 추가와 가득 찬 경우 보존을 경계 입력으로 별도 검사. |
| Q6 Gate에서 일부 2·미확인 9 이탈과 원절 33개 비용. | [표시·조사 자리](evidence/slots.csv) · [편집 원절](evidence/editor-cost.csv) · [같은 카드의 해석 분기](truth.csv) | 실측을 정책에게 필요한 고유 원절과 23쌍 재판독으로 제한했다. 조건부 건수 0, 조건부 성공률 미산출. | N1-03의 양점 후보 둘은 B/C 모두 남았다. P1-07은 조건 하나만 해결해도 원한 추론과 반환 차이가 남는다. [반례](evidence/counterexamples.md) | 사용자 실제 클릭/이해, 표본 외 일반 발생률, 조건 하나의 사람 평가. |
| Q7 같은 이름·역 ID라도 승차 방향/행선지와 편성이 남는다. | [MBTA Park Street L350–389](https://github.com/mbta/screens/blob/78293b2121def3f6e93d4e84b9c345bc7f32829f/config/config.exs#L350-L389) · [LOC 2018560366 Names/Notes](https://www.loc.gov/item/2018560366/) · [LOC MARC p.138](https://www.loc.gov/aba/publications/FreeCSB/CSB_108.pdf#page=138) | 공식 MBTA 코드·규격의 실제 키, LOC 목록 및 공식 예시. 연구 점수의 분모에 포함하지 않았다. | `Park`와 `PARK STREET [R]`은 같은 역인데 동일 Park Street도 70075/70076이 다르다. 동일 편성의 Hindemith 판은 연도로 갈린다. [역/서지 원장](domains.csv) | GTFS live 개별행, 작곡 대조 목록과 악보 표지. LOC 2018560490의 Names와 책임표시 원문부터 확인한다. |

## 파일과 합계

- [재집계](evidence/recount.json)에서 120 예정 칸과 두 층의 77 배열 끝을 합산했다. 43 반환을 고유 41 첫 본문과 두 동일 이슈 자리로 분해했다. 첫 글부터 카드×정책까지 출처 ID 및 NFC 위치를 확인했다.
- [독립 검사기](replay/verify.py)는 양점·동점 정렬 및 상한을 독립 계산하고 두 정책의 공통과 차집합으로 이동을 확인한다. 표시 11+4와 0+15, 조사 23+17이 같은 예산을 보존한다. 조건부와 확정 직접의 빈도는 별도다.
- [출처](sources.jsonl)는 37개 고유 산입 원전, 신규 23 및 재열람 14에 연결된다. 발행자별 기준과 쟁점별 실패 기록이 있다. 적격 자연 저자 5/8 및 목적 1/4로 PARTIAL이고 두 개별 서지·원책임표시 대조도 미완료다.
- 원본 5개의 지문과 투영을 고정판에 연결했다. 단계 5에서 두 별도 Python 프로세스의 출력 파일 다섯 개가 동일했다. 정량 분석은 새 질문을 대상으로 하고 경계 산식은 별도 표에 기록했다. [경계 확인](evidence/counterfactual.json)
