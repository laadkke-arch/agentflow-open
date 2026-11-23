# AF-RES-100 선행 입력 독립 점검

작성 역할: 별도 하위 에이전트 `dependency_audit`. 지정 Git 원문을 읽었으며 새 Stack Overflow 질문·답이나 다른 분야 외부 원문은 열지 않았다. 이 메모는 선행 연구 자료 검토이고 AF-RES-100의 고유 외부 1차 자료 하한에는 산입하지 않는다.

## 읽은 고정 입력

- [AF-RES-096 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/fce8d0ded93fe1f13f2c4978ed273c1ceef32934/docs/workstreams/research/AF-RES-096/HANDOFF.md)
- 아래 결과 파일은 모두 `1d399f630930d2763459e16509c5224b0cded9a0`에서 읽었다. 표의 blob은 Git 객체에서 확인했다.

| 파일 | blob SHA |
| --- | --- |
| RESULT.md | e947e9b50224f39a84785ddaf47f8e16d800bbe7 |
| protocol.json | 68727b3e5860b8bfa77f35de70f522c28797b614 |
| corpus-plan.json | 8282e1547661af76f5ddefd9525420187e11a647 |
| evidence/intake/intake.json | aa1f0c0bdad86aa6aba0483074035bbab9c3fc78 |
| pairs.csv | de51cb97bcebb8d85a81739c2d6f349c485ced13 |
| evidence/audit/displacement-audit.md | b0661286f8a2f6c67a82798eced4faf862c1d843 |
| evidence/post-evaluation-sensitivity.json | ea588c7ab0898d8599d488496d7aa0c7d2d15730 |
| experiment.py | c5392a8435f6dd9a4d2b236cceec92e07f8e4528 |
| evidence/crossdomain/report.md | 7c385623b691c3970ebf18527e3ab0c1fdb16871 |

재열람 경로의 기준은 [096 결과 디렉터리](https://github.com/laadkke-arch/agentflow-open/tree/1d399f630930d2763459e16509c5224b0cded9a0/docs/workstreams/research/AF-RES-096)다. 해당 Git 객체를 읽은 것이고 이 검토에서 외부 공식 파일을 다시 읽거나 프로그램을 실행한 것은 아니다.

## 제외 ID와 사건 독립성

이전 intake 60개와 선정 8개의 합집합은 정확히 68개, 중복 0개다.

```json
[78253195,78262117,78264525,78265746,78296361,78304807,78305924,78311115,78317715,78320282,78325655,78330476,78337654,78337845,78340421,78342087,78343435,78344013,78366187,78368160,78368831,78374396,78379111,78381387,78383239,78391549,78393001,78397008,78401284,78403902,78258237,78267487,78273711,78300525,78311072,78358965,78359068,78363131,78372646,78391068,78403073,78461996,78462145,78481889,78495314,78509090,78510593,78517094,78530529,78552455,78563147,78563491,78566705,78567123,78575243,78575468,78580879,78596229,78624199,78652004,79322478,79388729,79389414,79410149,79332660,79369213,79375162,79393445]
```

선정 사례 대응은 J1=79322478, J2=79388729, J3=79389414, J4=79410149, P1=79332660, P2=79369213, P3=79375162, P4=79393445다. P3는 최초 본문에서 이전 주 질문의 repost라고 자술하지만 원 ID는 주어지지 않았고 096에서 추적하지 않았다. 68개 ID 제외는 실제 문제 사건·사용자의 독립성을 입증하지 않는다. 새 모집에서 원 질문 링크·재게시 자술·같은 원 입력을 별도로 기록하고 불명은 그대로 남겨야 한다.

## 공식 파일 범위

파일당 최대 2,097,152바이트의 UTF-8 텍스트이며 Python `fnmatchcase`를 사용한다. `*`는 `/`를 포함하므로 해당 패턴의 하위 트리는 재귀 범위다.

| 도구 | 고정판 | 포함 패턴 | 제외 |
| --- | --- | --- | --- |
| jqlang/jq | jq-1.7.1 / 71c2ab509a8628dbbad4bc7b3f98a64aa90d3297 | docs/content/manual/v1.7/manual.yml; src/*.c; src/*.h; src/*.y; src/*.l; src/*.jq; tests/* | tests/*.png |
| jgm/pandoc | 3.6 / 8a72b8449ddccd84fcdffc1a09ae18c4baaca32a | MANUAL.txt; doc/*.md; src/Text/Pandoc/*.hs; test/*.md; test/*.txt; test/*.native; test/*.html; test/*.tex; test/*.lua; test/*.xml; test/*.json | 없음 |

기존 인접 범위는 다음과 같다. AF100에서 처음 등장하는 도구는 현재 지시대로 질문 이전 최신 안정판과 범위를 별도로 정해야 한다.

| 저장소·판 | 고정 SHA 또는 배포판 | 포함 범위 |
| --- | --- | --- |
| asciidoctor/asciidoctor | 0908d45fef9350dbdc68d312ae2b4e8d63bda091 | README.adoc; docs/*.adoc; lib/*.rb; test/*.rb; test/fixtures/*.adoc; test/fixtures/*.xml |
| rstudio/rmarkdown | 204879ff62c00df6b0910c4ed6a1f8e143c551e8 | README.md; R/*.R; man/*.Rd; tests/*.R; tests/*.Rmd; inst/rmarkdown/* |
| pandoc-ext/diagram | 023b31752cb5b63cd8bab828b268fa60ebd16d0c | README.md; diagram.lua; test/*; tests/*; _extensions/diagram/*.lua |
| drolbr/Overpass-API | a0db4f392f744d5e1304331edbf542ef6d6ce2fa | README; README.md; src/overpass_api/*.cc; src/overpass_api/*.h; src/test-bin/*; osm-3s_testing/expected/* |
| GNU/coreutils | 9.5 / ftp.gnu.org/gnu/coreutils/coreutils-9.5.tar.xz | doc/coreutils.texi; src/cat.c; tests/cat/*; tests/misc/cat* |
| GNU/grep | 3.11 / ftp.gnu.org/gnu/grep/grep-3.11.tar.xz | doc/grep.texi; doc/grep.in.1; src/*.c; src/*.h; tests/*; 단 tests/Makefile 및 tests/Makefile.in 제외 |

## 정확한 순위 규칙과 AF100 변경점

096 `tokens()`는 `set(re.findall(r'[a-z0-9_]+', unicodedata.normalize('NFKC', s).casefold()))`다. 파일 본문과 각 질의의 토큰 교집합 크기를 센다. 두 질의의 점수를 합산하지 않고 두 질의 토큰 합집합의 서로 다른 일치 토큰 수로 다시 정렬한다. 순위키는 `(-score, repo+'/'+path)`이며 동률은 대소문자를 구별하는 사전순이다. 파일명 가점·동의어·어간·빈도·문서길이 보정이 없다. 점수 0은 전체 순위 원장에 남기되 노출에서 제외한다.

raw anchor는 원 텍스트에서 `(?<![a-z0-9_])(?:정렬된 matched tokens)(?![a-z0-9_])`를 `re.I`로 검색한 첫 위치다. 점수용 NFKC 정규화와 달리 원문에서 위치를 찾으므로 복원에 실패할 수 있다. 실패 시 offset 0과 fallback을 기록한다.

- A: main 상위 4파일. 경계 B: 같은 main 상위 2 + adjacent 상위 2. 대조 B: A와 동일. 인접 공석을 주 도구로 메우지 않는다.
- 096은 100자 전·600자·짧으면 공백패딩이었다. AF100은 200자 전·최대1,200자·원 문서 끝에서 중단·패딩 없음이다.
- 096 protocol의 `empty slots consume no attempt`와 결과 설명의 빈 파일 과금 사이에 문구 차이가 있다. 실제 공석0이라 수치 영향은 없다. AF100은 사용자 현재 지시를 따라 빈자리·실패도 첫 접근 1회로 과금한다.
- 096은 같은 열린 파일의 절 이동194회를 새 접근으로 세지 않았다. AF100은 이를 F에서만 허용하고, S의 재열람·검색을 금지한다. 표시된 각 구간의 원문 Unicode/UTF-8 경계를 기록한다.

## 선행 결과와 반대조건

사전 전체8쌍은 A만0/B만0/양쪽5/모두미완결3, 경계6쌍은 양쪽4/모두미완결2, 대조2쌍은 양쪽1/모두미완결1이다. P3를 옵션만 허용하는 요청으로 좁힌 사후 민감도는 양쪽4/모두미완결4다. 불일치분모0이므로 승률은 산출 불가다.

동일 연구자가 A/B를 모두 읽었다. 사전 봉인 전 공통 재검토에서 P3 A/B 부분→완결, P4 A 부분→완결, P4 B 반박→완결로 바뀌었다. 원 기록을 보존했지만 독립 발견률은 아니다. 큰 매뉴얼이 main 상위2에 남았다는 사실과 같은 파일 안의 자유 탐색이 새 F/S 비교의 이유다.

밀려난12자리 감사에는 완결 손실0과 별개로 J2의 `tests/jq.test` 누락키/null 원시험 corroboration 손실, J4의 `src/builtin.c` Oniguruma 없는 build 실패조건 설명 손실이 있다. 둘 다 원 사용자 실행 실패로 승격하지 않는다. P3의 원문은 옵션을 물었지만 사전에는 출력 목표만 고정했다. AF100은 이처럼 둘로 읽히는 요구를 후속 답 공개 전에 주 해석·민감도로 봉인해야 한다.

## AF100에서 반복하지 않을 타 분야 예제

096 고정판은 Sphinx v8.1.3 `a1510de4777eaa2e569435f95b05f6f3293d7035`, GDAL v3.10.0 `35a44cc570cdf4dbd55611e4bd61da76e56bc221`, PROJ9.5.1 `41f79ccfe107d3951dac6826f289b55d17cc3b81`이었다.

Sphinx에서는 text 빌더 줄블록/문단, graphviz text/man alt, 기존 캐시의 dot 호출 생략, dot 부재의 HTML DOT fallback, test-ext-graphviz의 inline/외부 DOT·neato·상대 이미지/URL, PNG/SVG 상대경로 검사, `dot -V` 실패 skip을 이미 사용했다.

GDAL/PROJ에서는 WGS84→UTM11 `(32,-117.5,0)`의 grid 없는 대조, EPSG4746→4326 `(50.5,10,0)`와 OnlyBest/BETA2007 부재, gridshift 인수/파일/영역 오류, optional `@`와 null grid, 미리 다운로드 후 network off, 도달 불가 endpoint, 후보 목록 생성만으로 network를 읽지 않는 원 시험을 이미 사용했다. 이 메모는 해당 원 시험을 새로 열거나 실행했다는 주장이 아니다.

## 점검의 한계

이 검토는 선행 고정 파일의 인수와 구현 규칙 확인이다. 새 사례의 정확성·독립성, AF100 패킷 판정, 외부 프로그램 실행은 검증하지 않았다. 096의 session check exit2와 common cloud_check exit0/no_active_sessions를 구별했다. AF100의 계약 상태는 새 명령의 실제 결과로 판단해야 한다.
