# AF-RES-112 출처 대사 감사

## 판정

**필수 배당 충족은 21/24이며 PARTIAL이다.** 실제 링크 인계 공개 요청이 6개 중 3개만 확보되어 3개 부족하다. 공식 문서·원 사례와 실패·회귀층의 초과분은 이 부족을 상쇄하지 않는다. 이 문서는 출처 중복·저작 경계·직접 열람 범위 감사이다. 독립 수신자 판독, main gold 작성 또는 수신 성과 검증을 자칭하지 않는다.

| 필수층 | 목표 | 확보한 고유 1차 저작 | 필수 배당 | 부족 | 같은 층 초과 미배당 |
|---|---:|---:|---:|---:|---:|
| 자연 링크 인계 공개 요청 | 6 | 3 | 3 | **3** | 0 |
| 목적 판별 공식 문서·원 사례 | 8 | 13 | 8 | 0 | 5 |
| 별도 회귀·실패·상충 | 6 | 16 | 6 | 0 | 10 |
| 박물관·기술 표준의 원 규격과 실제 예 | 4 | 4 | 4 | 0 | 0 |
| 합계 | **24** | **36** | **21** | **3** | **15** |

근거는 `../SCOPE.md`의 보조 대조·산입·완료와 네 입력 원장이다. 사건 모집의 적격 3개는 Godot이며 LilyPond 주 사건은 0이다. LilyPond의 2018년 요청, 후속 응답, 검색 히트 및 보조 문서를 새 주 사건으로 바꾸지 않았다.

## 입력 보존과 총계의 뜻

| 입력 원장 | 보존한 행 |
|---|---:|
| `../recruitment/godot/sources.jsonl` | 41 |
| `../recruitment/lilypond/sources.jsonl` | 24 |
| `../gold-work/sources.jsonl` | 27 |
| `../supplemental-sources.jsonl` | 5 |
| 합계 | **97** |

정규화 파일은 97행을 그대로 보존하고 각 행의 `provenance.original_row`에 원 JSON 객체 전체를 넣었다. 모든 식별자에는 `GREC:`, `LREC:`, `GOLD:`, `SUPP:`를 적용했고 발견된 원 `source_id` 충돌은 **0개**다. 입력 파일별 SHA-256은 `allocation.json`에 있다. 원 원장과 다른 경로는 수정하지 않았고 커밋하지 않았다.

| 계수 | 수 | 해석 |
|---|---:|---|
| 원문 직접열람 기록 행 | 85 | 같은 저작의 재열람·절·포트 및 제외 재게시를 포함 |
| 직접 읽은 고유 저작 계보 | 74 | 아래 재게시 1개를 포함한 URL·저작 중복 제거 수 |
| **고유 1차 직접열람 저작** | **73** | 재게시 1개 제외; 관련 없는 원 이슈를 포함하는 전체 자료 범위 |
| 필수 네 층에 배당 가능한 저작 | 36 | 층별 상한을 적용하기 전 |
| **필수 배당 충족 저작** | **21** | 6/8/6/4 배당을 적용한 결과 |
| 심사·관련성 제외 1차 저작 | 34 | 실제 읽었지만 필수 배당 0 |
| 미배당 보조 1차 저작 | 3 | 후속 메일 2개와 IIIF cookbook 1개 |
| 기존 접근실패 행 | 12 | LilyPond 11 + 폐기된 Godot demo ref 1 |
| 그중 검색 히트만 있고 개봉 실패 | 2 | 접근실패 12에 포함되는 부분집합 |
| 같은 저작의 성공 중복 행 | 11 | 동일 요청 3 + Godot 매뉴얼 추가 절·판 3 + 엔진 추가 파일·PR 4 + 포트 1 |
| 제외한 재게시 행 | 1 | 선행 원댓글을 다시 게시한 Godot docs 이슈 |

따라서 `97 = 직접열람 85 + 접근실패 12`, `85 = 고유 1차 73 + 같은 저작 중복 11 + 제외 재게시 1`, `73 = 필수층 가능 36 + 심사·관련성 제외 34 + 미배당 보조 3`이다. 73은 독립된 저자 73명, 사건 73개, 실험 73회 또는 성공 73건을 뜻하지 않는다.

`GOLD:REJECT-79944`의 원 `count_unique_primary=false`는 관련성 제외와 고유성을 섞고 있었다. 원문 이슈 전체를 실제 읽었다는 기록이 있고 다른 원장과 겹치지 않으므로, **전체 고유 1차 직접열람 수에는 1**, **필수 배당에는 0**으로 정규화했다. 이 한 건 때문에 원장의 단순 true 합계 72와 감사 총계 73이 다르다. 반대로 `GREC:G-SCREEN-5675`는 원문에 같은 작성자의 선행 댓글 재게시임을 명시하므로 SCOPE의 재배포 제외를 적용했다. [재게시 원문](https://github.com/godotengine/godot-docs/issues/5675)

## 저작 경계와 사건 계보

**Godot 공식 매뉴얼은 전체 1저작이다.** Resources, Resource, ResourceUID 문서와 3.4/4.0/4.7 판은 다른 URL이어도 같은 매뉴얼 계보다. 동일 Godot 엔진의 scene_tree/resource source files와 PR 3개도 프로그램 계보 1개로 합쳤다. PR의 작성자가 다르거나 수정판이 달라도 전체 프로그램 파일 수로 자료 수를 늘리지 않는다. 공식 블로그 글, 릴리스 설명, 독립 실행용 Truck Town 데모는 매뉴얼의 다른 절이 아니라 각각 목적과 발행 단위가 별도인 저작으로 구분했다.

**요청 3개와 그 원 예제 3개는 별도 저작이지만 같은 사건에 종속된다.** 본문 보고와 실행 가능한 코드 산출물의 저작 단위는 구별할 수 있어 문서·원례층에 배당한다. 같은 작성자·같은 사건에서 나온 자료라는 관계는 `work_relations`에 명시했다. 이 6저작을 6개의 자연 요청 또는 6개의 독립 corroboration으로 세지 않는다. 같은 원 예제의 후속 Godot 4 포트는 해시·URL·설정이 달라도 원 사례 1개 계보로 묶었다. Truck Town의 폐기된 `4.0-dev` ref는 접근실패이며, 별도 역사 커밋을 직접 읽었다고 원 링크의 그 판에 도착한 것으로 바꾸지 않는다.

**LilyPond의 공식 문서는 5저작이다.** Learning Manual, Notation Reference, Extending LilyPond, Contributor Guide, Changes는 공식 제목·목차·대상과 발행 목적이 서로 다른 문서이다. 각 문서의 절·번역·판·HTML/PDF는 해당 저작 안에 묶는다. 현재 개발판 Changes는 별도 변경기록 1개로 확보 수에는 포함하지만 필수 8개 배당에는 쓰지 않았다. 과거 문의에 개발판 동작을 소급하지 않는다.

**LilyPond 회귀 입력은 wrapper URL이 아니라 upstream fixture 4개로 구분한다.** `tag-filter.ly`, `tag-group.ly`, `part-combine-relative.ly`, `part-combine-global.ly`는 각기 원파일명·입력·기대 설명이 있는 독립 회귀 자료이다. 같은 파일의 여러 Staff, 마디, 함수 호출은 한 저작이다. 게시 빌드 2.24.4와 입력의 `version` 선언은 구분한다. 이 산입은 서로 다른 원자료 단위라는 뜻이며, 서로 독립된 구현·저자나 이번 감사에서 실행해 통과한 시험이라는 뜻이 아니다.

**메일과 미러는 읽은 진술에 한정한다.** 네 직접열람 메일 중 실패보고 2개와 보조 후속 응답 2개의 저작 경계를 유지한다. 후속 메일에 인용된 원 요청·응답을 별도 직접열람으로 추가하지 않는다. lists.gnu.org와 mail.gnu.org 별칭, HTTP/HTTPS 재시도, 같은 월 index의 접근 시도는 새 1차 저작이 아니다. 같은 thread의 모집 사건은 원 요청 계보에 묶으며, 후속 메시지를 읽었다는 사실로 접근 실패한 원 요청을 읽었다고 하지 않는다.

**타분야는 규격 2개와 실제 자료 2개로 배당한다.** IIIF Presentation 2.1/3.0은 같은 규격 계보 1개, Harvard Art Museums의 object 299843 manifest는 실제 박물관 발행 자료 1개, RFC 9110은 원 규격 1개, 고정 commit의 Werkzeug 원 테스트는 실제 구현 사례 1개다. Harvard의 Canvas 7개나 테스트 assertion 수를 독립 저작으로 세지 않는다. 별도 IIIF cookbook recipe는 구성 예제로 총계에는 남기되 실제 박물관 자료 배당을 추가로 채우는 데 쓰지 않는다.

## 필수 배당의 구체적 선택

| 층 | 배당한 정규화 source_id |
|---|---|
| 요청 3 | `GREC:G-REQ-56680`, `GREC:G-REQ-57026`, `GREC:G-REQ-57268` |
| 공식문서·원례 8 | `GOLD:G1-EXAMPLE`, `GOLD:G2-EXAMPLE`, `GOLD:G3-EXAMPLE`, `GOLD:DOC-GODOT`, `LREC:L-D01`–`LREC:L-D04` |
| 회귀·실패 6 | `GREC:G-SCREEN-57714`, `GREC:G-SCREEN-58003`, `GREC:G-SCREEN-61053`, `LREC:L-F01`, `LREC:L-F03`, `LREC:L-F04` |
| 타분야 4 | `SUPP:X-IIIF`, `SUPP:X-HARVARD`, `SUPP:X-RFC9110`, `SUPP:X-WERKZEUG` |

문서층은 원 사례와 안정판 매뉴얼, 실패층은 두 분야의 별도 원 보고 및 서로 다른 검증 대상 fixture를 선택했다. 모든 초과 자료도 원장·독립 저작 목록에 남긴다. 선택은 자료 역할·판·저작 중복에 따른 장부 배당이며 수신 성과나 기대 답에 맞춘 사건 대체가 아니다.

## 대표 원문 재열람

이번 출처 감사는 기존 **1차 저작 10개와 제외 재게시 1개**를 직접 다시 열었다. 성공 도구 개봉은 **12회**이며 RFC의 처음 열기와 해당 절 열기가 각각 1회다. 이 재열람은 고유 저작 수에 **0개**를 추가한다. 자세한 도착 URL, 시각 정밀도, 담당 문맥과 위치는 `allocation.json.audit_rereads`와 정규화 각 행에 있다.

| 재열람 원문 | 확인한 정확한 위치 | 시각과 한계 |
|---|---|---|
| [Godot 3.4 Resources](https://docs.godotengine.org/en/3.4/tutorials/scripting/resources.html) | Nodes and resources, External vs built-in, Loading resources from code, Loading scenes, Freeing resources; rendered lines 6–89 | 02:13:28 UTC까지 완료한 배치, 개별 요청시각 미기록. 같은 매뉴얼 경계 확인 |
| [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#section-8.6) | §8.6 Content-Length, lines 1744–1765 | 같은 조회 배치 clock 02:13:28 UTC. 개별 완료 미계측; 원문 조건문 확인만 |
| [IIIF Presentation 2.1.1](https://iiif.io/api/presentation/2.1/#basic-types) | §1.2, §2.1 Manifest/Sequence/Canvas, lines 88–116 | 같은 조회 배치 clock 02:13:28 UTC. 개별 완료 미계측; 판·정의 확인 |
| [Werkzeug 고정판](https://github.com/pallets/werkzeug/blob/6389612fd1ee1bd93579eed5026e8fd471d04abd/tests/test_wrappers.py) | lines 1064–1073, `test_response_304_no_content_length` | blob `8bc063c74f81c005258e135ea4bae2785df1eb69` 일치. 같은 배치 clock 02:13:28 UTC; 실제 HTTP 도착 URL 미노출, 실행 아님 |
| [Godot docs #5675](https://github.com/godotengine/godot-docs/issues/5675) | 선행 #5597 댓글 1039255921을 원문으로 지목한 귀속 표기 | 02:16:10 UTC까지 완료. 제외 재게시 경계 확인 |
| [Learning Manual](https://lilypond.org/doc/v2.24/Documentation/learning/scores-and-parts) | 2.24.4 §4.4.5, `hornNotes`, `include` | 하위 출처 감사 02:13:32–33 UTC |
| [Notation Reference](https://lilypond.org/doc/v2.24/Documentation/notation/different-editions-from-one-source) | §3.4.2, Using variables/Using tags | 같은 배치, 별도 매뉴얼 경계 확인 |
| [Extending LilyPond](https://lilypond.org/doc/v2.24/Documentation/extending/lilypond-variables) | 2.24.4 §1.2.2, lines 20–22 | 같은 배치, 음악 변수와 Scheme 음악식 범위 확인 |
| [Contributor Guide](https://lilypond.org/doc/v2.24/Documentation/contributor/lilypond-scoping) | 2.24.4 §10.14, lines 12–21 | 같은 배치, 파일 및 중첩 scope 설명 확인 |
| [Changes](https://lilypond.org/doc/v2.27/Documentation/changes-big-page) | 2.27.5 since 2.26, Major changes, lines 30–36 | 같은 배치, 개발판과 과거 판 구분 |
| [tag-filter 원문](https://lilypond.org/doc/v2.24/input/regression/f5/lily-a8bde065.ly) | `sourcefilename`의 `input/regression/tag-filter.ly`, `common`, `keepWithTag`, 세 Staff | HTTP200 02:14:57.575896 UTC. 기존 SHA-256 `2942592c…7c416c` 일치. 조판 실행 아님 |

이번 감사에서 .ly 4개는 웹 도구의 `text/x-lilypond` 미지원으로 실패했고, 그중 대표 1개는 공식 HTTP GET으로 다시 받아 위와 같이 확인했다. 나머지 회귀 3개는 기존 HTTP200·해시 영수증 대사에 한정한다. 메일 4개 원 URL은 이번에 모두 timeout이었다. **기존 원장에 남은 직접열람을 부정하지 않지만 이번 감사가 그 본문을 독립 재확인했다고 쓰지 않는다.** 이 8회 감사 접근실패는 기존 원장 접근실패 12행과 별개이다.

## 접근·시각·범위 한계

97행 모두의 외부 원문을 새로 여는 전수 재현은 수행하지 않았다. 원장의 저자·판·정확한 위치·한계와 가용 영수증을 전수 대사하고 대표 원문을 다시 열었다. 긴 진단 중간을 읽지 않은 두 Godot 이슈, bounded symbol만 읽은 엔진, 원문만 읽고 실행하지 않은 테스트·회귀 자료의 범위를 정규화에서 보존했다. 한 구간의 열람을 저장소 전체 독해나 프로그램 실행으로 확대하지 않는다.

Godot 원장 시각은 첫 열람 뒤 다시 수행한 GET의 시각이라는 영수증 설명을 보존했다. 이미 문서화된 반복 GET **40회**는 새 저작 수가 아니며, 정규화 중복행 11개나 이번 감사 개봉 12회와 단순 합산해 전체 접근 횟수라고 하지 않는다. LilyPond 매뉴얼·메일 공통 시각은 연구 단계 종료 후 기록시각이다. 회귀 4개와 Harvard는 기존 수신 영수증의 정확한 시각으로 정규화하고 원래 값을 `provenance.original_row`에 남겼다. gold 원장의 시간 구간을 개별 순간시각으로 만들어내지 않았다.

후속 `../gold-work/clarifications.md`에 따르면 공통 `01:52:00Z/02:00:02Z`의 시작은 **회고적으로 분 단위 반올림한 추정**이며 실제 첫 읽기 계측값이 아니다. 종료값은 실제 clock 관측이지만 그 후에도 일부 후속 읽기가 이어졌으므로 **모든 행을 포괄하는 상한도 아니다**. 원장의 `bounded observed session interval`은 정밀도를 과장한다. 해당 **24행의 `accessed_at_utc`는 null**로 정규화하고 원 구간과 정정은 `reported_session_label` 및 원행에 보존했다. 나머지 gold ZIP 3행의 개별 UTC는 바이트 수신 완료로만 인정한다. 이 provenance 공백을 출처수에서 숨기지 않으며, 개별 읽기 순서나 사전봉인 준수는 이 구간만으로 증명할 수 없다. 원장과 봉인된 결과는 수정하지 않았다.

원장의 `reading_actor=protocol_audit`는 그대로 보존했다. 개별 이름이 없는 LilyPond 및 supplemental 원장에는 `not_recorded_by_name`을 쓰고 추정자를 사실로 채우지 않았다. 이번 감사 주체는 `/root/source_audit`, 한정 하위 경계 검토는 `/root/source_audit/lilypond_boundary`로 따로 표시했다. 이 구분은 독립 gold 또는 독립 수신 절차를 새로 증명하지 않는다.

LilyPond의 고정 모집 index가 확보되지 않았으므로 시간순 첫 40의 분모는 **unknown**이다. 공석은 0개 사건으로 남기며 전체 사용자 문의가 없었다고 해석하지 않는다. Godot의 현재 이슈 본문은 편집 가능하고 일부 후속 기록은 2025 이후이므로 생성 당시 스냅샷과 동일하다고 주장하지 않는다. 이 감사는 기준답·수신 답·성과를 보고하지 않는다.
