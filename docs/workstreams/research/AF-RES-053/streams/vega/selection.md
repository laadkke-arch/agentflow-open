# Vega-Lite 모집·선정 메모 — 후속 자료 열람 전

작성 주체는 root의 같은 모델 보조 작업자 `vega_frame`이다. 독립 사람 평가가 아니다. 이 메모를 쓰기까지 후보의 댓글·상태·반응 수·연결 PR·릴리스·시험·후속 출력은 열지 않았다. 문서 비교도 아직 하지 않았다.

## 모집 완전성

단어별 검색의 반환 수는 label 26, overlap 1, axis 41이며 `incomplete_results:false`였다. 그러나 GitHub의 단어 검색과 고정한 제목 substring 조건은 다르다. 전 issue의 created/asc 메타데이터를 100개씩 4페이지(400개)까지 읽어 제목만 필터했고, 첫 40의 마지막 생성일보다 뒤인 2023-10-23까지 닿았다. 전체 기간의 검색 total_count는 513이다. 이 감사에서 단어 검색에 없던 #7161, #7193, #7810, #8272를 첫 40에 복구했다. 정렬·선정 규칙을 바꾼 것이 아니라 검색 도구가 빠뜨린 항목을 보충한 것이다. 400개 본문을 판독한 것은 아니다. 첫 40개만 본문 판독했다.

- 고정 frame은 2021-01-06 #7161부터 2023-01-19 #8656까지 40행이다.
- 각 실제 issue REST 본문을 다시 직접 열어 검색 때 읽은 body와 SHA256을 비교했다. 40개 모두 일치한다. #8656은 urllib 요청에서 403을 받았고 같은 공개 issue를 GitHub connector로 열어 복구했다.
- #7887의 body는 null이다. 빈 본문 확인은 모집 행에는 남기되 실질 원문 저작 수에는 넣지 않는다. 실질 본문은 39개, 선정 요청은 3개다.
- 모든 본문은 이번 세션의 최초 가용 REST 판이다. 처음 생성할 때의 수정 전 본문과 제목을 복원한 증거는 없다. 현재 제목·본문으로 정한 표본이며 당시판 인과 판단은 보류한다. 정확 본문 해시·행 수는 frame.csv에 있다.
- vega_frame은 본문에서 등장한 이미지·editor·gist·예제·PR 링크의 목적지를 열지 않았다. 이후 root가 #7278의 본문 data 첨부를 열었으며 아래에 별도로 기록했다. 본문에 적힌 해결책과 링크 제목의 노출은 frame.csv에 남겼다.
- 고정 substring frame 안에서 완전 단어 `label|overlap|axis`에 맞는 행은 30/40이다. 이는 exact-word 규칙의 새 첫 40 재모집이 아니라 현재 frame 내부의 민감도다.
- 재현 조회 URL·시간·반환 번호는 retrieval-receipts.json, 직접 issue body 확인은 direct-body-receipts.json. cache/는 원문 임시 보관이며 .gitignore로 커밋에서 제외했다.

## 첫 세 적격 요구

선정에서 정상·경계는 연구자가 새로 만든 이상적 입력이 아니라 본문에 서로 구별되어 적힌 입력 조건을 뜻한다. 정상 동작이 반드시 실행 검증됐다는 뜻은 아니다. 입력·원하는 화면 속성이 본문에 있고 경쟁 조작의 정답이 본문에서 확정되지 않은 첫 세 건을 골랐다. 선택지는 연구자 제안이며 당시 API 가용성을 아직 확인하지 않았다.

| 자리 | issue·일자 | 본문 위치 | 명시 입력·목표 | 정상·경계 | 원문 명시 금지 | 연구자 추정·결손 |
| --- | --- | --- | --- | --- | --- | --- |
| V01 | [#7278](https://github.com/vega/vega-lite/issues/7278), 2021-03-02 | body L3-L7, L12-L75, L78-L80 | wrapped facet에서 bar/line의 독립 Y axes. nested Elasticsearch `_source` fields와 count/sum이 spec에 있음 | 정상은 첫 editor 링크의 dual-axis 예제, 경계는 자기 nested data로 바꾼 코드. 본문은 이 차이를 명시 | 별도 금지 문장은 없음 | 수치값·facet 수 보존을 연구자 제약으로만 가정. root가 원 첨부 `asset_data.txt`를 확보했으며 nested data 135행 확인. 정상 editor의 압축 spec은 아직 미복원. schema v4는 정확 runtime patch를 증명하지 않음 |
| V02 | [#7422](https://github.com/vega/vega-lite/issues/7422), 2021-04-30 | body L1-L3, L5-L67, L70 | scatterplot matrix의 값 접근을 유지하고 축·범례 제목에 escape backslash가 보이지 않아야 함 | 정상은 원래 일반 이름의 예제, 경계는 이름에 `.[]`가 있는 3개 penguin record와 repeat row/column | `.[]` 필드 접근에는 escape가 필요하다는 저자 설명 | 다른 4×4 cell의 축 제목은 각 field에 대응해야 함. 하나의 고정 title을 모든 cell에 복사하면 목표를 바꿀 위험. 정확 제품판 미명시 |
| V03 | [#7507](https://github.com/vega/vega-lite/issues/7507), 2021-06-04 | body L1-L5, L8-L63, L78-L95 | y축 section 라벨 중 resilience=0만 빨강, 다른 라벨은 검정 | 정상은 resilience 31/19/39/47/25/16/25/46/문자열 1의 9개, 경계는 fifth section의 numeric 0 | 별도 금지 문장은 없음 | 이름·순서·값 대응 유지와 추가 동적 입력은 연구자 제약. schema v2와 condition object의 당시 가용성은 아직 검증 전. 실제 runtime patch 미명시 |

## 문서 비교 전의 후보 A/B 제안

아래 조작은 정답·당시 가용성 확정이 아니며 root가 카드 봉인 전에 API 확인 여부를 기록해야 한다. 본문 밖 일반 기술 지식에서 제안한 부분도 여기 공개한다.

| 자리 | A 후보 | B 후보 | 공통 입력·한 번에 바꾸는 속성 | 판정 허용 규칙 |
| --- | --- | --- | --- | --- |
| V01 | 원 입력에서 nested fields의 값은 그대로 두고 평평한 별칭으로 materialize하여 facet/encoding에서 별칭 참조 | nested path를 그대로 두고 independent y scale의 선언 위치/범위를 바꿈 | 입력 record·aggregate·wrapped facet 요구는 동일. A는 필드 표현, B는 scale resolution 범위 | 두 독립 Y axes가 실제로 보이며 각 bar/line 집계값과 원 record 대응이 보존되는지를 둘 다 확인. 값/축 수만 맞고 배치가 틀리면 성공 아님. 구체 API와 별칭 집합을 못 고정하면 선택지 미확인 |
| V02 | escaped field access를 유지하며 cell마다 표시 title을 원래 문자열로 별도 지정 | repeat·color field 참조에서 escape를 제거하고 자동 title을 사용 | 3개 record와 4×4 repeat 목록 유지. A는 표시 문자열, B는 accessor 문자열 | 모든 셀에서 값 접근과 각 축의 서로 다른 title 대응이 함께 필요. 정확한 per-repeat title 표현식이 당시판에서 불가하면 A 미확인. 한 title로 모든 셀을 덮는 변경을 A의 성공으로 세지 않음 |
| V03 | axis label의 category identity에 알려진 zero-category 이름을 매칭해 빨강 지정 | 원 spec처럼 source record의 resilience property를 axis label 조건에서 직접 검사 | 원문 inline 10 record·같은 축·같은 red/black 값 유지. 바뀌는 것은 조건이 참조하는 객체·속성 | 원문 sample의 1 red/9 black은 범주 예측 가능. arbitrary incoming data에서도 맞는다고 확대하지 않음. category identity API의 이름·기본값은 아직 미확인 |

V03 A의 axis-label 객체와 V02의 presentation/accessor 분리는 일반 사전지식에서 나온 후보다. N/I/D의 특정 문구에서 얻었다고 주장하지 않는다. 세 후보 모두 source/body 노출을 카드에 이어 적어야 한다.

## 앞선 제외가 결과를 바꿀 조건

| 앞선 후보 | 제외 이유 | 이 판단이 틀릴 최소 자료 |
| --- | --- | --- |
| #7161 | StackVega가 정의되지 않고 정상 비교 입력이 본문에 없음 | 최초 본문 또는 원 첨부에 정상/경계 두 입력이 실제 존재 |
| #7193 | labelExpr가 작동한다는 답이 본문에 이미 있음 | 초기판에는 그 답이 없고 후일 추가된 사실의 복원 |
| #7228 | 충돌 회피 목표는 있지만 정상·경계 Vega-Lite 입력 쌍이 없음 | 원 요청의 Vega-Lite 입력 또는 원 이미지가 두 입력을 명확히 구별한다는 직접 증거 |
| #7285 | facet→column으로 바꾸면 성공한다고 이미 쓰여 있음 | 처음에는 답이 없었던 수정판 복원 |
| #7333 | v4/v5 대비와 stack:false 성공 답이 이미 있음 | 처음에는 답이 없었던 수정판 복원 |
| #7372 | PR follow-up 링크 한 문장뿐 | 최초 본문의 독립 요구·입력 복원 |
| #7394 | tiny point의 interaction 목표는 있지만 정상 입력이 미특정 | 최초 본문/원 GIF에서 두 입력 조건과 보존할 화면 상태가 직접 확인 |
| #7407 | 원하는 nested facet 축 제목 한 번 표시는 명확하나 정상 비교입력이 없음 | 요청 당시 정상·경계 두 spec 또는 명시 조건 복원 |
| #7500 | ExprRef로 이미 작동한다고 본문에 있음 | 해결 전 초기판의 복원 |

이 자료 결손 때문에 최초판 복원 후 첫 세 적격 요구가 달라질 수 있다. 현재 frame을 성공 예측이 쉬운 후순위 사례로 교체하지 않았다.

## 원 입력 확보 보충 — 후속 결과는 아님

root가 [#7278 asset_data.txt](https://github.com/vega/vega-lite/files/6070643/asset_data.txt)를 직접 열어 26,368 bytes, SHA256 `70253a76662d3cdc0ecc8661f60262634c12f80f639b684c608703e8d9d76e9c`를 기록했다. `data.values.hits.hits` 135행이며 nested `_source.Readability`가 빈 문자열을 포함한 문자열이라는 점, inner/outer 독립 y 선언이 모두 있다는 점을 root가 확인했다. 영수증은 `../../evidence/7278-attachment-receipt.json`. 동일 이슈의 첨부이므로 새로운 독립 저작으로 세지 않는다. 정상 editor URL에 압축된 spec은 아직 복원하지 않았으므로 정상/경계의 동일성은 미확인이다. 이 보충은 첨부 입력 확보이며 해결 댓글이나 후속 출력 열람이 아니다.
