# P3 사후 판독 — JEP97

원 검색 봉인 `fbc05801af45f21e60d6901f3293f9af9969ef8d` 이후의 조사다. 원 검색의 순위·분모·판정·비용은 수정하지 않았다. 별도 사후 열람 24회와 출처 행 17개를 남겼으며, 출처 행 수를 독립 원저작 수로 쓰지 않는다. 같은 모델의 문맥을 이어받은 작업자가 수행했고, 독립 인간 판독이나 무힌트 실험이 아니다.

## 가장 중요한 변경: 첫 통합판과 최초 생존 브랜치판이 다르다

| 층 | Git 증거 | 그 판에서 읽은 조건 | 영향 |
|---|---|---|---|
| 최초 생존 PR 브랜치판 | [0f4510266ead738e62f1d9e412d6bb9e7eb7a97d](https://github.com/jupyter/enhancement-proposals/blob/0f4510266ead738e62f1d9e412d6bb9e7eb7a97d/97-add-schema/add-schema-to-notebook-format.md), 작성 2023-03-08 20:28:15Z, 커밋 20:33:35Z; 파일 added, blob `78d78356ae2388a2cb99e67fc062e5fe1019a5eb` | L19–60 정규 URI와 ../ 경계, L110–113 옛 필드 유지가 있다. L74–96의 minor는 minimum 6이고, 불변 문서·일대일 매핑·const 6은 없다. | 봉인한 C2 전체가 창설 때부터 있었다고 말할 수 없다. |
| 수정 PR 브랜치판 | [e2651761a98f673d9c1e05d02e33ac4b3668c736](https://github.com/jupyter/enhancement-proposals/blob/e2651761a98f673d9c1e05d02e33ac4b3668c736/97-add-schema/add-schema-to-notebook-format.md), 2023-03-14 18:16:02Z | L19 일대일, L30 불변, L64·71 const, L580 매핑 조건이 추가돼 있다. | 봉인 C2는 이 후행 층에서 확인된다. |
| 첫 main 통합판 / 봉인 실험 입력 | [b9ab810ae0fc50ac7494fdf9d345738e1cf6751d](https://github.com/jupyter/enhancement-proposals/blob/b9ab810ae0fc50ac7494fdf9d345738e1cf6751d/97-add-schema/add-schema-to-notebook-format.md), 2023-07-11 | 실험에 사용한 조건이 있으나 후행 토론과 수정을 거친 판이다. | 기존 실험은 이 판을 대상으로 한 관측으로 남긴다. 최초 제안 실험으로 승격하지 않는다. |

근거: PS-P3-S02–S04, P3-POST-D01. 3월 8일 파일 자체의 date-started는 3월 1일이지만, 그날 원고는 확보하지 못했다. 위 첫 생존 브랜치보다 앞선 모든 Git·비Git 원고가 없다는 주장도 하지 않는다. 또한 수정판의 diff에는 required에 $schema가 추가되지만 확장 schema의 required에는 빠진 내부 불일치가 있어 하나의 실행 가능한 명세로 합성하지 않았다.

## Q7: 제안자가 이미 알고 있던 것과 새로 확인한 것

[3월 16일 agoose77의 발언](https://github.com/jupyter/enhancement-proposals/pull/97#issuecomment-1471548986)은 기존 additionalProperties:false가 추가 필드를 거절하고, nbformat은 검증 오류를 알리면서도 읽을 수 있으며, 옛 필드 유지는 충분히 관대한 소비자에만 도움이 된다고 설명한다. 따라서 strict validator 반례를 제안자에게 새로운 설계 지식이라고 주장할 수 없다. [3월 17일 bollwyvl의 발언](https://github.com/jupyter/enhancement-proposals/pull/97#discussion_r1139519862)은 스키마를 런타임에 원격으로 가져오는 것을 요구해서는 안 된다는 조건을 이미 제시한다. C가 찾은 식별과 실행 시 해석의 분리도 URL만으로 신규라고 셀 수 없다. 근거: PS-P3-S01, P3-POST-D02–D03.

[7월 11일 수락 발언](https://github.com/jupyter/enhancement-proposals/pull/97#issuecomment-1630425438)은 찬성 8, 반대 0, 기권 0, 미투표 3을 적고 있고, PR은 같은 날 병합됐다. 현재 수정 가능한 PR 본문에는 찬성 체크박스 9개가 있어 당시 발언의 숫자와 합치지 않았다. 제안 수락은 확인했으나 JEP97의 실제 구현·배포·사용 결과는 이번 출처에서 확인하지 못했다. 검색에 명시적 후속 구현이 나타나지 않았다는 사실도 구현 부재의 증거는 아니다. 근거: PS-P3-S01, evidence.json, P3-POST-D04.

## Q4·Q5: 옛 독자가 읽는가와 엄격한 검증을 통과하는가는 다른 관측이다

PR 생성 전에 발행된 [nbformat v5.7.3](https://github.com/jupyter/nbformat/releases/tag/v5.7.3)은 2023-01-12 발행, 커밋 `bbd0f83b67a126cd04c48a03ad053c52e6597d96`이다. 이 판의 [reads 코드](https://github.com/jupyter/nbformat/blob/bbd0f83b67a126cd04c48a03ad053c52e6597d96/nbformat/__init__.py#L63-L98)는 ValidationError를 기록한 후 노트북을 반환한다. [validator 코드](https://github.com/jupyter/nbformat/blob/bbd0f83b67a126cd04c48a03ad053c52e6597d96/nbformat/validator.py#L45-L107)는 현재보다 높은 minor를 검사할 때 최신 로컬 schema의 additionalProperties를 완화한다.

따라서 같은 추가 필드라도 raw 4.5 schema를 직접 적용하는 검사, nbformat의 미래 minor 검사, nbformat.reads의 반환 여부가 다른 관측을 낼 수 있다는 적용 가설이 생긴다. 이 코드는 canonical URI 판별이나 불변 URI↔내용 매핑을 구현했다는 증거가 아니다. PS-P3-S11–S13, P3-POST-D02.

원래 [TestAPI.test_capture_validation_error](https://github.com/jupyter/nbformat/blob/bbd0f83b67a126cd04c48a03ad053c52e6597d96/tests/test_api.py#L71-L100)와 [test_future](https://github.com/jupyter/nbformat/blob/bbd0f83b67a126cd04c48a03ad053c52e6597d96/tests/test_validator.py#L203-L213)는 이러한 차이를 기대한다. 여기서는 시험을 실행하지 않았다. release commit의 check-runs API가 돌려준 0은 현재 반환된 CI 기록 개수이며, 과거 시험이 없었다거나 통과했다는 뜻이 아니다. PS-P3-S14–S16, P3-POST-D08.

별도의 선행 결정 [PR343](https://github.com/jupyter/nbformat/pull/343)은 normalize가 relaxed validation을 대체하지 못한다는 이유로 해당 옵션의 폐기를 되돌렸다. 2023-01-12 병합과 v5.7.3 출시 포함은 확인된다. 작성자가 설명한 nbviewer 실패는 직접 재현하지 않았다. 이것은 JEP97 채택 기록과 구분되는 기존 검증 정책의 실제 수정 사건이다. 이 PR과 출시를 하나의 독립 사건으로만 산입한다. PS-P3-S17·S11, P3-POST-D05.

## VTML의 당시 존재와 gist 접근 실패

[WWW4 공식 전체 프로그램](https://www.w3.org/Conferences/WWW4/Program_Full.html)의 1995-12-12 P01 세션에는 Vitali·Durand의 논문과 원문 링크가 있다. 원 검색 B에서 직접 읽은 [원논문](https://www.w3.org/Conferences/WWW4/Papers/190/)의 버전 투영 원리는 2023년보다 앞선 발표 자료임을 확인했다. JEP97 저자가 이를 알았는지, 2023년에 유지되는 재사용 구현이 있었는지는 미확인이다. 이번 논문 재열람 응답은 rewritten summary로 표시돼 새로운 직접 읽기나 원저작 수로 세지 않았다. PS-P3-S07–S10, P3-POST-D06.

최초 브랜치부터 알려져 있던 [Bollweg migration gist](https://gist.github.com/bollwyvl/a6e1ae13125f01ff04edf121e30a462a)는 HTML과 raw 두 경로 모두 접근에 실패했다. 내용을 추정하거나 원저작 수에 넣지 않았다. PS-P3-S05–S06, P3-POST-D07.

## 남는 최소 행동

[ NEXT.md ](NEXT.md)에 옛 버전·입력·명령을 고정했다. `probe_notebook_compatibility.py`와 `fixtures.json`은 재개용이며 실행되지 않았다. 이 폴더에 추가한 독립 산입 단위는 PR343 사건 1건이며, 같은 JEP의 여러 판·토론, 기존 nbformat 소스의 여러 파일, VTML 재열람·발행 metadata는 중복 산입하지 않는다.

| 가장 중요한 약점 | 다음 첫 조사 | 판단이 바뀔 관측 |
|---|---|---|
| 최초 main보다 앞선 생존 브랜치에서 봉인 C2가 빠져 있다. 3월 1일 원고도 미확인이다. | 3월 1일 원고나 그보다 앞선 branch/blob을 확보하고 immutable·bijection의 존재를 대조한다. | 실제 창설 원고에 두 조건이 함께 있었음을 입증하는 고정 원문이면 최초판 부적격 판단을 재검토한다. |
| 옛 라이브러리 코드와 시험의 기대를 읽었으나 목표 독자 환경을 실행하지 않았다. | 고정 v5.7.3 환경과 실제 소비자 버전에서 보존한 4입력을 검사한다. | 같은 구성에서 read/validate 실패·성공이 가설과 다르면 C1 적용 가설을 수정한다. |
| gist 본문과 JEP97 실제 출시 경로가 미확인이다. | gist API receipt를 확보하고 JEP97 구현 commit→test→release를 하나의 계보로 잇는다. | 실제 구현과 시험이 같은 C1/C2를 충족하면 제안 수락만 확인된 상태를 실제 적용 근거로 갱신한다. |

