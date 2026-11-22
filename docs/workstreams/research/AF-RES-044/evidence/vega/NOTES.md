# Vega-Lite 원장 판독 — AF-RES-044

## 고정 순서와 분모

규칙은 공통 SCOPE v1이다. GitHub API 고정 질의 `repo:vega/vega-lite is:issue created:2020-01-01..2025-12-31 support in:body`, created asc·최초40을 취득했다. `frame-V.csv`는 40노출을 전부 보존한다. 첫 계약층 두 건 #5751·#5755, 첫 이름/지원층 두 건 #6135·#6860을 선택했다. #6062의 texture/pattern은 encoding object/channel 조건을 가진 실제 요청이어서 이름층으로 낮추지 않았다. 유지보수 TODO·기능 통합 설계·중복해법 재서술은 이름만 요청으로 바꾸지 않았다.

요구·토큰·발견 범위를 먼저 `requirements-V.json`, `discovery-plan.json`에 썼다. 이후 공식 HTML 목차에서 실제 href만 추출하고 `freeze-V.json`에 24슬롯 입력의 SHA를 봉인했다. 후보 본문을 읽은 시각은 `candidate-fetch-receipts.json`, 뒤늦게 댓글을 연 시각은 `comment-read-receipts.json`에 있다. 이 경로 작성자는 A/B/C를 계산하지 않았다. 부모가 ① 원격 커밋 SHA를 0832f18bcb040871fa300db708a67d6f7f8866c7로 제공했으며, 로컬 b3ed7b4는 동일 tree를 원격 API로 저장하기 전 커밋이었다.

첫6 규칙의 결과는 V1 config→View Configuration 1개+빈5, V2 projection 5개+빈1, V3 text 5개+빈1, V4 transform 첫6이다. 비빈17·빈7·고유 exact URL17·독립 후보 HTML5다. 의미 판독이 불리하다는 이유로 title나 tree 해법 링크로 교체하지 않았다. 긴 generic token이 먼저 선택되는 이 전향 규칙 자체가 V1에서 부제 config가 아닌 view config를 수집하는 원인이 되었다. 이는 병합 이전 후보 수집 부족이며 병합 손실이 아니다.

## 원요구와 판정

| 요구 | 층 | 보존한 요구 | 원풀 관측 | 근접 오답 |
| --- | --- | --- | --- | --- |
| V1 [#5751](https://github.com/vega/vega-lite/issues/5751) | K | v4 schema·당시 latest에서 config로 title과 subtitle을 red로 설정 | `spec.html#config`는 view 크기/배경이다. subtitleColor나 원 버그 해결의 근거가 없다. 완전 대안0. | direct title 속성으로 우회하는 것은 원 config 경로의 성공과 다름. |
| V2 [#5755](https://github.com/vega/vega-lite/issues/5755) | K | 미터 단위 데이터·identity/reflectY에 graticule labels를 결합해 투영 유지 | Projection Types의 identity/reflectY 하위조건은 확인. graticule 결합까지 가진 V2.A1 전체와 labels 성공 V2.A2/A3는 미확인. 완전 대안0. | mercator에서 되는 결과를 identity 요구의 해결로 세면 방향/조건이 바뀜. |
| V3 [#6135](https://github.com/vega/vega-lite/issues/6135) | N | Vega-Lite에 word-cloud 지원 | text mark와 텍스트 속성만으로 word-cloud layout 지원을 입증하지 못함. 완전 대안0. | Vega wordcloud 지원을 Vega-Lite 지원으로 전이. |
| V4 [#6860](https://github.com/vega/vega-lite/issues/6860) | N | Vega-Lite tree transform·dendrogram 계열 지원 | transform/aggregate 지원 문서에 tree 지원 근거가 없음. 완전 대안0. | 일반 aggregate 또는 별개 Vega tree transform을 원 Vega-Lite 기능으로 취급. |

V3 최초 요청의 두 문장은 짧아 그대로 보존할 수 있다: “Vega supports word cloud. Please also support it in vega-lite as well.” 나머지 원요구의 첫 문장은 requirements 원장에 있다. 이슈 본문은 API의 최초 게시자 body 현행 스냅샷이다. 생성일·수정일·body 해시를 남겼으며 편집 이전 역사판은 **미확인**이다. 댓글을 최초본문으로 섞지 않았다.

`coding-V.json`의 supports/full_document_supports는 빈 집합이다. 이는 관측한 원풀의 완전 필수 atom 입증이 없다는 뜻이다. V2의 identity·reflectY는 봉인된 compound atom 일부만 만족하므로 `subcondition_facts`에 남겼다. 같은 요구 원자를 판독 후 잘게 쪼개 입증 수를 늘리지 않았다. 조건부 상태를 예로 바꾸지도 않았다.

## 무손실 반례와 다른 문서/다른 구현

V2 첫 링크의 고정800단어 창에는 identity(725번째 token), reflectY(735번째 token)가 들어 있다. [Projection Types](https://vega.github.io/vega-lite/docs/projection.html#projection-types)의 별도 카드가 가려져도 그 하위조건의 근거는 첫 대표 본문에 이미 있다. 후보 카드 손실과 문서 근거 손실을 구별해야 한다. 반대로 기본 창이 Documentation Overview의 세 링크뿐인 V2-2에서는 해당 속성을 읽었다고 세지 않는다. 같은 문서 전체를 허용하면 이 제한은 달라지지만 graticule labels의 완전 해결은 여전히 생기지 않는다.

[Aggregation](https://vega.github.io/vega-lite/docs/aggregate.html)의 encoding aggregate와 transform aggregate는 같은 상류·같은 집계 목적이지만 JSON 배치가 다르다. 이것은 tree layout의 대안도 아니며 호출 계약을 없애는 근거도 아니다. [Vega tree](https://vega.github.io/vega/docs/transforms/tree/)와 [Vega wordcloud](https://vega.github.io/vega/docs/transforms/wordcloud/)는 공식 지원 문서를 직접 읽었지만 주 원풀 밖의 반증이다. Vega-Lite Overview가 기술하는 compile 방향은 Vega-Lite→Vega이다. 모든 Vega transform을 Vega-Lite 문법에서 사용할 수 있다는 역방향 보장은 아니다.

## 같은 상위 이슈의 군집 의존

봉인 뒤 댓글에서 [#6135의 유지보수자 판단](https://github.com/vega/vega-lite/issues/6135#issuecomment-601549625)과 [#6860의 유지보수자 판단](https://github.com/vega/vega-lite/issues/6860#issuecomment-753447333)이 모두 #1872를 duplicate 대상으로 연결함을 발견했다. [#1872 최초본문](https://github.com/vega/vega-lite/issues/1872)은 geographic/dorling cartogram과 treemap 요청이다. V3의 word cloud, V4의 tree/dendrogram을 그대로 다시 적은 문장은 아니다. 서로 다른 소비자의 구체 기능지원 요구를 독립 표집 단위로 유지하되, 공통 유지보수 결정 군집을 공유한다. 이 네 건을 통계적 독립 표본으로 보장하거나 빈도 신뢰구간으로 확대하지 않는다. 후속 조사는 서로 다른 해결·정책 군집의 두 이름 요청을 새 전향 표본으로 먼저 봉인하는 것이다.

## 도달 범위와 정확성

`windows-V.json`은 17 URL의 실제 fragment 존재, HTTP 문서 해시, 엄격 판독창·전체문서 해시, 실제 href 및 단어 위치를 제공한다. 비빈17에 대응하는 독립 HTTP 원문 요청은5다. 같은 HTML을 여러 fragment로 다시 읽은 것을17개 독립 원문으로 세지 않았다. 실제 사람의 클릭·채택은 전부 **미확인**이다. 부모의 별도 두 클릭 하네스가 시행별 도착을 기록한다.

첫 임시 추출기에서 HTML comment node를 문자열 element로 취급해 두 번 실패했다. 최종 `window_metadata.py`는 comment/script/style/form/edit controls를 제외하고 h1 뒤에서 정확히800 공백 token을 센다. 임시 출력의 h1 포함·text_content 붙임 차이를 최종 위치로 쓰지 않았다. 후보 순서/요구/그룹 key를 바꾼 것이 아니라 사전 판독창을 구현한 추출 오류 정정이다. 재판독한 identity 위치는 위 수치와 같다.

정확 semver는 게시 index에 명시되지 않으므로 C key는 미확인 필드를 가진 singleton이다. 본문에 v6 schema 예가 보이더라도 이를 exact release 또는 v4 역사판 동일성으로 소급하지 않는다. 정체성 metadata는 gold 판독 전 공식 목차 라벨·URL·edit-page repository에서 만든 `metadata-V.json`을 그대로 쓴다.

## 파일과 재개

- 입력: frame-V.csv, requirements-V.json, discovery-plan.json, pool-V.csv, metadata-V.json, toc-hrefs.json, freeze-V.json.
- 판독: sources-V.jsonl, candidate-fetch-receipts.json, windows-V.json, coding-V.json, near-misses-V.json.
- 반증: comment-read-receipts.json, supplement-read-receipts.json와 본 메모.
- 공급자 문서 재취득: `python -B docs/workstreams/research/AF-RES-044/evidence/vega/read_candidates.py`; 창 metadata 재생성: `python -B docs/workstreams/research/AF-RES-044/evidence/vega/window_metadata.py`. 현재 HTML이 바뀌면 옛 hash를 덮지 말고 새 진단 출력으로 별도 비교한다.
- 임시 원본문 전체 사본은 공개 결과에 넣지 않는다. 재취득 해시·정확 href·자체 요약을 보존한다. 공급자 실행·렌더링·역사 환경 재현은 수행하지 않았다.
