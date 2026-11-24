# AF-RES-240 범위와 사전 예측

## 기준판

- 계획 링크의 SHA는 `914dbfa789ebec97063ed97130ea2a71c2e9f503`이다. 시작 때 GitHub에서 읽은 통합 head는 `64e139f16309e41e30f9ec634eabe17fef908bbd`다. [GitHub 비교](https://github.com/laadkke-arch/agentflow-open/compare/914dbfa789ebec97063ed97130ea2a71c2e9f503...64e139f16309e41e30f9ec634eabe17fef908bbd)에서 앞 5 / 뒤 0, 변경 파일은 `docs/automation/dot-control.json` 하나다. 계획 링크의 JSON에는 AF-RES-240 항목이 없고 AF-RES-229까지 있다. 시작판은 AF-RES-240의 실행 요구·브랜치·경로를 추가하고 시도 1을 RUNNING으로 기록한다. 양쪽 AF-RES-222 결과 핀은 같으며 고정 인계와 이번 지시의 표본·버전·판정은 일치한다.
- 의존은 AF-RES-222의 `fe41449d156eb5e723c254a0530863468c084480` 하나다. 중앙 표기 DONE과 자체 PARTIAL(전거 결측과 실제 라이브러리 실행 0)을 따로 보존한다. 고정판의 HANDOFF.md, RESULT.md, names.csv, consumers.csv, history.csv를 GitHub에서 직접 읽었다. [고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/fe41449d156eb5e723c254a0530863468c084480/docs/workstreams/research/AF-RES-222/HANDOFF.md)
- 작업 브랜치 `work/research-af-res-240`를 위 시작판에 만들었다. 소유 경로 `docs/workstreams/research/AF-RES-240/`와 의존 SHA는 `session.json`에 고정했다. 실행 위치는 제공된 클라우드 셸이다.

## 표본

모집은 선행 names.csv의 UCD 16.0.0 여섯 행이다. 01A2, A015, 2118, FE18은 correction, 000A·FEFF는 control·alternate·abbreviation의 대조다. 다섯 공식 Name, 13개의 Name_Alias(정정 4, 제어 3, 대체 1, 약어 5), 000A의 UCD placeholder 한 건을 `inputs.csv`에 그대로 봉인한다. 그 placeholder의 공식 Name 검색은 두 소비자 모두 N/A다. FE18 Name은 `BRAKCET`, correction은 `BRACKET`을 그대로 사용한다. 새로 여는 UCD 15.1.0 및 16.0.0의 원행과 바이트를 뒤에서 대조한다.

고정 실행 대상은 CPython v3.13.0 / 15.1.0과 ICU4C release-76-1 / 16.0이다. 두 라이브러리에서 옛 Name→코드, 별칭→코드, 코드→Name을 각각 평가한다. 코드×소비자×방향 36자리 중 34자리 적용, 2자리 N/A. 각 반복에서 CPython은 lookup 18 + name 12 = 30회, ICU는 세 choice를 각각 써서 u_charFromName 54 + u_charName 18 = 72회다. 2회씩 총 204호출이 예정되며 별칭 검색은 그중 (13 + 39) × 2 = 104회다. 재생·반례·버전 API는 이 분모와 별도다.

CPython은 `name(cp)`와 `name(cp, None)`을 별도 호출한다. ICU choice는 `U_UNICODE_CHAR_NAME`, `U_CHAR_NAME_ALIAS`, `U_EXTENDED_CHAR_NAME`을 쓰고 매 호출 `U_ZERO_ERROR`로 시작한다. u_charName 기본 버퍼는 길이 256. 호출마다 정수 반환, status 정수와 이름, 종료·버퍼 조건을 기록한다. 동일 API 인수의 두 결과를 원값으로 비교한다.

비교 예측은 `predictions.csv`의 36행을 원형 보존한다. CPython의 정확 입력 18개는 모두 검색되고, 역방향은 다섯 Name과 000A의 ValueError/default None을 예상한다. ICU old→code의 원표는 choice 미기재이므로 UNICODE/EXTENDED 성공 및 ALIAS 실패를 이번 확장 예측으로 추가한다. correction은 ALIAS 검색·표시에만 나오고 그 외 9별칭은 세 ICU choice에서 실패할 것으로 예상한다. EXTENDED는 기존 Name을 표시하고 000A는 합성 이름을 표시할 것으로 예상한다. ICU 실패 예상은 헤더 `U_INVALID_CHAR_FOUND`와 구현 `U_ILLEGAL_CHAR_FOUND` / `0xFFFF` 두 예측을 보존한다.

반례 입력은 `controls.csv`에 봉인한다. 정확 철자 기준 1조건씩 비교한다. 일반/알고리즘/CJK/합성 이름의 ASCII 대소문자, 공백, LF→L, 공식 alias와 legacy 표현, 유효 U+FFFF, 버퍼 경계 및 별도 시간대 Link→입력 수용→표시를 본다. 이름 범위 밖의 반례는 36자리 집계에 합치지 않는다.

범위에서 뺀 것은 역사 최초 승인, 도서관 전거, AF-RES-227~229, 시간대 계산 정확도, 다른 빌드·언어 전체의 일반화다. 시간대 비교는 IANA 2024b와 CLDR 46을 출발점으로 ICU의 canonical ID와 소비자가 보존하는 키를 대조한다.

## 노출 및 단계

계획 링크와 시작 문서, 의존 인계·원표를 먼저 열었다. 이 커밋으로 표본·정적 예측·반례를 고정하고 GitHub에 올라간 뒤 새 원문과 배포 소스를 열고 빌드한다. ② 새 원문·검증된 판·정확 입력 두 실행의 원영수증, ③ 필수 표·주관측, ④ 반례·정정, ⑤ RESULT·SELF_CHECK, ⑥ 최종 검사와 고정 결과판 대조 후 HANDOFF 단독 커밋을 순서대로 둔다. 문헌 목표는 UCD 4, CPython 5, ICU 7, 222 원표 2, 시간대 4, 총 고유 원저작 22 이상이다. 동일 저작 재열람과 실패 경로는 원장에는 남기고 성공 고유 수에서는 제외한다.

`python -m workbench.session start af-res-240 --allow docs/workstreams/research/AF-RES-240/ --dependency work/research-af-res-222=fe41449d156eb5e723c254a0530863468c084480 --output docs/workstreams/research/AF-RES-240/session.json --fetch` 종료 0. 실행 출력은 [stdout](receipts/session-start.stdout), [stderr](receipts/session-start.stderr)에 있다.
