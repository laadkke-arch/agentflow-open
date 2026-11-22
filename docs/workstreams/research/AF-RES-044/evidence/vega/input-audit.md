# 묶음2 입력 감사 — Vega 담당 내부 재검토

감사 시각: 2026-11-22T20:35:19Z 이후. 대상 고정 커밋: `b36cc513ccbc1616168401ec9564866038e880a3`. 감사자는 V 표본을 직접 만든 같은 보조 에이전트다. 따라서 V에 대한 자체 점검이며, P·C에 대해서도 내부 병렬 검토일 뿐 사람의 독립·맹검 판독이 아니다. 이 감사에서는 입력, 봉인, 규칙 일치 여부만 검사했다. A/B/C 그룹, 회수율, 새 gold를 계산하지 않았고 원자료를 수정하지 않았다.

## 1. 감사 결론과 상태

**72자리의 선언된 순서와 80노출·23원자는 재구성된다. 그러나 이것이 자연 8요구의 실험 입력을 모두 관측했다는 뜻은 아니다.** P의 24자리는 발행 HTML 접근 실패로 생긴 관측 결측이며, V의 7자리는 실제 범주에서 관측한 링크 부족이다. 또한 원격 CSV의 줄끝이 정규화되어 봉인 SHA와 원격 바이트가 다른 오류가 있고, V3는 원요구에 없는 `text` 토큰으로 Text 범주를 선택한 사전규칙 이탈이 있다. C4의 예정 양성 자격은 봉인 원자를 엄격하게 읽을 때 아직 입증되지 않는다.

| 항목 | 감사 상태 | 확인한 사실·정확한 위치 | 허용되는 판단 |
| --- | --- | --- | --- |
| 루트 입력 크기·순서 | 검증 | `pool.csv` 데이터72행, 12 case별 rank1..6; `frame.csv` 데이터80행, P/V 각각40·노출1..40; `requirements.csv` 데이터23행 | 선언된 48 natural/24 control 슬롯과 12개 원요구 구조는 보존됨 |
| 표집 질의와 순서 | 검증 | P/V `search-receipt.json`의 저장 질의·기간·sort=created asc·per_page40; frame의 날짜/번호 오름차순과 양 원장 N2/K2 | 두 원장에 같은 사전 검색을 적용한 기록이 있음. 현재 API 결과를 역사적 최초 본문 버전으로 오인하지 않음 |
| 원요구→통합 원자 | 검증 | `evidence/cases.json`의 12개 required_atoms와 `requirements.csv`의 id/text가 전부 일치 | 통합 시 조건 삭제·추가 없음. C2 원본 R1/R2를 통합 A1/A2로 이름만 바꾸었으며 문구는 같음 |
| 실제 href resolve | 검증 | 비빈41행 모두 `urljoin(html_url, raw_href) == url`; V pool/TOC와 C freeze의 순서·DOM순번 보존 | 연구자가 URL/fragment를 만들어 채운 흔적은 이 입력에서 없음. 목적지 성공은 별도 문제 |
| P1–P4 | 검증된 결측 | `pool.csv` P1-1..P4-6 및 `evidence/pandoc/pool-freeze.json`: `unobserved`, raw HTML/hash/DOM 모두 미확인 | 원풀 완전 대안 수와 회수율은 **미확인**. 후보0·적격0·해당 없음으로 바꾸면 오류 |
| V 실제 부족 | 검증 | `pool.csv` V1-2..6, V2-6, V3-6: `exhausted_scope`; 시작 HTML 해시와 선택 범주 총 href 수1/5/5/80이 `discovery-selections.json`에 있음 | 총7개의 관측된 빈 슬롯. 단 V3 범주를 고른 규칙 이탈은 아래 별도 판정 |
| C 미확인 키 | 검증 | `display-metadata-freeze.json`: version=미확인인24행 전부 identity_key_complete=false, singleton 이유 있음; 반대 플래그 불일치0 | 기본 C 계산에서 이24개를 같은 unknown 값이라는 이유로 합칠 수 없음. U 민감도만 별도 가능 |
| C2-5 대상과 발행자 | 검증 | `control-C2.json` slot5: publisher=pandas development team, 대상 Altair; display metadata 412행부터 upstream=vega/altair, version=미확인 | pandas 2.0.3은 발행 문서판이며 Altair 구현판이 아님. host만으로 pandas 구현에 배정하면 오류 |
| C1-6 원 href | 검증된 실패 | `freeze-C1.json` 원 href `../advanced/clients/#client-instances`; candidate receipt C1-6은 HTTP200이지만 fragment_found=false | **접속 성공≠해당 절 도착 성공**. 다른 Client 절로 자동 수선하거나 전체 본문을 기본 창으로 제공할 수 없음 |
| C1-4 Requests 도착 | 판단 불가 | candidate receipt는 HTTP503 failed이고, CONTROL_SCOPE는 별도 직접 읽기·403 이력을 구분함 | 웹 원문을 읽은 사실로 실제 DOM fragment 도착 성공을 대신할 수 없음. 후속 정상 도착 관측이 없다면 클릭 경로는 미확인 |

## 2. 바이트 봉인 오류: CSV CRLF/LF

로컬 원본과 묶음2 원격 Git 객체를 직접 비교했다. JSON·SCOPE·C freeze는 바이트까지 같지만 아래 CSV7개는 로컬 CRLF가 원격에서 LF로 바뀌었다. **모든 파일의 CRLF→LF 정규화 비교 및 CSV 파싱 행 비교는 일치한다.** 이는 요구·순서·분모가 바뀐 증거가 아니라, 바이트 해시를 원격 재현성 검증에 그대로 사용할 수 없는 봉인 결함이다. 원래 해시를 지우지 않고 원격 바이트 해시와 전송 정규화 원인을 함께 보존해야 한다.

| 파일 | 원 봉인 SHA256(CRLF) | 묶음2 Git blob SHA256(LF) |
| --- | --- | --- |
| pool.csv | `3917fd7c01f2e0b9994b0fb9b231b573a0e2e75e3afc43f8dbc0d811ec28eca8` | `53ac7e9dbb95a029aae6c834e7222df3c009b1c4ad6e0993aea7b2ce62982b28` |
| frame.csv | `1aa712fd2e6fe5e8633df4b5e83bfd3a78854bdccd3610ae6d723432a4de3d0f` | `5d70e16f93431a8203d70e39142633637ef480f9a938a9b4f31377a0c1ad88c8` |
| requirements.csv | `3d2948422128c9d0b9400b84ded1ac5b3f0bbe2ebe9799275b5b535552f38391` | `28d41407046a4cad838d7040baba157283d6eee6cf73221e5571ac8ec64d1e49` |
| evidence/vega/frame-V.csv | `8a3af1481066b3f43458080acbd5e69a173750599497ad41f3c4ed5c3e1737b3` | `324b4d67f29c4e7be10d5ffc15f335b052c9368851aafc06b05a6186666ef824` |
| evidence/vega/pool-V.csv | `cbcd708af358ecdca462e0dfe0aaa5551ad7ed3a1fc3d448fe9eb363e8a5806b` | `904e19876e87043b35adcc26027b4d1fb874032fb207890712a747ed694c4983` |
| evidence/pandoc/frame-P.csv | `6458962f0733fa1ec4e844f514eeec9869274fc2b6bfd9a2c3371b8f9671bc14` | `9a2118d48b5d1d1731ba13244df5a8619c179440381f042b794fa99335ff6af5` |
| evidence/pandoc/pool-P.csv | `ec80e6c8677b3b8c53b67e9203f940592111e9093c17bb8c158bc358194f9b32` | `506f252e1f1a012224e9c765ced9980c68aad85a2a8c3cbd8c7213f2bbb996d4` |

`input-freeze.json`의 나머지 JSON2개 해시는 원격과 일치한다. P/V lane freeze에 있는 비CSV 항목도 모두 일치한다. 원격 Git 객체를 읽은 명령은 `git show b36cc513ccbc1616168401ec9564866038e880a3:docs/workstreams/research/AF-RES-044/<파일>`이며, 결과 바이트에 Python `hashlib.sha256`과 `csv.DictReader`를 적용했다. 로컬 HEAD도 감사 도중 부모가 해당 원격 SHA로 맞춘 것을 확인했다.

## 3. 사전규칙 일탈·해석 한계

### V3의 연구자 추가 토큰

SCOPE 19행은 토큰을 원요구 명사에서 가져오도록 한다. 그런데 `evidence/vega/discovery-plan.json` 41–45행의 V3 토큰 중 `text`는 [#6135](https://github.com/vega/vega-lite/issues/6135)의 제목이나 70자 최초 작성자 본문에 없다. 감사에서 API 원문을 다시 열어 확인했다. 실제 선택도 `discovery-selections.json` V3의 matched_token=`text`, matched_label=`Text`다. 따라서 이것은 **원요구의 직접 명사만 허용한다는 원규칙과 다른 연구자 연상어 확장**이다. 계획은 후보 본문 열람 전에 봉인되었으므로 나중의 적격 판정을 키나 순위에 넣었다는 증거는 없지만, 원규칙 준수로 승인할 수 없다.

영향 범위는 V3의 6슬롯 및 그로부터 나온 모든 보기·경로 해석이다. 현재 봉인 풀은 그대로 보존해야 한다. 원규칙에 따른 무일치 fallback 풀은 이 감사에서 계산·열람하지 않았으므로 결과는 **미확인**이다. 원규칙 결과가 같다고 추정하면 안 된다. V4의 `hierarchy`, P4의 `output`도 원문 직출어가 아니라 해석어지만, V4 실제 선택은 제목에 있는 `transform`이고 P4 풀은 결측이어서 이 감사에서 추가 풀 영향은 확인되지 않았다.

### 노출과 표본 독립성

SCOPE 5–7행의 사전 pilot 노출, P NOTES의 첫15본문 일괄 노출, 양쪽 원요구의 이미 제시된 비교 해법은 기록되어 있다. 따라서 완전한 무노출·맹검 설계로 표현해서는 안 된다. 첫 작성자 본문은 현재 GitHub API 본문이며 최초 게시 당시 수정 전 revision을 확보한 것은 아니다. 생성일은 frame에 있지만 현재 본문과 최초 역사적 본문 동일성은 **미확인**이다.

V3/V4는 각각 word cloud와 tree transform이라는 서로 다른 요청이고, [#1872](https://github.com/vega/vega-lite/issues/1872)는 여러 layout을 묶는 상위 이슈다. 두 건을 같은 해법의 단순 재서술이라고 단정할 자료는 없지만, 같은 상위 maintainer 결정으로 닫힌 종속성은 있다. 이 둘을 통계적으로 독립인 소비자 반응 두 번으로 일반화할 수 없다. P4의 N/K 경계와 P1 출력 방향 해석은 `evidence/pandoc/requirement-interpretation-note.json`에 이미 별도 기록되어 있으며, 봉인 원자를 사후 교체하지 않은 점은 확인했다.

### 보강 탐색 계열 확장

SCOPE의 탐색 출발 계열에서 pandas와 Python3.11로 확장한 사유는 `evidence/control/CONTROL_SCOPE.md`, `evidence/crossfield/controls-exploration-notes.md`와 실패 원장에 남아 있다. 이는 처음부터 고정된 확률 표본이 아니라 접근·해법 노출 후 고른 메커니즘 대조다. C1/C2의 원문 자연 순서는 보존되었으나, ‘같은 용도의 여러 링크’라는 양성 목표가 곧 ‘같은 호출 계약’이라는 뜻은 아니다. 모든 보강을 무조건 성공 양성 네 건으로 세는 것은 입력만으로 정당화되지 않는다.

## 4. 표시 metadata의 재현성

C2-5의 publisher와 대상 upstream 구분은 올바르다. [pandas Altair 절](https://pandas.pydata.org/pandas-docs/version/2.0/ecosystem.html#altair) 43–45행을 다시 열었으며, Altair라는 Python 도구와 DataFrame 지원을 소개하는 문서임을 확인했다. 원문판 pandas2.0.3에서 Altair 구현의 판을 가져오지 않고 미확인 singleton으로 둔 것도 적절하다. 반면 첫 C2-1은 여러 도구를 소개하는 pandas ecosystem 원문이므로, 그 카드의 upstream 하나와 카드가 입증하는 여러 대안 ID를 동일한 것으로 취급하면 안 된다.

다음 항목은 틀렸다고 확정하지 않고 **표시시점 근거의 세밀도가 부족한 값**으로 남긴다.

| metadata | 상태 | 이유·영향 |
| --- | --- | --- |
| C1-1 role=migration | 판단 불가 | 목적지는 auto-redirects 정책 GitHub discussion이다. 출발 페이지가 compatibility guide인 사실과 목적지 자체의 역할은 다르다. `upstream_evidence`는 모든 control에 공통인 문장이라 이 역할을 정한 정확한 label/위치가 없다. 현재 version unknown singleton이라 기본 병합을 허용할 근거는 되지 않음 |
| C1-2 component=httpx.get | 판단 불가 | 표시 메타 근거로 선언한 원 href/label은 timeouts이며 `httpx.get`는 API 예제에서 확인할 수 있는 값이다. 이 값을 표시 단계의 어떤 독립 추출로 얻었는지 별도 위치가 필요. 현재 version unknown singleton |
| C3-2 upstream=python/cpython | 해석 주의 | 발행 저장소는 python/peps, 문서 대상은 Python 언어 기능이다. CPython 구현으로 묶는 해석을 metadata 문장에 밝혔지만, publisher만으로 CPython 고유 구현이라고 판정한 것은 아님. Python 구현 일반과 CPython을 혼동하지 않아야 함 |
| C4-6 role=test 단일 값 | 판단 불가 | [이슈 #90908](https://github.com/python/cpython/issues/90908) 140–146행은 feature/API/test PR을 함께 나열하며 204–206행은 설계·시험 설명이다. 시험에 관한 내용은 있지만 test만이 유일한 역할이라는 메타 근거는 부족. 시험 본문을 열지 않고 실행 성공 D3로 바꿀 수 없음 |
| Python candidate version=3.11 | 세밀도 차이 확인 | pool은 발행 문서 title의 3.11.18을 보존하지만 C 키는 branch/기능 도입판3.11만 쓴다. Vega에서는 정확 semver 미확인을 singleton 사유로 썼으므로 판의 정밀도가 일관된지 별도 판단이 필요. 원키를 바꾸지 말고 이 차이를 한계로 남겨야 함 |

위 항목은 key에 gold를 넣었다는 증거가 아니다. 다만 `display-metadata-freeze.json`의 공통 출처 문장만으로 개별 component/purpose/role의 추출을 모두 재현했다고 승인할 수 없다. 실제 key 계산은 이 감사의 범위 밖이다.

## 5. C3·C4 봉인 원자와 양성 자격

### C3

`freeze-C3.json`의 두 원자는 constructor의 Exception/BaseException 경계와 except*의 부분 매칭·미처리 전파다. PEP 메타데이터는 [PEP654](https://peps.python.org/pep-0654/) 6–13행에서 Final, 작성2021-02-22, Python-Version3.11을 확인했다. `evidence/pandoc/control-review.md`의 보완 문서 판독은 이 봉인과 일치한다. C3-3/C3-4는 동일 exceptions 문서의 공유 절이므로 별도 구현 두 개가 아니며, C3-5의 except* 계약과 조합하는 원풀 양성 근거는 존재한다. 다만 이 감사는 새 수치·경로를 계산하지 않았다.

PEP 첫800 단어의 실제 목차를 따라 같은 PEP의 Specification으로 이동하면 두 역할을 한 문서에서 확인할 가능성이 있다는 반례가 이미 내부 재독에 있다. ‘동일 상류라면 반드시 보완 근거를 잃는다’는 일반화는 이 경로 검증 전 허용되지 않는다. 이는 연구자가 생성한 앵커를 추가하는 것이 아니라 원문에 있는 전이의 검사다.

### C4

`freeze-C4.json` 8–13행의 A1에는 `distinguish gather`, A2에는 두 await와 exception forwarding이 명시돼 있다. 원 request가 이 원자보다 짧다는 이유로 봉인된 추가 조건을 조용히 삭제할 수 없다.

[Data model #async-context-managers](https://docs.python.org/3.11/reference/datamodel.html#async-context-managers) 1401–1425행을 다시 읽었다. 도착절은 두 메서드의 awaitable 반환 의무·동기 메서드와의 의미상 유사성을 설명하지만, `async with` 호출자가 두 결과를 await하고 예외 정보를 전달하는 전체 절차를 직접 제시하지 않는다. 그 절차는 별도 [Compound statements #async-with](https://docs.python.org/3.11/reference/compound_stmts.html#async-with)에 있다. 따라서 다른 창의 의미를 읽은 것으로 합치지 않는 strict 판정에서 C4.A2 완전 입증은 **미확인**이다. 별도 정상 두 클릭 시행에서 두 원자 전체가 입증되는지 확인하기 전 C4를 성공 양성으로 승인하면 안 된다.

`evidence/pandoc/control-review.md` 54–59행의 엄격/넓은 해석 차이를 보존하는 것이 맞다. 이는 Python에 그 동작이 없다는 부정이 아니라, 고정한 링크·도착 범위가 요구 전체를 증명하는지의 문제다. 보강4건 모두 양성이라는 수용 조건은 아직 자동 충족되지 않는다.

## 6. 날짜·범위·다음 확인

자연 최초 노출 생성일은 모두 사전 기간 안이며 N/K 선정은 양 원장 각각2개다. 요구 봉인(P20:10:47, V20:11:50)→풀 봉인(P20:13:19, V20:13:06)→control 봉인(20:18:08)→공통 봉인(20:26:00)의 파일 시각은 기록과 양립한다. 하지만 시각 문자열 자체는 독립 타임스탬프 서비스의 증명은 아니다. API 현재본문과 과거원문의 동일성, 실행 성공, 실제 사용자 클릭·채택은 이 입력으로 확인할 수 없다.

공식 Python 문서의 현재 발행 title은 3.11.18이며 Data model footer는 2026-10-26 갱신을 표시한다. 이를 2022년 초기3.11.0 본문으로 소급하면 안 된다. Pandas2.0.3 원문과 현재 Altair/Bokeh 홈페이지는 다른 시점의 자료이며, 일반 이름층 근거와 특정판 상호호환 보증을 구분해야 한다.

최소 후속 확인은 다음 세 가지다. 첫째, 바이트 정규화 진단을 별도 파일에 보존하고 원격 SHA 기준 검산을 사용한다. 둘째, V3 규칙 이탈과 P24 결측을 결과/수용 기록에 반영한다. 원규칙 V3 재관측은 새 진단 버전으로만 가능하다. 셋째, C4의 봉인 A1/A2 및 metadata 역할 위치를 그대로 두고 실제 도착 범위의 입증 가능성만 검증한다. 이 감사가 원자료를 고치거나 양성 분모를 완화하는 근거가 되어서는 안 된다.
