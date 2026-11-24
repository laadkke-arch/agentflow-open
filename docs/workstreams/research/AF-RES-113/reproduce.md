# AF-RES-113 재현 절차

이 절차는 고정 문서판에서12자리를 재구성하는 방법이다. 검색 시점이나 2023년 원 작성자의 지식을 재현하는 실험이 아니다. 원장에 있는 현재 본문 지문과 새 취득 본문이 다르면 새 입력판으로 기록하고 기존 원경로 판정을 소급 변경하지 않는다.

## 1. 고정 계약과 자료 순서

계획판 `670ecde1dab07aede6760618a7d907f0cdff185a`, 시작판 `581b863dfb9f90106c2a07fb749d0cada51b0a25`, 의존 인계 `e547d88834ff8adfcea9039e32c48b5be97e1eb3`, 의존 검사 결과 `c212aab782008f263cbee14f6304c029dc82ce3a`를 구별한다. 의존 결과를 다시 수행할 필요는 없다. 최종 검사 대상 결과 SHA는 HANDOFF의 `검사한 결과 SHA`를 사용하며, 마지막 HANDOFF 커밋과 같다고 가정하지 않는다.

먼저 SCOPE.md·manifest.json·evidence/start를 읽고 다음 봉인을 순서대로 확인한다.

| 단계 | 원격 SHA | 먼저 고정한 것 |
| --- | --- | --- |
| 모집규칙 | de98a81eb36893e2f8c094a18a35677fde96ff51 | 원 요청을 보기 전 모집·예산·링크선택·공석 규칙 |
| 요청 | 1be1509413347d23d34d2b609597ea23438452bc |120프레임·6요청·현재 원글 지문·대응 모호성 |
| 공통 기준 | 96a754e80f9bbeb5f65e544f7e7f81457b245971 |4시작절·2공석·13기지안/시험행·12추가 자리, 링크3개 |
| 추가 노출 |11287afdf0c3a0d990f125b72c4f75e9af42f38f |3회 개봉·각3000자·초록 한계·추출 보정·판독 packet지문 |

이후 사전 판정·검증·결과·영수증 커밋은 evidence/seals/commits.jsonl 및 HANDOFF를 따른다. 사전 판정 커밋 전에 사후 원전·외부 분야를 읽지 않았다는 시간 경계를 확인한다. 최초 일반 Git push는 인증 부재로 실패했으며, 원격 증거는 GitHub에 실제 읽히는 위 SHA다.

## 2. 모집 프레임

두 공개 API 요청을 사용한다. `is:issue`가 PR을 제외하며 `created`는 UTC 기준이다.

```text
https://api.github.com/search/issues?q=repo%3Alibrosa%2Flibrosa+is%3Aissue+created%3A2023-01-01..2024-12-31&sort=created&order=asc&per_page=100
https://api.github.com/search/issues?q=repo%3Ascikit-image%2Fscikit-image+is%3Aissue+created%3A2023-01-01..2024-12-31&sort=created&order=asc&per_page=100
```

실제 요청 URL은 각 `evidence/recruitment/*/acquisition.json`에 저장한 값이 우선한다. 응답을 `(created_at, number)`로 정렬하고 첫 60건만 frame.csv와 대조한다. 60번과 61번의 시각이 같으면 추가 페이지로 동시각 번호순을 확정한다. 이번에는 두 프로젝트 모두 경계 시각이 다르다.

선별 입력은 제목·번호·생성시각·URL이 가려진 opening body뿐이다. state·labels·comments·후속·수락을 제외한다. librosa 순번2/5/8, scikit-image 순번2/3/5가 첫 적격3건이다. 선택 전 제외7행과quota뒤미선별107행을 그대로 유지한다. 배치 출력으로 librosa10건·scikit-image12건의 본문이 노출된 사실은 별도이며,22건을 정식 모집분모로 바꾸지 않는다.

원글을 다시 읽을 때는 `/repos/{owner}/{repo}/issues/{number}`의 body만 추출하고 UTF-8 SHA256을 requests.jsonl과 대조한다. `updated_at`은 원문 최초판을 입증하지 않는다. 해시가 달라졌으면 현재판 재현 실패를 기록하고 새 봉인을 만든다.

## 3. 문서판과 네 공통 절

계획일 전 cutoff는 `2026-11-24T00:00:00Z`다. 공식 releases에서 draft/prerelease를 제외하고 published_at이cutoff이전인 최신 stable을 선택했다. 태그 ref를 실제 commit까지 해제했다.

| 프로젝트 | 안정판·고정 소스 | 공식 API 목차 |
| --- | --- | --- |
| librosa |1.0.1 /9caf46a4ecaeb8ea24bb541231065c9f761174ae |https://librosa.org/doc/1.0.1/api/index.html |
| scikit-image |0.26.0 /ee0a7a3ebd9ac8c2602f40e55bc015a3c8a81ae8 |https://scikit-image.org/docs/0.26.x/api/api.html |

R1 stream, R3 recurrence_matrix, R4 rank.otsu, R5 dilation의 각 `dt#symbol`을 포함하는 부모 `dl.py.function` 전체가 공통 절이다. R2는 요청된 librosa public symbol이 없고, R6은 복합 roundtrip 시험의 단일 API 대응을 보류했으므로 원래 공석을 유지한다. 이를 나중에 참고문헌이 있는 함수로 바꾸지 않는다.

Inline Examples·Notes·대역폭 항목의 참고문헌은 공통 노출이며 새 추가 링크 성과로 세지 않는다. `evidence/common/*-common.json`에는 실제 DOM 순서의 전체 href·제외 이유·원 docstring 대응을 저장했다. 배포 HTML에 생성되는 gallery 링크가 있으므로 소스 docstring만으로 gallery 존재 여부를 판단하지 않는다.

`acquire.py` の取得・抽出例:

```sh
python -B docs/workstreams/research/AF-RES-113/acquire.py REPLAY-R1 https://librosa.org/doc/1.0.1/api/generated/librosa.stream.html --symbol librosa.stream
python -B docs/workstreams/research/AF-RES-113/acquire.py REPLAY-R4 https://scikit-image.org/docs/0.26.x/api/skimage.filters.rank.html --symbol skimage.filters.rank.otsu
```

이 명령은 새 열람이며 원래 시행은 아니다. 저장된 text_sha256과 일치할 때만 같은 본문판으로 취급한다. HTML의 ETag/Last-Modified만으로 본문 일치를 판정하지 않는다.

## 4.12자리와 추가 열람

모든 자리의 기준은 hops.jsonl이다. URL을 선택한 후 실제 읽기에 실패해도 더 잘 열리는 링크로 해당 자리를 바꾸지 않는다.

| 요청 | A | B |
| --- | --- | --- |
| R1 |독립 예제 href없음; inline만 |원저작 href없음 |
| R2 |공통 시작 공석 |공통 시작 공석 |
| R3 |독립 예제 href없음 |Wang DOI, DOM10. 선행 Zelnik-Manor 인용에는 외부href없음 |
| R4 |Rank filters, DOM4 |Wikipedia 설명은 원저작이 아니므로 공석 |
| R5 |Cornea inpainting, DOM8 |원저작 href없음 |
| R6 |공통 시작 공석 |공통 시작 공석 |

추가 링크는 원문 main/article의 첫3000 Unicode codepoints, 그림0, 코드·표·caption도 문자예산에 포함한다. `node_text`는 각 text fragment 안의 연속 whitespace를 한 공백으로 줄이고 비어 있지 않은 fragment를 LF로 연결한다. script/style/nav/footer/hidden/headerlink는 제외한다. 이미지의 실제 픽셀은 열지 않는다. UTF-8·huge_tree와deep-copy를 쓰며 예산 밖 method 절로 건너뛰지 않는다.

R5-A 최초2261자 절단과 R3-B 오해석은 같은 응답byte 재파싱으로만 보정했다. `evidence/hops/extraction-correction.json`과 공통4개 지문 불변 검사를 읽는다. Nature 자동 cookie redirect를 실제 수신했지만 원계정 로그인은 없었다. 일회성 code 값은 영수증에서 지웠고 목적지와 error는 남겼다. 초록·구독preview를 방법 본문으로 바꾸어 세지 않는다.

## 5. 판독 재구성

서로 다른 새 자동 문맥 두 개에 같은6원글·같은공통절·기지안과 각자의추가본문만 준다. 원래 packet 원문은 외부 저작 전체 재게시를 피한 임시 캐시이고, 고정 packet 지문·공통/추가 지문·각 독자의 실제 읽은 범위는 `evidence/arms/{A,B}/`에 보존한다. 새 취득본이 지문과 맞지 않으면 원판독의 재현이 아니라 새판 시험이다.

한 경로의 판정이나 다른 경로의 추가내용, 모집자의 불필요한 옆 함수/후속 이슈 노출, 사후원전을 다른 독자에게 전달하지 않는다. 판독자는 원 요청의 변경과 보존조건을 함께 지지하는 새 단위·순서·책임·판별시험만 세고, 새로운 분야명이나 일반적인 학습을 목표 적합성으로 바꾸지 않는다. root의 종합은 양쪽을 읽은 종합이며 독립 인간 학습효과가 아니다.

## 6. 사후 원전·반례·집계

사전 판정 뒤에만 구현·회귀·원 논문 방법·외부분야를 읽는다. sources.jsonl에서 `phase`, `unique_counted`, `work_id`, `allocation`을 대조한다. 같은 API의 docstring, 같은 논문 미러/초록, 재열람과 검색metadata를 중복 산입하지 않는다. 자료배당은 요청6/프로젝트8/원방법6/외부4이며 외부는 두 분야 각2다. 발견실적과 검증자료 수는 별개다.

`decisions.csv`는12자리의 기존/새선택·구별입력·예상/관측·판정근거를 재구성한다. baseline-tests13행은 이미 알려진 안/시험이며 추가링크의 새시험 수에 합치지 않는다. transfer.csv의 사후전이는 원경로발견이 아니다. 양쪽의 추가본문을 직접 읽은 쌍만 비교가능 분모에 넣고, 나머지를 비교불가로 둔다. 빈자리9개나초록1개를 성공/부정효과로 대체하지 않는다.

## 7. 결과 SHA 검사

HANDOFF의 고정 결과 SHA를 깨끗한 checkout으로 읽은 뒤 다음을 실행한다. 아래는 재현 명령이며 이번 실제 exit코드와 실행범위는 `evidence/acceptance-evidence.json`을 따른다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-113/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-113/recalculate.py --check
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

TMPDIR은 **검사checkout의docs밖**에 두어 임시복사 재귀를 피한다. 공통검사 통과는 원프로젝트 알고리즘·MKV·S390x 실행 성공이 아니다. 명시manifest1개와자동세션발견수도별도로 기록한다. 검사 뒤 영수증·HANDOFF 변경은 검사한 결과 SHA에 소급 포함하지 않는다. 결과판 원장·RESULT·재현코드의byte동일성을 다시 대조한다.
