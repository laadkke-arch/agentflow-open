# Moment 자연 보고층 — 판독·집계 메모

## 봉인과 분모

[title-frame-seal.json](title-frame-seal.json)은 본문 열람 전 제목만 저장한 프레임이다. 2021–2025 전체 이슈 142개가 1,000개 검색 상한보다 작아 월별 분할 대신 전기간 두 페이지를 읽었다. 생성시각→정수 번호순, PR 제외이며 제목 정규식에 맞은 것은 80개다. 최초 30본문을 전부 읽고 본문 기준 적격 20개 중 첫 세 개를 선정했다. 제목 검색 offset 한 건의 익명 HTTP 403은 GitHub connector 재조회로 해결했다. 복구 후 여섯 검색 합집합과 키워드 없는 census의 첫 30 사이에 누락은 **관측 0**이다. 결과를 본 뒤 표본을 고친 것은 아니다. [검색 시도](search-log.jsonl) · [offset 복구](offset-title-retry.json) · [30행 프레임](frame.csv)

`N-M1=#922`, `N-M2=#925`, `N-M3=#926`이다. #926은 자기 `format('z')`가 이름 대신 offset을 표시했다는 **정성 관측**과 호출을 제공하므로 포함했다. 구체 지역·숫자가 없는 것을 이유로 더 풍부한 다음 #929로 교체하지 않았다. 숫자 날짜/offset 문자열만 적격으로 보는 사후 민감도에서는 #929가 세 번째가 되지만, 이는 본 선정이 아니며 사용판 판정 0이라는 결과도 바꾸지 않는다.

현재 저장소의 #1158은 `created_at=2021-03-27`이지만 timeline에 **2026-09-14 transfer**가 있다. 원래 생성시각순이라는 계약에 따라 5번째 자리로 유지하고 날짜/offset 자체가 아닌 비교 불리언 질문이라 제외했다. 당시 이 저장소에 존재한 이슈 전체를 복원한 모집이라고 하지 않는다. 제목 판독 전에 결정한 현재 목록 범위의 한계다. [이관 이벤트](timeline-checks.json) · [원 API](https://api.github.com/repos/moment/moment-timezone/issues/1158/timeline)

| 단위 | 분자/분모 | 뜻 |
| --- | --- | --- |
| 원 공개 이슈 주소 추적 가능 | 3/3 | 세 선정 보고 원문을 열었다. |
| 저자가 게시한 어떤 관측이라도 있음 | 3/3 | #926의 정성 관측도 포함. |
| literal 날짜·offset 결과 | 2/3 | #922, #925만 정확 문자열; #926은 숫자 미기재. |
| 같은 보고의 특정 지역·원 입력·literal 출력 | 1/3 | #922만 지역 명시. 다만 파싱한 UTC는 미확인. |
| 선정 사례 실제 provider 자료판 라벨 | 관측 0/3 | 0.5.32라는 패키지 표기는 dataVersion 출력이 아니다. |
| 시대·프로세스·입력·지역·로드·출력 전체 결속 | 관측 0/3 | 원 실행 공급자/자료판 영수증이 없다. |
| 실제 로드 바이트 지문 | 관측 0/3 | 공식 태그의 지문을 과거 run 지문으로 쓰지 않았다. |
| 세 보기 비교 셀 | 9/9 | 자연 3×V0/V1/V2. 실제 사용판 귀속의 상승은 관측 0/3. |

외부 sources는 40행, 최소수 산입 계보는 26개(이슈 21, 버전별 공식 원전 5)다. 나머지 14행은 부적격 본문, 같은 로더/생성자료 개정, 발행 메타데이터로 중복/비산입 표시했다. “26”은 실행 사건 수나 참가자 수가 아니다. 보고 몸통 30개·댓글 endpoint 10개·선정 세 개와 이관 건의 timeline 4개를 읽었다. 참여자는 로그인 계정으로만 식별하며 삭제 계정 ghost를 실명/독립 인원으로 추정하지 않는다. [counts.json](counts.json) · [sources.jsonl](sources.jsonl)

## Q1 — 어떤 출력인가

선정 세 개 모두 작성자가 쓴 이슈 본문이다. 기계 원 stdout으로 읽지 않는다. API current body와 `updated_at`, 본문 UTF-8 해시를 보존했다. 선택 세 건의 공개 HTML과 timeline도 직접 열었지만 최초 공개 body의 별도 버전을 복원하지는 못했다. 댓글의 생성/편집 시각은 따로 기록했다. 공개 body가 나중에 편집될 수 있다는 제약을 유지한다. [issue-snapshots.json](issue-snapshots.json) · [comment-snapshots.json](comment-snapshots.json) · [HTML/편집 점검](issue-html-edits.json)

N-M1의 실제 보고는 2021-01-08 09:00+01:00이며 08:00+01:00은 기대값이다. N-M2의 한 자리/두 자리 hour 두 결과는 실제라고 작성자가 표시했다. N-M3의 PST는 원하는 출력의 예이고 실제 지역이나 실제 결과값으로 쓰지 않았다. 후속 명시 format 해결 댓글은 관측 성공을 말하지만 정확한 after-output, 버전 또는 install 영수증이 아니다.

강한 보조 사례 A-M967-M은 유지보수자가 **하나의 Node REPL transcript**에 같은 Date 값, zone, 여러 format/offset, dataVersion, package version을 게시했다. 이것도 작성자가 공개한 transcript라는 O-R이다. CI 원 stdout O-M으로 승격하지 않는다. [원 transcript](https://github.com/moment/moment-timezone/issues/967#issuecomment-1019463236)

## Q2 — 같은 순간인가

- N-M1: 원 입력 `2021-1-8 08:00`은 offset/format이 없다. 출력 09:00+01:00을 순간으로 해석하면 08:00Z이고, 의도한 08:00+01:00은 07:00Z다. 두 UTC 값은 연구자의 산술이며 실제 파서 내부 입력 영수증이 아니다. [#922](https://github.com/moment/moment-timezone/issues/922)
- N-M2: `guess()` 반환 지역이 없다. 출력에 offset도 없으므로 -05 지역에서 UTC 파싱된 첫 입력과 현지 파싱된 두 번째 입력이라는 설명은 **양립 가능한 경로**일 뿐 원 실행 판정이 아니다. core 버전·브라우저·호스트 시간대도 미확인이다. [#925](https://github.com/moment/moment-timezone/issues/925)
- N-M3: 날짜도 지역도 없으며 fold/gap 여부를 판단할 입력 자체가 없다. PST를 America/Los_Angeles로 바꾸면 안 된다. [#926](https://github.com/moment/moment-timezone/issues/926)

반례 탐색에서 #989를 직접 읽었다. 원저자가 초 단위 `unix()`를 ms를 받는 `Zone.utcOffset`에 넣었다. 유지보수자의 **별도** 입력/출력 예시는 2022와 1970을 가른다. -60은 Zone API의 UTC 서쪽 분이며 Moment 객체 `utcOffset()`의 동쪽 분과 부호 규약도 다르다. 2022-08-25 문서 정정은 ms를 명시했다. 이를 데이터판 수정의 증거로 바꾸지 않는다. [원 이슈/재현](https://github.com/moment/moment-timezone/issues/989#issuecomment-1152829460) · [공식 정정](https://github.com/moment/momentjs.com/commit/d0dc7f13dfbb08de1774ab01fdb4590293f558e4)

## Q3 — 선언·공식 패키지·실제 로드

0.5.32 고정 `index.js`는 기본 packed JSON을 읽는다. 하지만 `tz.load()`는 받은 객체의 version을 전역 dataVersion에 대입하고, `tz.add()`도 공개다. 선언된 패키지판만으로 커스텀/덮어쓴 자료나 여러 번들 로드를 배제할 수 없다. `guess()`는 Intl 또는 호스트 offset 추정과 캐시를 쓴다. [고정 loader](https://github.com/moment/moment-timezone/blob/3128dda269e4c08e11fc42e3dfbaeed1f7e33542/moment-timezone.js#L528) · [기본 진입점](https://github.com/moment/moment-timezone/blob/3128dda269e4c08e11fc42e3dfbaeed1f7e33542/index.js)

Moment core 2.29.1의 ISO regex는 두 자리 시를 요구하고, 인식 못한 비엄격 문자열은 native Date로 넘어갈 수 있다. 이것은 N-M1/2와 양립하는 설명이다. 그 원저자가 실제로 core 2.29.1을 로드했다는 주장은 아니다. #925 유지보수자가 첫 답에서 쓴 single-digit year는 원저자 지적 뒤 **hour에 관한 typo**라고 인정했다. 정정 전 답을 원 입력 설명으로 인용하지 않았다. [core 고정판](https://github.com/moment/moment/blob/b7ec8e2ec068e03de4f832f28362675bb9e02261/src/lib/create/from-string.js) · [typo 인정](https://github.com/moment/moment-timezone/issues/925#issuecomment-766717317)

두 적극적 반례:

1. **A-M938: 사용 자료판 라벨은 있고 이 날짜 출력은 없다.** 원저자의 utils import 블록은 dataVersion=2021a를 게시했다. 0.5.33 utils의 CommonJS `require('./')`가 기본 index를 통해 데이터를 가져오는 것도 직접 읽었다. 날짜 입력/출력은 없다. 따라서 “2021a를 표시한 로더 보고”는 가능하지만 어떤 UTC 순간의 날짜 결과는 미확인이다. [원 보고](https://github.com/moment/moment-timezone/issues/938) · [고정 utils](https://github.com/moment/moment-timezone/blob/ffc41900fed9efa9a31e87f0eadd66ec86b5046a/moment-timezone-utils.js#L12)
2. **A-M967-M: 같은 보고 안의 L 라벨과 출력은 연결되지만 H는 없다.** 유지보수자의 2022-01-23 REPL은 `0.5.34/2021e`, Sao_Paulo, Date 입력, -03:00 출력을 연결한다. 원저자 2021-11-24의 -02:00, 다른 참가자 2022-01-04의 host/tz 불일치와는 각각 다른 사건이다. 배포 파일 또는 실제 loaded pack hash가 없어 “공식 바이트 전체가 그 판”이라는 강한 문장은 보류한다. [세 사건 원 위치](receipts.csv)

## Q4 — 단일 관측과 단일 지역 지문도 충분하지 않다

신규로 필요한 공식 후보 0.5.31–0.5.34만 확인했다. 인수 059의 0.5.41–0.5.44 배포 파일은 다시 열거·해제·실행하지 않았다. npm은 0.5.31의 발행을 2020-05-17, 0.5.32를 2020-11-14, 0.5.33을 2021-02-06, 0.5.34를 2021-11-10으로 기록한다. 세 자연 보고 생성시각까지의 후보에서는 뒤 두 npm판을 제외할 수 있다. 상류 2021a가 따로 존재할 가능성이나 커스텀 bundle은 이 npm 제외와 별개다. [발행 메타데이터](package-metadata.json)

공식 태그의 전체 packed JSON을 읽고 Rome·Athens·Sao_Paulo 멤버 문자열을 비교했다. 각 지역 멤버의 바이트는 2020a, 2020d, 2021a, 2021e에서 각각 동일하다. 예를 들어 Rome의 1,011 UTF-8 bytes는 SHA-256 `ebc19f8feb975df485f2a1aabece72f31d9cfdcf80309008af76b103556a3c50`다. 이는 다운로드한 **공식 소스 멤버 문자열**의 지문이며 원 사용자 메모리/파일 지문이 아니다. [멤버 비교](candidate-edition-files.json)

따라서 같은 reader/입력을 유지하면 그 지역의 값이나 멤버 하나로 전체 자료판을 구분할 수 없다. 정확한 전역 라벨/whole pack을 보는 경우와 구분해야 한다. N-M2/3는 지역/순간/정확 값 자체가 부족하므로 수치 기반 유일판 제거도 하지 않았다. 후보는 완전 열거가 아닌 공개 네 판의 제한된 하한이며 유일판 주장은 **미확인**이다. [candidate-editions.csv](candidate-editions.csv)

보조 #929는 원저자 UTC/지역/실제 +03:00 출력이 모두 있고 유지보수자와 작성자가 DST 정상 동작에 합의했다. 그래도 당시 dataVersion는 없고 그 이전의 2020a/d/2021a Athens 멤버가 같으므로 자료판은 여전히 복수다. 이것이 “출력이 정확히 보고되어도 사용판은 복수”의 반례다. [#929](https://github.com/moment/moment-timezone/issues/929)

## Q5 — 변경 구간을 줄 수 있는가

선정 세 보고에서 같은 시스템·같은 입력의 before/after 두 관측과 설치/재배포 영수증을 확보한 것은 **관측 0/3**이다. #922의 “며칠 전까지 됐다”는 최초시각/값이 없고, 해결 댓글은 변수와 region도 달라진다. #925는 명시 format 변경의 해결 보고다. 이를 `(t0,t1]` 자료판 변경 구간으로 쓰지 않는다. #967의 여러 날짜/참가자도 같은 프로세스의 변화로 합치지 않는다. 판 공표 시각은 수신·로드 시각이 아니다.

판정이 바뀌려면 이미 공개된 같은 시스템/run 계보의 동일 입력·서로 다른 dataVersion/지문·출력 두 관측, 그리고 설치/배포 receipt가 필요하다. 자연 표본의 원본문·모든 댓글, 선정 건 timeline과 HTML, 고정 loader를 읽는 범위에서는 이를 찾지 못했다. 새 사용자에게 로그를 요구한 것이 아니다.

## Q7 — 세 보기와 추가 비용

[views.csv](views.csv)에 3사례×3보기=9행을 두었다. 이 세 사례의 strict 사용판 귀속은 어느 보기에서도 늘지 않았다. 대신 V2가 왜 확정할 수 없는지, 어떤 원인 대안이 남는지를 분명히 한다.

- 개별 비용은 V0 이슈 GET 1, V1의 새 개별 GET 0(공통 공식 원전을 참조), V2 댓글+timeline+HTML 3으로 사례당 4, 합계 12개 실제 read 요청이다. 모든 이슈/보조 모집비용은 이 세 보기 합계와 별도다.
- V2 HTML만 실측한 수신 bytes는 #922 220,626, #925 246,127, #926 222,356이다. connector 반환의 문자 수를 HTTP bytes로 바꾸지 않았다. 따라서 합계 689,109B는 HTML 부분 비용이며 모든 취득 비용이 아니다.
- 공통 후보/로더·공식 문서 열람은 공유 비용이다. 동일 자료를 세 사례의 네트워크 비용으로 세 번 더하지 않았다. npm index 173,751B는 HTTP 수신 실측이며 추출한 네 판 메타데이터의 저장 크기와 다르다.
- 제품 사용자는 “작성자가 이 값을 보고했다”를, 유지보수자는 “이 parser/loader 경로와 양립한다”를, 배포 담당자는 “이 공개판의 기본 data label은 이렇다”를, 감사자는 “같은 REPL의 self-report 라벨과 값이 연결된다”를 각각 구분해 반환할 수 있다. 해당 실행의 공식 멤버 지문이 없으면 네 관점을 합쳐 H 수준 문장으로 만들지 않는다.

## 반증 범위·미실시

첫 결론인 “자연 보고의 버전만으로 실제 자료판을 알 수 없다”를 깨는 근거를 찾으려고 첫 30본문을 모두 읽고, 이후 #938의 dataVersion 보고, #967의 완전한 REPL 라벨, #1015의 버전/출력 댓글을 직접 대조했다. #967은 **한 보조 실행의 L 귀속**에는 성공했지만 자연 표본의 사용판을 소급해 채우지는 못한다. 단일 지역 멤버가 전체판을 식별한다는 대안은 실제 네 태그의 같은 바이트가 반박한다.

신규 날짜 변환 실행, 설치, CI 실행, 원저자 연락은 **미실시**다. 현재 재현으로 과거 관측을 대체하지 않았다. 이 하위 작업의 결과는 natural cohort와 지정 보조 원자료에 한정되고, 실행물 우선층과 다른 분야의 모집/집계는 통합 담당의 별도 파일을 따른다.
