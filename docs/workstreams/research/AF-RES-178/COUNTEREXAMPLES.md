# 경쟁 설명·반례·분야 비교 (④)

## 한 함수 이름이 아니라 연산 계약
- 하류 유지자 관점: S07/S08은 폐기 경고 및 의존성 현대화를 함께 처리했다. NumPy/sklearn 규격 버전 가정은 자연스럽지만, S19/S20의 **유효한 PEP440 개발판**이 반례다. strict Version으로 정상 import 가능하더라도 min gate가 달라질 수 있다. S26의 CI는 '*' 분기에서 적혀 있는 numpy 고정값을 설치하는 증거가 아니고 doctest exit를 무시한다. 테스트 행렬과 실제 설치 문자열을 구별한다.
- 기존 비표준 입력 사용자: S43의 Manjaro release 원문은 parse 당시 True, LooseVersion False(<)를 보고했다. S03의 21.3 LegacyVersion fallback은 비규격을 받아도 순서가 다름을 설명할 후보. S04의 23.0 parse는 Version으로만 이어지므로 그 문자열에서 거부 예상. 정확 보고 버전 미확인. 이는 import 성공이 허용 영역과 순서를 보장하지 않는 경우. **실제 지명 프로젝트에서 이 문자열을 받았다는 증거는 없다.**
- 포장 도구 작성자: S44의 ScanCode 신고는 과거의 wild version까지 수용하는 요구. PEP440 강제는 배포/설치의 표준 입력에 적절하지만 역사적 수집과 다른 계약. LegacyVersion 역시 LooseVersion 보존을 뜻하지 않는다.
- 좁은 단일 권고: S34의 matplotlib 3.4.1과 S27의 1.5.0 gate는 두 규칙에서 >= True로 추론된다. S21의 안정판 1.2.3,1.2,1 fixture는 strip/strict 모두 True 기대. 직접 설치나 실행 결과가 아니다. 규격 입력만 처리하더라도 전순서 보존 목적이면 자동 교체 금지: 1.0.dev0 비교가 반례. 단일 권고의 조건은 '규격 순서가 목적'이지 '규격 문자열'만이 아니다.
- Elpy S13/S15: import 또는 경고 수정으로 config가 표시되었다는 것과 update 판단의 정확성은 다름. 연결 실패 false 및 latest null, RPC 환경 변화, pkg_resources 문제 등 경쟁 원인. S32는 setuptools 설치목록 ERT이지 Python LooseVersion fixture 아님.
- S11의 2026 PR은 조사기간 밖, 아직 open. 현대 Matplotlib만 지원하면 gate 삭제라는 제3후보를 보여준다. S07도 obsolete check 제거를 제안. 실제 지원 최소값과 예외 설치환경의 증명이 선행.
- MNE S21은 strip=True를 gate에 국한. S20에서 구방식 == False, <= False인데 strip하면 둘 다 True; 전역 normalizer로 확대하면 안 된다. _compare_version strict 자체는 유지. 12 fixture는 가짜 모듈에 __version__을 주입하는 기대값이며 실제 장비 실행 아님.

## 다른 분야에서 옮길 것과 버릴 것

| 원문 | 관찰 가능한 순서 | 옮길 원리 | 옮기면 틀리는 것 |
|---|---|---|---|
| Debian Policy §5.6.12 S36 | epoch:upstream-revision; tilde precedes empty and other chars | 도메인별 토큰 의미와 필드 순서 먼저 고정 | PEP440 dev/local 순서를 Debian의 ~·revision에 그대로 적용 |
| RPM rpm-version(7) S37 | EVR; 1.0-1 < 1.0-5 < 1.0.1; ~와 ^ 의미 | 배포자 접미사를 무시하지 말고 upstream/release 구분 | Python Version에 rpm EVR을 입력하거나 ^를 보편 접미사로 제거 |
| University of Arizona S38 | Cutter A55 before A6 (소수 0.55 < 0.6) | 필드마다 다른 수치 해석과 정렬 규칙 명시 | 숫자 조각 정수 비교: 55>6이므로 서가 순서 반전 |
| University of Illinois S39 | class 정수/소수 + Cutter 소수 + 연도 | 식별/정렬 목적, 소수 자릿수 및 별도 필드를 구분 | 청구기호를 release/min gate 또는 호환성 판단으로 간주 |

이는 소프트웨어 버전 규약 이식이 아니라 역할·단위·연산에 따라 다른 비교 원전을 찾아주는 원리. 라이브러리의 안내는 해당 기관 발행 원문이고 LC 본체 편집 문서의 독립 대조는 미확인.

## 조합 가능한 설계 대안 (제품 DB 미결정)
1. 가벼운 링크+예외: 확정 목적이면 원전 하나와 적용 이유. 비용 낮음, 숨은 입력 도메인과 dev gate 누락 위험.
2. 입력 계약 분기: source (PyPI/metadata, vendor release, archive, call number), operation (min/equality/order), accepted/rejected examples, prior semantics (strict/loose/strip), environment/edition. 필요한 것만 원문 링크와 고정 버전으로 붙임. 사용자 추가 질문 비용이 있지만 오추천 줄임.
3. 증거 연결: proposal→merge→tag→actual result를 별도 표현. 링크의 변경/사라짐과 코드 의미 변경을 분리. 원자료 없는 단계는 보류. 동일 신고 계보 S19/S20을 독립 표본으로 부풀리지 않는다.
4. 조합 조건: A01 역사를 A02 현재 권고와 병렬로 보여줄 수 있지만 둘을 동치로 표현하지 않음. A03과 A04는 실제 입력이 다를 때만 추가; 불명확하면 최소 질문. A05는 dependency floor 증명 후에만.
5. 비용·실패: 각 조건 검증에 추가 원문/판/실측 비용. 전체 후보 미리 대량 수집이 아니라, 사용자가 보존하려는 구체 연산과 실자료 값으로 필요한 후계 수를 줄이는 방향. 단일 권고에 반례가 하나라도 관련되면 조건부/보류.

## 반증 탐색 결과
- 규격 문자열도 차이 나는 반례: 발견(S19/S20).
- 비규격에서 파서 교체가 수용 또는 정렬을 바꾸는 반례: 발견(S43, 별도 계보).
- 고정 테스트가 runtime 입력을 대표하지 않는 경우: 발견(S26, S32, S21); 현업에서 누락된 특정 동일 프로젝트 문자열까지 연결은 미확인.
- 좁은 안정판: S34/S27 문서 원값 및 S21 fixture. 실행 동일성 미확인.
- 동작이 바뀌지 않는 성공: Elpy #1951/#2055는 함수가 바뀌지 않으므로 경고 또는 모듈부재 해결이 버전 순서 회복의 증거가 아님.
