# C3·C4 보강 표본의 독립 재독

검토자: Pandoc 담당 별도 에이전트. 확인 시각: 2026-11-22 20:25 UTC. 이 문서는 부모 에이전트의 판정과 분리해 원문을 다시 읽은 내부 검토이며, 독립 사람의 판정이나 사용자 실험은 아니다. A/B/C 그룹 및 회수율은 계산하지 않았다. 봉인 원자와 후보 순서는 변경하지 않았다.

**C3는 완전 경로가 입증된다. C4는 봉인된 A2의 엄격한 판독에서 완전 경로가 아직 입증되지 않으므로, 예정된 양성이라는 이유로 통과시켜서는 안 된다.** C3에는 같은 PEP의 한 절이 두 역할을 함께 입증하는 실제 반례가 있다.

## 1. 입력과 원자료 재현

검토 입력은 `evidence/control/freeze-C3.json`(SHA256 `612ed55064439541be35a81b92bd13ec5677fbe9640c70545ad3523c4c108a90`), `freeze-C4.json`(`aa105e69ab4fd41ae802b836c6370df7ea9997fc8b90a4259eefcbc4cc145cd7`), SCOPE의 기본 창·2클릭·W 규칙이다. Python 공식 문서와 PEP를 웹으로 직접 열어 해당 절을 읽고, 별도 HTTP 재취득과 lxml DOM 파싱으로 발행 HTML·href를 대조했다. 임시 원문 복사본을 추가 저장하지 않았다.

[What’s New 3.11](https://docs.python.org/3.11/whatsnew/3.11.html)의 재취득 HTML은 366,782 bytes, SHA256 `ad3de952cae03b47ed776620a6bb2d9dee633d329731c615034e77b3468dfc6a`이며 봉인과 일치한다.

| 사례 | 재확인한 문서 전체 a[href] 순번과 raw href 순서 | 결과 |
| --- | --- | --- |
| C3 | 151 `#pep-654-exception-groups-and-except`; 152 `https://peps.python.org/pep-0654/`; 153 `../library/exceptions.html#ExceptionGroup`; 154 `../library/exceptions.html#BaseExceptionGroup`; 155 `../reference/compound_stmts.html#except-star`; 156 `../reference/compound_stmts.html#except` | 봉인된 6개와 순서까지 일치 |
| C4 | 298 `#asyncio`; 299 `../library/asyncio-task.html#asyncio.TaskGroup`; 300 `../reference/datamodel.html#async-context-managers`; 301 `../library/asyncio-task.html#asyncio.create_task`; 302 `../library/asyncio-task.html#asyncio.gather`; 303 `https://github.com/python/cpython/issues/90908` | 봉인된 6개와 순서까지 일치 |

문서 판 표시는 Python **3.11.18**이다. 이를 초기 3.11.0의 모든 세부 동작으로 일반화하지 않는다. `except*` 문서는 3.11.4에서 달라진 별도 포장 동작도 명시한다. 현재 원자의 미처리 예외 전파와 그 변경을 혼동하지 않는다.

## 2. C3: 기본 창과 완전 경로

| 후보 | 기본 도착 창에서 확인한 범위 | 원자 판정 |
| --- | --- | --- |
| C3-1 | release의 PEP654 절: 도입·그룹·부분 매칭 개요 | A1의 constructor 경계, A2의 미처리 예외 전파가 부족 |
| C3-2 | PEP 첫800 단어: 3.11 메타데이터·목차·동기 | 직접 창에서는 constructor·전파 명세 부족. 목차의 실제 `#specification`은 다음 클릭으로 이용 가능 |
| C3-3 | ExceptionGroup이 속한 Exception groups 절 | A1 예. A2는 부분: subgroup/split 반환값과 except*의 자동 전파를 같은 사실로 세면 안 됨 |
| C3-4 | BaseExceptionGroup이 속한 같은 절 | A1 예. C3-3과 같은 문서·공유 설명을 다시 보여 줌 |
| C3-5 | compound statements의 except* 절 | A2 예. 부분 매칭과 마지막 미처리 예외 재발생을 명시. A1의 constructor 경계는 없음 |
| C3-6 | ordinary except 절 | 기본 창에서는 근접 오답. 그룹 내부의 부분 매칭을 ordinary except가 해 주는 것으로 읽을 수 없음 |

위 표의 1차 근거 위치는 [release PEP654 절](https://docs.python.org/3.11/whatsnew/3.11.html#pep-654-exception-groups-and-except), [Exception groups](https://docs.python.org/3.11/library/exceptions.html#ExceptionGroup)의 두 constructor 설명·`subgroup`·`split`·마지막 New in 3.11, [except*](https://docs.python.org/3.11/reference/compound_stmts.html#except-star)의 첫 두 문단과 예제 바로 다음 미처리 예외 문단이다. 웹 판독 위치는 각각 94–99, 534–607, 123–154행이다.

완전 문서 조합은 C3-3+C3-5 또는 C3-4+C3-5이다. 둘은 서로 다른 구현 대안이 아니라 같은 Python 계약의 증거 조합이다.

**반증된 초기 직관:** 반드시 보완 문서 두 개를 읽어야 한다는 직관은 틀린다. [PEP654 첫 화면](https://peps.python.org/pep-0654/)의 목차에 실제 `#specification`이 있다(전체 DOM 11). [Specification](https://peps.python.org/pep-0654/#specification)은 h2 section이며 다음 h2 Backwards Compatibility 전까지 constructor 경계와 except*·Recursive Matching·Unmatched Exceptions를 모두 포함한다. 따라서 `C3-2 원문 → 목차 Specification`은 총 두 번의 실제 링크 열람으로 같은 원문의 두 역할을 확인할 수 있는 후보 경로다. 첫 화면에서 확인한 Python-Version 3.11도 같은 시행에 남는다. 웹 위치는 constructor 87–91, 매칭 342–345, 미처리 전파 394–415행이다. 이 링크는 연구자가 만든 앵커가 아니다.

W에서는 C3-2 자체의 전체 확인 범위가 두 원자를 입증한다. C3-6도 전체 같은 compound 문서를 허용하면 except* 절을 읽을 수 있어 A2를 제공하지만, constructor A1까지 자동으로 얻지는 않는다. C3의 판독 범위 민감도는 손실이 항상 생긴다는 주장에 대한 실제 반례로 보존할 필요가 있다.

## 3. C4: 양성 자격의 아직 풀리지 않은 부분

| 후보 | 기본 창에서 확인한 범위 | 검토 판단 |
| --- | --- | --- |
| C4-1 | asyncio release 개요: TaskGroup의 종료 대기·추천 | fail-fast 취소와 await 메서드 프로토콜은 부족 |
| C4-2 | Task Groups 절 | 첫 비취소 실패 때 형제 취소·전체 종료 대기는 직접 입증. 본문 예외가 `__aexit__`에 전달된다는 부분도 있음. 두 메서드를 await하는 전체 호출 프로토콜은 명시하지 않음 |
| C4-3 | Asynchronous Context Managers 절 | 두 메서드의 awaitable 반환 의무와 동기 메서드와의 의미상 유사성은 직접 입증. `async with`가 두 결과를 await하며 예외 정보를 전달한다는 전체 절차는 참조한 다른 위치에 있음 |
| C4-4 | Creating Tasks 절 | 개별 Task 생성·스케줄링. 그룹 실패 정책 및 전체 A2의 대안이 아님 |
| C4-5 | Running Tasks Concurrently의 gather 절 | 기본 `return_exceptions=False`에서 첫 예외를 즉시 전파하고 다른 awaitable은 취소하지 않는 근접 오답 |
| C4-6 | 이슈 첫800 단어 | 유지보수자의 설계·시험 설명과 TaskGroup 종료 대기 동기를 확인. 전체 await 프로토콜의 독립 명세는 확인하지 못함 |

위 판정은 [TaskGroup](https://docs.python.org/3.11/library/asyncio-task.html#asyncio.TaskGroup) 250–273행, [gather](https://docs.python.org/3.11/library/asyncio-task.html#asyncio.gather) 306–323·362–364행, [비동기 context manager](https://docs.python.org/3.11/reference/datamodel.html#async-context-managers) 1401–1425행, [이슈 #90908](https://github.com/python/cpython/issues/90908) 유지보수자 첫 설명 204–215행을 직접 대조한 것이다.

두 가지 판정 차이를 별도로 남겨야 한다.

1. **A1 원자의 비교 요구.** 원 request의 본문은 TaskGroup 실패 정책인데, 원자에는 `distinguish gather`가 덧붙어 있다. 이를 필수 증거로 엄격하게 읽으면 C4-2뿐 아니라 C4-5의 비교 근거도 필요하다. 비교를 단순한 근접 오답 검사로 의도했다면 원자의 표현이 과도하다. 현재 봉인은 수정하지 말고 두 해석과 영향을 기록해야 한다.
2. **A2의 의미상 참조 허용.** C4-3은 두 동기 메서드와 의미가 유사하고 반환값은 awaitable이어야 한다고 규정한다. 따라서 넓은 의미 독해로는 프로토콜을 추론할 수 있다. 그러나 기본 창에서 읽지 않은 `__exit__`의 예외 인수 의미나 다른 문서의 await 순서를 이미 읽은 것으로 취급하면 판독 범위가 넓어진다. strict 창 기준으로 A2 complete는 **미확인**이다. 이 문제는 Python 기능의 부재가 아니라 증거 범위의 문제다.

정확한 두 await 및 예외 전달은 [compound statements #async-with](https://docs.python.org/3.11/reference/compound_stmts.html#async-with)의 의사 코드에 있다(웹 816–847행: enter await 832, 예외 인수 exit await 840, 정상 종료 exit await 844). C4-3 도착절에는 이곳으로 가는 실제 `compound_stmts.html#async-with`가 있다(DOM 956). `C4-3 → 그 링크`는 2클릭으로 A2를 입증하지만, 같은 시행에서 C4-2의 A1까지 읽었다고 합치면 안 된다. C4-2 절의 실제 href 목록에는 compound async-with 링크가 없고, datamodel과 `__aexit__` 링크가 있다. 따라서 C4-2→C4-3→compound의 세 원문 도착을 두 클릭 성공으로 기록해서는 안 된다.

W는 Data model의 앞선 `__exit__` 인수 설명(1248–1254행)을 함께 읽게 하므로 예외 전달 의미의 부족은 줄인다. 다만 W가 다른 원문인 compound statements까지 무료로 확장해 주지는 않는다. **C4에서 W만 바꾸어 완전성이 확보됐다고 확정하기 전에도, await 명세를 어느 실제 문장으로 입증했는지 남겨야 한다.**

gather의 반례는 정확히 기본값과 자식의 비취소 실패에 한정한다. gather 자체를 취소하면 남은 awaitable도 취소되므로, “gather는 형제를 절대 취소하지 않는다”는 일반화는 원문과 충돌한다.

## 4. 창·전이 구현에서 필요한 수정 제안

`windows-controls.tmp.json`을 독립 재독 후 교차 확인했다. PEP의 `window.text`는 800 단어로 제한됐지만 `window.links`에는 그 뒤 본문 목차 링크도 들어 있다. 예를 들어 DOM 11 `#specification`은 첫 목차의 유효 링크지만 DOM 68 같은 href는 본문에서 다시 나오는 링크다. **텍스트 창에 포함된 href만 기본 전이로 허용**해야 한다. 전체 main의 모든 링크를 허용하면 800 단어 규칙이 사라진다. 이 문제는 첫800을 쓰는 C4-6에도 점검해야 한다. 원자료와 수정 이유를 보존하고, 원 후보 6자리 순서 자체는 바꾸지 않는다.

fragment가 dt/span에 붙은 경우 “해당 element 뒤”와 “그 element가 속한 전체 section”이 같은 범위는 아니다. 부모 probe는 가장 가까운 section 전체를 반환한다. 본 검토의 C3 constructor/TaskGroup 핵심 판정은 각 target 뒤에도 근거가 있어 뒤집히지 않지만, 링크 목록과 도착 전 문단을 제공 근거로 세는 경우 차이가 날 수 있다. 기본 구현의 정확한 시작점을 SCOPE 해석 기록에 남기고, 무단으로 섹션 앞부분까지 넓히지 않는 것이 필요하다.

## 5. 통합 시 권고

- C3는 위 두 문서 조합과 PEP 목차의 한 문서 경로를 모두 gold 후보로 검사한다. PEP 전체와 같은 문서 fragment는 독립 원문 수를 늘리지 않는다.
- C4는 의미상 참조를 인정하는 판정과 실제 창 안 명세만 인정하는 판정을 구분한다. 후자를 유지할 때 예정했던 양성 조건은 현재 **미충족**으로 남긴다. 사후에 원자를 느슨하게 고쳐 통과시키지 않는다.
- 본 재독의 출처는 부모가 이미 읽은 원문과 중복이므로 `review-sources.jsonl`의 `counted`는 전부 false다. 새 fragment와 별도 재독자라는 이유로 최소28의 분자를 늘리지 않는다. 접속 성공·의미 판독·사용자 반응을 합치지 않는다.

