## 판단과 적용 범위

**관측 사실:** 이번 여섯 경계 요청에서는 B의 인접 원문이 실제로 노출·열람되었지만, 완결된 답을 오직 B에서 얻은 쌍도 오직 A에서 얻은 쌍도 없었다. 두 대조에서는 허용 범위와 네 노출 파일을 같게 유지했고 완결 판정도 같았다. 이것은 [봉인 pairs.csv](pairs.csv)의 기술 통계이며, “인접 자료는 쓸모없다”거나 두 정책이 일반적으로 동등하다는 추정이 아니다.

**연구자 추론:** 상위 두 자리에 큰 주 도구 매뉴얼이 남아 있었고, 그 한 파일 안에서 여러 절을 조합할 수 있었던 점이 단독 적중이 없었던 결과를 설명할 가능성이 있다. 600자 발췌는 같았지만 이후 읽을 수 있는 전체 파일의 길이·탐색 절 수·인지 비용은 같지 않다. 같은 연구자가 두 경로를 읽었으므로 이 자료는 독립 독자에게서 측정한 발견 확률이나 시간 대비 효율이 아니다. [protocol.json](protocol.json), [194회 절 탐색을 포함한 exposure.jsonl](exposure.jsonl), [독립 접근 감사](evidence/audit/route-audit.md)가 이 구분의 근거다.

**설계 제안:** 결과 카드에는 `후보 목록에 있음 → 실제 원문을 읽음 → 최종 링크로 반환함 → 명시 조건을 완결함`을 서로 다른 필드로 유지한다. 외부 실행 도구가 필요하다는 사실과 외부 프로젝트의 원문 링크를 반드시 반환해야 한다는 사실도 구별한다. P4에서는 외부 TeX/PDF→SVG 처리가 필요하지만, 그 경계를 주 도구의 공식 Lua 예제가 이미 설명한다. 이 제안은 새 정책의 승리를 관측한 것이 아니다.

## 방법과 변경 기록

### 모집·원 조건

Stack Exchange의 현재 공개 질문을 `creation` 오름차순으로 모집하고 같은 시각은 ID 오름차순으로 고정했다. 모집 응답의 질문 필드는 ID·tags·creation_date뿐이다. 점수·채택·답·댓글은 원 응답에서 가렸다. `revisions`로 각 질문의 가장 이른 본문을 취득하고 GUID와 생성 시각을 보존했다. `revision_number=1` 및 생성 시각 일치는 확인됐지만, Stack Exchange의 grace-period 편집으로 최초 게시 바이트가 바뀌었을 가능성은 배제하지 못한다. [frame.csv](frame.csv), [jq 필터·본문 원장](evidence/jq/report.md), [Pandoc 모집 원장](evidence/pandoc/report.md)에 원순번과 제외 이유가 있다.

태그별 첫 경계3개와 첫 대조1개만 골랐고 후순위에서 더 좋은 사례로 교체하지 않았다. jq의 2순위는 이미 채운 내부 대조라 제외했다. jq는5순위, Pandoc은4순위에서3+1이 찼으므로 H2로 확장하지 않았다. 088·092의 고정 이전60 ID와 겹친 신규 ID는0이다. 후순위 jq40개·Pandoc27개는 할당량 충족이라는 이유를 남겼다. jq45개와 Pandoc10개를 직접 읽은 기록은 모집76개의 기계 취득과 구분한다.

경계는 이름이 있는 생산자/소비자와 실제 입출력 동작이 함께 적힌 경우다. J2의 cat은 단순 전달자라는 이유로 탈락시키지 않았다. J4의 jq는 본문이 아니라 모집 태그에만 있고 본문의 `command` 자리에는 구현 선택 여지가 있다. 인접 grep은 본문의 실제 파이프에서 왔으며 태그 조합으로 추가하지 않았다. P2의 Docker는 실행 호스트여서 별도 문서 생산/소비 도구로 세지 않았다. P4의 diagram은 사용자가 시도한 필터이며 반드시 그 필터만 써야 한다는 조건은 없다. P1–P4에는 독립 조건이 하나뿐이므로 둘째 칸은 공석이다. [R0-J1–J4 및 R0-P1–P4](sources.jsonl)의 짧은 원문·GUID·한계가 이러한 분류를 지지한다.

### 고정판·파일 범위·순위

모든 비교판은 질문 생성 전에 공개된 판/커밋이다. 사용자 실제판은 별도 필드이며 `latest`, 컨테이너 태그 또는 비교판을 사용자판으로 간주하지 않았다. [corpus-plan.json](corpus-plan.json)은 jq1.7.1, Pandoc3.6, 고정 Asciidoctor·rmarkdown·diagram·Overpass 커밋, coreutils9.5·grep3.11의 공식 원문 범위를 고정한다. [corpus-files.jsonl](corpus-files.jsonl)의3,560행은 파일 ID·원주소·판·해시·경로를 제공한다. 사전 구축은 archive8회/22,951,621bytes였고 파일명 메타데이터를 검토한 뒤 같은 archive로 한 번 재구축했다. 모델에게 corpus 본문을 보여 주기 전에①을 원격 봉인했다.

NFKC+casefold 후 `[a-z0-9_]+` 토큰의 정확한 집합 일치만 사용했다. 검색 두 벌의 파일별 서로 다른 일치 토큰 수를 세고, 두 결과는 일치 토큰의 합집합으로 다시 정렬했다. 동점은 고정 `repo/path`의 대소문자 구별 사전순이다. 경로명 점수·동의어·어간 추출은 없다. 점수0은 전체 순위에 남기되 노출하지 않았다. 같은 매뉴얼의 미러·다른 판을 추가 결과로 세지 않았고, 한 파일은 한 결과다. A는 주 도구 상위4, 경계 B는 같은 주 도구 상위2+인접 상위2, 대조 B는 A와 같은4를 제시했다. 인접 공석을 주 도구로 채우지 않는 규칙이었으나 이번64자리에는 공석이 없었다.

발췌는 첫 일치 지점의100자 앞부터600자이며 raw-anchor 실패면 offset0, 짧은 파일은 공백 채움으로 고정했다. 이번에는 anchor fallback과 padding이 모두0이었다. 파일을 slot순으로4개 모두 열어 반대조건을 찾는 정책이어서 조기 중단은 없었다. 본문4회 예산은 실패·빈 파일·재시도에도 부과하나 실제 경로에서는 그런 실패가0이었다. 같은 열린 파일의 절 이동은 기록했지만 새 본문 접근으로 세지 않았다. 숨은 디렉터리 탐색, 다른 경로만 읽은 절, 사후 답은 사전 근거로 쓰지 않았다. 독립 감사는48개 순위 파일의43,482행, 동점 관계43,204개, 점수0행33,318개,64발췌를 재계산해 불일치0을 확인했다. [순위 감사](evidence/audit/ranking-audit.md)를 참조한다.

### 공통 기준 재검토와 기억 노출

태그 안의 순서는 A→B, B→A, A→B, B→A로 번갈았다. jq 담당자와 Pandoc 담당자는 서로 다른 태그를 맡았지만, 각자는 자기 태그의 두 경로와 여러 사례를 읽었다. 따라서 두 번째 경로와 뒤 사례에는 기억 노출이 있다. 파일마다 다시 열었음을 기록하는 것은 기억을 없애는 조작이 아니다.

② 이전에 루트가 J4의 문서에 근거한 구체적 filter 합성과 Pandoc의 실행 미확인 판단 사이에서 채점 기준이 일관되는지 확인했다. 원 질문·조건·질의·파일 범위는 바꾸지 않았다. P3의 미연결 `-V` 제안 대신 원 R 문자열에 raw HTML 표지를 넣는 구체적 조합을 만들었고, P4는 공식 RawBlock 예제에 원 TikZ preamble과 SVG 포함 방식을 연결했다. 이미 열린 공통 주 도구 파일만 각 경로에서 다시 읽었다. P3 A/B는 부분→완결, P4 A는 부분→완결, P4 B는 반박→완결로 바뀌었다. 최초 판단8개, 변경시각·이유·해시, 최종 기억 고지를 [pre-review](evidence/pandoc/pre-review/), [evaluation-review.json](evidence/pandoc/evaluation-review.json), [구체 합성안](evidence/pandoc/documentary-syntheses.md)에 보존했다.

이 재검토는 **양쪽 경로를 읽은 뒤의 공통 평가**이며 독립 맹검 발견이 아니다. 추가 본문 접근0, 사후 결과 노출0이라는 절차 준수와 별도로 이 한계를 유지한다. 최종 사전 판단은 `2026-11-23T18:25:06.526715+00:00`에 확정했고② 원격 SHA `d03ca37daf0c43688c68bc39417d84a9b84803e9`의 실제 확인은 `18:27:16.851Z`였다. 최초 공개 후속 HTTP는 그 뒤1.253346초에 시작됐다. [seal2 영수증](evidence/seal2-receipt.json), [최초 사후 열람](evidence/outcomes/first-open.json), [독립 봉인 감사](evidence/audit/source-count-audit.md)가 순서를 확인한다.

## 더 넓은 범위가 잃은 것은 무엇인가

[밀려난 파일 독립 감사](evidence/audit/displacement-audit.md)는 여섯 B 경계쌍이 밀어낸 A의3·4순위 **12/12자리**를 조사했다. 고유 파일은10개이고 A에서 모두 열었다. 그중 실제 판정·반환에 사용한 자리는2/12였다. 명시 조건10개의 A/B 상태는 같았고 A만 완결한 쌍은0/6이었다. 밀려난 파일 하나만을 단독 근거로 기록한 전체 조건도0이었다. 그러므로 요청된 “필수 주 도구 파일이 밀려나 A만 성공한 새 사례”는 이 표본에서 **미관측**이다. 발견하지 못한 사례를 가상 승패로 추가하지 않는다.

그렇다고 손실 자체가 전혀 없는 것은 아니다. J2에서 A는 [JQ-0080의 누락키/null 원 시험](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/tests/jq.test)을 반환했지만 B는 매뉴얼과 cat 문서를 반환했다. 같은 진단은 남았지만 원 시험의 corroboration이 사라졌다. J4에서 A가 반환한 [JQ-0002 regex 구현](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.c)의 **Oniguruma 없는 build에서는 match가 지원되지 않는 구체적 반대조건**이 B의 최종 반환에서 빠졌다. 사용자의 실제 build는 미확인이어서 이것을 B 실행 실패로 바꾸지는 않는다. 완결점수 손실0과 진단·실패조건 설명 손실0은 서로 다른 주장이다.

반대로 B가 더한 자료에도 차이가 있다. [CU-0001/0002](https://git.savannah.gnu.org/cgit/coreutils.git/tree/doc/coreutils.texi?h=v9.5)는 cat의 원바이트 전달을 확인하지만 없는 offset을 만들지 못한다. Overpass의 [OP-1142](https://github.com/drolbr/Overpass-API/blob/a0db4f392f744d5e1304331edbf542ef6d6ce2fa/src/overpass_api/core/index_computations.h)와 [OP-1322](https://github.com/drolbr/Overpass-API/blob/a0db4f392f744d5e1304331edbf542ef6d6ce2fa/src/overpass_api/statements/make_area.cc)는 좌표·영역 계산에서 같은 어휘를 썼지만 연속 JSON 객체 묶기와 맞지 않았다. P1의 Asciidoctor 원 시험2개는 role이 실제 방출된다는 진단을 보강했고, P4의 diagram 원문은 CodeBlock/RawBlock 부조화를 설명했다. 후보 노출6/6을 관련 정답 노출6/6으로 바꾸어 말하지 않는 이유다.

### P3의 “옵션”을 필수 수단으로 읽는 사후 민감도

[R0-P3-POST-REVIEW](https://stackoverflow.com/revisions/1B054996-200D-4090-BAC2-A656EDCBC92D/view-source)의 첫 문단은 Pandoc에 그런 **옵션**이 있는지 묻는다. 사전 C1은 원치 않는 br를 제거하는 출력 목표로 고정했고, raw HTML 표지를 R 값에 추가하는 해법도 허용했다. 이는 동작 목표를 만족시키는 대안이지만 사용자가 물은 수단에 가장 직접적으로 답한 방식은 아니다. “원 문자열 표지를 바꾸지 않고 Pandoc 옵션으로만 답해야 한다”를 필수조건으로 읽으면 사전 raw 합성은 완결로 채점하기 어렵다.

이 해석을 사후에 조용히 넣어 원 승패를 덮어쓰지 않았다. 별도 민감도에서는 P3 A/B를 부분으로 두어 **전체 양쪽4/8·어느 쪽도4/8, 경계 양쪽3/6·어느 쪽도3/6, 대조 양쪽1/2·어느 쪽도1/2**가 된다. A만0/B만0/비교불가0과 불일치분모0은 그대로다. 사후 채택 옵션을 사전 접근에서 발견한 것으로 대체하지 않는다. 변경한 가정·원값·새값·시각·영향 P3를 [별도 기록](evidence/post-evaluation-sensitivity.json)에 고정했고 [metrics.json](metrics.json)에 원행에서 다시 계산한 별도 열을 둔다. 이 민감도는 완결5/8이라는 크기의 조건 의존성을 보여 주며 새로운 맹검 실험이 아니다.

## 사후 공개 행동·실행·다른 해법

[outcomes.csv](outcomes.csv)는 질문자·답변자·연구자 실행, 최초 답 revision과 수정 시각, 현재 채택을 별도 열에 둔다. 원 자료는 [공개 메타데이터·영수증](evidence/outcomes/), [jq 사후 보고](evidence/post-jq/report.md), [Pandoc 사후 보고](evidence/post-pandoc/report.md)에 있다. 답8개는 모두 질문 생성30일 안에 작성됐지만, 현재 채택표지4개가 언제 붙었는지는 알 수 없다. 삭제된 후속은 현재 API로 복원할 수 없으며, “공개 후속 없음”은 실제 시도하지 않았다는 뜻이 아니다.

- **채택과 완결의 불일치 — J2.** [현재 채택 답](https://stackoverflow.com/revisions/4DB44BBE-C949-4542-BB30-1A1951A2B774/view-source)은 배열 전체를 유지해 두 필드를 만드는 스코프 해법이다. 질문자는 [긍정 댓글](https://stackoverflow.com/questions/79388729#comment140003480_79388975)을 남겼다. 그러나 [다른 최초 답](https://stackoverflow.com/revisions/1EF3B84A-D656-4F00-954D-02A25190DC11/view-source)은 start/end를 null로 출력한다. 원 입력에 없는3645/3820과 title/artist 대응을 확정한 실행이 없으므로 사전 부분 판정을 유지한다. 사용자가 핵심 병목을 해결했다고 느끼는 것과 연구자가 예시 전체를 충족했다고 판정하는 기준은 다를 수 있다.
- **주 도구의 다른 절이 답인 사례 — P3 및 J3.** [P3 최초 채택 답](https://stackoverflow.com/revisions/DF73AC92-8281-499B-963C-D995EEE0FB91/view-source)은 Pandoc `markdown_in_html_blocks`를 끄는 옵션이다. 인접 rmarkdown은 인자를 전달하지만 핵심 동작은 Pandoc reader 확장이다. [J3 최초 채택 답](https://stackoverflow.com/revisions/5D70FEFA-D7F3-4AC3-AB07-3FFFAA3DB427/view-source)은 `_nwise(2)`와 add를 쓰며 함수가 undocumented라고 명시한다. 수정판은 `while`·slice 대안을 더했다. 사전에는 같은 원 요구를 주 도구의 range·인덱싱·더하기로 구성했으므로 답과 코드가 같아야만 완결이라는 기준은 쓰지 않았다.
- **인접 도구의 짧은 대안 — J4.** [비채택 최초 답](https://stackoverflow.com/revisions/22082265-DA41-447F-BE2B-81A7024980CE/view-source)은 `grep -Po`와 recursive PCRE로 중첩·빈값·반복 예시의 입출력을 보여 준다. grep의 -P 지원과 literal balanced brackets라는 조건이 있다. 이것은 사후 발견이며 B가 사전에 찾은 구체적 해법이 아니다. jq만으로도 문서 합성안이 있었으므로 grep이 반드시 필요했다는 관측도 아니다.
- **후속에서 목표가 바뀐 사례 — P1.** [질문자 self-answer](https://stackoverflow.com/revisions/6F659201-6815-46E2-BB6F-5C2C61CC5090/view-source)는 Strong 전체를 custom-style=test인 Span으로 바꾼다. 원 simpara의 문단 role별 스타일 전달과 입력/대상이 다르다. 자기 보고 성공은 기록하되 원 요구 완결로 소급하지 않는다.
- **외부 변환이 실제 필요한 조건과 남은 실패 — P4.** [공개 답](https://stackoverflow.com/revisions/04B193AD-FEB3-4D6A-9618-B08ADC4315FF/view-source)은 PDF를 MuPDF로 SVG화하는 명령과 화면을 제공한다. 화면은 별도 SVG를 지지하고 원 LaTeX→HTML 통합·질문자 성공을 입증하지 않는다. 사전 공식 RawBlock 예제 역시 TeX와 PDF→SVG 도구를 호출한다. 외부 단계 필요성은 강하지만, 지정 인접 프로젝트 diagram 자체가 유일 필수라는 뜻은 아니다.

### 이 연구자가 실행한 보조 확인

실행은 모두② 이후이며 사전 접근 예산·승패에 넣지 않았다. 공식 고정 바이너리를 작업 경로의 캐시에만 두었고 시스템 패키지를 설치하거나 봉인 filter를 고치지 않았다.

| 대상 | 실제 입력·판·명령의 위치 | 관측 결과 | 적용 한계 |
| --- | --- | --- | --- |
| J4 | [jq1.7.1 공식 checksum 영수증](evidence/post-jq/download-record.json), [13회 전체 실행 원장](evidence/post-jq/runtime-results.json), 봉인 A/B filter | 원 R0 line/empty 및 연구자 nested/repeat/neighbor/no-marker의4벡터×2경로,8/8 기대출력 일치 | literal balanced 한 줄 문법. 원 사용자 판·실제 grep은 미확인 |
| J4 반례 | 같은 봉인 A filter, 연구자가 추가한 `specificword=["]"] status=ok` | exit0이지만 `specificword=["]`로 조기절단. JSON quoting 의미를 기대한 출력과 불일치 | 원 R0가 요구하지 않은 문법 확장 반례. 사전 조건을 사후 추가해 패배로 바꾸지 않음 |
| J1 | 잘린 R0 JSON 및 닫힘만 최소 수리한 입력, 봉인 filter | 원 조각 exit5; 수리본은3행 정확 일치 | 수리본 성공은 원 사용자 완전 입력이나 실행 성공이 아님 |
| J3 | 연구자 `.elements` envelope와 원 단순 배열 변형, jq1.7.1 | 두 실행 기대출력 일치 | 실제 Overpass 전체 질의·입력은 없음 |
| P3 | [Pandoc3.6 실행 원장](evidence/post-pandoc/execution.json); 원 SIGNATURE/template를 쓴 합성 post-knitr Markdown | 기본 표 안 br38; 봉인 raw 표지0; 사후 옵션0. 세 실행 exit0. 두 수정안 출력은 바이트 동일, 원 table 보존 | R 미설치로 실제 R→knitr→Pandoc 전체는 미실시. 사용자2.11.2/3.1.11 실행과 비교판3.6 구별 |
| P4 | 같은 Pandoc3.6; 원 TeX, 봉인 RawBlock Lua | AST exit0, RawBlock2개 중 TikZ1개. 전체 filter exit83, 내부 pdflatex exit1 | `pdflatex.fmt` 부재. pdf2svg·TeX 패키지도 미설치. 생성 SVG/HTML 그림 성공은 미확인 |

재현에 필요한 짧은 jq 입력·필터·stdout·stderr는 [validation](evidence/post-jq/validation/)에 있다. `prepare_runtime.py`와 `reproduce_runtime.py`는 새 checkout 재현용이며 wrapper 자체는 구문만 검사했다; 실제 관측은 두 원 runner의13회다. Pandoc 입력은 [prepare-probes.py](evidence/post-pandoc/prepare-probes.py)가 고정 revision GUID와 hash로 재구성하며 재구성 exit0을 확인했다. [run-probes.py](evidence/post-pandoc/run-probes.py)는 봉인 filter hash를 확인한다. P4 의존성을 갖춘 환경에서 실행할 명령과 입력은 이 파일 및 마지막 HANDOFF에 남긴다.

## 다른 분야 대조: 알려진 경계와 새 요청 발견의 구별

[Q7 상세 보고](evidence/crossdomain/report.md)는 Sphinx v8.1.3 `a1510de4777eaa2e569435f95b05f6f3293d7035`, GDAL v3.10.0 `35a44cc570cdf4dbd55611e4bd61da76e56bc221`, PROJ9.5.1 `41f79ccfe107d3951dac6826f289b55d17cc3b81`의 공식 명세·실제 conf·원 fixture·회귀 기대값14개를 대조했다. 이것은 이미 지정된 교정 사례로서 신규 모집0/경로0이며, 이를 찾아내는 정책의 승률은 **산출 불가(신규 탐색 분모0)**다. 이 환경에서 그 상류 시험을 실행한 것으로 쓰지 않는다.

| 목표 | 원래 경로 안에서 끝나는 대조 | 외부 입력/호출이 없으면 깨지는 조건 | 틀리는 전제와 직접 근거 |
| --- | --- | --- | --- |
| Sphinx 자체 출력과 그래프 | text 빌더는 문단·표 문자열을 출력하며 Graphviz node의 text/man도 `[graph]`/alt로 표현한다. 이미 생성된 해시 경로의 그림은 dot 호출 전에 캐시로 반환한다. | 캐시되지 않은 DOT를 새 PNG/SVG/PDF로 만들어야 하면 dot subprocess에 원문을 stdin으로 넘겨야 한다. dot 부재 시 HTML에는 escaped DOT fallback이 나와도 원 목표 그림은 없다. | “HTML 파일 생성=그림 생성”, “확장 설정=실행파일 설치”, “초록 시험=Graphviz 실행”은 성립하지 않는다. [Q7-S2 구현](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/sphinx/ext/graphviz.py#L260-L343), [Q7-S6 자체 text 원시험](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/test_builders/test_build_text.py#L42-L55), [Q7-S8 dot -V 실패 시 skip](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/sphinx/testing/fixtures.py#L224-L239) |
| GDAL 변환과 PROJ grid | WGS84→UTM 원시험의 grid_req=None는 별도 데이텀 grid가 없는 대조다. PROJ 라이브러리 자체까지 불필요하다는 뜻은 아니다. 로컬 grid를 미리 받으면 network off에서도 변환할 수 있다. | EPSG4746→4326, (50.5,10,0), OnlyBest=True는 de_adv_BETA2007.tif가 없으면 예외를 기대한다. False의 수치 출력은 원 '최선만' 조건을 낮춘 결과다. | “후보가 보임=grid 읽음=정확 변환”, “수치 반환=같은 정확도”는 성립하지 않는다. [Q7-G2 only-best 시험](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/osr/osr_ct.py#L573-L597), [Q7-G3 grid 없는 투영](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/osr/osr_ct_proj.py#L30-L57), [Q7-G7 후보 생성 시 network 활동 없음](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/test/unit/test_network.cpp#L2246-L2281) |

PROJ의 optional `@` grid나 `null` 0이동은 오류 회피와 요구 정확도 충족을 분리하는 추가 반례다. grid 파일이 존재해도 입력 좌표가 유효 영역 밖이면 실패할 수 있고, 도달 불가 endpoint는 객체 생성 후 실제 변환에서 실패한다. [Q7-G5](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/docs/source/usage/transformation.rst#L328-L368), [Q7-G6](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/test/gie/gridshift.gie), [Q7-G7](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/test/unit/test_network.cpp#L1237-L1291)을 직접 읽었다. 호출 경계는 이름이 다른 실행 단계뿐 아니라 추가 데이터 자원의 가용성일 수도 있다는 것이 연구자의 추론이다.

## 재계산·봉인·검사 범위

`assemble_result.py`는 원 `pairs.csv`·16개 judgment/access/exposure로 세 표와 분모를 다시 만들고② metrics와 일치함을 확인한다. `build_sources.py`는 원 자료의 필드를 정규화하되 원 행 전체와 위치도 보존하고 URL·본문 hash 중복을 제외한다. 별도 감사자는 순위·접근·46자료·밀려난12자리를 독립 코드로 검산했다. 해당 감사의 최초 결과·오탐 수정·경고를 지우지 않았다. 예컨대 서로 같은 `tests/manual` 시험 입력을 매뉴얼 미러로 오인했던 초기 감사는 남기고 분류기만 고쳤다.

①의42개 대상 중39개는 바이트 그대로,3개의 CSV는 저장소 `.gitattributes`의 CRLF→LF 정규화 뒤 같았다. ②의169개 대상 중168개는 바이트 그대로, `pairs.csv`는 같은 EOL 정규화 뒤 같았다. 이를 전부 원 바이트 완전일치로 보고하지 않는다. 결과 GitHub 재열람은 원격 Git blob의 정규화된 바이트와 비교한다. 원격 묶음 SHA와 최종 대상 SHA·검사 명령·종료값은 [HANDOFF.md](HANDOFF.md)에 둔다. 마지막 HANDOFF는 결과 검사 이후의 별도 단독 커밋이므로 이전 검사 SHA에 포함됐다고 하지 않는다.

지정 계약 명령은 `work/research-af-res-092=e0d7ecda64bab2bd5d5779a9fb2a18d39a83bcdf`를 요구하지만 현재 원격 끝은 `e742bc665efde0d3883ec4d0f5479e03e914fcbf`여서 종료값2로 거부됐다. `manifest.json`은 그 실패·의도한 시작판/경로/고정 의존·계약 스냅샷을 보존한 영수증이고 성공 manifest가 아니다. 연구 인수 자료를 새 끝으로 몰래 바꾸거나 검사기를 약화하지 않았다. 중앙 진행표와 다른 경로는 수정하지 않으며, 고정 과거 결과를 의존으로 허용할 계약 정합 처리는 진행 담당에게 인계한다. 공통 검사의 `no_active_sessions`는 새 세션 계약 통과를 뜻하지 않는다.

## 가장 중요한 불일치와 약점 — 정확히 3건

| 틀릴 수 있는 주장 | 다음 조사 대상·입력·방법 | 판정을 바꿀 관측 |
| --- | --- | --- |
| **1. “인접 원문 두 자리를 보장해도 완결 이득·손실은 없다.”** 이번0불일치는 큰 매뉴얼이 상위2자리에 남은 파일 단위 예산과 같은 연구자의 사후 공통 평가에 의존할 수 있다. J2/J4에는 점수 밖 corroboration·실패조건 설명 손실이 실제 있었다. | 새로운 공개 요청을 같은 생성순 모집으로 고정하되 다른 작업에서 절 단위와 파일 단위 예산을 별도 사전 등록하고, 서로의 읽기·해법을 모르는 독자에게 A/B를 배정한다. 밀려난 필수 절과 반환 실패조건도 추적한다. 기존8질문의 답을 알고 재실험한 값을 신규 발견률로 쓰지 않는다. | 같은 원 요구·같은 예산에서 인접 원문만이 필요한 중간 형식을 지지한 B만 완결, 또는 밀려난 주 도구 절만이 필수조건을 지지한 A만 완결이 실제로 관측되면 이번 결과의 일반화가 깨진다. |
| **2. “문서상 완결5쌍은 원 사용자에게 실행 가능한 완결답이다.”** 사용자판/전체 입력은 미확인이고 P4 실행은 의존성에서 실패했다. P3를 옵션만의 답으로 좁히면 양쪽완결은4/8이다. J2 긍정 후속은 모든 숫자를 입증하지 않으며 J4는 quoting 확장에 실패한다. | 우선 P4 원 TeX·봉인 Lua를 TeX standalone/xcolor/tikz·pdf2svg가 있는 정확한 환경에서 실행해 그림의 노드·간선·HTML 포함을 확인한다. 다음으로 P3의 옵션만 허용 여부와 실제 R4.4.2/rmarkdown2.29/Pandoc3.1.11.1 원 Rmd, J2 offset 원 입력, J4 문자열 문법을 고정한다. 원 사용자 실행과 연구자 재현을 따로 기록한다. | 같은 명시 조건·원 입력·사용판에서 봉인안이 그림/줄바꿈/배열 대응을 충족하지 못하거나 사용자 요구 수단을 바꾸면 실행 가능한 완결 주장은 철회한다. 전체 산출물·판·명령이 재현되면 '실행 미확인'을 줄일 수 있다. 사전 승패와 사후 민감도는 별도 열로 보존한다. |
| **3. “본문의 생산자/소비자 명명 규칙이 중요한 외부 경계를 포괄한다.”** cat 같은 단순 전달자도 포함하며 J4 주 도구는 태그에만 있다. GDAL의 grid는 앞뒤 실행 단계가 아닌 추가 입력 자원이고 Q7은 미리 지정된 교정 사례다. | 별도 신규 요청 모집에서 실행 단계·라이브러리·데이터 자원 경계를 사전 구분한다. Sphinx는 깨끗한 캐시에서 dot 유무, GDAL은 (50.5,10,0)·OnlyBest·BETA2007 유무/해시/영역을 고정하여 실제 출력·skip·오류를 기록한다. 새 요청에서 그 자료를 찾는 비용도 별도로 측정한다. | 이름 있는 생산자가 없어도 추가 자원만으로 성패가 갈리는 요청이 반복되거나, 외부 실행이 필요해도 주 도구 원문만으로 모든 경계가 완결되는 요청이 많으면 현재 명명 규칙을 제품의 일반 탐색 규칙으로 확대할 근거가 약해진다. |
