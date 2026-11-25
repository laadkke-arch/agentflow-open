# AF-RES-263 HANDOFF

**작업자 자체 상태: PARTIAL.** 조사·설계 산출물과 반례 분석은 고정 커밋 완료. 원규격 접근 및 정확판 실행/기대시험 확인이 미달하므로 DONE으로 승격하지 않는다. 중앙 상태는 착수 시 RUNNING, dot-control.json을 작업자가 수정하지 않았다.

- 결과 고정 SHA (HANDOFF 직전): `13f1959136af192fc8ae837c8c283d7340eddaad`
- 착수 SHA `f02dd5d726bb85e4acabfed29c433eacfa31810f`, 작업 브랜치 `work/research-af-res-263`, 소유 경로 `docs/workstreams/research/AF-RES-263/`.
- 선행 AF-RES-250 중앙 DONE/자체 DONE(설계 범위), HANDOFF SHA 5bdad00c83302686817a770672ff118147c6cb9c. 시작판 및 계획판의 의존 SHA 일치. SCOPE 봉인 e5fd197b3ef76afb474d1e52f5b56bd677d5fc2a.
- 결과 읽는 순서: [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/13f1959136af192fc8ae837c8c283d7340eddaad/docs/workstreams/research/AF-RES-263/RESULT.md) → [requirements.csv](https://github.com/laadkke-arch/agentflow-open/blob/13f1959136af192fc8ae837c8c283d7340eddaad/docs/workstreams/research/AF-RES-263/requirements.csv), [relations.csv](https://github.com/laadkke-arch/agentflow-open/blob/13f1959136af192fc8ae837c8c283d7340eddaad/docs/workstreams/research/AF-RES-263/relations.csv) → [assemblies.md](https://github.com/laadkke-arch/agentflow-open/blob/13f1959136af192fc8ae837c8c283d7340eddaad/docs/workstreams/research/AF-RES-263/assemblies.md) → [COUNTEREXAMPLES.md](https://github.com/laadkke-arch/agentflow-open/blob/13f1959136af192fc8ae837c8c283d7340eddaad/docs/workstreams/research/AF-RES-263/COUNTEREXAMPLES.md), [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/13f1959136af192fc8ae837c8c283d7340eddaad/docs/workstreams/research/AF-RES-263/sources.jsonl) → [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/13f1959136af192fc8ae837c8c283d7340eddaad/docs/workstreams/research/AF-RES-263/SELF_CHECK.md), [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/13f1959136af192fc8ae837c8c283d7340eddaad/docs/workstreams/research/AF-RES-263/SCOPE.md).
- 고정 결과 compare: base→result ahead 11, behind 0, 8 변경 파일 모두 소유 경로, dot-control 및 외부 수정 0. 마지막 HANDOFF는 별도 단일 파일 커밋; 최종 인계 SHA는 이 파일 자신에 기입할 수 없어 커밋 응답과 branch head에서 확인한다.

## 완료/보류

- 원장 43행: 고유 산입 34 (형식/작성자 4, 구현/시험 14, 소비자/결정 10, BagIt 6), 5 접근 실패+4 성공 보조 미산입. 같은 계보 여러 자료를 독립 실험으로 세지 않음. 검색/재조회 횟수와 개별 UTC 정확 시각 미기록, GNU 원저작 미러는 판 제한 표시. 두 실제 목적: libarchive #1034 작성자 symlink 보존; GNU bug-tar/Automake 교차 게시 #19616 최초 메일(2015-01-16) 독립 file bytes 배포 및 hardlink 배제. 4셀+hardlink 및 경계 3행, 3×3 제거 9자리 완료. BagIt RFC+프로필, LOC/APTrust 정책 두 기관.
- 핵심: 같은 이름, 동일 논리 멤버, 같은 시점 t, 같은 최종 디렉터리 엔트리, 한 산출물에서 type2와 type0+B>0 동시 요구는 충돌. 그러나 링크 보존+경로로 내용 읽기는 target 동봉으로 양립. GNU -h만으로 독립 payload 보장 금지(T09 GNU 회귀 기대, C10 실제 보고). 하드링크는 동일 inode이고 archive linkname 의존은 별도. BagIt fetch는 전송 예정 대상이지 이미 수신된 bytes가 아님.
- 대안 P(보존+target), D(독립 일반 파일), P+D(두 배포물), 별도 이름 변형. 각 계약과 철회 조건, 원자료 제거 후 유지/재개/복구 첫 URL 명시. 설계자에게 3개 결정 묶음과 9개 제거 행을 넘김; 하나의 최종 해법 강제하지 않음. 성능/시간/실제 비용 측정 없음.

## 다음 첫 행동 및 검증 요청

1. https://pubs.opengroup.org/onlinepubs/9799919799/utilities/pax.html 현행 원규격 직접 접근(이번 403); size/typeflag/linkname/linkdata/extended records의 exact 판을 확인. https://www.gnu.org/software/tar/manual/html_chapter/Formats.html 및 dereference/hard-links 공식 원문 재시도(이번 timeout), mirror de72aa0c의 판 동일성 대조. 원장 성공/실패·판 위치 갱신.
2. [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/13f1959136af192fc8ae837c8c283d7340eddaad/docs/workstreams/research/AF-RES-263/SELF_CHECK.md)의 정확한 fixture, GNU tar 1.35 승인 binary/해시, libarchive v3.8.4 source SHA d114ceee6de08a7a60ff1209492ba38bf9436f79, CPython v3.13.0 source SHA 60403a5409ff2c3f3b07dd2ca91a7a3e096839c7로 Codex 검증. 4셀, 순서 역전, --hard-dereference 대조, true hardlink pair와 raw header/추출 lstat/open/inode receipt. GNU exact --hard-dereference 공개 시험 원파일 확인. 실제 신규 실행 0, 독립 검토 없음. 실패/반전 기준과 수집 명령은 SELF_CHECK에 있음; 정확 GNU release source digest 미확인이라 영수증에 기록.
3. C01 #1034 수정 전 최초판과 target 동봉 의도, C10 원 archive digest·정확 버전, 기관 BagIt 실제 ingest receipt 미확인. 필요 시 원 게시자 공개 기록 및 기관 고정판을 추가 판독. 이미 확보한 250 결과나 242/251/254/255 자료를 다시 재조사하지 않음.

## 색인 제안 (변경하지 않음)

AF-RES-263 | 동일 이름·멤버에서 링크/일반 bytes 충돌 | PARTIAL | 13f1959136af192fc8ae837c8c283d7340eddaad | RESULT, requirements, relations, assemblies, sources, SELF_CHECK | R2 상위 목적 양립, X1 형식 충돌, R4 역참조 dedup 반례; 두 배포물과 BagIt 단계별 참조 비교 | next: POSIX 공식판 → Codex 4셀/하드링크 영수증.

자체 점검은 문서 구조와 GitHub 변경 경계 및 출처의 판독을 대상으로 했으며 독립적인 재현·검토로 간주하지 않는다. 조건을 낮추지 않고 PARTIAL로 종료한다.
