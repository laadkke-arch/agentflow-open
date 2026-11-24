# AF-RES-206 HANDOFF

**PARTIAL** · 시도 1 · Codex Cloud 실행 및 자체 검토, 2026-11-24 UTC. 발행기관 full ZIP의 본문을 받지 못했다. 검산 결과, 결손, 재개 명령은 배정 브랜치 `work/research-af-res-206`에 저장했다.

## 결과와 근거

- 직전 결과 SHA `7292580b919335d196b54fbfa3b8cc8ba327f5f6`. 시작 SHA `c860f8240ab7b7077e2d5b63e438ddd83ff69a27`, 계획 기준 `050278651b11a2a3a49d45baebf41c707c06b700`, 의존 AF-RES-188 `a0fcb2d1229e01639b27d34f8cb336fca7cf3cfc`. 작업 경로 `docs/workstreams/research/AF-RES-206/`. [범위와 판정 규칙](SCOPE.md)
- [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/7292580b919335d196b54fbfa3b8cc8ba327f5f6/docs/workstreams/research/AF-RES-206/RESULT.md), [출처 원장](sources.jsonl), [points](points.csv), [deltas](deltas.csv), [claims](claims.csv), [자체 검토](SELF_CHECK.md). 재현용 [compare.py](compare.py), [inputs](inputs.json), [실행 영수증](receipts/README.md)이 있다.
- X16/X17의 40개 정방향 행은 줄바꿈을 제외하면 동일하다. 188의 6자리·4고유점은 사본과 원문 토큰·Decimal·전체 출력 토큰이 일치한다. X05 격자 표는 X20/X22의 역방향 입력과 40/40행 일치한다. T05의 역입력 E/N과 순기대 E/N도 각 자료와 40/40점 일치했다. TP31의 X05−X16 차이는 E −0.003 m, N +0.004 m, 높이 −0.001 m, TP32는 E −0.001 m, N +0.001 m, 높이 0 m다. [축별 관측](deltas.csv) · [실행 원출력](receipts/comparison.stdout.jsonl)
- 직접 연 자료 40, 고유 산입 25/22. 발행기관 팩/배포 유형 6/6은 기관의 공개 문서이고, 재게시·시험·설명 6/6, 정의 5/4, 188 2/2, 조석·교정 6/4다. 직접 연 자료 중 15건은 재게시·포함 범위 등을 이유로 제외했고, 미열람·접근 실패 경로 15건을 보존했다. 발행기관에서 직접 받은 팩 멤버는 0개, 주점 원행 0/6자리·0/4고유점, 별도 충돌점 원행 0/2다. 공식 점별 공차는 0/6자리 확인이다. 기준면 설명, 지역 모형 표준오차, 구현의 검사 허용치는 각각 해당 근거에 연결했다. [자료 분모](SELF_CHECK.md#자료-분모) · [발행 ZIP 결손](members.csv)

## 차단 상태

`https://www.ordnancesurvey.co.uk/documents/resources/OSTN15-OSGM15-DevelopersPack.zip`의 Cloud GET은 환경의 CONNECT 403에서 종료 56, origin 응답 코드 000, 0바이트였다. 공개 웹 리더는 발행 링크를 찾았고 ZIP content type을 처리하지 못했다. 발행기관의 실제 HTTP 상태, redirect chain, 바이트 길이·SHA, 내부 버전·헤더는 미확인이다. Cloud 환경의 `www.ordnancesurvey.co.uk` 및 `geomatics.cc` 공개 HTTPS 호스트 추가 제안은 `pending_confirmation`이다. 마지막 관리 환경 조회에서도 제한 정책이 적용 중이고 추가 호스트는 없었다. [실제 전송 영수증](receipts/publisher-attempt.txt)

## 재검증

- 결과 SHA를 원격 브랜치에서 다시 가져왔다. 그 SHA의 RESULT, SELF_CHECK, source ledger, CSV, code 및 영수증을 읽었고, 표 순서와 마지막 약점 3행, Q 7개, 분모, 자료 연결 및 차이를 검사했다. RESULT blob `18d5fbe7ba361c29fa0c8319322853ce7c1f04fe`, SELF_CHECK blob `a1a0fb09c5ff039be15e40a24eb8b4e194e95f25`, source ledger blob `6c68c1199f614b20f0016ec77bc23494df6e194a`다.
- 해당 SHA의 `compare.py --fetch-comparators --controls`를 새 임시 경로에서 실행했다. 원본 팩 부재로 예상 종료 2, stderr 0바이트이며 points·deltas·members가 커밋 파일과 바이트 단위로 일치했다. 통제 14건 모두 예상대로 동작했다. HTTP 200으로 받은 실제 grid-banger ZIP은 시험 이름 5개가 있었지만 full 원시 격자가 없었다. [실행](receipts/fresh-replay.stdout.jsonl) · [통제](receipts/controls.stdout.jsonl)
- 코드가 들어간 단계 ④ SHA `392dbe840d351c1e9e2873207dcd16511be20a76`의 깨끗한 checkout에서 공통 검사 종료 0을 확인했다. 전체 `check-all`의 세션 상태는 `no_active_sessions`다. 결과 SHA의 개별 `workbench.session check ... --fetch`는 21:16:39 UTC에 `passed/remote_checked`였고 허용 밖 변경은 0개였다. 그때 최신 통합판 `bb146773bbffba5e724e8c842951e2c25198c2da`와 시작판의 파일 차이는 진행표 한 곳이며 계약 해시는 동일했다. 독립 검토 및 발행자 원파일 양성 시험은 미실시다. [공통 검사](receipts/repository-checks.txt)

## 재개 첫 행동

발행기관 호스트의 HTTPS GET이 허용된 환경에서 [OS00 배포 페이지](https://www.ordnancesurvey.co.uk/geodesy-positioning/coordinate-transformations/resources)의 full 링크를 받아 같은 파일을 확인한다. 실행 입력과 예상 산출물은 고정 결과 SHA의 `inputs.json`에 있다. 브랜치의 checkout 루트에서 다음 명령을 사용한다.

```sh
owned=docs/workstreams/research/AF-RES-206
run_dir=$(mktemp -d)
python "$owned/compare.py" --work "$run_dir" --fetch-comparators --download-publisher --controls
```

X05의 원 HTTP HTML까지 보존할 수 있는 환경이면 `--download-x05`를 추가한다. 행 검증이 성공하면 origin 응답의 URL/redirect/status·length·SHA, full 데이터 형상과 ZipInfo가 생성된다. `$run_dir/publisher-full.zip`에서 test README, 네 방향별 fixture, 사용자 가이드·모형·판 표기를 열어 동봉 가이드의 판·공차/flag 절을 기록한다. 검사기가 파일 이름·형상·헤더를 거부하면 `members.csv`와 ZIP 경로를 먼저 읽고 발행자 판을 확인한 다음 매핑을 갱신한다. 공식 파일의 6고유점과 사본을 다시 조인하고, 과거판의 동일성은 보존된 발행기관 지문 또는 판 기록으로 따로 확인한다. 그 증거가 없으면 과거판은 미확인이다. [재현 절차](receipts/README.md)

색인 반영 제안 · **AF-RES-206 PARTIAL** · OSTN15/OSGM15 시험 파일의 방향별 재게시 비교, 188 사본 6자리/4 TP 재현, X05 역입력·T05 순기대 비교 · 발행기관 ZIP 원행과 점별 공차 확인은 OS01 재실행에서 이어받음.
