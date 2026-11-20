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

## 선정 원장 감사에 따른 추가 — P0386 / C31

첫 접두부 묶음 이후, gold 공개 전 원문 항목 분절을 다시 점검했다. PEP386은 Distutils를 하나의 도구로 묶으면 Setuptools와2개처럼 보였지만, 원문은 LooseVersion·StrictVersion의 문법/비교 동작을 독립적으로 비교한다. Setuptools parse_version을 합치면3개이고, RPM과 Debian/Ubuntu의 명시 비교까지5개다. 초기 분절은 SCOPE의 독립 설계 변형 규칙과 어긋났으므로 적격 누락을 복구했다.

이 문서는2010-03-21 Accepted 반영과2014-08-22 PEP440 대체가 확인되어 대체층에서 PEP354 다음에 놓인다. 이미 동결한30개는 보존하고 C31을 추가하여31개(Rust8/Python9/Swift8/KEP6)로 확장한다. 최초 선정 오류를 없던 것으로 하지 않으며, 이로 인한 층별 포함 내역과 기존 P0563의 추가 대체층 성격을 원장에 남긴다. 최초30개의 실행 순서는 그대로 두고 C31을 끝에 붙인다. 이 보정 시 C31 실행 결과는 없었고 기존 A의 일부 실행은 진행 중이었다. 따라서 완전히 오류 없는 사전 선정이라고 주장하지 않는다. C31 접두부도 gold 파일보다 먼저 별도 커밋한다.

## 실행 후 선정 원장

계획과 구별한 실행 기록이다. 아래는 실제 읽기 또는 부분 선별 결과이며, 자동 길이 검사만 한 문서를 D1 완독으로 세지 않는다. 원장에는 URL·판·시각·세부 이유가 있다.

### Rust RFC

상세 원장: `evidence/cases-rust/selection.json`; 기록 40행.

| 건너뛴 문서 ID | 이유 | 확인 범위 |
|---|---|---|

| R0001, R0003, R0019, R0026, R0034, R0040, R0048, R0049, R0050, R0059, R0060, R0063, R0066, R0068, R0071, R0079, R0086, R0087, R0089, R0092, R0100, R0107, R0109, R0111, R0112, R0115, R0116 | fewer_than_3_items | 직접 비교절 읽기 |

| R0002 | process_not_feature | 직접 비교절 읽기 |

| R0090 | no_comparison_section | 직접 비교절 읽기 |

| R0130, R0131, R0132 | quota_already_met | 직접 비교절 읽기 |



### Python PEP / Swift Evolution

상세 원장: `evidence/cases-ps/selection.json`; 기록 91행.

| 건너뛴 문서 ID | 이유 | 확인 범위 |
|---|---|---|

| P0215, P0431, P0203, S0001, S0003, S0007, S0009, S0010, S0012, S0013, S0015, S0017, S0024, S0026 | fewer_than_3_items | manual_comparison_section_read |

| P0241, P0314, P0345, P0100, S0005, S0006, S0008, S0011, S0014, S0023 | no_comparison_section | manual_comparison_section_read |

| P0344, P0367 | no_explicit_supersession | manual_comparison_section_read |

| P0622, P0631, P3153 | eligible_beyond_quota | manual_comparison_section_read |

| S0002, S0004 | prefix_not_historically_recoverable | manual_comparison_section_read |

| S0028, S0029, S0030, S0031, S0032, S0033, S0034, S0035, S0036, S0037, S0038, S0039, S0040, S0041, S0042, S0043, S0044, S0045, S0046, S0047, S0048, S0049, S0050, S0051, S0052, S0053, S0054, S0055, S0056, S0057, S0058, S0059, S0060, S0061, S0062, S0063, S0064, S0065 | eligible_beyond_quota | automated_section_length_screen_only |

| P0205, P0206, P0207, P0208, P0209 | eligible_beyond_quota | partial_comparison_preview_only |



### Kubernetes KEP

상세 원장: `evidence/cases-kep/selection.json`; 기록 45행.

| 건너뛴 문서 ID | 이유 | 확인 범위 |
|---|---|---|

| KEP-24, KEP-117, KEP-135, KEP-281, KEP-365 | fewer_than_3_items | 직접 비교절 읽기 |

| KEP-34 | no_decision_date | 직접 비교절 읽기 |

| KEP-85, KEP-95, KEP-115, KEP-116, KEP-121, KEP-166, KEP-213, KEP-266, KEP-268, KEP-351, KEP-378, KEP-382, KEP-423, KEP-427, KEP-491, KEP-492 | no_comparison_section | 직접 비교절 읽기 |

| KEP-177, KEP-265, KEP-284, KEP-361 | empty_template | 직접 비교절 읽기 |

| KEP-504, KEP-531, KEP-536, KEP-541, KEP-548, KEP-554, KEP-555, KEP-556, KEP-557, KEP-559, KEP-563, KEP-565, KEP-566 | screened_past_quota_for_fallback | 직접 비교절 읽기 |


