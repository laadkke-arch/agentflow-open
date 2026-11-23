# 고정 결과 SHA 검증

검사 대상은 `03c6102d6c0d90f6722550d5e2cb1c7219e49b5f`이며, 2026-11-23 17:00:39–17:00:50 UTC에 완료했다. 이 문서와 영수증을 붙이는 이후 커밋 및 마지막 HANDOFF를 앞선 검사에 포함했다고 말하지 않는다.

| 검사 | 실제 명령·입력 | 결과 |
|---|---|---|
| 개별 계약·소유권 | `python -B -m workbench.session check docs/workstreams/research/AF-RES-090/manifest.json --fetch` | exit0, passed, remote_checked, 허용 범위 밖0 |
| 연구 원장·표 대조 | `python -B docs/workstreams/research/AF-RES-090/tools/validate_research.py` | exit0,495 checks, clean fixed SHA |
| Python stream | `python -B docs/workstreams/research/AF-RES-090/streams/python/validate.py` | exit0; 원격에 없는raw cache 재해시는 이 실행에서 미실시, 사전작업트리검사에 별도 보존 |
| 저장소 공통 검사 | `python -B scripts/cloud_check.py --environment chatgpt-work --fetch-contract --require-clean` | exit0, doctor/acceptance/research-case/original-smoke/sessions 단계 모두 exit0 |
| 위 acceptance의 원래 공통 검사 | `python scripts/check.py --require-git` | 55개 unit tests OK, 두 lab test/demo·export·Git bundle 복원 passed |

공통 wrapper의 마지막 `check-all`은 `no_active_sessions`, count0이다. 등록 경로에서 활성 manifest를 찾지 못한 성공 종료를 다중 세션 검증 성공으로 표현하지 않는다. 이번 manifest의 실제 검증은 첫 행의 **명시적 개별 session check --fetch**가 맡았다. 두 결과를 모두 보존했다.

원래 공통 검사기를 수정하지 않았다. 임시 복제본과 TMPDIR를 모두 AF-RES-090 소유 경로 아래 두었으며, 검사 시작/끝 SHA가 같고 두 시점 모두 clean이었다. 검사가 만들어낸 .workbench/lab 출력은 그 임시 복제본에만 생겼다. 필요한 로그·영수증을 복사한 뒤 복제본은 정리했다. 환경 이름 chatgpt-work는 호출자 label이며 별도 클라우드 계정 연결의 증명이 아니다.

`summary.json`은 명령·UTC·종료값·로그 해시를, `common-cloud-receipt.json`은 각 공통 단계와 start/end checkout을, `acceptance.json`은 lab/export/backup 범위를 보존한다. `../remote-result-verification.json`은 동일 결과 SHA의14개 파일을 GitHub에서 다시 읽어 업로드한 원문과 비교한 기록이다. `../result-scope-verification.json`은 변경 경로와 중앙 dot-control 불변 확인이다.

프로젝트 예제 R/Python 실행, SVG/JS 재생, IIIF viewer·EPUB reader 실행은 미실시다. 이번16행은 봉인한 링크 경로의 실제 관측으로, 가능한 모든 수동 URL 조합의 최단 경로를 전수 조사한 결과가 아니다. 주 접근 실패·판 미확인·명시 경로 부재를 실행성공으로 확대하지 않는다.
