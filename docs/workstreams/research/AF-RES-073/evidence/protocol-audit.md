# AF-RES-073 모집·질의 규칙 사전 검토

검토자: `/root/recruit_mep`, 같은 모델의 별도 작업 문맥. root의 전체 선행 대화를 상속했고 잠정 선정표를 읽었다. 독립 인간 판독·가림 판독이 아니다. 검색 결과나 후행 채택 자료는 읽지 않았다. 이 검토의 외부 접근은 선정된 두 최초 Git blob의 GitHub 원문 재열람 2회이며 원실험 비용·새 독립 원저작 수에 넣지 않는다.

## 읽은 범위

- `SCOPE.md`의 모집 순서·author date 정렬·JEP→SPEC 보충·9보기 비용 규칙.
- `recruitment/jep/selection.json`, `frame.csv`, `recruitment-proof.json`.
- `recruitment/spec/selection.json`.
- [JEP122 최초 Git blob](https://github.com/jupyter/enhancement-proposals/blob/2b194a3c090fd375321871c47a3de503a0758206/122-jupyter-book-incorporation/jupyter-book-incorporation.md): Guide-level explanation, Reference-level explanation, Rationale and alternatives, Unresolved questions, FAQ, Appendix.
- [SPEC9 최초 Git blob](https://github.com/scientific-python/specs/blob/846579d4b8d5ca90ba6a9792c263574c73b9f48d/spec-0009/index.md): front matter, Description, Choosing a governance model, How to pick, What to do after adoption.
- SPEC 모집의 8개 고정 커밋에 `git show -s --format=%aI%x09%cI SHA`를 직접 실행해 양 시각을 UTC 기준으로 비교했다. read-only 명령 종료0.

## 판정과 필요한 조치

| ID | 판정 | 근거·의미 | 검색 봉인 전 조치 |
| --- | --- | --- | --- |
| PA-01 | 첫 적격 거버넌스 제안을 조용히 건너뛰면 선택 편향 | 사용자 모집문에는 조직·거버넌스를 제외한다는 조건이 없다. JEP122는 실제 소프트웨어 프로젝트의 책임 이관안을, SPEC9는 프로젝트의 의사결정 절차 선택안을 기술한다. 하위 순번의 더 기술적인 제안을 선호하는 사후 제외는 금지한다. | 현 선정 유지. 결과에 기술 구현 설계와 조직 절차 설계를 구분하고, 거버넌스 2건의 검색 결과를 일반적인 소프트웨어 부품 탐색 우위로 일반화하지 않는다. |
| PA-02 | JEP122 C1이 구현 보장으로 강화될 위험 | 원문은 이관 저장소를 호환·연동 가능성과 Jupyter 전략의 정합성으로 골랐다고 설명한다. 조직 이관만으로 기술 연동이 구현된다고 말하지 않으며 Reference-level 절은 기술·표준 변경을 제안 범위에서 제외한다. | C1을 **호환성과 전략 정합성을 기준으로 이관 대상 저장소를 고르는 조건**으로 쓰고 기술 성공 보장으로 쓰지 않는다. 어느 보기에도 새 문서 엔진 설계/보장된 상호운용을 추가하지 않는다. |
| PA-03 | SPEC9의 조건은 권고를 고정한 연구 입력 | Description은 내용이 권고임을 명시한다. C1 변경 가능성, C2 공개 기록은 실제 원문에 있지만 특정 설치된 조직에서 강제되는 규칙이나 이미 확인된 성과는 아니다. | 고정 연구 C1/C2로 사용하되 출처 수준을 권고로 남긴다. 일반 구성원에게 공개가 제공된다는 사실과 의결 권한·실제 집행을 구분한다. |
| PA-04 | Git 첫 추가와 작성 최초판은 다른 증거 | JEP122 최초 Git 추가는 2024-05-22이지만 같은 blob의 Appendix는 이전 3월 초안을 명시한다. SPEC9의 본문 날짜 2024-06-04는 첫 Git 추가 2024-09-10보다 이르다. | `first_git_version_verified`, `earliest_known_draft_verified`, `founding_author_draft_verified`를 분리한다. 이 두 선정안을 창설 당시 원본이 입증된 엄격층으로 승격하지 않는다. 당시 최초 초안 부재를 현재 Git 이력의 첫 add로 메우지 않는다. |
| PA-05 | author/committer 정렬 표기는 통일 필요, 현재 SPEC 첫8 순위는 동일 | SCOPE는 author UTC를 봉인했고 SPEC selection은 main committer order라고 이름 붙였다. 8개 고정 add 커밋은 timezone 표현은 달라도 author/committer의 UTC 순간이 각각 동일해 원순번 변화는 없었다. | 통합 frame은 SCOPE의 author UTC를 canonical로 명시하고 committer는 별도 열에 보존한다. 이 검토는 SPEC 전체 가능한 경로를 재모집한 검사가 아니라 제공된 8커밋의 시각 대조다. |
| PA-06 | 살아 있는 과거 브랜치는 원순번과 내용 출처를 별도로 보완 | SPEC7의 main 최초판보다 이른 브랜치 blob이 알려져 있고 권고 동작도 달라진다. 현재 고정 모집틀은 main 도달 이력이며, 사후 발견한 브랜치로 raw rank를 조용히 대체하면 모집틀이 달라진다. | main 원순번을 그대로 남기고 `earliest_known_commit`, 시각, 원판 차이를 별도 열로 연결한다. 본문 원뜻은 더 이른 확인판을 우선한다. all-surviving-branches 정렬 민감도는 별도 분석으로 표시하고 같은 모집순위로 혼용하지 않는다. |
| PA-07 | MEP 공석 보충은 JEP 다음 순번부터 | 현재 SCOPE의 보충 순서는 JEP→SPEC이며 JEP122가 첫 적격이므로 다음 검사 대상은 JEP 원순번2의 restart clarification이다. SPEC의 더 흥미로운 기술 제안으로 즉시 이동하면 고정 보충 규칙을 어긴다. | JEP118 최초 blob에서 적격 여부를 먼저 판정한다. 탈락이면 이유를 적고 JEP 순서대로 진행한다. 최대3건·최소2프로젝트 조건은 유지한다. |
| PA-08 | Git 시각만으로 당시 공개·인지·채택을 선언할 수 없음 | author 시각은 작성 메타데이터, committer 시각은 해당 커밋 생성 메타데이터다. 둘 다 그 시각에 공개 검색으로 접근 가능했다거나 제안자가 특정 해법을 알았다는 별도 사건 증거가 아니다. | Q7에서 공개 PR/토론·출시·채택의 날짜를 별도 열로 검토한다. 검색 봉인 전 후속 결과를 열어 이 구멍을 채우지 않는다. 현재 검색 순위로 당시 검색 순위를 추정하지 않는다. |

## 엄격층과 관측층의 권고 표기

1. **Git 최초 추가층:** 고정 모집 HEAD와 파일 계보에서 최초 add/이전판 부재를 확인한 공개 저장소 판. 이 사실 자체는 재현 가능하다.
2. **더 이른 확인 초안층:** 이름 변경·이관·살아 있는 브랜치 또는 원문 자체의 언급을 통해 더 앞선 판을 확인했을 때 그 판과 차이를 보존한다. 소실·미확인인 초안은 존재 언급과 미확인을 함께 둔다.
3. **창설 당시 판 엄격층:** 저자가 시작한 때의 원문이라는 근거가 있는 경우에만 산입한다. 현재 JEP122/SPEC9에는 이 근거가 충분하지 않다. 엄격층 분모가 비면 비어 있다고 적고 0%를 계산하지 않는다.

연구를 계속하는 것은 가능하다. 다만 3개 첫 Git blob을 확보했다는 사실을 **적격 창설 최초판3건을 충족했다**고 바꾸면 안 된다. 원뜻·역할 보존과 동일 비용 비교의 관측 결과는 남기고, 초기판 조건 미달은 최종 수용 상태에서 PARTIAL 사유로 보존할 수 있다.

## 초기 결론을 뒤집는 반례

- 조직 구조 이관 검색에서 기술적으로 유용한 도구가 나오더라도 해당 도구는 JEP122의 실제 책임 분리 선택을 해결하지 않을 수 있다. 도구 이름이 같은 생태계에 속한다는 것만으로 적격으로 세지 않는다.
- SPEC9의 공개 회의록은 C2를 만족할 수 있지만 변경 절차가 없어 C1을 만족하지 못할 수 있다. 같은 문서·같은 구성에서 두 조건을 대조해야 한다.
- C가 주체·대상을 복원한 뒤 원 프로젝트의 이미 알려진 제안만 더 많이 반환할 수 있다. 새 URL 수가 늘어도 새 선택은 0일 수 있다.
- JEP/SPEC의 더 이른 저자 초안이 뒤에 확보되면 그 초안에서 조건·대안이 달라질 수 있다. 현재 관측판 실험을 소급 수정하지 말고 초기판 차이로 재분류한다.

## 재현용 시각 대조

SPEC main 최초 추가 순서와 UTC 시각은 아래와 같고, 이 8건에서는 author/committer 기준이 일치했다.

| 순번 | ID | 최초 add SHA | UTC |
| --- | --- | --- | --- |
| 1 | SPEC9 | 846579d4b8d5ca90ba6a9792c263574c73b9f48d | 2024-09-10T20:01:21Z |
| 2 | SPEC7 | 15e704894f653fc4ca65c3ce6a6cdadb05634a0e | 2024-08-29T15:05:55Z |
| 3 | SPEC8 | 41f2a8489f3cb9da7b0e7d686fa2e160adec2243 | 2024-07-29T17:05:10Z |
| 4 | SPEC6 | 9209c89696ea2bce4460f59f9694ad9c82f99d6a | 2024-02-06T20:10:52Z |
| 5 | SPEC5 | 0dab527d07d885cc001973147e2d2698630d6922 | 2022-09-22T21:38:47Z |
| 6 | SPEC4 | a53b7562b1d00a6044de0e7c34b8eb2a8f631c02 | 2022-09-05T15:14:47Z |
| 7 | SPEC3-current | 89963912e0500f5ab8f9037752ae0b770c0787a7 | 2022-02-14T20:18:40Z |
| 8 | SPEC2-API-dispatch | 124874527a4bff89bf7cdee706babfa0a8b51e88 | 2021-12-18T18:18:24Z |

기존 원문 인용량을 늘리지 않기 위해 본 감사는 두 제안 원문을 추가 직접 인용하지 않고 절·고정 주소와 해석만 남겼다.

