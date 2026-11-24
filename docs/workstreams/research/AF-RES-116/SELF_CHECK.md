# AF-RES-116 SELF_CHECK — Q1~Q7 근거·분모·미확인 대사

## 점검 범위와 현재 판정

이 문서는 가림 의미 판정이 끝난 뒤 전체 소유 원장을 공개한 상태에서 수행한 후속 대사다. 원래 가림 판정은 각 수신자의 누적 표시만을 근거로 했으며, 이 점검에서 새로 읽은 조건 매핑·다른 판정·기준자료를 그 판정에 소급하지 않는다. 가림 판정 파일은 수정하지 않았다. 이 문서를 추가 독립 가림 평가나 원 소프트웨어의 재실행으로 해석하지 않는다. [Pandoc 평가 범위·종료·입력](evaluation/evaluator-pandoc.json#L27-L69), [ImageMagick 평가 범위](evaluation/evaluator-imagemagick.json#L5-L28)

**실제 수신은 18/18꾸러미·54/54단계를 마쳤고, 마지막 답의 full_supported는 0/18이다.** 단계별 부분 복원은 8/54, 관련 문서상 예외 flag는 4/54, 위험한 확정은 0/54다. 정당한 보류와 부분 복원은 동시에 성립할 수 있어, 보류 flag는 54/54이지만 primary grade의 보류는 46/54다. 이는 반복 단계 관측의 합계이며 54개의 독립 사건이나 실제 실패 재현 횟수가 아니다. [수신 분모](analysis/trial-summary.json#L5-L24), [Pandoc 판정 27행](evaluation/judgments-pandoc.jsonl#L1-L27), [ImageMagick 판정 27행](evaluation/judgments-imagemagick.jsonl#L1-L27), [단계 판정 규칙](SCOPE.md#L39-L47)

| 대사 항목 | 현재 원장 값 | 해석과 근거 |
| --- | ---: | --- |
| 모집 frame | 50+50=100행 | 순서 검증과 직접 body 선별을 구별한다. [frame 검증](evidence/audit/checks.json#L16-L60) |
| 직접 선별·선정·제외·미선별 | 9 / 6 / 3 / 91 | 91행은 순차 모집 종료 뒤 미선별이며 실패 사례가 아니다. [선별 원장](recruitment/audit/screening.json#L5-L30) |
| 최종 출처 원장 | 273행 | 현재 `source_rows`와 실제 행수를 대조했다. 원장 행수는 저작 수·수신 개봉 수가 아니다. [최종 집계](analysis/source-counts.json#L2-L12), [추가 감사 기록](sources.jsonl#L237-L260) |
| 고유 산입 저작 | 37 | 필수 분류 34개와 선별용 원문 3개다. [분류·고유 수](analysis/source-counts.json#L5-L26) |
| 필수 분류의 목표 → 실제 | 6/8/6/4 → 6/9/6/13 | 자연 요청 / 정의·구현 / 별도 회귀·반대 입력 / 보조 비교. 목표 24와 실제 34를 비교하며 선별 3개는 넣지 않는다. [분류별 집계](analysis/source-counts.json#L6-L26) |
| primary target의 3개봉 도달 | 0/6 | 여섯 선언 구간 모두 고정 그래프에서 불가. 아래 Q2의 사건별 원장 참조. |
| 완전 답 근거의 도달성 | 불가 4 / unknown 2 / reachable 0 | P3·I3의 원 입력·환경 결손을 불가로 바꾸지 않는다. 아래 Q2 참조. |
| 수신의 미시작·조기 종료 | 각각 0꾸러미·0단계 | 관측 누락이 없는 것과 질문의 모든 증거가 있는 것은 별개다. [수신 집계](analysis/trial-summary.json#L5-L24) |
| 인용 전사 오류 | 1건 | `A image setting`의 n 누락. 위험한 확정이나 전체 과제 오답과 구별했다. [I2 C, 단계 2](evaluation/judgments-imagemagick.jsonl#L11), [인용 대사](analysis/trial-summary.json#L575-L582) |

출처 수의 변화도 별개 단위로 대사했다. 기존 기준자료 봉인의 검사 대상은 195행이었다. 여기에 실제 수신 표시 54행과 감사 재열람·접속시도 24행을 추가한 현재 원장이 273행이다. 뒤의 두 묶음은 고유 저작을 추가하지 않으며, 현재 고유 수는 37을 유지한다. 감사 이전 행수를 최종 확정값으로 재사용하지 않는다. [기준 봉인 검사 대상](evidence/audit/checks.json#L4-L15), [수신 반복 행 처리](evidence/audit-resolutions.json#L10-L14), [감사 24행](evidence/audit/source-reads.jsonl#L1-L24), [현재 집계](analysis/source-counts.json#L2-L26)

최종 검증 대상 SHA, 원격 재열람, 고정판 검사 명령·종료값과 인수 상태는 **[acceptance-evidence.json](evidence/acceptance-evidence.json)**의 확정 기록을 따른다. 이 문서에는 아직 결정되지 않은 최종 SHA나 검사 PASS를 선기입하지 않는다. 결과 커밋 이후 재열람·검사·영수증·HANDOFF를 분리한다는 완료 순서도 유지한다. [완료 규칙](SCOPE.md#L49-L51)

## Q1. 어떤 요청을 누구에게 넘겼는가?

**답 / 미확인.** 2023~2025년 공개 이슈를 프로젝트별 첫 50개로 고정하고, 원문에 조작 O와 보존 P가 함께 나타난 첫 세 건씩을 선택했다. 검색 어구는 모집 규칙이지 사건의 실제 주제 분류가 아니다. 예를 들어 P1의 `image`는 스크린샷 alt에 나타났으며 P1을 표·그림 변환 사건으로 바꾸지 않았다. 원 body는 현재 공개 스냅샷이며 최초 게시 당시의 미편집 원문을 복원했다는 뜻도 아니다. [모집 규칙](SCOPE.md#L9-L20), [선별과 P1의 어구 한계](recruitment/audit/screening.json#L17-L49)

| 사건 | 직접 원 요청 URL | 고정 판과 넘긴 O/P | 정상·반대 입력의 범위 |
| --- | --- | --- | --- |
| P1 | [Pandoc #8518](https://github.com/jgm/pandoc/issues/8518) | 2.19.2, HTML+TOC에서 B1/B2의 같은 그룹과 TOC 포함 유지 | A1/A2와 B1/B2는 원문 대조. 실행 재현은 아님. [사건 기록](cases.json#L7-L70) |
| P2 | [Pandoc #8522](https://github.com/jgm/pandoc/issues/8522) | 원 판 미지정, 연구 고정판 3.8.3. 설명·주석 원본을 직접 읽으며 bare 약어 집합 유지 | 설명 붙은 행은 도식 예시이며 전체 YAML·약어 목록 없음. [원 요청](cases.json#L72-L135), [고정판의 뜻](gold-work/pandoc/gold-notes.md#L61-L77) |
| P3 | [Pandoc #8526](https://github.com/jgm/pandoc/issues/8526) | 2.14.0.3, 표·그림 유지 및 실제 다음 페이지 float 뒤 하단 여백 보존 | 표 제거·그림 대체는 저자 보고. 원 body에는 output·engine·명령 없음. [사건 기록](cases.json#L137-L211) |
| I1 | [ImageMagick #6159](https://github.com/ImageMagick/ImageMagick/issues/6159) | 7.1.1-3, gray 정보를 meta로 추가하며 RGB 의미·외관 보존 | 원 입력·출력 첨부와 명령은 있으나 당시 viewer 해석은 body에서 미상. [사건 기록](cases.json#L213-L286) |
| I2 | [ImageMagick #6187](https://github.com/ImageMagick/ImageMagick/issues/6187) | 7.1.1-4, TIFF에서 원 채널 내용이 남는 PNG 추출 | 이전 판 성공·새 판 흰 출력은 저자 보고이며 별도 정상 PNG는 없음. [사건 기록](cases.json#L288-L351) |
| I3 | [ImageMagick #6237](https://github.com/ImageMagick/ImageMagick/issues/6237) | 7.1.1-6, JP2의 실제 색·채널 의미 유지 | 정상 RGB 기준값 없음. 4 components를 RGBA로 확정하지 않는다. [사건 기록](cases.json#L353) |

**직접 근거 / 실행 원장.** 실제 수신자는 원저자가 아니라 `fork_turns none`으로 시작한 AI 문맥 18개다. 같은 부모 모델 설정을 상속했으며 정확한 provider 모델 식별자·seed는 노출되지 않았다. 공통 시작점은 [Pandoc 매뉴얼](https://pandoc.org/MANUAL.html)과 [ImageMagick 명령행 진입점](https://imagemagick.org/script/command-line-processing.php)을 고정판 로컬 뷰어로 가공한 것이다. 실제 원저자 인계나 live HTTP 도착으로 부르지 않는다. [실행 18행](evidence/reader-launches.jsonl#L1-L18), [시작점 정의](SCOPE.md#L19-L20), [뷰어 방식](SCOPE.md#L31-L37)

**반증에서 확인한 것.** 원문의 기대를 이미 관측된 사실로 바꾸지 않았다. I3의 `4 components`와 grayscale 표시는 양립 가능성의 조사 대상이며, 원파일을 확보하지 못한 상태는 색 손실의 증명이 아니다. P3의 표 제거 대조는 “표를 유지해도 보존”의 성공이 아니다. [I3 원입력 결손·규격 구분](gold-work/imagemagick/gold-notes.md#L80-L98), [P3의 후속 증거 층](gold-work/pandoc/gold-notes.md#L83-L103)

**원래 / 실제 분모·결손.** 원래 100행 frame에서 직접 선별한 9행 중 6개가 자연 표본이며 3개는 제외, 91개는 미선별이다. 자연 사건·꾸러미를 사후 교체한 기록은 없고 실제 수신은 18/18이다. 다만 모집 감사자는 부모의 후보 검토를 상속했으므로 독립 가림 선별 일치도로 사용할 수 없다. [선별 원장](recruitment/audit/screening.json#L17-L30), [원요청 봉인 기록](evidence/seals.jsonl#L2), [수신 분모](analysis/trial-summary.json#L5-L24)

**판단을 바꿀 다음 관측.** 원문 body 해시·선정 순번·O/P 추출이 잘못됐다는 직접 원문이 나오면 사건 적격성과 인계 문장을 다시 평가해야 한다. 과거 미편집 원문, P2 전체 YAML, P3 정확 렌더 환경, I3 원 JP2와 band 정의가 확보되면 각 결손을 닫을 수 있다. 새 자료를 기존 수신자가 이미 읽은 증거로 소급하지 않는다. [선별 원문 해시 검사](evidence/audit/checks.json#L60-L90), [P2 결손](gold-work/pandoc/gold-notes.md#L77-L81), [I3 다음 입력](gold-work/imagemagick/gold-notes.md#L92-L98)

## Q2. 3개봉 안에 답과 예외를 읽을 경로가 존재했는가?

**답 / 미확인.** 선언된 primary target는 **6/6 모두 고정 뷰어의 3개봉 안에 완전히 표시되지 않는다.** 완전한 O/P/필수 E 근거의 의미 도달성은 P1·P2·I1·I2가 불가, P3·I3는 unknown이다. 뷰 그래프를 전부 열거했더라도 미확보 원 입력·환경 때문에 의미 기준이 닫히지 않은 두 사건을 불가로 바꾸지 않는다. 이 판정은 봉인된 문서면·이동·예산에 한정되며, 인터넷 전체나 원 소프트웨어의 작업 가능성 판정이 아니다. [도달성 정의](SCOPE.md#L39-L43)

| 사건 | primary target | full 의미 도달성 | 관련 근접 구간 | 실행 원장 행 |
| --- | --- | --- | --- | --- |
| P1 | 불가 | 불가 | fenced Div 입력 문법은 3회 내 가능 | [target/full/근접](reachability.jsonl#L1-L3) |
| P2 | 불가 | 불가 | 약어 loader의 결정적 구현은 corpus 밖 | [target/full](reachability.jsonl#L12-L13) |
| P3 | 불가 | unknown | figure 문단 3회, LaTeX layout 구간 2회 내 가능 | [target/full/근접](reachability.jsonl#L19-L22) |
| I1 | 불가 | 불가 | 채널 의미 결정에 원 TIFF·규격·구현 필요 | [target/full](reachability.jsonl#L31-L32) |
| I2 | 불가 | 불가 | 부분 Extract/Set 노출과 전체 선언 target 충족은 다름 | [target/full](reachability.jsonl#L38-L39) |
| I3 | 불가 | unknown | JP2 capability 표지는 파일별 색·채널 답이 아님 | [target/full](reachability.jsonl#L45-L46) |

**직접 근거 / 실행 원장.** 각 행의 `graph_complete`, 선언 구간, matching paths, `interval_reachability`와 `semantic_reachability`를 구별해 검토했다. 첫 열람도 1회이고 매 표시 총량은 내비게이션 포함 최대 1,500자다. 정확한 source offset·표시 hash가 있는 실제 노출과, 가능한 모든 경로 열거는 별도 자료다. [예산 규칙](SCOPE.md#L31-L37), [완전 열거와 실제 관측의 분리](reachability.jsonl#L1-L3), [54개 실제 표시 검증](analysis/trial-summary.json#L17-L26)

**반증에서 확인한 것.** “주 목표에 못 갔으니 관련 정보도 전혀 없다”는 해석은 P1의 문법 구간과 P3의 figure/layout 구간으로 제한된다. 반대로 그 근접 구간이 reachable이라는 사실이 full을 reachable로 바꾸지도 않는다. P1의 Div 문법은 결정적 TOC 순회 조건을 제공하지 않으며, P3의 geometry는 실제 float+table 여백 보존 증거가 아니다. [P1 구조 경로](reachability.jsonl#L3), [P1 가림 판정](evaluation/judgments-pandoc.jsonl#L21), [P3 누적 판정](evaluation/judgments-pandoc.jsonl#L14-L18)

**원래 / 실제 분모·결손.** 자연 사건 6개 중 완전 근거의 reachable opportunity 분모는 **0개**다. 4개 불가와 2개 unknown을 6개 실패나 6개 성공 기회로 합치지 않는다. 수신 18/18을 마쳤어도 이 분모는 증가하지 않는다. 따라서 이 자연 표본의 일반 효과율은 `null`이며 0%라는 효과 추정값으로 대체하지 않는다. [사건별 full 원장](reachability.jsonl#L2), [P2](reachability.jsonl#L13), [P3](reachability.jsonl#L20), [I1](reachability.jsonl#L32), [I2](reachability.jsonl#L39), [I3](reachability.jsonl#L46), [미관측 효과 규칙](SCOPE.md#L51)

**판단을 바꿀 다음 관측.** 동일한 봉인 문서면·허용 이동·3회 예산 안에서 선언 O/P/E를 모두 덮는 재생 가능한 경로가 제시되면 해당 불가 판정을 수정한다. P3/I3는 먼저 결손 입력을 확보해 의미 기준을 완성해야 한다. 예산·시작 링크·corpus를 바꾼 경로는 새 설계의 증거로만 비교한다. [도달성 규칙](SCOPE.md#L41), [P3 full의 missing_inputs](reachability.jsonl#L20), [I3 full의 missing_inputs](reachability.jsonl#L46)

## Q3. 한 줄은 새 정보를 주었고 제작 부담은 기록됐는가?

**답 / 미확인.** B는 원 요청의 보존조건 재진술, C는 실제 목차 표지 하나를 추가했다. 여섯 사건에서 B/C 유니코드 문자 수는 각각 같고 79~94자 범위다. 바이트 수는 다르다. C 표지는 P1 `Divs and Spans`, P2 `Reader options`, P3 `Images`, I1/I2 `Command-line Options`, I3 `Input Filename`이다. 표지가 새 정보라는 것과 충분한 답에 도움이 됐다는 것은 별도 판정이다. [문구 검사](authoring/packet-check.json#L3-L64), [작성 규칙](SCOPE.md#L24-L29)

**직접 근거 / 실행 원장.** 문구 제작자는 공통 요청과 목차 metadata만 읽은 새 문맥으로 기록됐고, gold·증인 경로를 읽지 않았다고 명시됐다. B의 원문 연결은 어구별 의미 대응이며 영문·한국어의 글자 일치가 아니다. 같은 이름의 두 `Reader options` 표지를 제거하거나 유리하게 정리하지 않았다. [제작 역할·한계](evidence/roles.json#L37-L52), [B의 원문 어구 연결](authoring/phrase-provenance.jsonl#L1), [문구 검사 의미](authoring/packet-check.json#L14-L20), [대응 방식](authoring/packet-check.json#L59-L64)

**반증에서 확인한 것.** K2에서는 같은 `Reader options` 이름의 다른 fragment가 필수 예외를 주지 않는다. 자연 P2에서는 A/B/C가 모두 같은 첫 Reader options와 다음 구간을 읽었고 약어 파일 본문에 도달하지 못했다. 즉 새 표지 하나만으로 정보 증가나 조건 복원이 보장되지 않는다. [K2 동일 표지·다른 fragment](calibration/preregistered-cases.json#L61-L95), [P2 실제 노출](trails.jsonl#L10-L18), [P2 판정](evaluation/judgments-pandoc.jsonl#L4-L12)

**원래 / 실제 분모·결손.** 여섯 사건의 B/C 열두 문장을 만들었다. 공유 제작 구간은 560.956346 wall 초, 실제 연구 파일 읽기 5회로 기록됐다. 이 시간은 대기·도구 지연을 포함하며 사건별 제작시간과 사람 능동시간은 없다. 전체 목차 전송은 잘렸으므로 121,700자/121,706바이트를 실제 노출량으로 세지 않는다. 이후 7,815자/7,815바이트의 목차 후보 투영은 별도로 기록됐다. [제작 읽기·잘림 정정](authoring/author-exposure.jsonl#L1-L6), [공유 제작 부담](authoring/author-exposure.jsonl#L7)

**판단을 바꿀 다음 관측.** 봉인 전 작성자가 본문·gold·증인 경로를 보았다는 접근 증거나, C 표지가 실제 노출 목차에 없었다는 원문이 나오면 작성 가림/새 정보 판정을 재검토한다. 효과 판단은 새 reachable 사건에서 같은 부담 기록과 가림 수신을 추가해 평가해야 한다. [실제 역할의 노출 한계](evidence/roles.json#L37-L52), [작성 동결과 부담 한계](authoring/author-exposure.jsonl#L7), [reachable 분모의 필요](SCOPE.md#L41-L51)

## Q4. 독자는 어느 순간 다른 길을 골랐는가?

**답 / 미확인.** 실제 표시 hash·문서·offset 열을 대조하면 **A/B는 6/6 사건에서 동일한 세 view를 보았다.** C가 다른 view를 본 자연 사건은 P1·P3 두 건이다. 이는 동일한 링크 ID를 눌렀다는 뜻이 아니다. I1·I2에서는 다른 링크 ID가 같은 view로 연결되는 경우도 있으므로 행동열과 노출열을 합치지 않는다. [P1](trails.jsonl#L1-L9), [P2](trails.jsonl#L10-L18), [P3](trails.jsonl#L19-L27), [I1](trails.jsonl#L28-L36), [I2](trails.jsonl#L37-L45), [I3](trails.jsonl#L46-L54)

| 사건 | A/B 노출 경로 | C의 분기 시점·결과 | 직접 실행 근거 |
| --- | --- | --- | --- |
| P1 | 시작 → General writer options → 다음 구간 | 2회째 목차 다음 구간, 3회째 Divs and Spans. 선택 이유에 안내 표지를 언급 | [A/B](trails.jsonl#L1-L6), [C](trails.jsonl#L7-L9) |
| P3 | 시작 → Creating a PDF → Variables for LaTeX | 2회째 목차 다음 구간, 3회째 Images. figure 전제·형식 예외 확인 | [A/B](trails.jsonl#L19-L24), [C](trails.jsonl#L25-L27) |
| P2·I1·I2·I3 | 조건별 실제 view 동일 | 새로운 C 표지가 같은 도착을 낳음 | [P2](trails.jsonl#L10-L18), [I1~I3](trails.jsonl#L28-L54) |

**직접 근거 / 실행 원장.** ABC·ACB·BAC·BCA·CAB·CBA의 사건별 배정과 18개 별도 AI 문맥, 매 선택의 이유·직전 답·표시 hash를 남겼다. 인간 참여자는 0이며 OS 격리는 없다. 같은 모델 설정을 상속한 AI의 문맥 분리는 인간/다른 모델 집단의 독립 반복이 아니고, exporter도 모델 문맥의 독립성이나 다른 파일 비접근을 증명하지 않는다. [순서와 가림](SCOPE.md#L28-L29), [실행 문맥](evidence/reader-launches.jsonl#L1-L18), [역할 한계](evidence/roles.json#L3-L5), [기계 검사 한계](analysis/README.md#L57-L63)

**반증에서 확인한 것.** “C가 길을 바꾸면 충분한 재구성도 좋아진다”는 해석은 P1이 제한한다. C는 관련 구조 절에 도착했지만 원 그룹의 TOC 구성원 보존이나 필수 E3를 복원하지 않았다. P3에서는 A/B의 PDF·여백 조건과 C의 figure·형식 조건이 서로 달랐으며, C의 결과를 전체 조건상 우월한 답으로 바꾸지 않는다. [P1 C 판정](evaluation/judgments-pandoc.jsonl#L21), [P3 A/B/C 판정](evaluation/judgments-pandoc.jsonl#L2-L3), [P3 A/C](evaluation/judgments-pandoc.jsonl#L14-L18)

**원래 / 실제 분모·결손.** 18꾸러미의 54단계가 모두 관측·답변됐다. 여섯 사건에 각 조건 한 번씩이므로 같은 사건·조건의 반복 표본은 없다. paired 비교의 단위는 여섯 사건씩의 A↔B/B↔C/A↔C, 총 18쌍이며 54단계를 독립 표본으로 늘리지 않는다. 사람 선택·능동시간·채택은 미관측이다. [계획·쌍 정의](SCOPE.md#L28-L36), [완료와 쌍 분모](SCOPE.md#L51), [실제 수신](analysis/trial-summary.json#L5-L24)

**판단을 바꿀 다음 관측.** 동일 view로 분류한 두 표시의 hash/본문이 다르거나 원 선택 이유가 틀리게 옮겨졌다는 로그가 있으면 해당 대사를 수정한다. 단서의 선택 효과를 일반화하려면 reachable 사례와 사건·조건 반복 또는 다른 독자군의 독립 관측이 필요하다. 현재 관측은 선택과 노출의 차이를 기술하며 일반 인과효과를 추정하지 않는다. [실제 선택·hash 원장](trails.jsonl#L1-L54), [관측 없는 효과의 처리](SCOPE.md#L51)

## Q5. 가까운 절 도착이 충분한 판정으로 이어졌는가?

**답 / 미확인.** full은 마지막 답 기준 0/18, 전체 단계 기준 0/54다. 부분 복원은 Pandoc 5단계와 ImageMagick 3단계를 합친 8/54이고, 위험한 확정·label_only·unsupported_or_wrong의 primary grade는 모두 0이다. 보류를 제대로 설명한 답을 단순 라벨 일치로 처리하지 않았고, 무관한 매뉴얼 사실을 과제 부분 복원으로 올리지 않았다. [Pandoc 집계·규칙](evaluation/evaluator-pandoc.json#L29-L34), [Pandoc 수](evaluation/evaluator-pandoc.json#L70-L91), [ImageMagick 수](evaluation/evaluator-imagemagick.json#L50-L70)

**직접 근거 / 실행 원장.** 다음은 불변 가림 판정을 조건 매핑과 사후 결합한 대사다. `partial`·`counterexample`는 단계 flag이며 final packet 성공 수가 아니다. [조건 매핑](evaluation/masking-map.json#L1-L110), [Pandoc 원판정](evaluation/judgments-pandoc.jsonl#L1-L27), [ImageMagick 원판정](evaluation/judgments-imagemagick.jsonl#L1-L27)

| 지표 | A | B | C | 합계 / 분모 |
| --- | ---: | ---: | ---: | ---: |
| 마지막 full_supported | 0/6 | 0/6 | 0/6 | 0/18 |
| 부분 복원 단계 | 3/18 | 3/18 | 2/18 | 8/54 |
| 관련 문서 예외 flag | 1/18 | 1/18 | 2/18 | 4/54 |
| 위험한 확정 단계 | 0/18 | 0/18 | 0/18 | 0/54 |
| 작은 인용 전사 오류 | 0 | 0 | 1 | 1건 |

**반증에서 확인한 것.** 네 counterexample flag는 서로 다른 네 실제 실패가 아니다. I2의 세 조건이 모두 본 `Set`의 “꺼져 있던 alpha를 opaque로 초기화”하는 예외가 3단계이고, P3 C의 “RTF는 figure 미지원”이 1단계다. 전자는 `demo.tif`의 채널 상태·흰 출력 원인을 확인한 것이 아니며, 후자는 원 float+table overflow를 재현한 것이 아니다. [I2 C](evaluation/judgments-imagemagick.jsonl#L12), [I2 B](evaluation/judgments-imagemagick.jsonl#L15), [I2 A](evaluation/judgments-imagemagick.jsonl#L24), [P3 C](evaluation/judgments-pandoc.jsonl#L18)

특히 **P1 C의 구조 절 도착은 full뿐 아니라 충분한 부분 재구성도 아니다.** 원답의 “부분 확인”은 fenced Div 문법·중첩 가능성을 확인한 말이며, 요청한 HTML+TOC 조작과 B1/B2 구성원 보존 또는 필수 E3를 설명하지 못한다. 이를 `justified_hold=true, partial_reconstruction=false`로 판정했다. 표제 도착을 semantic 성과로 올리지 않는 핵심 대사점이다. [불변 판단](evaluation/judgments-pandoc.jsonl#L21), [평가자 불일치 기록](evaluation/evaluator-pandoc.json#L50-L58), [결정적 구조 근거](gold-work/pandoc/gold-notes.md#L35-L57)

**원래 / 실제 분모·결손.** 단계별 인용 95개 중 정확한 누적 표시 일치는 94개다. r13 단계 2의 `A image setting`은 실제 `An image setting...`의 전사 오류다. 원답 수정은 거절되어 그대로 남았고, 거절은 4번째 개봉이 아니다. 다음 답변에서 오류를 인정한 것을 새 오류로 중복 계산하지 않았다. [인용 집계](analysis/trial-summary.json#L575-L582), [minor 오류 판정](evaluation/judgments-imagemagick.jsonl#L11), [거절·후속 기록](readers/r13/events.jsonl#L7-L12)

**판단을 바꿀 다음 관측.** 같은 단계까지 실제 표시된 구간에서 누락됐다고 판단한 O/P/E가 직접 지지된다는 증거가 나오면 그 행의 판단 근거를 재검토할 수 있다. 다음 단계·gold·외부 지식을 이전 단계의 성공 근거로 넣지는 않는다. P1의 문법 도착을 부분 성공으로 인정하려면 단순 syntax 이상의 요청 관련 조건 복원이 실제 원답과 노출에서 확인돼야 한다. [누적 판정 원칙](SCOPE.md#L43), [P1 missing evidence](evaluation/judgments-pandoc.jsonl#L21)

## Q6. 단서의 가능성과 오류를 별도 교정·반증으로 확인했는가?

**답 / 미확인.** 자연 사건을 바꾸지 않고 구성 교정 K1·K2를 별도 봉인·재생했다. K1은 `Using pandoc`→`Character encoding`의 3개봉에서 standalone 출력과 UTF-8·지역 인코딩 예외를 덮었다. K2의 올바른 Reader options는 2개봉에서 제목 이동·첫 제목 예외를 덮지만, 같은 표제의 defaults 절로 간 3개봉 경로는 두 필수 구간을 모두 놓친다. 이는 구성 경로의 문서 증인 확인이며 자연 독자의 새 선택이나 Pandoc 실행 결과가 아니다. [사전 구성·요구 구간](calibration/preregistered-cases.json#L3-L95), [재생 결과](calibration/replay-check.json#L5-L70)

**직접 근거 / 실행 원장.** K1의 직접 절은 [Using pandoc](https://pandoc.org/MANUAL.html#using-pandoc)와 [Character encoding](https://pandoc.org/MANUAL.html#character-encoding), K2는 [Reader options](https://pandoc.org/MANUAL.html#reader-options)다. 링크는 현재 위치 식별용이며 판단은 봉인한 3.8.3 구간·offset에 근거한다. 시작 화면만으로 충분한 D0는 JPEG→PNG 기본 호출과 shell 줄 연결법이라는 별도 새 요청의 사후 진단이다. D0를 두 사전 교정이나 자연 6사건에 더하지 않는다. [K1 구간](calibration/preregistered-cases.json#L15-L48), [K2 fragment 구분](calibration/preregistered-cases.json#L63-L95), [D0 범위·직접 표시](calibration/start-only-diagnostic.json#L2-L25)

**반증에서 확인한 것.**

- **서로 다른 보존조건:** 별도 2×2 RGBA+ICC 합성 입력을 설치된 ImageMagick 7.1.1-43에서 검사한 결과, `-strip`은 alpha 샘플을 유지하고 ICC를 제거했으며 `-alpha off`는 ICC bytes를 유지하고 alpha를 모두 255로 만들었다. 두 조건의 독립성이 실제 실행된 보조 반례다. 자연 I1~I3 역사판 재현이나 수신자의 4개 문서 예외 flag에 합산하지 않는다. [실행과 경계](gold-work/imagemagick/gold-notes.md#L132-L141)
- **부품 위치와 적합성:** Prusa의 부품 표지·모델 대응과 교체 절차의 베어링 방향, 새 키트 조립과 운용 후 윤활 조건을 구별했다. 번호를 찾았다는 사실은 해당 상태에서의 수리 적합성 증거가 아니다. [발행자 직접 URL과 읽은 쪽](analogies/ANALOGIES.md#L15-L16), [원문 링크](analogies/ANALOGIES.md#L50-L53)
- **기록관 위치와 내용:** Yale 항목·finding aid는 확인했지만 원 편지 이미지는 403으로 읽지 못했다. Eisenhower의 같은 Box 38 / Final TV Talk (1)에 있는 낭독본과 보도자료는 실제 PDF를 비교해 수정 흔적·본문 시작의 차이를 확인했다. 이 별도 사례가 Yale의 미열람을 성공으로 바꾸지는 않는다. [두 사례의 관측 수준](analogies/ANALOGIES.md#L9-L23), [원 항목·PDF URL](analogies/ANALOGIES.md#L54-L65)

**원래 / 실제 분모·결손.** 사전 교정 2건에는 증인 경로 2개와 근접 오답 경로 1개가 있다. 보조 비교는 13개 고유 발행자 저작·67개 이질적인 읽기/수신 작업이며 자연 성공 분모는 0건 추가다. 원 편지 접근 실패, JP2 원첨부 404, 역사 소프트웨어 미실행은 실제로 확인한 접근 실패·미관측 상태이지 자연 수신 실패율이나 보존 실패 재현이 아니다. [교정 분모 제외](calibration/replay-check.json#L25-L70), [보조 저작·작업 대사](analogies/ANALOGIES.md#L33-L41), [I3 404](gold-work/imagemagick/gold-notes.md#L82-L98)

**판단을 바꿀 다음 관측.** 같은 도구의 재생에서 K1/K2 필수 구간이 보이지 않거나 near-wrong 경로에 예외가 실제 포함돼 있으면 교정 판정을 수정한다. Yale 원 편지, 정확한 I3 원 JP2, 실제 모델별 부품 교체를 확보하면 해당 미확인을 별도로 해소할 수 있다. “문서에 적합성 조건이 있다”는 현재 판단을 “단서가 수행에 도움을 줬다”로 바꾸려면 새 수신 선택·수행 관측이 필요하다. [교정 검증 기준](calibration/replay-check.json#L5-L70), [보조 비교의 다음 관측](analogies/ANALOGIES.md#L67-L71), [I3 필수 입력](gold-work/imagemagick/gold-notes.md#L92-L98)

## Q7. 언제 한 줄 작성 비용을 감수할 만한가?

**답 / 미확인.** 이 자료만으로 한 줄 작성의 일반 순편익·사람 시간 절약·원 개발자의 채택은 결정할 수 없다. 완전 근거에 도달 가능한 자연 기회 분모가 0이므로 일반 효과율은 `null`이다. 관측된 것은 18쌍의 노출·판정 비교와 실제 부담이다. 시작 링크만으로 충분한 D0 같은 질문, 단서 외에 engine·파일·예외 확인이 필요한 P3/I3 같은 질문을 구별하는 설계 후보는 남길 수 있다. [효과·비용 규칙](SCOPE.md#L45-L51), [D0](calibration/start-only-diagnostic.json#L2-L25), [P3/I3의 full unknown](reachability.jsonl#L20), [I3](reachability.jsonl#L46)

**직접 근거 / 실행 원장.** 수신 비용은 다음처럼 실측 표시량으로 대사했다. 세션 wall 합계는 각 조건 여섯 세션의 기록을 합한 것이며 병렬 실행이 겹친다. 전체 작업 경과시간·사람 능동시간·절약시간으로 해석하지 않는다. [조건별 표시 비용](analysis/trial-summary.json#L584-L608), [세션별 measured_session_wall_seconds](analysis/trial-summary.json#L27-L441), [능동시간·채택 한계](analysis/trial-summary.json#L610-L616)

| 조건 | 실제 개봉 | 전체 표시 문자 | 전체 표시 UTF-8 bytes | 본문 문자 / 내비게이션 문자 | 세션 wall 합계(초) |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 18 | 25,714 | 26,464 | 18,737 / 6,977 | 247.582408 |
| B | 18 | 25,714 | 26,464 | 18,737 / 6,977 | 292.783088 |
| C | 18 | 25,655 | 26,413 | 16,073 / 9,582 | 268.800095 |
| 합계 | 54 | 77,083 | 79,341 | 53,547 / 23,536 | 전체 경과시간으로 합산하지 않음 |

B/C 한 줄은 각각 총 527자이며 UTF-8은 B 1,204바이트, C 1,116바이트다. 제작 공유 wall 560.956346초와 읽기 5회에는 대기·자체 검증이 포함되어 사건별 원가를 나눌 수 없다. 잘린 목차 시도의 정확한 실제 노출은 `null`이다. [여섯 문구 길이·바이트](authoring/packet-check.json#L3-L57), [제작 부담과 결손](authoring/author-exposure.jsonl#L3-L7)

**반증에서 확인한 것.** 세 조건 모두 사건당 3회씩 읽었으므로 이 실행에서 관측된 절약/추가 개봉 수의 조건 간 차이는 0이다. C의 표시량이 조금 다르고 P1/P3에서 경로가 달라졌다는 이유로 시간 절약을 주장할 수 없다. P1 C의 관련 절 도착은 과제 부분 복원도 아니며, P3 C는 RTF 예외를 더 확인했지만 A/B가 읽은 PDF·여백 조건과 다른 증거를 얻었다. [개봉·표시 비용](analysis/trial-summary.json#L584-L608), [P1 한계](evaluation/judgments-pandoc.jsonl#L21), [P3 각 판정](evaluation/judgments-pandoc.jsonl#L2-L3), [P3 A/C](evaluation/judgments-pandoc.jsonl#L14-L18)

| 역할 | 현재 근거에서 남길 설계 후보 | 아직 비용 정당화로 볼 수 없는 이유 |
| --- | --- | --- |
| 경로 작성자 | 먼저 고정 시작점에서 O/P/필수 E까지의 기회가 있는지 확인하고, 없는 경우 예산·출처 확장이 필요함을 표시한다. | 자연 표본에서 reachable full 기회가 없었다. [도달성 표](reachability.jsonl#L1-L3), [P3 unknown](reachability.jsonl#L20) |
| 후속 조사자 | 단서와 함께 다음 확인 입력을 명시한다. P3는 렌더 환경, I3는 원파일·채널 정의가 우선이다. | 관련 표제·일반 설정만으로 보존 성질이 확정되지 않는다. [P3 기준 층](gold-work/pandoc/gold-notes.md#L87-L103), [I3 다음 검사](gold-work/imagemagick/gold-notes.md#L92-L98) |
| 링크 유지 편집자 | 이름·URL 외에 판·fragment·원본/대체본과 읽을 조건을 함께 보존한다. 단순 질문이면 시작 링크를 유지할 수 있다. | 같은 표제의 다른 절, 같은 폴더의 다른 원 항목이 존재한다. [K2](calibration/preregistered-cases.json#L63-L95), [기록관 원문 비교](analogies/ANALOGIES.md#L17-L23), [D0](calibration/start-only-diagnostic.json#L2-L25) |

**원래 / 실제 분모·결손.** 비교는 원래 계획한 6사건×3조건=18꾸러미와 세 쌍 유형×6사건=18쌍으로 완료됐고, 전조건 성공은 각 조건 0/6이다. full 기회 분모 0, 의미 unknown 2사건, 사람 능동시간·채택 미관측, 사건별 제작비 미측정을 별도 결손으로 유지한다. “관측하지 못함”을 소프트웨어상 불가능이나 독자 실패로 대체하지 않는다. [수신 분모](analysis/trial-summary.json#L5-L24), [쌍·미관측 규칙](SCOPE.md#L51), [제작 결손](authoring/author-exposure.jsonl#L7), [인간 관측 한계](evidence/roles.json#L3-L5)

**판단을 바꿀 다음 관측.** 새로운 자연 요청을 모집할 때 문구를 만들기 전에 full reachable 기회와 입력 완전성을 별도 봉인하고, 같은 예산에서 A/B/C의 정확한 절·O/P/E·오확정·추가 읽기를 반복 비교해야 한다. 실제 사용자의 준비·수신 능동시간과 채택을 측정한 자료가 생기면 비용 정당화 판단을 추가할 수 있다. 현재 자료의 0/18은 그 후속 효과율을 대신하지 않는다. [사전 순서·가림 규칙](SCOPE.md#L24-L29), [도달성과 미관측 효과 원칙](SCOPE.md#L39-L51)

## 절차 한계와 root 최종 검토 필요사항

1. **사전 봉인의 내용 고정과 시각 독립 증명을 구분할 것.** 원장에는 원격 고정 SHA 재열람·git 순서·읽기 시각이 남아 있지만, 최초 원격 갱신의 원시 영수증은 보존되지 않았다. 기존 봉인 기록의 작성 시각이 원 모집 뒤라는 점을 독립 timestamp 증명으로 포장하지 않는다. 최종 원격 재열람은 과거 최초 봉인 시각을 소급 증명하지 않는다. [봉인 기록](evidence/seals.jsonl#L1-L9), [시각 한계](evidence/audit-resolutions.json#L22-L27)
2. **preprotocol 보조 탐색을 명시할 것.** cross-domain 탐색 시작은 03:57:08 UTC로 기록됐고 `cross_domain_pre_protocol=true`다. 보조 비교는 탐색적 자료로 남기며 자연 A/B/C 처리나 사전 모집 효과의 증거에 넣지 않는다. [직접 시각·분류](evidence/audit-resolutions.json#L25-L27), [보조 범위](analogies/ANALOGIES.md#L3-L9)
3. **같은 모델 설정 AI, 절차적 가림, 잔여 문구, OS 격리 부재를 함께 유지할 것.** 새 문맥 18개는 같은 부모 설정을 상속했고 인간 참여자는 없다. 평가에는 reference가 제공됐지만 수신자의 실제 누적 표시와 대체하지 않았다. Pandoc 답변 두 곳에 “안내 문구”라는 간접 잔여 단서가 있고, ImageMagick에는 전사 정정 시도·예산 문맥이 남아 있다. 완전 가림이나 OS 접근 통제의 증거로 부르지 않는다. [실행 문맥](evidence/reader-launches.jsonl#L1-L18), [OS·인간 한계](evidence/roles.json#L3-L5), [Pandoc 잔여](evaluation/evaluator-pandoc.json#L28-L48), [ImageMagick 잔여 절차 문맥](evaluation/evaluator-imagemagick.json#L23-L48)
4. **불변 판정과 합산을 재확인할 것.** Pandoc 5+ImageMagick 3=8 partial 단계, 1+3=4 관련 문서 예외 flag이며, P1 C 구조 절 도착을 partial로 올리지 않는다. r13 전사 오류는 1건이고 거절된 overwrite를 추가 개봉·추가 오류로 세지 않는다. [Pandoc 판정](evaluation/evaluator-pandoc.json#L50-L91), [ImageMagick 판정](evaluation/evaluator-imagemagick.json#L50-L70), [정정 거절](readers/r13/events.jsonl#L7-L12)
5. **최종 원장과 검사 snapshot의 분모를 맞출 것.** 현재 `sources.jsonl` 273행·고유 37·필수 34가 최종 집계에 반영되는지 확인한다. 과거 source seal 검사 195행, 수신 반복 54행, 감사 반복 24행을 다른 고유 저작으로 세지 않는다. 이 문서의 출처·행 링크도 최종 고정판에서 검사한다. [최종 수](analysis/source-counts.json#L2-L26), [과거 검사 snapshot](evidence/audit/checks.json#L4-L15), [감사 반복행](sources.jsonl#L237-L260)
6. **최종 인수 증거를 확정할 것.** 결과 SHA·원격 재열람·검사 실행 결과·검사 영수증과 HANDOFF 순서는 [acceptance-evidence.json](evidence/acceptance-evidence.json)에 실제 완료한 값으로 기록한다. 그 파일의 최종 SHA와 이 점검의 근거 링크가 동일 결과판을 가리키는지 root가 검토해야 한다. 아직 미확정인 값은 빈칸 또는 명시적 미확인으로 남기며 실행 실패로 대체하지 않는다. [인수 순서](SCOPE.md#L49-L51)

