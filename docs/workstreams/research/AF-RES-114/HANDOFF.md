# AF-RES-114 인계

**PARTIAL.** [고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450/docs/workstreams/research/AF-RES-114/RESULT.md), 24기능 카드, 탐색 6쌍과 구성 4쌍의 순위·비노출 판정, 두 DB 재생과 비용을 수용할 수 있다. 두 트래커의 지정 순차 창, 6개 자연 요청의 실제 조회, 매뉴얼의 대응 PO가 미확인이다. 최초 본문 확인과 독립 의미 판독은 0건이다.

다음 첫 행동은 검사한 결과 SHA에서 [frame.csv](https://github.com/laadkke-arch/agentflow-open/blob/4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450/docs/workstreams/research/AF-RES-114/frame.csv)와 [재현의 자연 모집 절](https://github.com/laadkke-arch/agentflow-open/blob/4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450/docs/workstreams/research/AF-RES-114/reproduce.md#미확인-자연-표본을-복구할-첫-실행)을 여는 것이다. 필요한 최소 새 입력은 Blender·KDE의 첫 40/41 경계까지의 생성 UTC·원 ID·작성자 본문이 있는 표와 해당 발행판의 한국어 PO revision이다. 이 실행 환경의 공개 호스트 셸 요청에서 CONNECT 403이 났고 웹의 조회 쿼리도 응답을 주지 않았다. 개별 공개 이슈와 공식 코드 미러의 판독 범위는 확보했다.

## 수용 범위

- 탐색 144판정은 직접 0, 일부 6, 충돌 138이다. 영문 심벌을 유지한 한국어 Clone Layers 대조는 1→1이었다. 공식 UI PO를 포함한 보조판에서는 한국어 Box Mask가 조사 밖에서 조사·표시 1위로 들어왔다. EXR 역할 충돌을 내린 영어 실험에서 근거 미연결 후보가 그 표시를 채웠다. 고정 자연 96행은 요청 공석의 재생 상태다. [판정·표 1~3와 Q1~Q7](RESULT.md)
- 검사 결과 SHA는 `4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450`다. GitHub의 소유 파일 37개와 고정 원자료 6개를 바이트 대조했다. 대표 HTML 원절 5개를 다시 읽었고 MARC 기록의 두 번째 접근은 restricted URL이었다. 첫 열람은 [자료 원장](sources.jsonl)에 있다.
- 같은 SHA의 깨끗한 별도 checkout에서 명시 session check, 공통 cloud check, 기존 check, 두 DB 재생, 표 생성, 독립 산술, diff 검사를 실행했다. 7개 명령이 종료 0이다. 독립 산술은 10 순위 파일의 672행, 768 SQL, 원장 4파일, 교란 3개를 대조했다. 공통 검사의 자동 세션 발견은 0이며, 명시 session check는 remote_checked다. [확정 검사 증거](evidence/acceptance-evidence.json)
- 원본 GUI 검사는 미실시다. Krita 5.3.0에서 기존 PNG File Layer 및 변형 마스크의 문서 축소와 Advanced Export를 검사하고, Blender 5.3.0에서 #130134의 Box Mask→Viewer 및 미연결 Double Edge Mask를 검사할 입력과 단계는 [재현](reproduce.md)에 있다. 동일 작업자 재판독과 산술 구현의 독립성을 구분했다. [질문별 자체 검사](SELF_CHECK.md)

## 첫 공개 입력과 검사 명령

공식 호스트 응답을 읽을 수 있는 환경에서 아래 GET으로 시작해 링크된 재현 절의 순서·날짜·본문 경계를 봉인한다.

```bash
curl -fLsS 'https://projects.blender.org/api/v1/repos/blender/blender/issues?state=all&type=issues&limit=50&page=1' -o blender-page-1.json
curl -fLsS 'https://bugs.kde.org/rest/bug?product=krita&creation_time=2023-01-01T00%3A00%3A00Z&limit=1000&offset=0' -o krita-page-0.json
curl -fLsS 'https://bugs.kde.org/rest/bug/464692/comment' -o krita-464692-comment.json
```

검사 재실행 입력은 위 결과 SHA의 catalog.jsonl, queries.jsonl, sources.jsonl과 세 truth 원장이다. 저장소 루트에서 `python -B -m workbench.session check docs/workstreams/research/AF-RES-114/manifest.json --fetch` 및 `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean`을 실행한다. DB·표·산술의 정확한 명령은 [재현](reproduce.md)에 있다.

## 단계별 원격 확인

| 묶음 | SHA | GitHub 다시 읽은 시각과 범위 |
| --- | --- | --- |
| 모집·계약 | `9bd43fc6621abdae8131b2a8e8fb3cc263fd8677` | 03:58:13 UTC · 2파일 |
| 조작 카드·대역어 | `c7036922e6073207dbcb8b44990531fdc3afa1d6` | 04:04:14 UTC · 4파일 |
| 요청 원문·번역·순위 비노출 판정 | `1784204173153e23f2b5225012e05bda6aa8415e` | 04:13:44 UTC · 7파일 |
| 네 방식 실행·교란 | `ade317363116345b18af53eb75b2aeffb31b78d7` | 04:24:22 UTC · 15파일 |
| 결과·재현·반례 | `4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450` | 04:28:40 UTC · 고정 결과 37파일 |
| 검사와 기준 SHA 전사 | `e598e24e74d3ecb68fdf73c506f9c0b8f6e47235`, `cbe92ad361fc86ffc77b57f15f1aeaf3531c51eb` | 04:30:27 UTC · 확정 검사 파일 |

색인 한 줄은 **AF-RES-114 · 기능 24 · 한·영 별칭 조회와 역할 재정렬의 2×2 · 보조판에 한국어 직접 1건 신규, 영어 교체 오추천 반례 · 자연 창·매뉴얼 PO 미확인으로 PARTIAL**이다.

| 가장 중요한 불일치·약점 | 다음 조사·직접 열 자료 | 어떤 관측이면 판단이 바뀌나 |
| --- | --- | --- |
| 시간·ID가 고정된 자연 표본 0/6 | 공식 GET으로 40/41 경계를 고정하고 [frame](frame.csv)의 공석을 먼저 검토 | 범위가 입증된 첫 세 건씩에서 직접 적격이 확인된다 |
| 현재 운영의 한국어 효과는 UI PO와 한국어 HTML 보조판에 한정 | Blender 5.3 RST/POT 및 ko PO, Krita 대응 SVN PO와 발행 HTML, [키 차이](sources.jsonl) | 같은 판·같은 키로 연결한 별칭에 신규 직접 적격이 재현된다 |
| 충돌 벌점이 모르는 후보를 앞세우고 태그 하나를 잃은 양성도 내린다 | [E-B2 및 E-K2 추적](evidence/table2.csv)과 [Box Mask 교란](evidence/ranks-box_role_omitted.csv)의 독립 판독 | 같은 조사 집합에서 직접·일부를 보존하면서 확인된 충돌을 낮추는 표시를 재현한다 |
