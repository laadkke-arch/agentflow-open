# C3·C4 실제 두 번째 목적지 검토

묶음2 원격 SHA `b36cc513ccbc1616168401ec9564866038e880a3` 이후, 수정된 `evidence/control/candidate-read-receipts.json`의 C3/C4 기본 창만을 출발점으로 삼았다. 후보·원자·6자리 순서·표시 metadata·A/B/C key를 변경하지 않았다. 그룹 계산과 커밋은 하지 않았다.

## 분모와 실제 접근

| 단위 | 관측 |
| --- | ---: |
| 출발 후보 창 | 12 |
| 보존한 실제 href 발생 | 336 |
| 고유 목적지 URL(fragment 포함) | 185 |
| fragment 제거 요청 문서 URL | 60 |
| HTTP200 문서 | 59 |
| HTTP404 문서 | 1 |
| 도착 창을 확인한 URL | 177 |
| HTTP200이지만 literal fragment가 없는 URL | 7 |
| 접속 실패 URL | 1 |
| 별도 새 시작 상태로 확인한 두 단계 시행 | 2 |

동일 URL의 반복 발생과 자기 링크·메뉴·로그인·프로필 링크도 버리지 않았다. `targets.json`의 각 `source_occurrences`에는 후보 ID, 원 href, DOM 순번, 최초 창 및 최초 문서 해시가 남아 있다. 같은 문서는 한 번 HTTP 취득한 뒤 그 문서의 실제 DOM에서 여러 fragment를 판독했다. 이는 부모가 수행하는 전체 독립 시행과 구별되며, 이 파일만으로 모든 경로를 독립 사용자 시행이라고 주장하지 않는다.

고유 URL 분모는 C3 89개, C4 99개이며 두 요구가 공유하는 URL3개가 있어 합은185개다. 원풀의 완전 대안 분모 또는 새로운 구현 수로185를 사용하면 안 된다.

## 변하지 않은 원자의 판독

`control-second-hop-coding.json`의 `supports`는 **해당 도착 창 안에서 복합 원자의 모든 조건을 확인한 경우**만 담는다. `partial`과 `subcondition_facts`는 전체 원자를 충족하지 않는다. 원문 판이 다른 사실이나 초안 제안을 합쳐 최종3.11 계약으로 만들 수 없도록 `version_alignment`와 `conflicts`를 별도로 남겼다. `unknown`은 접속·fragment 실패다.

| 사례·원자 | 목적지 단독에서 전체 원자를 확인한 URL 수 | 의미 |
| --- | ---: | --- |
| C3.A1 | 8 | Exception groups의 공유 section을 보여 주는 여러 실제 fragment. 독립 대안8개가 아님 |
| C3.A2 | 4 | PEP Specification/except* 및 Python3.11 except*/try 절 |
| C4.A1 | 0 | TaskGroup 도착절은 취소·대기를 입증하지만 frozen 원자의 gather 대비까지 같은 기본 창에 있지 않음 |
| C4.A2 | 1 | `compound_stmts.html#async-with`의 실제 await 확장 |

위 수는 원자·URL의 진단 수치이며 A/B/C의 이득·손실 수치가 아니다. C3 부분 원자 행은33개, C4 부분 원자 행은12개다. C4의 도착 미확인 행8개는 부적격 또는 증거 부재로 치환하지 않는다.

### 별도로 실제 확인한 두 단계

1. `C3-2 https://peps.python.org/pep-0654/`를 새로 열었다. 첫800 단어의 Python-Version3.11 및 DOM11의 raw `#specification`을 확인한 뒤, 그 실제 href를 새 요청으로 열었다. 도착 element는 `section#specification`, 범위는4,886단어다. 해당 절의 constructor 설명과 except*·Unmatched Exceptions를 읽었다. 첫 창의 availability와 둘째 창의 constructor·처리 계약을 같은 시행에서 합치면 **C3.A1+A2가 완전**하다. 목적지 단독 A1의 availability 부족을 별도 시행이나 연구자 기억으로 보충한 것이 아니다.
2. `C4-3 https://docs.python.org/3.11/reference/datamodel.html#async-context-managers`를 새로 열었다. 실제 DOM956 `compound_stmts.html#async-with`를 확인하고 목적지를 새 요청으로 열었다. `span#async-with`는 해당 async-with section으로 도착한다. enter await, 예외 인수로 exit await, 정상 종료의 None 인수 exit await를 읽어 **C4.A2만 완전**하다. 이 두 클릭에 TaskGroup 실패 정책 C4.A1을 추가하지 않았다.

네 번의 요청은 모두 HTTP200이고 두 번째 목표 fragment도 실제 존재했다. `control-second-hop-independent-trials.json`에는 각 fresh 시작, 실제 href, 원문 해시, 두 비용과 판독 위치가 있다. 실제 사람의 클릭·독서 시간·이해·채택은 **미확인**이다.4,886단어 절 전체를 빠르게 읽었다는 주장도 하지 않는다. 읽은 범위는 그 안의 필요한 명세·예제 문맥이다.

## W에서만 달라지는 같은 원문

| 같은 열린 원문 | 기본 창과 달라지는 확인 범위 | 남는 한계 |
| --- | --- | --- |
| [PEP654](https://peps.python.org/pep-0654/) | 표제3.11+constructor+except*를 허용하면 C3 두 원자를 한 원문에서 확인 | 여러 fragment가 여러 독립 원문이 되지는 않음 |
| [Python3.11 exceptions](https://docs.python.org/3.11/library/exceptions.html) | base/concrete 예외에서 출발했어도 Exception groups 절을 읽으면 C3.A1 확인 | split의 rest 반환은 except* 자동 전파가 아님 |
| [Python3.11 compound statements](https://docs.python.org/3.11/reference/compound_stmts.html) | ordinary except/다른 절에서 출발했어도 except* 또는 async-with의 확인된 명세를 읽을 수 있음 | C3 constructor 또는 C4 TaskGroup 정책을 제공하지 않음 |
| [Python3.11 asyncio tasks](https://docs.python.org/3.11/library/asyncio-task.html) | Task Groups와 gather 두 절을 함께 읽으면 frozen C4.A1의 비교까지 충족 | C4.A2의 두 메서드 await 확장은 없음 |
| [Python3.11 data model](https://docs.python.org/3.11/reference/datamodel.html) | 앞선 동기 exit의 예외 인수 의미를 함께 읽음 | awaitable 반환 규정에서 caller의 두 await를 추가 추론하는 문제는 남음; strict A2 미충족 |
| [TaskGroup 최초 커밋](https://github.com/python/cpython/commit/602630ac1855e38ef06361c68f6e216375a06180) | 기본800 단어 뒤 taskgroups.py의 __aexit__70–153, _abort174–179, _on_task_done181–232에서 취소·대기 구현을 확인 | gather 대비 및 언어가 두 메서드를 await하는 전체 호출 명세는 없고, 초기 구현과 최종3.11 판의 동일성도 자동 가정하지 않음 |

다른 긴 원문, 특히 여러 답장이 한 HTML에 이어지는 메일 스레드 전체는 정독하지 않았다. 그 W 적격은 `full_document_review_status=미확인`으로 남겼다. 빈 `full_document_supports`를 전수 무지원 판정으로 해석하면 안 된다. W는 같은 원문의 범위만 바꾸며 다른 원문·다른 판·세 번째 클릭을 무료로 허용하지 않는다.

## 직접 확인한 잘못된 경로와 판 차이

- [EdgeDB taskgroup.py 원 href](https://github.com/edgedb/edgedb/blob/master/edb/common/taskgroup.py)는 HTTP404였다. 추정한 새 저장소/경로로 교체하지 않았다.
- #90908의 실제 [75453](https://github.com/python/cpython/issues/75453) 링크는2017년 itertools.zip_longest 문서 이슈, [75494](https://github.com/python/cpython/issues/75494)는2017년 Linux os.chflags 이슈로 도착했다. 출발 댓글의 TaskGroup 문맥과 목적지 내용이 다르다. 의도했을 법한 PR로 raw href를 고치지 않았다.
- PEP의 실제 `/3/builtins/exceptions.html#lib-exception-groups`, `/3/reference/compound_stmts.html#except-star`, `/3/tutorial/errors.html#tut-exception-groups`는 **Python3.15.2**였다. 현재판이 비슷한 기능을 설명한다는 사실과3.11 계약을 입증한다는 판단을 분리했다.
- GitHub 이슈의 `#top`, `#issue-1199075312` 및 다섯 `#event-*`는 취득 DOM에 같은 literal id/name이 없었다. 관측은 DOM 목표 미확인이다. 브라우저의 `#top` 특수 스크롤 처리까지 실패한다고 주장하지 않으며 이 HTTP/DOM 점검에서는 해당 기본 범위를 미확인으로 남긴다.

## 범위 구현 정정과 보존

초기 helper는 비heading fragment를 가까운 section/main까지 올렸다. 이 때문에 각주·목차 backlink·GitHub 댓글이 무관한 다른 절까지 포함할 수 있었다. 원자의 변경 없이 **21URL**을 다음과 같이 정정했다.

- aside 각주는 실제 각주 block만 판독한다.
- inline backlink/목차 a는 해당 p/li 등의 구조 block만 판독한다.
- GitHub comment fragment는 header만이 아니라 같은 `comment-viewer-outer-box`의 header+body를 읽는다. 다른 댓글/이슈 전체로 확대하지 않는다.
- dt constructor/TaskGroup class는 부모와 합의한 “그 절” 해석을 유지한다. 두 constructor가 공유하는 설명과 Task Groups의 dt 바깥 계약 문단을 포함하되, 별개의 다른 section으로 확장하지 않는다.

`arrivals-v1.json`은 넓은 최초 결과, `arrivals-v2.json`과 `scope-corrections-v2.json`은 GitHub header만 잘랐던 중간 결과다. 최종 `scope-corrections.json`에는 원래/정정 locator·단어 수·본문 해시·HTML 해시와 재취득 receipt가 있다. `coding-draft-v1.json`은 create_task의 일반 추천, PR의 설계 질문, TODO·pagination을 wait_all 하위사실로 과하게 묶었던 초안이다. 정확한 실제 진술이 있는 창으로 좁힌 최종 코딩에서 C4 부분 원자 행은19→12로 바뀌고, 완전 원자 수는 변하지 않았다. 이 오류들은 후보나 수용 기준을 바꾼 것이 아니다.

## 재현과 검증

작업 저장소 루트에서 아래 순서로 실행한다. 네트워크 원문을 읽고 owned path의 결과 파일만 쓰며, 내려받은 코드는 실행하지 않는다. 현행 원문이 바뀌면 기존 receipt의 SHA256과 먼저 비교해야 한다.

```bash
python -B docs/workstreams/research/AF-RES-044/evidence/pandoc/control-second-hop-probe.py
python -B docs/workstreams/research/AF-RES-044/evidence/pandoc/control-second-hop-scope-correction.py
python -B docs/workstreams/research/AF-RES-044/evidence/pandoc/control-second-hop-code.py
```

최종 검증에서 targets/arrivals/coding의185URL 집합, targets/arrivals의336발생, 출처185행의 모든 필수 필드, 두 시행의 cost2·성공 fragment·원자 판정이 일치했다. source ledger185행은 모두 `counted=false`다. 이 경로 감사 자료를 최소28의 분자 증가로 주장하지 않는다. 제3자 전체 본문 임시 파일은 최종 전달 전에 제거했다. 완전 원문은 재현 시 직접 열어 읽고, 최종 보관물에는 해시·위치·연구자의 요약·판정만 남긴다.

