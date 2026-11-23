## 5. 판별할 수 있는 것과 판별할 수 없는 것

**이 제한된 공개 자료 묶음에서는 인접 링크의 문서 근거 이득이 읽기 단위에 따라 달랐다.** 같은 후보 목록에서 F는 P1 한 건만 B 단독 완결이고 S는 그런 건이 없다. F의 A 단독 완결은 0건이다. 이것은 이 모집·순위·구간 규칙에서 관측한 근거 가용성의 차이이며, 인접 정책의 일반 우월성이나 동등성의 추정이 아니다. 전체 원 사용자 실행 성공은 주 지표가 아니다.

비교 가능한 F 7쌍에서 A는 4/7, B는 5/7의 문서 완결이다. 경계 5쌍은 A2/5·B3/5, 대조 2쌍은 양쪽2/2이다. S의 비교 가능한 7쌍은 양쪽0/7이다. P3의 두 비교는 인접 연구판을 고정하지 못했으므로 제외했다. 8개 배정 쌍 또는 16개 배정 자리를 분모로 제시할 때에도 그 공석을 패배로 처리하지 않는다. F의 승패가 갈린 쌍은 1개이고 B가 1/1이다. S의 승패가 갈린 쌍은 0개여서 그 안에서의 승률은 **산출 불가**다. 독립 사용자 집단의 효과 크기나 유의확률은 산출하지 않았다. [주 판정](judgments.jsonl), [16쌍](pairs.csv), [자동 집계](evidence/derived/metrics.json).

파일에서 발췌로 바꾸면 16개 정책·질문 자리 중 9개가 완결에서 미완결로 바뀐다. 질문 수준에서는 J1·J2·J4·P1·P4의 5개 행이 바뀐다. J3·P2는 양쪽 읽기 단위에서 미완결이고 P3는 양쪽 비교불가다. 고정 후보가 같으므로 이 전환을 파일 선택 변경으로 설명할 수는 없다. 그러나 표시한 문자·절 이동·사람의 시간은 같지 않다. F에서 접근 가능한 문자 합은 6,509,235자지만 실제 표시한 것은 반복 포함 270,609자이며, S는 74,400자다. F에는 102번의 추가 절 이동이 있고 S에는 없다. 따라서 비용을 “파일 접근 네 번”으로만 나타내면 F의 추가 독해 자원을 숨기게 된다. [원 접근 로그](evidence/packet-access/), [구간 규칙](protocol.json).

### 충분한 근거를 못 찾은 경우와 패킷에 충분한 근거가 없는 경우

초기 독자와 사전 별도 근거 대조 사이 완결 변경은 **0건**이다. 이번 기록에서 “허용된 패킷에 충분한 근거가 있었는데 초기 독자가 완결로 판단하지 못했다”고 확인된 자리는 0개다. 이는 그런 실패가 없다는 보편적 증명이 아니다. F에서 미완결인 J3는 C1 추가 연산은 지지하지만 필수 Bash 경계가 부분이고, P2는 원 import와 같은 결과를 잇는 근거를 찾지 못했다. S에서는 J2의 null/배열 순회, J4 B의 입력 구조, P4의 필터 단계 같은 일부 단서가 있어도 전체 필수 조건을 모두 지지하지 못했다. 관측된 불충분과 기술적 불가능성을 구분한다. [초기 32판정](evidence/initial-judgments.jsonl), [사전 변경 원장](evidence/audit/pre-outcome-changes.jsonl), [사후 별도 의미 검토](evidence/resume2/semantic-review.md).

F 완결 9자리에서 문서의 깊은 절을 직접 인용할 수 있었던 것이 S에서 차단되는 사례가 핵심이다. 예를 들어 P1 B는 knitr `plot.R`의 문자13900–18600에 있는 함수 경계를 이용한다. P4는 Pandoc 매뉴얼의 문자188840–192200에 있는 YAML 절을 이용한다. 최초 어휘 일치 주변의 한 구간은 이 절들을 제공하지 않는다. “S에서 못 찾음”은 그 파일 전체에 근거가 없다는 뜻이 아니다. 첫 일치가 도입부·라이선스·다른 용례일 수 있는 현재 추출 규칙의 성질까지 포함한 결과다. [knitr 고정 구현](https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/R/plot.R), [Pandoc 고정 매뉴얼](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt).

### 가장 불리한 해석으로 다시 읽기

P1의 주 해석은 공개 전부터 전역 설정 또는 한 번 등록한 helper를 허용했다. 그러나 제안된 helper를 정의하기만 하면 기존 `knitr::include_graphics(...)`가 자동으로 바뀌는 것은 아니다. 기존 호출을 helper 이름으로 바꾸어야 한다. 내장 옵션만 허용하거나 기존 호출을 전혀 바꾸지 않는 해석에서는 F B 단독 이득이 사라진다. P1을 최초 Pandoc 연관성이 없는 모집 사례로 제외해도 남은 6개 비교 가능 F쌍의 B 단독 이득은 0이다. 이 두 민감도는 유일한 양성 결과가 얼마나 좁은 조건에 매여 있는지 보여 준다. [사전 P1 해석](protocol.json), [원 최초 질문](https://stackoverflow.com/revisions/32603E8D-E453-4BCB-895B-83AFBE3FB468/view-source), [별도 의미 검토](evidence/resume2/semantic-review.json).

J2의 F 완결도 원문이 명시한 `.Event[]`와 Data 형태에서의 조건부 변환 근거이다. 실제 전체 로그의 envelope와 EventData 없는 사건까지 무조건 처리했다는 주장이 아니다. 사후 자기답에는 UserData만 있는 사건과 원 설명의 수정이 나타난다. 이를 새 필수 조건으로 넣으면 두 F 자리를 미완결로 읽는 엄격 민감도가 필요하다. J1에서 최종 JOIN 복구, P4에서 최종 PDF 전체 실행까지 요구하는 경우도 사전 등록한 좁은 진단/파싱 기준과 구분했다. 표4의 민감도는 각각 따로 적용했으며 합산하지 않는다. [J2 최초 자기답](https://stackoverflow.com/revisions/CE0C3B2C-23EA-43DE-8F89-4B01A7CC654A/view-source), [수정 자기답](https://stackoverflow.com/revisions/5931D56D-480F-4826-9124-71C9BDE946CB/view-source).

## 6. 밀려난 절, 신규 제약, 공개 후속의 귀속

경계 요청 6건의 교체는 A3·4 두 파일과 B3·4 두 자리, 총24자리로 보존했다. J2의 B는 jq `from_entries` 원 시험을 밀어내지만 남은 매뉴얼이 같은 연산을 설명한다. J3는 jq argv 소비 구현을 잃고 Terminal 설정 schema를 얻어도 Bash 문제를 해결하지 못한다. J4의 AWS 예제는 입력 구조를 확인하지만 원 질문에 없던 Iops를 채우지 못한다. P1에서만 knitr 함수 입력 연결을 얻어 주 완결이 달라진다. P2의 CeTZ 소스는 WASM 자원 요구를 드러내지만 Pandoc resolver 성공을 제공하지 않는다. [24자리 밀림 원장](displacement.csv), [원 절 대조](evidence/resume2/source-audit.md).

승패는 같으나 **필수 실패 조건이 제거됐다**고 확정할 자연 요청은 찾지 못했다. 추가 구조 정보·시험·제약을 얻은 경우는 있으나 제거된 실패로 세지 않았다. 반대로 “외부 의존을 알기 위해 언제나 인접 도구 링크가 필요하다”는 주장은 Pandoc 매뉴얼의 LaTeX 엔진 요구, FAQ의 글꼴/엔진 제약, Lua filter 문서의 외부 interpreter/library 설명과 맞지 않는다. 같은 주 파일 안에서도 필요한 외부 의존이 설명될 수 있다. [Pandoc PDF 설명](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt#L110-L134), [Lua filter 도입부](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/lua-filters.md#L1-L44).

재개 흐름의 공개 후속은 봉인②를 원격에서 관측한 **2026-11-23T20:29:13Z 이후**에만 열었고, 그 흐름의 첫 API 요청은20:32:07Z이다. 원래 흐름은20:22:57Z의원격봉인후20:25:18Z에첫후속을열었다. 두흐름의시작시각을합치지않는다. 20개 API 응답의 실패는 0이며 8질문·5답·29revision·30일 내 댓글18개를 확인했다. 현 채택은 J2·J4·P4 3건이다. **같은 판·완전한 원 입력·필수 출력을 모두 연결한 실행 확인은 0/8**이다. 질문자 자기보고가 없다는 뜻은 아니며, 그 자기보고의 범위가 다르다는 뜻이다. [봉인 원격 관측](evidence/resume2/concurrency.json), [후속 CSV](outcomes.csv), [최초·수정·현재 연결](evidence/resume2/outcomes/evidence-details.json), [후속 검증](evidence/resume2/outcomes/validation.json).

- J1은 오류가 사라졌지만 원 JOIN을 하지 못했다는 질문자 보고다. 정상 종료를 목표 충족으로 바꾸지 않았다.
- J2는 최초 자기답의 원인 설명이 바뀌었고, 채택답은 yq 중심의 다른 경로와 한 Event 예제를 제시했다. 사전의 sed 선택이나 원 조건을 결과에 맞춰 교체하지 않았다.
- J3는 파일명 인수를 쓰는 대안의 성공 보고다. 원 JSON 내용 변수를 전달하는 방식과 .new의 실제 내용을 검증한 것은 아니다.
- J4와 P4는 채택 및 답변자 제안과 주 해석이 맞지만 질문자 실행로그가 없다.

원래흐름의추가행동집계는5답/4질문,질문자30일내댓글·자기답5/8,질문자본문수정3/8,합집합7/8이다. J4/P4의수정은답보다먼저이므로7/8을답채택뒤실행으로읽지않는다. 두흐름의60entity대조에서귀속차이는없었으며이집계는 [통합귀속감사](evidence/audit/concurrent-outcome-review.md)에남겼다.
- P1은 helper가 이미 쓰이던 방법이라는 질문자 보고다. 새 제안으로 인한 채택이나 개선 효과로 귀속하지 않았다.
- P2는 후속이 없으므로 계속 미확인이다. P3는 작동 Dockerfile 자기보고가 있으나 파일·digest·PDF가 없으므로 연구판 공석과 원 입력 결손을 해소하지 못한다.

원래 흐름의 사후 감사가 채택 시점을 미확인이라고 기록한 것은 당시 수집 범위의 한계다. 이번 재개는 공식 question timeline의 accepted_answer 항목(SO-API-0007·0011·0019)에서 J2·J4·P4의 30일 내 시각을 추가로 확인했다. 이벤트의 user는 답 작성자 메타데이터이며 실행한 사람의 증명이 아니다. 두 흐름을 새 답이나 새 성공으로 중복 세지 않는다.

이 문단의 각 귀속은 [후속 상세 보고서](evidence/resume2/outcomes/report.md)의 해당 질문 URL, 최초 답 revision, 수정 revision, 댓글 ID와 연결된다. 답변자·질문자·다른 참여자의 역할을 구분했으며, 공개 프로필로 유지관리자 여부를 추측하지 않았다. 어떤 참여자에게도 연락하지 않았다.

<!-- PERSPECTIVES -->

## 8. 다른 분야의 반례와 적용 한계

**GDAL/PROJ:** 새 명명 사례는 warp의 수직 보정이다. 고정 GDAL3.10.0 주 문서는 자동 수직 변환의 단일 밴드 조건과 `-novshift`를 직접 설명한다. 대응 상류 fixture는 100인 한 픽셀과 상수20 GTX 그리드에서 기대120을 검사한다. 선택적 결손 그리드 시험은 100을 유지한다. PROJ9.5.1 문서는 자원 탐색 순서와 `@` 선택적 결손의 의미를 더 구체적으로 설명한다. 따라서 주 설명만으로 충분한 조건과 실제 자원을 확보해야 완성되는 조건을 나눌 수 있다. [GDAL 주 문서](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/doc/source/programs/gdalwarp.rst#L624-L652), [새 상류 fixture](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/utilities/test_gdalwarp_lib.py#L1865-L1935), [PROJ 자원 탐색](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/docs/source/resource_files.rst#L19-L82), [선택적 그리드](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/docs/source/operations/transformations/vgridshift.rst#L23-L45).

기존 환경의 GDAL3.10.3/PROJ9.6.0으로 수행한 별도 보조 실험은 한 밴드100→120, 두 밴드100유지, novshift100유지, 선택적 결손100유지, 필수 그리드 결손 예외의 5조건 모두 기대와 일치했다. 일부는 상류 fixture의 재구성이고 일부는 문서로부터 만든 연구 변형이다. 고정판 상류 테스트 실행이나 실제 geoid 정확도 검증으로 주장하지 않는다. [명령·입력·기대·실제값](evidence/resume2/crossdomain/gdal-runtime.json).

**Sphinx/Graphviz:** 새 사례는 inheritance-diagram의 클래스·캡션과 PNG/SVG fixture이다. 주 문서는 어떤 클래스를 지정하고 캡션을 넣는지 설명한다. native Graphviz 실행 파일과 출력 renderer 지원은 별도 확인이 필요하다. 상류 시험의 `if_graphviz_found`는 명령을 시작할 수 있는지 확인하지만 `check=False`라서 gate 통과만으로 정상 종료나 SVG 지원을 보증하지 않는다. 로컬 Graphviz2.42.4의 작은 DOT→SVG probe는 성공했으나 Sphinx/docutils/pytest 환경이 없어 Sphinx 상류 테스트는 실행하지 않았다. [상속도 문서](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/doc/usage/extensions/inheritance.rst#L11-L42), [새 PNG/SVG 시험](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/test_extensions/test_ext_inheritance_diagram.py#L156-L262), [실행 기록](evidence/resume2/crossdomain/graphviz-runtime.json).

이 두 지명 사례는 신규 검색 적중·8요청·32자리·16쌍에 넣지 않았다. 096의 OSR OnlyBest/BETA2007 또는 일반 graphviz/text-cache 예제를 다시 사용하지 않았다. 다만 공통 gate `sphinx/testing/fixtures.py`는 096에서 이미 읽은 보조 파일이라 재사용을 명시하고 신규 최소개수·새 fixture에서 제외했다. 문서·구현·시험이 같은 저자 계보를 공유할 수 있으므로 고유 파일 수를 독립 연구 수로 바꾸지 않는다. [계보·버전·새 fixture 범위](evidence/resume2/crossdomain/report.md), [보조 파일 산입 검증](evidence/resume2/crossdomain/validation.json).

## 9. 모집·눈가림·자료 수의 자가검산

모집은 2025-07-01~12-31 UTC의 현재 jq/pandoc 태그 검색 결과를 생성시각, 숫자 ID순으로 정렬했다. 프레임은 jq24·Pandoc15 총39행이고 최초 본문을 직접 연 것은 jq7·Pandoc15 총22건이다. 각 태그의 경계3·대조1이 채워져 2026Q1 보충은 사용하지 않았다. 이전68 ID와 겹치는 선정 ID는 없고, 이미 답을 읽은 질문을 새 적중으로 넣지 않았다. 본문의 기존 참고 질문/블로그는 같은 사건 재게시 증명이 아니며 독립성 미확인으로 남겼다. jq 현재 제목24개의 최초본문 전 노출은 모집 단계의 실제 이탈로 기록했다. J4의 선두 jq 표기 변화 외 선정 제목은 같았고, 답·점수·댓글·채택은 그때 보지 않았다. P1의 현재 태그와 최초 태그 차이는 표1과 민감도에 남긴다. [프레임](frame.csv), [모집 고정 규칙](protocol.json), [범위](SCOPE.md).

4개 모델 읽기 문맥에 Latin square로 배정했고 같은 질문의 네 패킷은 다른 문맥이었다. 파일 URL은 출처 증명을 위해 보였으므로 정책을 추측할 가능성까지 제거한 눈가림이라고 주장하지 않는다. OS 차단도 아니며 모델의 훈련 기억은 관측할 수 없다. 선행 질문에서 같은 파일을 본 자리는24/32이고 같은 질문의 다른 경로를 먼저 보았다고 선언한 주 자리는0이다. 주 지표를 독립적인 사람의 발견률이 아닌 패킷 안 근거 가용성으로 한정한다. [배정](evidence/assignments/), [구조 검토](evidence/audit/independent-integrity-review.json).

초기 판정은 32자리·60조건·115인용이고, 각 인용은 허용 원 파일의 문자/바이트 경계 안이며 첫 판정 이전에 표시된 구간으로 덮인다. 재개 중 이전 세션의 봉인②가 원격에 나타난 후 중복 읽기를 즉시 중단하고 격리했다. 그 부분 판정과 접근은 주 지표·주 비용에 포함하지 않는다. 이후 의미 검토는 정책과 기존 판정을 아는 별도 모델 문맥이며 사람이 한 검토가 아니다. 그 검토의 변경 권고도0이다. [격리 기록](evidence/resume2/concurrency.json), [중복 제외 자료](evidence/resume2/duplicate-reading/), [별도 의미 검토](evidence/resume2/semantic-review.json).

{{SOURCE_ROWS}}개 통합 출처 원장 행 중 고유 최소개수 산입은46개다. 재개에서 감사한160행과 원래 흐름의143행, 통합 뒤 채택타임라인/실행계획의 비산입 보조기록을 함께 보존하며, 원래143행과 새보조기록은 추가 산입하지 않는다. 원 질문8, 주 공식16, 인접 공식10, 독립 상류시험5, 타 분야 공식5·fixture2이며 요구된 26개 및 각 하위 하한을 충족한다. 원 질문 추가 모집14행, 후속 답/댓글/API83행, 빈 시험·파생 시험·동일 fixture 보조 파일은 별도 비산입이다. 같은 원문을 A/B/F/S에서 다시 열어도 한 개다. 모든 산입 자료에는 고정 URL·UTC·지문·실제 확인 내용·한계·저작 계보가 있다. 전체 원문 재배포 대신 재열람 주소·짧은 필요한 근거·해시를 남겼다. 외부 본문 cache를 다시 내려받는 것은 독해 수에 추가되지 않는다. [sources.jsonl](sources.jsonl), [원문 표시 영수증](evidence/resume2/postseal-access.jsonl).

## 10. 재현·계약·검사 범위

저장소의 기존 시작판은 `01177554d0fbd33a914ea9c982c348d442d1358d`, 이번 재개 때 직접 읽은 통합판은 `daf01339d0a81a3a8f19fad43b497480aa62515f`이다. 배정 계획판은 `fcde6becc49120c5be91adf43fb5b4aa42e71d48`이다. 096의 연구 결과 입력은 `1d399f630930d2763459e16509c5224b0cded9a0`, 인계/운영 의존은 `fce8d0ded93fe1f13f2c4978ed273c1ceef32934`이다. 의존 원격은 같았고 연구 입력을 바꾸지 않았다. 원천 결과·중앙 dot-control은 수정하지 않았다. [작업 manifest](manifest.json), [재개 확인](evidence/resume.json).

① `e0cb8eaec3cbd9a7e5d40291a5a883f33473ec2f`에서 모집·조건·순위·읽기 예산과 패킷을 봉인했다. ② `5d81bcbeb5f1248fc1dd2ce2d825cf6467353673`에서 32사전 판정과 근거 대조를 봉인했다. `747359a546daf5300d82afa0904cbbf71e211202`은 동시 세션 결과를 보존하고 재개 중복 읽기를 격리한 커밋이다. ③ `866ee7a68eec0f5c7077fec364685d6039d5ca75`는 후속·밀림·다른 분야·별도 의미 검토를 저장했다. 이후 `82e21d89eb592769f6f44ed75c9937400a565641`에서 원래 흐름③ `b3d7af5a3a55eba78adc6c3bd31db7eaf9de49b1`도 병합한 원격을 인수했다. 원래 흐름32개와재개46개는서로다른감사계수집합이다. 고정URL+본문지문으로28개가겹치며원래쪽에만4개·재개쪽에만18개가있다. 32가46의부분집합이라는뜻도아니며두수를더하지않는다. 최종46에는사후의더오래된DockerREADME가있지만초기P3공석을채우지않는다. 두 흐름의 원32판정은 동일하다. 최종 합성기는 재개 감사 subset의46개만 산입하고 원래143개 원장 행은 비산입으로 보존한다. 자세한 조정은 `evidence/resume2/concurrency-stage4.json`에 있다. ④ 결과판의 SHA와 마지막 작업별/공통 검사, GitHub 원격 재열람 영수증은 마지막 단독 [HANDOFF.md](HANDOFF.md)에 기록한다. 검사 명령을 제시한 것만으로 실행했다고 세지 않는다.

저장소 루트에서 아래 순서로 재구성한다. `hydrate_ledgers.py`는 커밋된 gzip 원장을 정확한 hash로 복원한다. `restore_cache.py --all`은 등록한 고정 source archive와 원 최초 질문만 복원하며, 새 원문이나 현재 답으로 대체하지 않는다. 검증은 신규 질문 모집이나 독립 독자 실험의 반복이 아니다.

```bash
python -B docs/workstreams/research/AF-RES-100/hydrate_ledgers.py
python -B docs/workstreams/research/AF-RES-100/restore_cache.py --all
python -B docs/workstreams/research/AF-RES-100/packet_builder.py --verify
python -B docs/workstreams/research/AF-RES-100/assemble_preseal.py --check
python -B docs/workstreams/research/AF-RES-100/validate_ledger.py
python -B docs/workstreams/research/AF-RES-100/assemble_supplement.py --check
python -B docs/workstreams/research/AF-RES-100/recompute.py --check
python -B -m workbench.session check docs/workstreams/research/AF-RES-100/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

`recompute.py --write`는 원장과 `case-notes.json`, 이 설명 파일에서 필수3표·층별 집계·민감도·RESULT를 다시 만든다. `--check`는 파일을 쓰지 않고 바이트 동일성을 검사한다. 인용 115개의 위치·바이트 변환과 최초 판정 전 노출까지 함께 검증한다. 결과판 공통 검사가 개별 session을 찾지 못해 건너뛰는 경우 별도 `workbench.session check` 결과와 구분해 인계한다. [자가검산](SELF_CHECK.md).

자연 요청의 jq/Pandoc/R/Typst/Docker 원 실행은 수행하지 않았다. 전체 입력·사용자판이 없는 경우 연구자 예제로 채우지 않았다. P4는 렌더링하지 않았다. 읽은 jq/sed/knitr/CeTZ 상류 원 시험은 실행 결과로 표시하지 않았다. Sphinx 고정판 시험의 필요한 node·환경과 GDAL 보조 입력은 [fixtures.json](evidence/resume2/crossdomain/fixtures.json)에 있다. 재현 가능한 문서 충분성·밀림·손실과 실행 미확인을 구분한 상태로 이 작업을 완료한다.


### 통합 후 추가 반례와 재검토

원래흐름의자료에서도결론을더좁히는반례를읽었다. AWS describe-volumes Example1의KmsKeyId닫는따옴표결손은원문그대로의JSONparse에서오류였다. [입력구간·오류영수증](evidence/supplemental/aws-example-validation.json)은AWS실제API실패나J4원입력실패를뜻하지않는다. 공식예시의Iops값을질문자값으로복사하지않았다.

GDAL3.10.0 원시험135s의2247행은f접두사없이 `{empty_grid_gtx}`를전달한다. 일반예외assertion만으로생성한grid의빈값이실패원인이라고보증하지않았다. Sphinx8.1.3 원시험의class_info순회는각원소의membership을확인하므로허용목록5개/6개를실제전체출력개수로보고하지않았다. [고정원문·정확행·반례](evidence/crossdomain/report.md), [원시험명령과입력](evidence/crossdomain/unrun.md)에다음최소확인을남겼다. 재개GDAL보조runner는expectation_met를기록하므로재실행시종료값만보지말고5개기대일치값도함께읽어야한다.

통합작성자는J2/J4/P4의공식accepted_answer timeline을다시열어각2025-07-14 21:04:27UTC,2025-08-06 11:30:01UTC,2025-07-25 13:35:19UTC와답ID일치를확인했다. [재열람영수증](evidence/outcomes/acceptance-verification.json)은변동가능HTTP응답의새지문을남기며원응답바이트가같다고가정하지않는다. 채택행위자·실행판·완전입력·필수출력을추가로입증한것은아니다. [별도통합귀속검토](evidence/audit/concurrent-outcome-review.md)는두흐름의질문8·답5·댓글18·revision29인60개공유entity대조와세타임라인재열람을구분했다.

최종재현순서는 [REPRODUCE.md](REPRODUCE.md),실행하지않은jq/sed/knitr/Pandoc고정원시험의실제runner·입력·환경은 [upstream-execution-plan.md](evidence/audit/upstream-execution-plan.md)에있다. 공통검사는수정없는결과SHAcheckout을owned cache안에만들어실행하며 [run_result_checks.py](run_result_checks.py)에실제명령과기록절차가있다.

<!-- RESULT_CHECKS -->

## 가장 중요한 남은 불일치·약점

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
|---|---|---|
| 유일한 B 이득 P1은 helper 호출 변경 허용과 현재 Pandoc 태그 모집에 의존한다. 최초 본문·태그에는 Pandoc이 없고 실제 SVG/EMF·helper·PPT가 없다. | 원 helper 구현, 실제 JPEG/SVG/EMF 파일과 같은 R Markdown 호출·knitr/rmarkdown/Pandoc 판을 고정한 입력. 기존 호출 불변 조건과 helper 조건을 나누어 실행한다. | 기존 호출을 바꾸지 않고 내장 옵션만으로 같은 선택이 되거나, helper 조건에서도 원 출력이 실패하면 P1의 해석 및 유일 이득의 범위를 바꾼다. |
| F/S는 같은 네 파일 접근이지만 표시량·절 이동·시간이 다르며 24/32자리에 선행 공유파일 노출이 있다. S의 첫 일치 규칙과 사람의 독립 발견률은 분리되지 않았다. | 동일 원 질문·고정 파일에서 절 선택 방식과 표시량/시간을 별도 배정한 새 맹검 문맥. 현재 원장은 `recompute.py --check`로 먼저 보존 확인한다. | 같은 표시 예산·독립 문맥에서도 P1의 이득이나 9자리 손실이 유지/반전되는 관측이 나오면 전달 단위에 관한 해석을 좁히거나 바꾼다. |
| 같은 판·완전한 원 입력·필수 출력 실행 검증은 0/8이고 P3는 고정 연구판 공석이다. J2 사후 UserData 사건도 원 조건부 변환 밖에 있다. | P3의 취득한 스레드에 없는 작동 Dockerfile·image digest·custom template·두 filter·원 Markdown, J2의 원 Security.json/evtx와 전체 envelope. 고정 GDAL/Sphinx node는 fixtures.json 명령대로 준비한다. | 원 자료로 최신 안정 소스와 실행이 연결되면 P3 비교 가능성을 재연구한다. 같은 입력의 성공·실패가 주 조건과 어긋나면 문서 충분성과 원 실행의 관계를 수정한다. |
