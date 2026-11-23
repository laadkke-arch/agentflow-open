# AF-RES-072 인계

**REVIEW_READY · 시도 1 · Codex Cloud.** 공개 원저작 20편과 보류 요청 6건의 120쌍을 판독했다. 보류 상위 3에서 L은 동종 부분 0/6·원거리 0/14, I와 H는 각각 1/6·1/14였다. P의 이름·목적 투영은 0/6·1/14였으며 I/H와 다른 원거리 사례를 찾았다. 직접 후보 분모는 0이다. L/I/H의 보류 18경로에서 두 조건·환경의 공동 확인은 관측 0이었다. 별도 CLI 양성 대조 X01에서 L의 첫 원문으로 조건과 환경을 확인했다. [표 1과 Q1–Q8](https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/RESULT.md)

I/H의 카드 구축 원문 취득은 20회·2,087,664 B였다. 라이브 빈 캐시에서 L 28,260 B/건, I 0 B/건, H 485,044 B/건이었다. H는 1회 응답 길이로 한도 초과를 확인했고, 즉시 반복에서 그 1편의 원문을 받았다. 라이브 49회 중 완전 응답 48회가 고정판 지문과 같았다. 오프라인 두 번의 순위와 표시 영수증은 바이트 단위로 일치했다. [비용 원장](https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/costs.csv) · [시도 원장](https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/fetches.jsonl)

## 고정 이력

저장소는 `laadkke-arch/agentflow-open`, 브랜치는 `work/research-af-res-072`, 소유 경로는 `docs/workstreams/research/AF-RES-072/`다. 계획판은 `320424d87f99e70c42eeb8cb7211467de27f2c2e`, 배정 시작판은 `17b9cd4090a924f30ad7a2c8fc24e86b08a0e785`다. 세션 계약의 원격 재조회는 `76b8c1d15812fbf91b879f8444fd188ae7445802`였다. 유일한 선행 작업은 AF-RES-068 `2c9642dff48ec0da2785c2c127d3a906182f7834`다. 결과 및 검증 대상은 `330efd4489a2bac012ff9be603020076a424ec6f`다. [계약](manifest.json) · [068 인계](https://github.com/laadkke-arch/agentflow-open/blob/2c9642dff48ec0da2785c2c127d3a906182f7834/docs/workstreams/research/AF-RES-068/HANDOFF.md)

| 단계 | 고정 SHA | 2026-11-23 UTC | 저장물 |
| --- | --- | --- | --- |
| 모집·예산 봉인 | `9c0306072f8a9fb0fa3bfea7040c750092a86c54` | 08:32:16 | 부모 목록, 제외, URL 경계, 요청판·조건 |
| 독립 카드·원본 | `17898b7748bb1909ecb0c54beba553d6168ec126` | 08:35:27 | 20편, 원본과 HTTP 비교, 압축과 권리 |
| 가림 판정 봉인 | `41b73e199f9529bc5ce3165532b87d88eb4d62d0` | 08:39:32 | 가명·섞인 순서와 120쌍 판정 |
| 순위 봉인 | `b74de450e7f0f0ffff150b8662cb840388a17aea` | 08:43:06 | 검색 코드, 조정, 독립 입력 경로와 보류 72행 |
| 실행·재생 | `168d8da351873873fa121932a6dc514386d524cb` | 08:47:07 | 두 재생 지문, 라이브와 반복, 비용 |
| 결과·반례·자체 점검 | `330efd4489a2bac012ff9be603020076a424ec6f` | 08:57 UTC 이후 | 세 결과표, Q1–Q8, 약점 세 건, 수용 원장 |

## 실제 검사

원격 브랜치를 새로 복제한 Codex Cloud checkout에서 Python 3.12.14와 lxml 6.1.1로 검증했다. 아래 작업 계약은 08:59:00.658077 UTC에 결과 SHA에서 종료 0, `passed / remote_checked`였다. 변경 68경로는 모두 계약 범위였고 outside·unmerged·errors는 빈 배열이었다. `audit.py`는 종료 0으로 모집·쌍 조인·허용 원본·세 예산·회수·비용·표 행/열을 검산했다. 두 재생의 동일 SHA-256도 다시 확인했다. 공통 `cloud_check.py`는 깨끗한 결과 checkout에서 종료 0이었다. 그 검사기의 자동 세션 검색은 `no_active_sessions`를 반환했고 이 작업의 계약은 명시한 경로에서 별도로 확인했다. [재생 대상·명령](reproduce.md) · [자체 점검](SELF_CHECK.md)

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-072/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-072/audit.py --replay-a /tmp/af072-out/freeze-a --replay-b /tmp/af072-out/replay-b
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
git diff --check 17b9cd4090a924f30ad7a2c8fc24e86b08a0e785 HEAD
```

2026-11-23 08:58:56.450272 UTC에 GitHub 결과 SHA의 본문·수용 원장·고정 순위·정답표·시도·비용·자체 점검을 다시 받았다. HTTP 200 7/7, `git show SHA:path`와 bytes 일치 7/7이다. GitHub의 렌더된 첫 세 표에서 24·144·8행과 약점 표 3행을 읽었다. raw Markdown 세 표는 각 9열이다. [GitHub 결과 본문](https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/RESULT.md) · [GitHub 수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/evidence/acceptance-evidence.json)

| 원격 확인 파일 | 바이트 | Git blob | 결과 |
| --- | ---: | --- | --- |
| RESULT.md | 111,405 | `a2d0d1e9d837528474927f74be73e7d2a40ca101` | 표 행 24·144·8 |
| evidence/acceptance-evidence.json | 3,371 | `6879f2256e786b523c548b057ff3f7113f60c97e` | 수용 항목 7 |
| ranks.csv | 14,228 | `b77c542698de38dc90ff66e7cfc7909d1ead0b95` | 72행 |
| qrels.csv | 43,102 | `c7b8500cae03d836fbcddc15224f5e75dfc31979` | 120행 |
| fetches.jsonl | 544,693 | `315c07972e27855025d2c46ce7dc6c2095002972` | 248행 |
| costs.csv | 13,987 | `4b1eb92c3bbc0c79e0edf70ed90a6cffde7edb07` | 153행 |
| SELF_CHECK.md | 4,926 | `9ebb9acc9ee12632dc7945a6c52c4c020f85b454` | Q1–Q8 원행·원절·반례 |

원격 재대조는 저장소 루트에서 다음 형식으로 반복할 수 있다.

```sh
af072_result=330efd4489a2bac012ff9be603020076a424ec6f
af072_prefix=docs/workstreams/research/AF-RES-072
af072_verify=$(mktemp -d)
for af072_file in RESULT.md evidence/acceptance-evidence.json ranks.csv qrels.csv fetches.jsonl costs.csv SELF_CHECK.md
do
  curl -fsSL "https://raw.githubusercontent.com/laadkke-arch/agentflow-open/$af072_result/$af072_prefix/$af072_file" -o "$af072_verify/remote"
  git show "$af072_result:$af072_prefix/$af072_file" > "$af072_verify/git"
  cmp "$af072_verify/remote" "$af072_verify/git" || exit 1
done
```

## 미확인과 다음 첫 행동

- 작성자 최초 본문과 Zotero 실물 터치 환경, 자연 한국어의 공식 요청은 미확인이다. 별도 번역 6건의 결과는 표본을 늘리지 않았다. 사람의 활동시간과 실제 사용자 요청량은 미측정이다. 공여·수신 설계를 정한 사람과 가명 재판독자는 같았고 추가 독립 판정은 미실시다. 순위 생성은 qrels가 없는 입력 폴더에서 실행했으며 판정과 순위를 별도 커밋으로 고정했다. [한계와 반례](RESULT.md#가장-중요한-불일치약점-3건)
- 새 검토의 첫 행동은 결과 SHA를 체크아웃하고, `python -B docs/workstreams/research/AF-RES-072/blind.py "$(mktemp -d)/packet"`으로 가림 자료를 만든 뒤 새 판정자에게 Z02/N01, Z04/W04·W06, O04/N05의 조건과 가명 원문만 읽히는 것이다. 순위와 판독표는 새 평가 봉인 뒤 결합한다. 독립 판정이 원거리 적격을 뒤집으면 R 회수 분모와 분자를 먼저 재계산한다. [재현](reproduce.md) · [초기 가림 판독](evidence/qrel-seal.json)
- 직접 후보의 다음 자료는 [OpenRefine 3.8.0 열 메뉴](https://github.com/OpenRefine/OpenRefine/blob/2fbe3d184f7bc9fe23ca15df5ee836a40bcc0967/main/webapp/modules/core/scripts/views/data-table/menu-edit-column.js?plain=1#L573-L609)와 [Zotero #3555](https://github.com/zotero/zotero/issues/3555)의 당시 뷰어 판이다. 색인에는 ‘공개 20편·6보류·120쌍, 직접 분모 0, 카드 부분·원거리 회수 각 1, 고정판 두 번 재생과 라이브 비교 완료’로 표시할 수 있다.
