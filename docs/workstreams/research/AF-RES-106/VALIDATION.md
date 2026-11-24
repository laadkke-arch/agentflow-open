# AF-RES-106 결과판 실행·재열람 영수증

검사받은 결과 SHA는 **`506f2f6e597899e653d99ab021ed36df0f1e45d6`**다. RESULT·SELF_CHECK·counts·재현 코드가 들어 있는 묶음④ 커밋이며, 원격에서 2026-11-24T00:37:05.560Z에 확인했다. 이 문서와 이후 영수증·HANDOFF는 결과 검사 뒤에 작성한 별도 커밋이다. 이를 이전 검사에 포함됐다고 소급 주장하지 않는다.

## 실제 실행

모든 명령의 실행 전후 HEAD는 같은 결과 SHA였고 `git status --porcelain`은 비어 있었다. wrapper는 세 명령이 끝난 뒤에만 영수증을 썼다. 상세 UTC·명령 배열·종료값·stdout/stderr SHA-256·clean 전후는 [run.json](evidence/validation/run.json)에 있다.

| 검사 | 실제 명령 | UTC 시작 → 종료 | 종료값·범위 |
| --- | --- | --- | --- |
| research_structure | `python -B docs/workstreams/research/AF-RES-106/tools/verify.py` | 2026-11-24T00:37:15.142873+00:00 → 2026-11-24T00:37:15.486327+00:00 | 0 · 147개 구조·봉인·선정·원장·자료계보·fragment·표 대사 통과. 의미/실행 인증 아님 |
| session_check | `python -B -m workbench.session check docs/workstreams/research/AF-RES-106/manifest.json --fetch` | 2026-11-24T00:37:15.497066+00:00 → 2026-11-24T00:37:21.866396+00:00 | 0 · 명시한 AF106 manifest 1개; remote_checked; 변경1452경로 모두 owned_path 안, outside/unmerged/errors 각0 |
| cloud_check | `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 2026-11-24T00:37:21.875573+00:00 → 2026-11-24T00:37:42.556186+00:00 | 0 · 공통 doctor/acceptance/research-case/original-smoke 성공. sessions 자동 발견0은 별도 미실시 |

[명시 manifest stdout](evidence/validation/session_check.stdout.txt), [공통 검사 stdout](evidence/validation/cloud_check.stdout.txt), [원 공통 receipt](evidence/validation/cloud-check.receipt.json), [공통 개별 로그 보존 목록](evidence/validation/common-log-map.json)을 함께 읽는다. stderr도 같은 디렉터리에 보존했다. 공통 acceptance의 실제 단위검사는55+7+9개가 통과했으나 연구의 의미 판독을 검증한71개 테스트라는 뜻이 아니다. `research-case`는 저장소의 reference-audit discovery fixture다.

공통 `workbench.session check-all --fetch`는 종료값0이지만 실제 응답은 **status=not-executed, reason=no_active_sessions, count=0, freshness=not_checked**였다. 명시 AF106 manifest 검사1개의 remote_checked/passed와 합치지 않는다. 환경명 `codex-cloud`는 호출자가 지정한 label이며 계정 연결·새 AI 세션·제품 배포를 입증하지 않는다. 공통 검사는 제품·브라우저 통합 검사가 아니다.

계약 SHA-256은 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`다. 검사 당시 integration은 `d678d6a92c130380cad96bfcd9e9846f9680503b`, task/scope base는 `32b6bb32989730df78d521c29a50dbebd3289b46`이다. 검사 후 원격 integration·운영 의존102를 다시 읽어 같은 끝임을 확인했다. [end-contract.json](evidence/validation/end-contract.json).

## 고정 결과판과 반환 위치 재열람

실제 명령은 `python -B docs/workstreams/research/AF-RES-106/tools/readback_result.py`이며, UTC 2026-11-24T00:37:53.191183+00:00 → 2026-11-24T00:38:35.698997+00:00, 종료값0이다. 총 **48건 중 48건 통과·실패0건**이다. [모든 원 URL·시각·응답·지문·id 영수증](evidence/validation/readback.json).

| 재열람 범위 | 건수 | 확인한 것 | 확인하지 않은 것 |
| --- | ---: | --- | --- |
| 결과 SHA의 GitHub 고정 파일 | 24 | RESULT 필수 세 표·SELF_CHECK·원장·재현·대표 PNG5개 등; HTTP200, 로컬 결과 commit blob과 bytes·SHA-256 일치 | GitHub 웹 UI 렌더의 시각 품질 |
| 주 사례 양판의 고정 원 HTML | 16 | HTTP200·원 보존 본문 SHA-256·지정 실제 DOM id 일치 | raw text/plain endpoint의 browser scroll |
| Matplotlib 옛/새 버전 문서 | 8 | HTTP200·반환 대상 actual DOM id 존재 | meta-refresh fragment 전달·브라우저의 실제 도착/화면 표시 |

root는 GitHub connector로 고정 RESULT 첫65행(필수 세 표)과 reproduce 전부를 직접 다시 읽었다. [connector-readback.json](evidence/validation/connector-readback.json). 이 두 독해는 위48건과 같은 저작의 중복 재열람이며 신규 고유1차 자료 산입0이다. 결과 bytes가 같은 것을 확인했으므로 표/분모/절/지문을 수정하지 않았다. 이전부터 고정된 원 예측도 그대로다.

## 게시와 경계

묶음③ `a9aea90170ad8d96d0e6fcb0513473902c7d2d80`는803경로, 묶음④ 결과는17경로를 바꿨다. 각 경로·blob·SHA-256·부모·tree·원격 UTC는 [checkpoint-3](evidence/checkpoint-3.json), [checkpoint-4](evidence/checkpoint-4.json)에 있다. 로컬 push 인증 실패 뒤 인증된 GitHub Git Data 경로로 동일 index tree를 게시했고, `expected_sha`·`force=false`로 앞 커밋에 이어 붙였다. [publication-method.json](evidence/validation/publication-method.json). 기존 커밋을 초기화하거나 덮어쓰지 않았다.

연구 결과의 제한은 그대로다. 주 실제8쌍+결원4, 고유 자료38, 원 목적 양성7/음성1, 일반 역할 양성8/음성0이다. 엄격한 잔류·미사용 반례는 상세 판독 범위에서 미확보이고, G는 실제16판 전부 미확인이다. R/Python 예제·브라우저·IIIF viewer는 실행하지 않았다. 별도 원장 대사318개는 같은 계열 AI의 결과 노출 후 검토이며 완전 맹검이나 사람 검토가 아니다.
