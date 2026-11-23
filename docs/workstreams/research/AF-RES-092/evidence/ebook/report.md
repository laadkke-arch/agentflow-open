# Q7 전자책: 본문·스타일·읽기 시스템 경계

신규 여섯 질문이나 A/B 점수와 분리한 타 분야 대조다. 열람은 2026-11-23 UTC. 고유 원자료 6건을 보수적으로 독립 저작/사건 계열 4개로 묶었다. W3C 규격 두 문서는 한 규격 계열, Readium 문서 두 개는 한 구현 문서 계열, KOReader 코드와 #13295 사건은 각각 한 계열이다. 댓글·PR·변경 파일·첨부 이미지·웹/원본 미러는 같은 계보의 보조 확인이며 원자료 최소량을 늘리지 않는다. 직접 프로그램을 실행하지 않았다.

## 관측과 반례

| 목적과 단계 | 직접 확인한 원자료 | 지지 또는 반박 | 남은 한계 |
| --- | --- | --- | --- |
| XHTML 본문·저자 CSS → EPUB 패키지 → 읽기 시스템의 표시 | [EB01: Reading Systems 3.3, 2023-05-25, §6.3](https://www.w3.org/TR/2023/REC-epub-rs-33-20230525/#sec-css) | 읽기 시스템은 저자 스타일과 사용자 상호작용에 따른 재정의를 구별한다. 본문에 올바른 태그가 있어도 최종 표시의 충분조건은 아니다. | 규범상 허용·권고와 특정 앱의 구현 결과는 다르다. |
| 같은 `.epub`, 가변 글꼴/동적 줄바꿈 목적과 페이지 형태 고정 목적 | [EB02: EPUB 3.3, §8.2.2.1](https://www.w3.org/TR/2023/REC-epub-33-20230525/#layout) 및 [EB04: Readium CSS 범위](https://github.com/readium/css/blob/49d1f549185efc4aa3ac6bedb5e11b5011b3851a/README.md#scope-of-this-project) | `reflowable`과 `pre-paginated`는 같은 컨테이너 안의 다른 레이아웃 계약이다. Readium CSS는 전자를 대상으로 하고 고정 레이아웃 EPUB에는 쓰지 말라고 명시한다. 포맷 이름이 같은 두 링크를 잇는 것만으로 조합이 성립하지 않는다. | 실제 특정 고정 레이아웃 책을 Readium에서 시험하지 않았다. 부적합 범위는 공식 명시로 판정한다. |
| 이미 적격한 XHTML 문서 → 읽기 시스템 CSS 변수 → 페이지/스크롤·글자 표시 | [EB03: 고정 Readium 사용자 설정 문서](https://github.com/readium/css/blob/49d1f549185efc4aa3ac6bedb5e11b5011b3851a/docs/CSS12-user_prefs.md#mechanism-for-user-settings) | `ReadiumCSS-after.css`를 로드한 뒤 `html`에 해당 변수를 설정하면 표시를 갱신한다. 한 읽기 시스템 안에서 스타일 변경과 렌더링을 처리하므로 매번 별도 변환기를 추가할 이유는 없다. | 필요한 CSS가 로드돼 있고 지원되는 변수·값을 쓰는 조건이다. 임의 EPUB 앱에 이 설정명이 통한다고 추정하지 않는다. |
| 동일 EPUB에서 코드의 고정폭 글꼴·제목 계층 유지 | [EB06: KOReader #13295](https://github.com/koreader/koreader/issues/13295), [질문자 우회 설정](https://github.com/koreader/koreader/issues/13295#issuecomment-2674824947) | 보고자는 2024.11과 2024.11-209, PocketBook/Linux를 명시했다. 동일 파일에서 독자 스타일 설정을 켜자 코드 글꼴과 제목 크기가 변했다. 첨부 두 이미지를 직접 열어 제목 크기 차이와 코드 글꼴 변화도 확인했다. 원인은 본문 생성 단계 하나에 한정되지 않는다. | 재현은 보고자의 기록이다. 이 조사에서 실행하지 않았고, 이미지가 주장한 실행 환경에서 만들어졌다는 독립 인증은 없다. |
| 넓은 독자 재정의의 부작용 → 더 좁은 선택자/읽기 시스템 수정 | [EB05: 고정 수정 코드](https://github.com/koreader/koreader/blob/fd54ddbd8f1aabcef1cc0adf3d8477fe84149cdb/frontend/ui/data/css_tweaks.lua#L430-L455), [수정 PR #14698](https://github.com/koreader/koreader/pull/14698) | 폰트 계열 재정의 후 코드 계열 요소를 고정폭으로 복원하는 규칙이 들어갔다. PR은 2025-12-08 병합됐다. 본문 파일을 다시 쓰지 않고 소비자 측 규칙을 고칠 수 있다는 근거다. | 병합은 모든 배포판 성공의 증거가 아니다. 질문자의 수정판 업그레이드 후 출력은 미확인. 글자 크기의 광범위 초기화 문제까지 모두 해결했다고 쓰지 않는다. |

## 반환 판단: 한 링크·두 링크·한 질문·유보

| 관점과 알고 있는 조건 | 줄 결과 | 이유와 다음 조건 |
| --- | --- | --- |
| 질문자: KOReader에서 기존 책의 코드 글꼴만 보존하려는 경우 | [한 링크: 보고자의 소비자 측 우회 설정](https://github.com/koreader/koreader/issues/13295#issuecomment-2674824947) | 입력 본문을 바꾸지 않는 경로다. 해당 읽기 시스템과 문제 설정을 쓰는지 먼저 맞춰야 한다. |
| 유지관리자: 과도한 폰트 재정의의 범위를 수정하는 경우 | [사건](https://github.com/koreader/koreader/issues/13295) + [고정 코드](https://github.com/koreader/koreader/blob/fd54ddbd8f1aabcef1cc0adf3d8477fe84149cdb/frontend/ui/data/css_tweaks.lua#L430-L455) | 증상·환경과 실제 수정 선택자를 연결한다. 사용자 성공과 병합 상태를 합쳐 세지 않는다. |
| 탐색기 편집자: “EPUB에서 글자 크기 조절”만 아는 경우 | 한 가지 되묻기: 해당 spine 항목의 `rendition:layout`이 `reflowable`인가, `pre-paginated`인가? | 두 값이 Readium CSS 적격성을 갈라놓는다. “EPUB 지원”만으로 완결 반환하지 않는다. |
| 도구 조립자: reflowable이고 Readium CSS 통합 권한이 있는 경우 | [범위](https://github.com/readium/css/blob/49d1f549185efc4aa3ac6bedb5e11b5011b3851a/README.md#scope-of-this-project) + [설정 메커니즘](https://github.com/readium/css/blob/49d1f549185efc4aa3ac6bedb5e11b5011b3851a/docs/CSS12-user_prefs.md#mechanism-for-user-settings) | 중간 계약은 `.epub` 문자열이 아니라 로드된 XHTML/CSS 및 변수 주입 위치다. 실제 앱 통합·렌더링 검증은 별도다. |
| 읽기 앱·레이아웃·수정 권한 모두 모르는 경우 | 근거 부족 유보 | 최소 관측은 패키지 layout 값과 읽기 시스템 이름/판이다. 새 부품 링크를 추가해도 이 공석은 사라지지 않는다. |

## 자기 결론이 틀릴 조건

앞단 수정을 항상 피할 수 있다는 결론은 EB02의 고정 레이아웃 조건과 EB04의 명시적 제외에 의해 반박된다. 모든 소비자 재정의가 좋은 해결이라는 결론은 EB06의 실제 부작용에 의해 반박된다. 소비자 측 수정의 가능성은 확인했지만, 신규 여섯 질문에서 B의 승률이 높다는 증거로 이 사례를 사용하지 않는다.

다음 최소 관측은 동일 입력 EPUB의 패키지 layout 값, 읽기 시스템의 정확판, 설정 전후 출력이다. 수정 커밋을 포함한 판과 포함하지 않은 판을 비교하면 “문서상 가능”과 “실제 해결”을 가를 수 있다. 이 실행은 미실시다.

## 재열람 자료

`sources.jsonl`은 직접 판독·한계 원장이고 `fetch_receipts.json`은 UTC·HTTP 상태·전체 응답 바이트의 SHA-256이다. 원문 전체를 복제하지 않았다. `EB06IMG1.png`와 `EB06IMG2.png`는 공개 이슈 첨부의 작은 비교 화면이며 각각 원상태/독자 스타일 적용 상태로 제시된 이미지다. 이미지 URL과 해시는 원장에 있다. 동일 사건의 두 이미지이므로 독립 사건 수를 늘리지 않는다.
