# AF-RES-134 자기검사

| 주장 | 고정 근거 URL·위치 | 결론을 뒤집을 조건 | 실제 찾아본 반증과 결과 | 남은 미확인과 다음 검사 |
| --- | --- | --- | --- | --- |
| Q1 · A 64개 JSON 및 B 4개 JSON의 origin 응답을 관측하지 못했다. A의 HTML #1은 6027 하나를 읽어 홍보로 제외했다. | [모집 고정판 frame](https://github.com/laadkke-arch/agentflow-open/blob/94a6269a48c7724cadeab912322b15759e4b6a88/docs/workstreams/research/AF-RES-134/frame.csv) A/B 전 행 · [HTTP](evidence/forum-http.jsonl) · [HTML](evidence/forum-html.jsonl) | 같은 공개 URL에서 origin 상태와 정확한 topic·post나 배열을 받는다. | 64 topic/4검색 HTML을 대조했다. 홈과 6027 접근 성공은 호스트 전체가 폐쇄됐다는 가설을 뒤집는다. JSON 접근은 CONNECT 403으로 막혔다. | 63 topic 상태·삭제와 B의 현재 순위를 미확인으로 둔다. 첫 실행은 `/t/6001.json` 및 `q=가중치` probe다. |
| Q2 · G1 22/40, G2 어떻게 24/24와 싶습니다 22/24를 보고 6건·6저자를 채택했다. | [G1 고정 창](https://github.com/laadkke-arch/agentflow-open/blob/94a6269a48c7724cadeab912322b15759e4b6a88/docs/workstreams/research/AF-RES-134/evidence/g1-window.jsonl) · [G2 공식 응답](evidence/g2-how-search.jsonl) · [G2 싶습니다](evidence/g2-want-search.jsonl) · [열람 로그](evidence/github-openings.jsonl) | G1 #30/#43의 그림이 필요한 tensor 목표를 명료화하거나 앞 모집층에서 같은 글을 발견한다. | 공식 저장소 목록 22개를 연결 도구의 22 ID와 대조했다. 공개 본체는 전부 열렸고 이미지 #39/#43은 직접 열리지 않았다. 서로 같은 이슈 2와 같은 FAQ 3을 다시 확인했다. PR로 리다이렉트된 슬롯 0개. | 본문 유보 두 건 및 포럼 교차 중복을 확인한다. 검색 노출과 채택의 단위를 유지한다. |
| Q3 · 저자의 목표, 기존 시도, 인용/로그, 거절과 보존 요구를 구절로 연결했다. 동일 문자열이 다른 역할일 수 있다. | [요청 봉인](https://github.com/laadkke-arch/agentflow-open/blob/94a6269a48c7724cadeab912322b15759e4b6a88/docs/workstreams/research/AF-RES-134/requests.jsonl) · [역할 반례](evidence/counterexamples.md) · [원문/구절](evidence/role-boundaries.jsonl) | 원저자가 표본별 확률이나 저장소 복사 자체를 명시적으로 목표로 삼는다. | 제외 G2-how-5에서 모델 가중치와 A10 단일 조사 적중을 확인했다. G2-how-20의 `.view`는 trace였다. `뷰어`는 저장 데이터의 시각화기다. 복사할 데이터량 보존과 복사를 피하는 두 외부 원저자 사례를 직접 읽었다. | 사용자 입력에 들어온 자연 공개 심벌과 카드 심벌을 각각 더 넓은 모집층에서 조사한다. 편집 시각 필드는 공개 첫 본문에 노출되지 않았다. |
| Q4 · 표시 판독 96쌍과 기준 96쌍을 점수 전에 커밋했다. 단일 프로세스 조건에서 D01 직접 1쌍이다. | [표시 봉인](https://github.com/laadkke-arch/agentflow-open/blob/2a4af7b6365e0f6c771ea5fc9b7aff81039d99f4/docs/workstreams/research/AF-RES-134/display-review.csv) · [기준 봉인](https://github.com/laadkke-arch/agentflow-open/blob/656825eff895d8878b94e5e67cf93a449566ffe2/docs/workstreams/research/AF-RES-134/truth.csv) · [D01 구현](https://github.com/pytorch/pytorch/blob/a8d6afb511a69687bbb2b7e88a3cf67917e1697e/torch/utils/data/dataloader.py#L410-L415) | Windows 원저자가 병렬 작업자 보존을 요구하거나 배치 출력을 직접 명시한다. | BatchSampler는 index list, loader/fetch는 dataset에서 실제 표본을 뽑는다. collate의 tuple·문자열 결과와 reshape의 copy 회귀를 읽었다. 단일 프로세스 경로 분기와 Windows spawn 문서를 대조했다. | 같은 사람이 두 번 판독했다. 독립 판독과 원래 HDF5 실행은 미실시다. 병렬성 보존을 따로 평가한다. |
| Q5 · B/C의 활성 별칭과 짝지은 순위 차이가 0이었다. Gate는 직접과 충돌을 각각 하나 보류했다. | [순위 고정판](https://github.com/laadkke-arch/agentflow-open/blob/d12a81d3eab3d07d8a99800a950e4fb850631397/docs/workstreams/research/AF-RES-134/ranks.csv) · [짝 차이](evidence/transitions.csv) · [별칭 감사](evidence/alias-audit.csv) | 조사 결합이 실제 있는 원문에서 카드가 양점 상한 안으로 들어오거나 기존 직접 후보를 밀어낸다. | B/C에서 126의 경계 검사 12개를 실행했다. 제외 원문의 `가중치를`는 C에서만, `뷰어`는 넓은 D 경계에서만 잡혔다. 흔한 영어 조사·코드는 G2-how-20에서 T01을 높였다. | 적격 원문에서 결합형 신규 직접·충돌을 아직 볼 수 없다. 출력 조건이 부족한 D01 원절을 어떻게 표시할지 검증한다. |
| Q6 · 관측 요청 6건×16=96쌍에서 직접이 있는 요청 1건이다. Gate의 모델상 추가 원절은 28개다. | [집계](evidence/metrics.csv) · [자리](evidence/slots.csv) · [추가 원절](evidence/editor-cost.csv) · [원장 재집계](evidence/recount.json) | 게이트 통과 후보가 있는 새 층에서 3개까지 표시되거나 다중 역할 모호성을 확인하는 실제 사용자 비용을 관측한다. | 조사8과 표시3을 후보별로 재집계했다. 공석 및 0점을 구별했고, G2에서 조사 충돌 2 중 표시 충돌 1만 해소됐다. G1·G2에 저자 반복과 검색 템플릿 노출을 확인했다. | 원문 미접근과 저자 중복을 보존한다. 클릭·이해·해결 효과는 실제 관측 설계가 필요하다. |
| Q7 · 운영 ID와 방향은 같은 역 이름을 가르고, BnF 전거와 역할은 같은 인물의 세 가지 연결을 가른다. | [MTA 23 St·Times Sq 행](https://data.ny.gov/resource/39hk-dx4f.json) L10/13/164/228/317/320/405/468–469 · [방향](https://www.mta.info/accessibility/stations) L206–210 · [전거 역할](evidence/domain-identities.csv) | 동일 도메인에서 이름·역할을 포함한 입력이 유일한 ID를 주거나, 단지와 방향의 선택이 링크를 바꾸지 않는다. | 23 St 네 역과 634의 6호선 이형을 비교했다. 405의 북서/북동 엘리베이터가 방향에 따라 다르다. Baudelaire의 저자/번역자/주제 링크가 같은 ARK로 연결된다. 두 Dumas의 이름과 저자 역할이 같아도 ID 없이는 유보된다. | 정규 GTFS를 받을 수 있는 환경에서 자식 승강장 ID를 검사한다. 이름만 나온 Dumas 원문은 저작·연대·ID를 확인한다. |

## 실행과 대조

- [재생 영수증](evidence/replay-validation.json)은 검사 SHA `d12a81d3eab3d07d8a99800a950e4fb850631397`와 실제 명령·stderr·stdout·종료값을 담는다. Python 3.12의 두 별도 아카이브/프로세스에서 seed 0과 37로 재생했다. 각각 공개 첫 본문 6개를 다시 받았고 첫 본문 지문, NFC 경계, 구절 지문, 투영, 한국어 경계 12개, 출력 6개 SHA가 모두 일치했다.
- [재집계 코드](replay/recount.py)로 모집 184행, 표시/기준 각 96행, 순위 288행 및 출처 186행을 세었다. B→C와 C→Gate 변화는 순위 위치 집합에서 다시 셌다. 출처 산입 고유 38편, 활성 alias 12개, 채택 작성자 6명이다. 자체 검색 슬롯과 실제 조사·표시 공석은 다른 분모다.
- PyTorch 고정 파일 13편의 원점 판·범위와 SHA-256은 [API 열람 원장](evidence/pytorch-files.jsonl)에 있다. Windows HDF5 실행은 미실시다. 아래 126의 기존 CPU 프로브는 자료 반환 및 공유 가정을 재시험하는 재개 입력이다. PyTorch·NumPy가 설치된 해당 판에서 실행한다. 원저자 Windows 환경의 동작은 별개 실험이다.
- 각 묶음을 GitHub의 고정 SHA에서 다시 열었다. 마지막 계약 검사 영수증은 `evidence/session-check.json`에 검사 대상과 시각이 기록된다. 별도의 독립 세션 판독은 미실시다.

```sh
af134_p126=abcdda426e2a2d19f0732752c221ea4d494458c4
git fetch --no-tags origin "$af134_p126"
af134_probe=$(mktemp -d)
git show "$af134_p126:docs/workstreams/research/AF-RES-126/probe_torch.py" > "$af134_probe/probe_torch.py"
python3.12 -m venv "$af134_probe/venv"
"$af134_probe/venv/bin/python" -m pip install --index-url https://download.pytorch.org/whl/cpu 'torch==2.5.1+cpu'
"$af134_probe/venv/bin/python" -m pip install 'numpy==2.1.3'
"$af134_probe/venv/bin/python" -B "$af134_probe/probe_torch.py"
```
