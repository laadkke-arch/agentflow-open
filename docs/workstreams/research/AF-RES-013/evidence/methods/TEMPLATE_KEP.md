# KEP 템플릿: Goals와 Alternatives 절의 도입 이력

## 확인한 결론

**Alternatives는 2020년 현행 경로 생성보다 앞선 최초 템플릿 계보에 이미 존재하며, 독립 Goals 절은 그 뒤 추가되었다.** 두 절을 템플릿의 `creation-date` 필드나 현재 파일의 최초 커밋 날짜로 일괄 처리하면 잘못된 연혁이 된다.

| 확인 대상 | 직접 확인한 커밋·판 | 작성 시각(UTC) | committer 시각(UTC) | 확인한 변화 |
|---|---|---|---|---|
| 추적한 계보의 최초 템플릿 제안에 Alternatives가 있음 | community [e99752b8f06125ce5b9dbc6e7eba4f108ab9f32a](https://github.com/kubernetes/community/commit/e99752b8f06125ce5b9dbc6e7eba4f108ab9f32a), M17 | 2017-08-31 23:34:45 | 2017-09-26 08:09:17 | 새 `contributors/design-proposals/kep-template.md`의 템플릿 코드블록과 절 설명에 Alternatives가 있다. 독립 Goals 머리말은 없다. |
| 독립 복사용 템플릿 파일에 Alternatives가 있음 | community [b01d0a7c1564fe0562d99b32608c4dd84136840d](https://github.com/kubernetes/community/commit/b01d0a7c1564fe0562d99b32608c4dd84136840d), M18 | 2017-09-26 06:32:57 | 2017-09-26 08:09:17 | 이전 파일을 지침으로 옮기고 `architecture/kep-template.md`를 추가한다. Alternatives는 이미 제안된 내용을 옮긴 것이다. |
| Goals와 Non-Goals 독립 머리말 추가 | community [1f9a673ae08e7767f1f5198dbb0b2ae588f00032](https://github.com/kubernetes/community/commit/1f9a673ae08e7767f1f5198dbb0b2ae588f00032), M19 | 2017-11-13 23:47:29 | 2017-11-14 23:59:19 | Motivation 아래의 두 머리말 및 안내를 `+` 패치로 추가한다. 이전 Motivation도 목표 설명을 요구했으므로 개념의 최초 언급과 머리말 신설을 구분한다. |
| Goals 추가 직전 부모 판 | community [c5abc490f90cb6b86c666daa8aeac58c587ba314](https://github.com/kubernetes/community/blob/c5abc490f90cb6b86c666daa8aeac58c587ba314/contributors/design-proposals/architecture/0000-kep-template.md), M20 | 해당 표에서는 날짜를 추론하지 않음 | 해당 표에서는 날짜를 추론하지 않음 | 전체 머리말을 직접 확인했다. Motivation과 Alternatives는 있고 Goals·Non-Goals 독립 머리말은 없다. |
| 현행 템플릿 README 경로 생성 | enhancements [400931940a25a8a6ca001f4fd9f8735bdd79edee](https://github.com/kubernetes/enhancements/commit/400931940a25a8a6ca001f4fd9f8735bdd79edee), M21 | 2020-02-07 21:41:42 | 2020-03-11 22:38:55 | `keps/YYYYMMDD-kep-template.md` 삭제와 `keps/NNNN-kep-template/README.md` 추가. 삭제된 이전 판에도 두 절이 존재한다. |

이 표의 날짜는 Git 커밋 메타데이터다. 실제 PR 병합 시각과 동일하다고 주장하지 않는다. Q1에서 간단히 기입할 때는 **Alternatives: 최초 제안 커밋 작성 2017-08-31 / committer 2017-09-26; Goals 독립 절: 작성 2017-11-13 / committer 2017-11-14**로 쓰는 것이 재현 가능하다.

## 경로 추적

아래는 실제 API 이력과 변경 파일 메타데이터를 읽어 확인한 경로다. 날짜는 이동 커밋의 committer 날짜다. 원문 API 응답은 저장하지 않았고 SHA·경로·날짜·요약만 남겼다.

| 시점 | 확인한 경로·변경 | 커밋 |
|---|---|---|
| 2017-09-26 | `contributors/design-proposals/kep-template.md` 최초 추가 | community `e99752b8f06125ce5b9dbc6e7eba4f108ab9f32a` |
| 2017-09-26 | 지침 파일과 `contributors/design-proposals/architecture/kep-template.md` 분리 | community `b01d0a7c1564fe0562d99b32608c4dd84136840d` |
| 2017-09-26 | `contributors/design-proposals/architecture/0000-kep-template.md`로 재구성 | community `638617160b838e6d02a305df0ed4d53557450f07` |
| 2017-11-14 | Goals·Non-Goals 머리말 추가 | community `1f9a673ae08e7767f1f5198dbb0b2ae588f00032` |
| 2017-12-19 | community의 `keps/0000-kep-template.md`로 이동 | community `12577ba491c311d1f8830ecc15bd38782398effc` |
| 2017-12-19 | enhancements에서 읽히는 초기 계보는 루트 `0000-kep-template.md` 추가로 시작 | enhancements `8d649b65c852a1fee68510ccf4b08c5f38258dcc` |
| 2018-12-01 | 루트 파일을 `keps/0000-kep-template.md`로 이동 | enhancements `fa8da20499361c9e7849b50031aa030012a1612d` |
| 2019-02-15 | `keps/YYYYMMDD-kep-template.md`로 이름 변경 | enhancements `f9facb2a4b79fa8495486e8899dfa9b17de9539d` |
| 2020-03-11 | 현행 `keps/NNNN-kep-template/README.md` 생성 | enhancements `400931940a25a8a6ca001f4fd9f8735bdd79edee` |

경로별 이력 요청 URL, 반환 개수, 커밋 SHA·날짜 목록은 `supplementary-SEARCH_LOG.json`에 있다. 현행 경로는 43개, `keps/YYYYMMDD-kep-template.md`는 7개, `keps/0000-kep-template.md`는 7개의 커밋을 반환했다. 각 요청은 `per_page=100`이므로 이 조회들의 다음 페이지 누락은 없었다.

주의할 관측이 있었다. 삭제된 옛 경로를 현재 기본 가지에서 조회했을 때 두 번 빈 배열이 반환되었지만, 바로 전 이동 커밋의 부모 SHA를 명시한 조회에서는 각각 이전 이력이 나왔다. 따라서 **기본 가지의 경로 이력 0건을 ‘그 파일은 과거에 없었다’는 증거로 사용하지 않았다.** `enhancements`에서 최초로 관측한 2017년 커밋은 부모가 없는 형태였으므로, 파일이 가리키는 `community`의 이전 경로를 따로 추적했다. 저장소 간 이력 변환 도구나 절차 자체는 이 조사에서 확정하지 않았다.

## 정답원으로서의 의미

초기 Alternatives는 optional로 명시되어 있다. 따라서 옛 KEP에서 이 절이 없거나 짧은 것이 반드시 작성 실패를 뜻하지 않는다. 사례당 항목 3개 이상이라는 포함 조건은 이 계열의 전체 문서에서 충분한 대안 기록이 있는 문서를 선택하는 조건이며, 계열 전체의 기록 충실도나 타 분야 인용 빈도로 일반화하면 안 된다. 이 판단은 초기 템플릿과 AF-RES-013의 표본 조건을 함께 읽은 연구자 해석이다.

또한 Goals라는 독립 머리말이 생기기 전에도 Motivation은 설계 목표를 기술하도록 요구한다. 따라서 시기별 접두부 추출은 머리말 문자열의 존재만 보지 말고 실제 문맥·시점·문서 판을 확인해야 한다. 커밋 이력 확인은 원문 구조의 변화를 설명하며 현재 사례별 입력에 정답이 섞이지 않았다는 별도 검사를 대신하지 않는다.

## 한계

- ‘최초’는 확인한 공식 KEP 템플릿 계보에서의 최초다. Kubernetes의 모든 이전 설계 문서나 개인 초안의 최초 용례를 조사하지 않았다.
- 커밋 작성 시각·committer 시각·PR 병합 시각을 구분했다. 마지막 항목은 이번 도입일 확인에 필요하지 않아 산출하지 않았다.
- 같은 템플릿의 여러 판과 이력 API를 서로 다른 최소 자료로 부풀리지 않는다. M17–M21은 템플릿 계보 보조 자료로 `counted: false`다.
- 커밋의 저자 사용자명·이메일·프로필 및 외부 본문 전체를 파일에 저장하지 않았다.
