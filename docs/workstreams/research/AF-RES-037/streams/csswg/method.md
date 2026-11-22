# CSSWG · 단계1 원장

2018–2024 생성 GitHub issue 7,161개 중 created ascending 최초40 metadata를 받았고, 첫4개가 행동·대안 적격이라 본문 심사는 네 번째에서 종료했다. 나머지36개는 제외 판정이 아니라 상한 뒤 미심사다. 이전 017/022/033 사건과 동일한 CSSWG issue는 없었다.

| 사건 | 최초 원문 | 원안만으로 확인한 선택 |
| --- | --- | --- |
| A-C01 / #2155 | [W3C opened mail](https://lists.w3.org/Archives/Public/public-css-archive/2018Jan/0002.html), 2018-01-01 08:51:05Z | 표 요소 sticky 예외를 없애 스크롤 머리글 유지 |
| A-C02 / #2156 | [W3C opened mail](https://lists.w3.org/Archives/Public/public-css-archive/2018Jan/0012.html), 2018-01-01 12:46:23Z | unknown -webkit pseudo-element 예외 명세화와 구현의 일반 invalidation 사이 선택 |
| A-C03 / #2157 | [W3C opened mail](https://lists.w3.org/Archives/Public/public-css-archive/2018Jan/0020.html), 2018-01-01 14:32:55Z | 표 열 selector 이름을 :nth-column에서 :nth-col로 바꿈 |
| A-C04 / #2158 | [W3C opened mail](https://lists.w3.org/Archives/Public/public-css-archive/2018Jan/0033.html), 2018-01-02 16:55:37Z | ::slotted의 허용 인자를 하나로 줄여 최적화 용이성 확보 |

## 초기판 확인과 정정

현재 API body를 최초판으로 확정하지 않았다. GH Archive는403/도구 접근 실패였고, 같은 W3C의 원 author notification인 `issues.opened` 메일을 직접 열어 네 건의 최초 본문을 복원했다. 생성시각·issue ID·메일 Message-ID·received 시각을 연결했다. GitHub URL과 W3C 알림은 같은 저작이므로 하나로 센다. 제3자 재인용·미러 문헌을 추가 산입하지 않았다.

#2157 현재 본문에는 CSS에서 약어를 흔히 쓰지 않는다는 설명이 추가돼 있다. 최초판에는 그 문장이 없다. #2158 현재 제목에는 :host가 추가됐으나 최초 제목·본문 범위는 ::slotted뿐이다. 초기 분석을 현재 제목의 :host까지 넓히지 않았다. `initial.json`은 원안 요약·해시와 차이를 보존한다. 원문 전체는 비커밋 `cache/`에만 있다.

#2157은 단순 편집 오타가 아닌 공개 selector 문법 명칭의 변경이다. 사용자가 입력할 API 명칭 대안이 식별되므로 포함했다. 다른 해석으로 명칭 변경을 제외할 경우 네 번째 이후를 사후 편입하지 말고, 이 사건을 뺀 A-C3 민감도만 별도 계산해야 한다.

## 노출 편차

네 사례를 root에 선정 보고한 뒤 초기 알림을 찾던 exact-ID 검색이 #2157 후속 회의 결의 스니펫을 반환했다. 이후 archive navigation에서도 Closed 제목이 보였다. 후속 페이지 본문은 열지 않았고 선정은 바꾸지 않았다. 그러나 **A-C03의 결말 완전 미노출 조건은 충족하지 못했다**. `attempts.jsonl` CSS-ATT05/06과 frame 행에 보존한다. 완전 blind 표집으로 보고하면 안 된다.

API response의 상태·수정시각·댓글수 필드는 원 payload에 존재하나 metadata 출력에서는 제거했고 선정에 쓰지 않았다. 최초 메일의 navigation에는 댓글 저자·제목이 보이지만 실제 후속 본문은 단계2 커밋 후까지 읽지 않았다. 당대 원문이 공개됐다는 메일 evidence와 당대 검색색인 여부는 다르며, 후자는 네 건 모두 미확인이다.

## 단계1 종료

`frame.json` 40행(선정4/심사후 탈락0/상한뒤 미심사36), `initial.json` 4행, `sources.jsonl` 원문4행과 `attempts.jsonl` 접근·노출 영수증을 root의 두 번째 커밋으로 봉인한다. 후속 결정·구현·반례 판독은 root의 봉인 확인 메시지 이후 시작한다.

## 단계2 확인 범위와 분모

부모가 `7a33c17be2d25b2c1936038205187e8108bf4482` 원격 봉인을 확인한 뒤 후속 본문을 열었다. CSSWG 네 이슈의 댓글 36개(14/16/3/3), 관련 타임라인, 고정 명세 변경, Mozilla 기록과 병합된 WPT/Servo 코드에서 같은 목적과 다른 범위를 구분했다. 현재 이슈 상태만으로 구현을 판정하지 않았다. 직접 실행한 브라우저 시험은 없으며, 시험 코드의 병합과 당대 실행 보고를 구분했다.

선정 적격은 A 4건이다. 그 안에서 확인된 타 분야 제공 원문과 명시적 선택 변경의 결합은 0건이며, 역사적 양성 대조의 적격은 0건이다. 따라서 조건부 회수율은 해당 없음이다. `followup.json`의 `strict_eligible=false`는 후자의 양성 대조 적격을 뜻하며 표집 적격 4건을 취소하지 않는다. 기존 소프트웨어 명세·HTML 명명·브라우저 호환성·selector 구현 최적화를 타 분야 원리로 바꾸어 세지 않았다.

A-C01의 표 sticky는 2017년 명세와 Mozilla 반영 기록이 이미 있다. A-C02는 당시 사용량 보고에 따라 unknown -webkit pseudo-element를 파싱에서 허용하는 선택이 명세 및 병합 시험에 반영됐다. 그때의 보고값을 원시 telemetry 실측으로 표시하지 않았다. A-C03은 초기안에 HTML 명칭 근거가 이미 있고, 후속 commit에서 이름만 변경됐다. A-C04는 Servo parser 변경과 거부 시험이 2017-12-20에 병합돼 2018-01-02 초기 제안보다 먼저다. 2020년 명세 정정을 2018년 즉시 구현의 원인으로 잇지 않았다.

`sources.jsonl` 21행은 같은 작품의 후속 판·댓글을 중복 그룹으로 묶어 고유 원문 13개만 센다. 이 중 최초 수신 원문은 4개다. CSSWG 스트림에서 확인된 비소프트웨어 제공 분야 원문은 0개이며, 이 13개로 전체 과제의 제공 원문 최소수를 채웠다고 주장하면 안 된다.

## 원장 정정

CSS-020의 날짜 초안 구간에는 `2017-12-15`가 들어갔으나, 직접 읽은 Bugzilla REST 댓글의 최초 시각은 `2017-12-17T17:43:51Z`다. append-only 원장을 보존하고 `source-corrections.json`에 기존 값, 정정 값, 직접 확인 이유, 분모 변화 0을 남겼다. 통합 원장에서는 이 정정을 적용해야 한다. 원문 댓글 시각은 `followup.json` A-C04의 timeline과 원래 URL/locator로 재확인할 수 있다.

## 검증

JSON/JSONL 파싱, 필수 source 키, source ID 고유성, 사건에서 참조한 source ID 존재, 사건 및 고유 원문 재집계를 확인했다. 결과는 `validation.json`에 있다. 공유 작업 트리의 Git 변경·커밋은 수행하지 않았다. `cache/` 원문 전체와 임시 응답은 부모의 commit 대상에서 제외해야 한다.
