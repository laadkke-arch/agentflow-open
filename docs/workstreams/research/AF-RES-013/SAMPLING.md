# AF-RES-013 — SAMPLING v1 (선정 전에 고정)

## 목록·기간·정렬·시드

시드 문자열은 `AF-RES-013-20261120-1313`, 숫자 시드는1313이다. 모집단은 아래 공식 목록에서 발견되는 공개 설계 제안이며, 결정 관측 창은2000-01-01~2024-12-31이다. 이후 결정은 역사적 검색과 현행 검색이 거의 같아지는 것을 줄이기 위해 본표본에서 제외한다. 이 한정은 표본 대표성을 위한 무작위 추출이 아니다.

| 계열 | 목록 주소 | 초기 목표 | 기본 정렬 |
|---|---|---:|---|
| Rust RFC | https://github.com/rust-lang/rfcs/tree/master/text | 8 | RFC 번호 오름차순 |
| Python PEP | https://peps.python.org/pep-0000/ 및 https://github.com/python/peps/tree/main/peps | 8 | PEP 번호 오름차순 |
| Swift Evolution | https://www.swift.org/swift-evolution/ 및 https://github.com/swiftlang/swift-evolution/tree/main/proposals | 8 | SE 번호 오름차순 |
| Kubernetes KEP | https://github.com/kubernetes/enhancements/tree/master/keps | 6 | KEP 번호 오름차순; 경로 사전순 tie-break |

각 계열의 전체 목록을 저장소 API/공식 목록에서 얻고, 실제 스크리닝은 결정문이 있는 표준/기능 제안을 대상으로 한다. 템플릿·프로세스·릴리스 일정·번호할당·오타수정은 제외한다. 문서 제목/초록만으로 적합을 확정하지 않는다.

## 두 층을 차례로 구성

1. **대체 층(최소5):** 공식 metadata의 Superseded-By/Replaces, 원문/후속의 supersede/replace/revert/reconsider 명시를 단서로 찾아 원문과 후속을 직접 확인한다. 계열 순서는 Python → Swift → Rust → Kubernetes, 각 계열 내부 번호 오름차순. 항목3개·고정판·결정일 조건을 통과한 앞5개를 먼저 선정한다. 일부 결정 변경은 partial_reversal로 명시한다. 후속이 존재할 뿐인 것은 제외한다.
2. **일반 층:** 각 계열에서 대체 층 중복을 빼고, 비교절이 존재하는 문서를 번호 오름차순으로 스크리닝한다. 각 계열 목표까지 앞의 적합 사례를 포함한다. 문서 수가 많은 계열은 기계적으로 비교절 후보를 찾을 수 있지만 최종 포함은 본문을 직접 읽은 뒤 판단한다. 빠른 스크리닝 규칙(예: alternatives heading/서로 다른 하위 항목/외부 링크)은 logs에 남긴다.
3. 한 계열에서 목표 미달 또는 대체층 부족 시 그 사실을 기록한 뒤 같은 목록의 다음 문서로 진행한다. 네 계열의 합계가30이 넘더라도 최소조건을 갖춘 사례를 임의 제거하지 않는다. 한 계열은 전체50% 이하를 유지한다. 부족분 대체 순서: Go design, 공개 ADR, IETF, TC39. 새 계열/규칙은 선정 전 이 문서의 별도 변경 절에 커밋한다.

시드는 선별된 사례의 실행 순서와 재검토 표본에 쓴다: SHA256(seed + ':' + case_id) 오름차순. 무작위 모집단 표본으로 부르지 않는다. 사례 ID는 계열 R/P/S/K와 실제 제안 번호를 결합하되 baseline 접두부에는 중립 C01… 식별자를 사용한다. gold의 내부 ID와 중립 입력의 대응은 실행자에게 주지 않는다.

## 스크리닝 기록

모든 실제 열린 후보를 evidence/selection-*.json에 {url,canonical_id,screen_order,outcome,reason,opened_at_utc,pinned_version}으로 기록한다. 미열람 목록의 수와 직접 스크리닝 수를 구별한다. 같은 후보를 재열람한 것은 한 사례다. 최초판/결정판/후속판은 같은 사례의 시점별 근거다.

건너뛰기 이유: fewer_than_3_items, no_comparison_section, empty_template, no_decision_date, prefix_not_historically_recoverable, after_window, inaccessible, process_not_feature, no_explicit_supersession, duplicate. 이유를 다른 사례가 유망하다는 선호로 바꾸지 않는다.

## 사례 외 자료와 출처 수

사례 원문>=30과 비사례 원문>=20은 분리한다. 비사례 목표는 템플릿/절차>=4, 방법론논문>=4, 다른분야 평가>=3, 생성형 인용 평가>=2(009기열람 제외), 리뷰토론>=5. 실제 연 URL·시각·절·요약·한계·D수준을 기록한다. 같은 사이트는 비사례 최소수에서 최대3개만 산입하며 github.com/raw/api는 같은 사이트로 합친다. 사례30개는 서로 다른 제안서가 단위라 호스팅 GitHub에 대한3개 상한을 적용하면 요청 자체와 충돌하므로 **네 독립 프로젝트 계열의 사례 수**로 보고하며 사이트별 문서 수도 함께 드러낸다. 이 해석은 과잉 산입하지 않게 보고서에서 명시한다.

## 아직 선정되지 않은 상태

이 첫 커밋 시점에는 템플릿4건의 열람 시도만 했으며 사례·gold·baseline을 만들지 않았다. 후속 스크리닝 원장과 접두부가 이 계획을 따라 작성된다.
