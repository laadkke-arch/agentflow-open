# AF-RES-102 실행·원격 재열람 영수증

검사한 연구 결과 SHA는 **092f4c5c56451bceb53e632f4bddf33db6cda168**다. 아래 검사는 해당 SHA의 깨끗한 체크아웃에서 실행했으며, 시작·종료 commit과 clean=true를 직접 확인했다. 이 문서와 영수증을 저장하는 후속 커밋, 마지막 HANDOFF는 앞 검사에 포함되지 않는다. 연구 본문·CSV·집계·재현 코드는 결과 SHA에 고정되어 있다.

## 실제 실행

| 검사 | UTC 시작 → 종료 | 종료값 | 실제 stdout |
|---|---|---|---|
| research_structure | 2026-11-23T22:42:13.668617+00:00 → 2026-11-23T22:42:13.839968+00:00 | 0 | [research_structure.stdout.txt](evidence/validation/research_structure.stdout.txt) |
| session_check | 2026-11-23T22:42:13.840031+00:00 → 2026-11-23T22:42:24.665596+00:00 | 0 | [session_check.stdout.txt](evidence/validation/session_check.stdout.txt) |
| cloud_check | 2026-11-23T22:42:24.665665+00:00 → 2026-11-23T22:42:37.173435+00:00 | 0 | [cloud_check.stdout.txt](evidence/validation/cloud_check.stdout.txt) |

정확한 명령은 다음과 같다.

~~~sh
python -B docs/workstreams/research/AF-RES-102/tools/verify.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-102/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
~~~

[전체 실행 영수증](evidence/validation/run.json)은 stdout/stderr 각각의 저장 위치·SHA-256과 UTC·종료값을 담는다. 파일 기록은 세 검사 명령이 모두 끝난 뒤에만 했으므로 --require-clean 검사를 영수증 쓰기로 오염시키지 않았다.

연구 구조 검사는45개 모두 통과했다. 봉인21+18개 지문, 모집/선택,12예측 자리와24판 자리의 연결,6층 혼동표·분모,477행/111고유 산입,624영수증 참조/484고유경로,필수3표12/24/12행과Q1~Q7·끝3약점을 재계산했다. 의미 판독이나 역사적 생성의 검증이라고 주장하지 않는다.

명시적 session check는 passed, outside_paths=[], unmerged_paths=[], errors=[]다. 공통 검사의 doctor·acceptance·research-case·original-smoke·sessions 명령은5개 모두 종료0이었다. 그러나 마지막 sessions가 자동 발견하여 검사한 실제 세션 수는 **0**이며 내용은 **not-executed / no_active_sessions / freshness=not_checked**다. 이 연구 manifest는 docs/tasks 아래가 아니므로, 공통 세션 탐색의 종료0을 이 작업 manifest 검사로 바꾸어 말하지 않는다. 앞의 별도 명시적 session check가 이 작업을 검사했다.

[원 공통 영수증](evidence/validation/cloud-check.receipt.json)과 run.json의 common_log_copies에5개 명령의 stdout/stderr10개 복사본과 원경로 대응이 있다. acceptance 안에서 scripts/check.py --require-git도 실제 실행됐다. 환경 codex-cloud는 호출자의 환경 표기이며 계정 연결·브라우저 실행·제품 작동의 증거가 아니다.

## 검사 시점 통합 브랜치 변화

시작 ac7abc85e12b3a5b5f87b694d00e9511332fe272에서 검사 당시7440dfcc7c7a6c6772b437877c422e70b9aab9f1로 통합 끝이 이동했다. 변경 파일은 docs/automation/dot-control.json 하나였고, AF-RES-102 항목 자체는 동일했다. AGENTS·STATE·DOT_AUTOMATION·RESEARCH_WORKFLOW·RESEARCH_BRIEF는 모두 같은 blob이며 운영 의존 끝5022d581d8d7a4a359250797d55c79f6b67d219c도 그대로였다. 시작 계약을 바꿀 사유가 없었고 중앙 진행표를 수정하지 않았다. [실제 blob 대조](evidence/validation/end-contract.json).

## 고정 GitHub 재열람

~~~sh
python -B docs/workstreams/research/AF-RES-102/tools/readback.py --commit 092f4c5c56451bceb53e632f4bddf33db6cda168 --output docs/workstreams/research/AF-RES-102/evidence/validation/readback.json
~~~

실행 UTC는 **2026-11-23T22:42:53.274697+00:00 → 2026-11-23T22:43:39.232389+00:00**, 종료값 **0**다. **22/22**개가 HTTP200이고 같은 commit의 Git blob 바이트와 일치했다. 
필수 표가 있는 RESULT, SELF_CHECK, reproduce, 계약/봉인/CSV/집계, 대표 양프로젝트 audit, 교차 분야 실물 감사, 원 PNG4개와 출처 색인을 실제 고정 GitHub URL로 다시 열었다. 각 원주소·최종 URL·MIME·길이·SHA-256은 [재열람 영수증](evidence/validation/readback.json)에 있다. 검색 미리보기나 링크 존재만 확인한 결과가 아니다.

## 실패와 미실시를 구별

- 최종 결과 SHA의 세 검사와 고정 GitHub22개 재열람은 모두 성공했다.
- 앞선 구조 검사기 개발 중 공란/세미콜론 영수증 처리 오류2건은 [draft 영수증](evidence/structural-check-draft.json)에 실패로 보존했고 검사기만 고쳤다. 과거 실패를 지우지 않았다.
- 현재 Matplotlib HTML 전체 바이트4/4 불일치는 [별도 실패 관측](evidence/return-url-checks.json)이다. 절4/4·PNG8/8 일치와 다른 검사이며 저장소 게이트 실패로 합치지 않는다.
- 최초 터미널 git push 인증 실패는 [발행 경로 기록](evidence/publish-path.json)에 보존했다. 이후 인증된 GitHub Git-data API와 expected-SHA ref 갱신으로 각 원격 커밋을 만들고 원격 tree를 로컬 index tree와 대조했다.
- 역사적 생성 job 재현, R/Python 예제 실행, 브라우저/EPUB reader/JS 실행, wheel 설치·entrypoint 호출, 사람 검토는 미실시다. 해당 명제는 미확인으로 유지한다.

단계별 원격SHA·변경 파일은 [checkpoints.json](evidence/checkpoints.json)에 있다. 이 영수증 묶음을 커밋한 후 마지막 HANDOFF 하나만 별도 커밋한다.
