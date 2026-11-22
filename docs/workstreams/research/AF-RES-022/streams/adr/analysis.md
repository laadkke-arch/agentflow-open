# F1 · 공개 저장소 결정 기록 8건 분석

## 이 묶음의 결과와 실제 분모

A01–A08은 Backstage 4건과 Kibana 4건이다. **엄격한 직접 미인지→발견 인과→실행은 0/8**, 알려진 해법의 제약을 재평가한 좁은 연결사슬은 **A01의 1/8**이다. 늦은 외부 발견·재평가 사건을 확인하지 못한 행은 A02·A03·A05·A06·A08의 **5/8**이다. 이 플래그는 처음 생애 인지일을 모른다는 뜻과 다르다. 대안을 이미 명시한 문서가 있어도 늦은 발견 사건은 미확인일 수 있다. A06은 최종 AAD 조건을 만족하는 기능이 최초 제안 뒤 제공된 별도 표시다.

최소 문헌 수에는 23개만 산입했다: 최초 결정 원문 8, 별도 후속 9, 공식 당시 판 6. sources.json의 나머지는 같은 문서 개정·동일 PR 코드·버전 부속 파일·접근 실패를 남긴 보조 원장이다. 원문 수와 사건 수는 다르다. A02와 A03은 다른 선택이지만 PR1385 하나가 함께 구현했으므로 후속 원문과 변경량을 두 번 세지 않았다. 공급자 node-crypto PR3의 작성자도 소비자 RFC 작성자 njd5475이므로 독립 관점으로 오인하지 않는다.

| 사례 | 원 선택·제안 | 당시 가능한 대안·조건 | 관측한 인지 | 확인한 후속 선택 | 가장 큰 빈칸 |
| --- | --- | --- | --- | --- | --- |
| A01 | catalog descriptor 형식; 2020-05-17 공개 PR | Kubernetes1.18.0 annotation은 string | 이미 아는 타입 제약 재평가; 댓글 생성~갱신 05-18~19 | 자체 catalog 유지, string 제약 부분 채택; PR918 코드 | 실제 피한 오류·노동량 |
| A02 | default 대신 named export; 2020-05-19 | React16.6 lazy는 default를 읽어 예외/adapter 필요 | 외부 글·lazy의 단순 언급; 첫 발견 미확인 | core export 전환; PR1385 | 읽기·마이그레이션의 실제 시간 |
| A03 | 공개 API의 index 경계; 2020-05-27 | 기존 깊은 재수출도 실제 코드에 존재 | 외부 인지 사건 미확인 | root→components→말단 경계; PR1385 | 원칙의 첫 소개·전체 시행 비용 |
| A04 | Component 먼저, API/Resource 후속; 2020-05-29 | KCC1.10.0 Spanner CRD | KCC 재평가 답글; 05-29~06-01 구간 | 먼저 Component라는 계획 유지; Resource 후속은 문서만 | KCC 실제 수집·운영 채택 |
| A05 | setup/start 분리; 2019-03-05 | 기존 start/stop와 개별 서비스 해법 | 내부 loader 이해 교정, singleton 거절; 외부 발견 미확인 | PR33455→35269 실제 단계 분리 | 전체 migration 인시·원 필요 시점 |
| A06 | encrypted attributes; 2019-03-22 | crypto primitive 재사용; 최종 AAD는 04-12 추가 | 내부 API 재평가와 같은 작성자의 기능 추가 | node-crypto1.0.0 + 자체 wrapper, PR34526 | 초기 AAD 요구 합의일·정확한 npm 배포일 |
| A07 | framework-agnostic mount API; 2019-05-10 | 이미 의존한 React Router4.3.1 | 전체 Router 노출을 05-28 개정판에서 검토·거절 | 외부 API는 독립 유지, 내부 Router는 재사용; PR41007 | 운영 전환·bundle 비용 |
| A08 | handler/context 공통 규약; 2019-05-11 | 기존 패턴·TS1.8 module augmentation | 원리가 이미 쓰였다는 진술, 내부 의존 제한 재평가 | 미병합40554→수정41251의 실제 ContextContainer | 반대자가 지적한 복잡성의 운영 결과 |

결과는 읽은 시행 시점의 판단이다. 그 뒤 모든 코드가 영구적으로 유지되었다거나 모든 사용자에게 배포되었다고 말하지 않는다. A04는 계획 유지 진술과 실제 KCC 실행을 혼동하지 않기 위해 outcome을 change_unconfirmed로 남겼다. 문서 PR 병합과 코드 병합은 별도 열이다. 모든 최초 공개 구현의 전 역사는 입증하지 못했으므로 first_public_implementation.date는 미확인으로 두고 earliest_observed_date만 보조 필드에 남겼다.

## Q1 · 결과와 독립적인 원장과 연속 표집

동결 commit은 00c2a14633e7503880f4aceb7c4909845298b3d7이다. [Backstage 목록](https://github.com/backstage/backstage/blob/ffe93e7aa7ebcc429ed98bfd02810314a6f27c73/docs/architecture-decisions/index.md)과 [Kibana 역사 RFC 목록](https://github.com/elastic/kibana/blob/dd31e406be605f8db329a9d3bf36164c1425a43c/legacy_rfcs/README.md)은 2024년 말 마지막 commit에 고정했다(ADR-I01/I02). 현재 Kibana ADR 경로는 workflows_management/dev_docs/adr이며 2024년 뒤 기록이어서 역사 표본에 섞지 않았다(ADR-I03).

원장 37개 제목·경로·생성 시각을 보존했다. 프로젝트당 4건에 도달할 때까지 적격 본문 심사는 9건이며 ADR001의 관리 절차 1건을 제외하고 8건을 선택했다. 남은 28건은 상한 이후 보류이며 부적격 탈락이 아니다. sampling.csv의 included는 true/false/deferred로 이를 나눈다. 원문 접근 불가로 제외한 선택 사례는 0이다. 잘못된 최초 파일 경로·옛 repo redirect·없는 version tag 요청은 재시도와 복구 경로를 별도로 기록했다.

ADR003·004를 포함한 이유는 이름이나 문체 자체가 아니라 module interop와 공개 API 경계에 영향을 주기 때문이다. 이 넓은 기준은 외부 해법 발견 기회가 작은 선택도 분모에 남긴다. 더 직접적인 외부 라이브러리 사례가 있는 후순위 MSW ADR로 바꾸지 않았다. 이로 인한 양성 비율의 희석 가능성은 한계다.

Kibana는 RFC 번호 대신 PR 생성 시각을 사용한다. mount 제안은 2019-05-10, handler 제안은 05-11로 최종 번호 0004가 0003보다 앞선다. 최초 mount 파일 자체도 0003이었으므로 최종 번호로 최초 commit을 열면404가 발생한다(ADR-X01). 이러한 날짜/번호 대리 오류를 실제로 찾아 고쳤다. 다만 보존된 문서는 병합 생존 편향이 있으며 이 8건을 조직 전체 결정 발생률의 분모로 쓸 수 없다.

## Q2 · 최초 필요, 공개 초안, 결정, 시행을 나누면 무엇이 달라지는가

A01은 [issue767](https://github.com/backstage/backstage/issues/767)의 공개 요구(05-08), 최초 ADR commit(05-17), 형식 교정 리뷰(05-18~19), 문서 병합(05-19), 파서 병합(05-20)을 분리한다(ADR-N01/D01/T01/R01/F01). 초안의 임의 JSON annotation과 병합판의 string 제한은 직접 비교했다. PR 생성일을 발견일로 쓰지 않았다.

A05는 최초 [init 초안](https://github.com/elastic/kibana/blob/57917dc50fd935b9511a4932f4540d61d86b70f6/rfcs/text/0001_lifecycle_init.md)과 병합된 setup 문서를 비교했다. 03-12 RFC 수용과 03-21 기존 start→setup 전환, 04-23 별도 client start 도입은 세 사건이다(ADR-D05/R05/F04/F05). 단순 이름 바꾸기만으로 선택 전체를 설명할 수 없고, 첫 rename 코드만으로 전체 기능 완성도 주장할 수 없다.

A07에서는 [05-28 commit](https://github.com/elastic/kibana/commit/0af7534a54fda41593ebc2e0521778c0a8bec0db)이 HandlerContext 변경과 전체 React Router 공개 API 거절 문구를 추가했다. 최초 05-10 초안의 대안은 mountModule과 별도 start 등록이었다. 최종 대안을 최초 질문에 소급하지 않는다(ADR-D07/R07/T07).

댓글의 생성과 갱신 시각이 다른 경우가 있다. API의 updated_at은 본문 편집인지 라인 메타데이터 갱신인지 분리하지 못한다. A01·A04 등의 인지 발언은 created→updated 범위로 저장했다. 고정 commit의 before/after가 결과 변화를 보강하지만 댓글 본문의 최초 상태를 임의 복구하지 않았다. 사적으로 처음 고민한 날·첫 기억은 이 공개 자료에서 모두 미확인이다. 필요한 최소 추가 자료는 그 당시 원 설계 노트 또는 편집 전 메시지다.

Backstage 4개 ADR은 병합 당시 상태 표가 Open이었다. 현재 보존판에서는 상태 표 자체가 없어졌다. accepted 표시나 문서 보존만으로 실행을 코딩하지 않은 실제 이유다(ADR-R01~R04, L01~L04).

## Q3 · 존재, 필요한 기능, 팀에서 사용 가능함은 같은 날짜가 아니다

A01은 [Kubernetes1.18.0 ObjectMeta](https://github.com/kubernetes/kubernetes/blob/v1.18.0/staging/src/k8s.io/apimachinery/pkg/apis/meta/v1/types.go#L233-L238)의 string→string 타입과 03-25 공식 배포를 확인했다. 이 조건은 05월 선택 전에 이미 가능했다. A02도 [React16.6 발표](https://legacy.reactjs.org/blog/2018/10/23/react-v-16-6.html)의 제공 시점과 같은 태그의 lazy resolver에서 default를 읽는 코드를 확인했다. 뒤늦게 나온 기능 때문에 예외가 생긴 것이 아니다(ADR-V01/V02/AUX04).

A04의 [KCC1.10.0 SpannerInstance CRD](https://github.com/GoogleCloudPlatform/k8s-config-connector/blob/a33e0d429b0a6beab41ce926b64f196bba78cbf3/crds/spanner_v1beta1_spannerinstance.yaml)는 리뷰보다 이틀 빠르다. 필수 config·displayName, 관측 상태, 라이선스 고지는 실제 파일에 있다. 그러나 팀의 GCP 권한, 모든 cloud를 아우르는 식별자, catalog 통합은 그 파일이 대신해 주지 않는다(ADR-V03).

반대편 A06은 [node-crypto PR3](https://github.com/elastic/node-crypto/pull/3) 전후를 비교했다. 최종 설계가 쓰는 AAD 인수는 최초 RFC 뒤에 추가됐다. 공급자 코드 병합은 04-12, 소비자 [PR34526](https://github.com/elastic/kibana/pull/34526)의 yarn.lock은 05-03 병합 시 1.0.0 tarball을 고정한다. 이는 현재 라이브러리를 과거에 그대로 추천하면 틀리는 조건이다. 다만 최초 초안에는 AAD 자체가 명시되지 않아 요구가 나중에 정교해졌다는 경쟁 설명도 남는다. 공급자와 소비자 작성자가 같은 사람인 만큼 독립된 외부 발견 이야기로 쓰지 않는다(ADR-V04/F06).

A07의 현재 검색에서 5.0 release도 나오지만 당시 Kibana manifest는 ^4.3.1이다. [4.3.1 release](https://github.com/remix-run/react-router/releases/tag/v4.3.1)와 그 BrowserRouter 코드를 먼저 읽고, 5.0의 호환성 제한은 대조로만 남겼다. 팀의 실제 판을 최신 검색 결과로 대체하지 않았다(ADR-V05/V10). A08의 TypeScript module augmentation은 1.8부터 가능했고 기존 코드에서도 쓰였다는 리뷰가 있어 새 기능 발견으로 해석할 수 없다(ADR-V06/T08).

## Q4 · 소개자, 제안자, 결정자의 인지는 다르게 관측된다

A01의 Rugvip은 Kubernetes 호환성 문제를 설명하고 kubectl 오류를 제시한 동료다. freben은 이미 Kubernetes를 인용한 제안자이며 처음에는 반박했다가 수정 완료로 답했다. 직접 관측은 특정 타입 제약의 재평가이지 Kubernetes의 존재에 대한 미인지가 아니다([리뷰 오류 제시](https://github.com/backstage/backstage/pull/894#discussion_r426644661), [작성자 답](https://github.com/backstage/backstage/pull/894#discussion_r427279096); ADR-T01).

A04에서도 KCC가 원 문서에 이미 등장한다. 따라서 동료가 상세 스키마를 제안한 것을 외부 대안을 처음 소개받은 사건으로 세지 않았다. [freben의 답글](https://github.com/backstage/backstage/pull/1072#discussion_r432819958)은 제안이 생각을 촉발했다는 재평가를 직접 보여준다. 다만 원본 상태는 KCC에서 가져오고 catalog에는 보조 참조만 두자는 생각이 실제 구현됐는지는 다른 문제다(ADR-T04).

A08은 처음부터 패턴이 이미 여러 곳에 쓰인다고 작성한다. 이후 handler라는 공통 규약을 명명한 것은 원리의 최초 발견이 아니다. 반대 리뷰어는 추가 복잡성이 필요 없을 수 있다고 주장했다. 최종 문서가 병합되었다고 이 반대 진술을 삭제하지 않았다(ADR-D08/T08).

A01·A04는 known_reassessment, A07은 결정 전 known_rejected를 확인했다. 나머지5개는 늦은 외부 발견 사건을 특정하지 못했다. 내부 API 재평가·단순 인용은 원장에 별도 남겼다. B 목적표집을 이 8건에 보태어 비율을 계산하지 않는다.

## Q5 · 실제 변경과 유지, 부분 채택을 어느 층에서 판정하는가

A01의 최종 [KubernetesValidatorFunctions](https://github.com/backstage/backstage/blob/26ba7c972cf1f662da45fbd3a71cc76b2e060395/plugins/catalog-backend/src/validation/KubernetesValidatorFunctions.ts#L79-L81)는 annotation 값을 문자열로 검사한다. 자체 catalog를 버린 것이 아니라 한 제약을 받아들였다(ADR-F01/C01). A02·A03의 [PR1385 diff](https://github.com/backstage/backstage/pull/1385/files)는 component 본체를 보존하면서 export 정책과 경로를 바꾼다. 같은 실행을 두 독립 성공으로 세지 않는다.

A07은 가장 유용한 분류 반례다. 문서에서는 전체 React Router API를 플러그인에 노출하는 대안을 거절하지만 [PR41007](https://github.com/elastic/kibana/pull/41007)의 내부 app_router.tsx는 React Router를 쓴다. 공개 API의 독립성과 내부 부품 재사용은 동시에 성립한다. 자체 구현 유지/외부 채택의 단일 이진값은 선택의 층을 잃는다. 작은 앱 요청 수, 제3자 bundling, legacy 이전 조건이 당사자가 밝힌 이유이며 인지 부재보다 더 잘 맞는 설명이다(ADR-T07/F07/V05).

A04는 [PR3957](https://github.com/backstage/backstage/pull/3957)이 스스로 문서 전용이라고 범위를 한정한다. 계획의 유지 답글은 있지만 KCC 실행으로 바꾸지 않았다. A08의 [PR40554](https://github.com/elastic/kibana/pull/40554)는 미병합이고 [PR41251](https://github.com/elastic/kibana/pull/41251)이 수정 구현이다. 미병합 초안을 운영 후 철회로 세지도 않았다.

이 계열에서 읽은 후속까지의 outcome은 replaced3, partial_adoption4, change_unconfirmed1이다. trial_reverted0·retained0은 그 방식의 사건이 일반적으로 없다는 뜻이 아니다. 보존된 문서 원장이라는 선택 범위와 후속 검색의 날짜 한계를 같이 읽어야 한다. 각 query·결과 제목·실제로 연 후속이 search-log.json에 있다.

## Q6 · 비용의 관측과 조기 링크의 인과효과를 분리한다

costs.csv에는 문서 PR 생성→병합의 달력 경과8행과 조기 링크의 회피 인시 미확인8행을 남겼다. 기간은 0.004618~38.983275일이지만 작업 시간이나 팀 생산성으로 해석할 수 없다. 가장 짧은 A02도 후속 구현은 한 달 뒤 PR1385에서 관측된다. 검토 기간이 짧다는 사실이 구현이 쉬웠다는 증거가 아니다.

직접 보고된 실제 인시는0/8이고 실제 피한 인시도0/8이다. A06 작성자가 말한 1만 항목당2–3ms·10만 항목당20–30ms는 wrapper 반복 처리의 추가 지연 추정이다([해당 댓글](https://github.com/elastic/kibana/pull/33740#discussion_r269105705)). 측정 노동시간이나 암호화 전체 benchmark로 바꾸지 않았다. A08의 재구현을 줄일 것이라는 주장도 장래 기대다.

폐기·재사용을 함께 보아야 한다. A01은 catalog와 parser를 유지하면서 annotation 타입만 바꾼다. A02·A03은 component 본체를 보존하고 export를 옮긴다. A06은 crypto primitive를 재사용하지만 AAD·saved object wrapper·권한 처리는 새로 통합한다. A07은 Router를 내부에 쓰면서 공개 mount 규약은 자체 설계한다. 삭제 줄 수를 버린 인시로 세지 않았고 각 PR을 합산하지도 않았다. 각 행의 minimum_next_record는 당시 작업 로그와 실제 포기·재사용 범위를 같은 단위로 잇는 최소 추가 입력이다.

## Q7 · 이름, 같은 분야 구현, 실제 관계 전이는 다른 판정이다

A01은 객체 envelope의 apiVersion/kind/metadata 관계와 annotation string 타입이라는 두 대응이 원 Kubernetes와 실제 Backstage parser/validator에 있다(ADR-D01/V01/AUX01/C01). 관계가 코드로 옮겨갔다는 증거는 있지만 software infrastructure에서 catalog로의 같은 넓은 분야·다른 생태계 재사용이다. 이를 특허·공학 관찰 연구 같은 독립 타 분야 증거로 재산입하지 않는다.

A02 문서는 과거 CommonJS 단일 export와 UNIX 원칙의 유사성을 명명한다. 그 비유를 원리에 의해 2020년 새 선택이 뒤집혔다는 인과 증거로 승격하지 않는다. A08은 handler 패턴이 기존에 쓰였음을 직접 밝히며 후에 공통 인터페이스를 만들었다. 두 사례는 이름이 붙었다는 사실과 새로운 구조가 전이됐다는 사실을 분리하게 한다. 다른 분야 사례와 분모는 이 F1 묶음이 담당하지 않으며 전체 보고서의 별도 원장을 필요로 한다.

## Q8 · 어떤 시점의 어떤 링크가 유용했는가

| 비교 | 당시 제공할 수 있던 링크·부분 | 필수 조건과 도입 비용 | 판정 |
| --- | --- | --- | --- |
| A01 vs A04 | A01: 2020-05-17 이전 Kubernetes1.18.0 ObjectMeta.Annotations 타입; A04: 05-27 KCC1.10 Spanner CRD | A01은 기존 도구 호환과 단순 타입 검증; A04는 팀 권한·식별·다중 provider catalog 연결이 추가로 필요 | A01은 실제 교정·코드 연결이 있으나 더 일찍 주었을 때의 절감량은 미확인. A04는 해당 링크가 있어도 Component 우선 계획 유지 근거가 있음 |
| A06 vs A07 | A06: 최초 03-22 시점에 최종 AAD 구현은 아직 없음; 04-12 이후 공급자 commit. A07: 기존 React Router4.3.1 release/API | A06은 필요한 기능·요구가 같이 진화하고 wrapper 통합은 남음. A07은 API 결합·bundle 비용 조건 | 먼저 알면 완성품을 즉시 쓸 수 있었다는 주장을 둘 다 지지하지 않음. A07은 이미 알고도 공개 API를 제한하고 내부 재사용 |
| A02 vs A08 | A02: React16.6 lazy resolver의 default 요구; A08: TS1.8 module augmentation 제한 | 이미 가능한 기능을 정확히 표현하는 규칙·adapter 및 의존 경계 구현 필요 | 존재 알림보다 조건·호환성의 정확한 연결이 유용할 가능성. 직접적인 조기 링크 인과효과는 미확인 |

이8건만의 엄격 양성 관측 하한은0/8이다. 늦은 인지 사건 미확인5개를 모두 음성/모두 양성이라고 놓는 기계적인 범위는0~5/8이지만, 최종 AAD 기능이 초기에는 없던 A06까지 조기 완성 해법 추천 가능성에 넣으면 과대평가다. 그 조건을 제외한 단순 논리 상한은0~4/8이다. 이는 **불확실성 설명용 산술**이며 실제 발생률·신뢰구간·제품 절감 효과가 아니다. 알려진 대안 거절과 내부 선택 위주 표집도 따로 표시해야 한다. 전체 A24에서 계산할 때는 root 원장의 정의를 일관되게 적용해야 한다.

## 이 묶음의 자체 확인과 남은 조사

- A01–A08 각각 최초 고정 원문, 개정판, 리뷰 주체, 후속 실행 또는 실행 미확인 이유가 있다. duplicate_017=false이며 다른 표본에 복제하지 않았다.
- 채택을 강제하지 않았다. A04의 KCC 시행, A02·A03·A05·A06·A08의 외부 첫 인지는 미확인으로 남겼다.
- A01의 제약 교정을 해법 존재 미인지로, A06의 후발 기능을 초기 제공 가능으로, A07의 공개 API 거절을 내부 라이브러리 전면 거절로 승격하지 않았다.
- 같은 문서의 최초·병합·2024 보존판과 같은 PR의 파일은 최소 원문에 중복 산입하지 않았다. 공급자와 소비자의 계보도 명시했다.
- 댓글 생성일과 내용 최초 시점은 구분했다. PR 날짜를 발견일로 쓴 행은0이다. 코드가 있다는 사실과 프로덕션 rollout 날짜 역시 구분했다.
- 실제 코드의 빌드·성능 benchmark는 이 조사에서 실행하지 않았다. 실행 근거는 공개 PR의 merge와 고정 diff/코드 직접 확인이다. 사용자 환경의 실행 성공이나 장애 감소로 말하지 않는다.
- 다음 첫 조사: A04에서 Config Connector를 실제 읽는 catalog processor와 당시 설계 연결을 찾고, A06의 AAD 조건 합의 시점·npm1.0.0 공개 메타데이터를 확보한다. 나머지 인지 미확인에는 당시 작성자 노트 또는 첫 소개 메시지 한 가지가 가장 직접적인 입력이다.

| 중요한 약점 | 해당 근거 | 이 약점이 바꿀 판단 | 다음 최소 확인 |
| --- | --- | --- | --- |
| 보존된 ADR/RFC와 넓은 내부 선택 기준 | ADR-I01/I02; sampling.csv | 외부 발견률의 해석 가능한 모집단과 희석 정도 | 미병합·삭제 기록까지 포함하는 별도 동일기간 원장 대조; 기존 A를 사후 교체하지 않음 |
| 인지 발언·실행·실제 비용을 완전히 잇지 못함 | ADR-T01/T04/F03; costs.csv | 조기 링크의 직접 절감액과 자체 유지의 인과 | 동시대 작업 로그·첫 소개 메시지·KCC processor의 실제 PR |
| 기능 제공·요구 상세화·같은 작성자 계보가 겹침 | ADR-D06/V04/F06 | 후발 제공을 외부 발견 지연으로 오인할 위험 | AAD 요구를 고정한 최초 revision과 npm1.0.0 publish 시각 |

