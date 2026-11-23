# AF-RES-090 인계

**상태: PARTIAL.** 지정된 비교·원자료 조사·원격 커밋·검증을 수행했다. 남은 접근/판 관계의 빈칸을 확인으로 올리지 않았다. 작업 브랜치는 `work/research-af-res-090`, 소유 경로는 `docs/workstreams/research/AF-RES-090/`다. 중앙 `dot-control.json`은 변경하지 않았다.

## 읽는 순서와 결과

1. [RESULT.md](RESULT.md): 필수 표 1~3, 분모, 8대응쌍, 반례, 마지막 정확히 3약점.
2. [cards.md](cards.md): 네 프로젝트의 두 목적별로 바로 반환할 URL·볼 절·주장 범위.
3. [targets.csv](targets.csv), [traversals.csv](traversals.csv), [sources.jsonl](sources.jsonl), [assets.jsonl](assets.jsonl): 봉인 목적, 실제 경로, 자료 계보, 자원 지문.
4. [SELF_CHECK.md](SELF_CHECK.md), [검사 설명](evidence/validation/README.md), [검사 영수증](evidence/validation/summary.json).

직접 적격 원자료 **45건·18계보**, 원장97행(직접HTTP91·선행6), **16판독·8대응쌍·22문서 열람·1,890,350 응답 본문 bytes**를 남겼다. 지정판 본문 목적의 엄격 충족은 **3/8**, 봉인한 후속 내용과 판 관계까지 함께 충족한 목적은 **0/8**이다. 후속 문서 자체는 R1 A에서1/8 읽혔고 판 관계가 미확인이다. R2의 정적 출력2행은 SVG/재생 성공에 넣지 않았다. 이 수치는 선택한 봉인 경로의 관측이며 가능한 모든 수동 URL 조합의 최단 경로를 전수 탐색한 값이 아니다.

핵심 결론은 **본문/내장 정적 출력에서 끝나는 목적에는 한 파일이 충분하지만, 고정 HTML의 존재·동일 bytes가 외부 후속 자원의 도달과 판까지 고정하지는 않는다**는 것이다. P3 stable도 동적 메뉴를 통해 두 번째 문서에서3.3.0 본문을 회복한다. P1/R1은 현재판 표지가 다르더라도 선택 코드가 같다는 긍정 반례가 있다. R2는 article HTML이 같지만 Source HEAD의 Rmd가 다르고, Using SVG files에는 실제 SVG/재생 payload 대신 정적 pre 출력만 있다. IIIF 내장Canvas의 선택적 URI 실패와 필수이미지 실패를 구별했고 EPUB의 표지는 실제 내장파일로 충분한 정적 자료를 갖췄다.

## 원격 커밋

| 묶음 | 원격 SHA |
|---|---|
| 실제 시작 통합판 | `c2709abf8d25163eed75a7553ebcbde966105b55` |
| ① 목적·URL·선정 규칙 | `973897922e07d0e63a4c68c377422b1a65ce0f27` |
| ② 시작 문서·다음 자원 후보 봉인 | `c2a3f387cc962abd1ef383e39f750cc23ee5e51a` |
| ③ 실제 열람·판 대조·타분야 원장 | `833071b378ab379188c7b62c4a013621a4958bdf` |
| ④ 판정·독자 카드·자가검산, **검사한 결과판** | [`03c6102d6c0d90f6722550d5e2cb1c7219e49b5f`](https://github.com/laadkke-arch/agentflow-open/commit/03c6102d6c0d90f6722550d5e2cb1c7219e49b5f) |
| 결과 SHA 검사·원격 재열람 영수증 | `870ac87f09225cbc346fa09fe4fe35dfa5b6a131` |

이 HANDOFF는 위 영수증 커밋 다음에 **이 파일 하나만** 담는 마지막 커밋으로 남긴다. 자기 SHA는 이 파일이 열린 Git commit으로 식별한다. 선행은 AF-RES-086 HANDOFF `6907534462af729f409c52ce08d3331de22c96e6`, 결과 파일군 `e6a79c3ac05b84ea1c7db313233df1717cade756`다. 계획 당시 foundation `62a80b9f…` 대신 실제 시작 SHA를 계약에 고정했다.

## 실제 검사와 미실시 경계

모든 아래 실행의 대상은 **`03c6102d6c0d90f6722550d5e2cb1c7219e49b5f`**다. 2026-11-23 17:00:39~17:00:50 UTC에 완료했다. 이후 영수증/HANDOFF 커밋을 그 검사에 포함했다고 말하지 않는다.

| 실시한 검사 | 종료값·관측 |
|---|---|
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-090/manifest.json --fetch` | **0**, passed·remote_checked, 계약 일치, 범위 밖0 |
| `python -B docs/workstreams/research/AF-RES-090/tools/validate_research.py` | **0**,495개 일관성 검사, clean 고정 SHA |
| `python -B docs/workstreams/research/AF-RES-090/streams/python/validate.py` | **0**, 커밋된 원장/영수증 검산 |
| `python -B scripts/cloud_check.py --environment chatgpt-work --fetch-contract --require-clean` | **0**, 시작/끝 clean·동일SHA |
| 위 공통 wrapper 안의 `python scripts/check.py --require-git` | **0**,55개 unit tests OK, lab test/demo·export·Git bundle 복원 passed |
| 원격 결과 재열람 | 동일 결과 SHA의14파일을 GitHub에서 직접 다시 읽어 업로드 원문과 일치; 변경248파일 모두 소유 경로 안, dot-control bytes 불변 |

공통 wrapper의 `check-all`은 count0·`no_active_sessions`다. 활성 세션을 실제로 검증했다는 뜻으로 쓰지 않는다. 이번 manifest의 유효성은 첫 행의 **명시적 개별 check --fetch**로 확인했다. 원래 공통 검사기는 수정하지 않았고 소유 경로 아래 임시 복제본/TMPDIR에서 실행했다. 원격 검사 영수증3파일도 다시 읽어 일치함을 확인했다.

프로젝트 예제의 R/Python 실행, SVG/JS 재생, IIIF viewer·EPUB reader 실행은 미실시다. 정적 문서/자원 읽기와 별개이며 실행 성공률은 **0/0 산출 불가**다. raw 전체 응답은 직접 읽고 해시 검산한 임시 캐시였고 최종 커밋에는 짧은 발췌·UTC·MIME·지문·재열람 URL을 남겼다. 역사적 배포/장애 복구/동시 제공/이전 빌드 로그는 다시 조사하지 않았다.

## PARTIAL 사유와 다음 첫 행동

주 판독의 R1-body-B·R1-next-B·R2-body-B는 각각 HTTP503에서 종료됐다. 보조 UI의 같은 주소에서는 소스를 읽었으므로 영구 장애나 보편적 독자 접근 불가로 일반화할 수 없다. R1 외부 도움말의 생성 당시 R판 연결도 미확인이다. IA old manifest/tile은 proxy503이어서 과거 tile404를 현재 origin 실패로 재현하지 못했다. R2의 SVG/재생 payload 명시 경로 부재는 확인된 제한이며, 실행 실패를 직접 재현한 것은 아니다.

**다음 첫 행동:** 위 GitHub 세 입구를 새 UTC 구간에서 일반 브라우저와 HTTP로 한 번씩 나란히 관측한다. 새 결과는 현재16행에 덮어쓰지 말고 별도 회차에 기록한다. 정상 소스를 받으면 실제 노출된 href 또는 문자 URI 복사를 구분하고 입구 포함2회에서 멈춘다. 다음 명령은 새 HTTP 입구 관측의 정확한 입력이며 이번 인계 뒤 자동 실행하지 않는다.

```bash
python -B - <<'PY'
from pathlib import Path
from datetime import datetime, timezone
import runpy
task_root = Path('docs/workstreams/research/AF-RES-090')
fetch = runpy.run_path(str(task_root / 'tools/http_evidence.py'))['fetch']
out = task_root / 'evidence' / ('followup-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
archive = 'https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html'
asciicast = 'https://github.com/r-lib/asciicast/blob/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html'
for name, url in [('R1-body-B', archive), ('R1-next-B', archive), ('R2-body-B', asciicast)]:
    receipt, _ = fetch(url, name, out, timeout=40)
    print(name, receipt['status'], receipt['final_url'], receipt['sha256'])
PY
```

검사 전체를 같은 조건으로 재현하려면 결과판에서 `python -B docs/workstreams/research/AF-RES-090/tools/run_validation.py 03c6102d6c0d90f6722550d5e2cb1c7219e49b5f`를 실행할 수 있다. 이 명령은 소유 경로 안의 임시 복제본을 사용한다. 기존 검증 영수증과 구별할 새 브랜치/회차에서 수행해야 한다.

## 핵심 약점 3건의 조사 제안

1. **GitHub 접근 관측의 불일치.** 입력은 위 세 blob 입구와 새 UTC·동일2회 예산. 같은 시점의 브라우저/HTTP가 모두 완전한 소스를 받으면 새 회차 접근 판정이 바뀐다. 현재503은 보존한다.
2. **본문 보존과 후속판/표현의 불일치.** 입력은 R2의 고정2.3.1 HTML·현재/고정Rmd 및 실제 SVG/cast payload 원URI, R1은 발행자가 고정한 R판·system.file 문서 URI다. 동일판의 실제 payload 또는 외부판 연결 근거가 생기면 자원/판 축이 바뀐다. 정적 pre만으로는 바뀌지 않는다.
3. **타분야 현재 필수자원 실패의 미재현.** 입력은 사건61의 [old manifest](https://iiif.archivelab.org/iiif/naeb-b101-f02-23/manifest.json)와 [old tile](https://iiif.archivelab.org/iiif/naeb-b101-f02-23$0/1024,2048,1024,1024/256,/0/default.jpg). 정상 연결에서 manifest의 필수 tile과 실제 실패 응답이 같은 시점에 연결되면 현재 사례로 확정할 수 있다. P3는 정확 root 표의 직접 메뉴/수동 조합 경로도 새 회차에 검토해,2회 도달을 관측하면 좁은 경로 결론을 수정한다.

**색인 제안 한 줄:** `AF-RES-090 | PARTIAL | 고정 HTML의 본문 충분성과 후속 자원·판 연결을16판독으로 분리 | docs/workstreams/research/AF-RES-090/RESULT.md | depends AF-RES-086@6907534462af729f409c52ce08d3331de22c96e6`.
