# AF-RES-092 재개 감사 · Q7 타 분야 원문

검토 대상: `b40b4dfeb8b7079f6568e511105117b02f477d14`의 RESULT/SELF_CHECK 및 audio·ebook 보고서/원장. 직접 재열람 UTC: 2026-11-23T17:13:48Z–17:14:12Z. 같은 팀의 별도 독해 감사이며 신규 A/B 실험, 독립 맹검 또는 구현 실행이 아니다.

**판정: 읽은 여섯 핵심 원문의 범위에서 수정이 필요한 실질 오류 0건.** 원문이 지지하는 문서·구현 가능성, 공개 보고자의 관측, 이 연구자의 미실행을 기존 결과가 구별한다. 새 결과를 원 실험에 추가하거나 원자료 최소량을 늘리지 않는다.

| 재열람 원문 | 직접 확인한 내용과 기존 주장 대조 | 남은 한계 |
| --- | --- | --- |
| [RFC 7845 §4·§5.1](https://www.rfc-editor.org/rfc/rfc7845.html#section-5.1) | granule clock은 채널당 48 kHz이고 입력 sample-rate 필드는 재생 rate 지시가 아니다. 디스크 PCM 출력의 sample-rate 선택과 즉시 재생을 구별한 요약이 맞다. | 이는 규격 독해이며 Safari 시간축 실패의 구현 원인을 직접 증명하지 않는다. |
| [WebKit #293310 최초 보고·후속 #5](https://bugs.webkit.org/show_bug.cgi?id=293310) | 최초 보고의 07:32:36.61 대비 Safari 7:58:26, Opus stream-copy WebM 대조, Safari 18.5 판을 확인했다. 후속 #5는 다른 입력의 공개 보고다. | 원 최초 파일·FFmpeg 정확판·우리 재현이 없다는 제한이 맞다. 후속 댓글도 동일 버그 사건으로 유지한다. |
| [EPUB Reading Systems 3.3 §6.3·§8.1.1.1](https://www.w3.org/TR/2023/REC-epub-rs-33-20230525/#sec-css) | 사용자 상호작용에 의한 저자 스타일 일부 재정의를 허용한다. reflowable 동적 페이지 처리와 pre-paginated의 spine 항목당 한 페이지 요구를 구별한다. | 사용자 재정의 허용은 모든 CSS 변경이 바람직하거나 특정 앱에 구현됐다는 뜻이 아니다. 기존 결과도 그 선을 넘지 않는다. |
| [Readium CSS 고정 README](https://github.com/readium/css/blob/49d1f549185efc4aa3ac6bedb5e11b5011b3851a/README.md#scope-of-this-project) | 명시적으로 reflowable EPUB 2/3을 대상으로 하며 fixed-layout EPUB에는 사용하지 말라고 한다. 같은 EPUB 이름만으로 적격성을 판정할 수 없다는 반례가 성립한다. | 이번 재열람은 범위 문서다. CSS 변수 주입 문서와 특정 앱의 렌더링은 추가 재검증하지 않았다. |
| [KOReader #13295](https://github.com/koreader/koreader/issues/13295) | 원 보고의 2024.11/2024.11-209, PocketBook/Linux, Markdown→EPUB 입력과 독자 스타일 토글 뒤 monospace·제목 크기 변경 설명을 확인했다. | 보고자의 실행 기록이다. 첨부 두 이미지의 이번 재열람 및 독립 실행은 하지 않았다. 기존 이미지 독해 기록을 새로 인증하지 않는다. |
| [KOReader 고정 CSS 수정](https://github.com/koreader/koreader/blob/fd54ddbd8f1aabcef1cc0adf3d8477fe84149cdb/frontend/ui/data/css_tweaks.lua#L430-L455) | 전체 font-family 상속 뒤 code/pre 등 요소에 monospace를 복원한다. font-size 전체 상속 규칙은 별도로 남아 있다. 기존 보고서가 글자 크기 문제까지 전부 해결했다고 쓰지 않은 것이 정확하다. | 코드 독해만으로 사용자의 수정판 설치·성공을 판정하지 않는다. 이번에 PR 병합 시각을 재조회하지 않았다. |

## 계보·과잉 일반화 점검

오디오 여섯 자료를 다섯 저작/사건 그룹으로 묶고 opusfile 코드와 API를 합친 기존 집계는 사건 독립성을 과장하지 않는다. 전자책의 W3C 문서 두 개, Readium 문서 두 개를 각각 한 그룹으로 묶은 것도 적절하다. KOReader 코드 저작과 사용자 사건은 별도 저작/사건 항목일 수 있으나, 둘을 독립 실행 두 건으로 해석하면 안 된다. 기존 RESULT는 29그룹을 29독립 실험이라고 부르지 않는다.

타 분야에서 소비자 수정이 가능하다는 사실을 신규 여섯 질문의 B 승률로 합산하지 않은 구분도 유지해야 한다. Q7 감사는 기존 PARTIAL 사유인 P2의 비교 결손, 원 사용자 정확판·출력 결손을 해소하지 않는다.

## 재열람 기록

여섯 직접 원문의 URL·판·열람시각·관측값·한계는 `resume-crossdomain-sources.jsonl`에 있다. 모두 기존 원자료 재열람이므로 최소량 추가 0, 신규 독립 사건 추가 0, 신규 경로 추가 0이다. 이번 접근은 모두 성공했으며 문서 내 검색어 `restoring`의 무일치는 접근 실패가 아니다. 기존 산출물과 사전 판정은 수정하지 않았다.
