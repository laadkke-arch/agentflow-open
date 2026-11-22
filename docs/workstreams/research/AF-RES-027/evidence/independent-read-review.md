# Homebrew 사례 별도 내부 판독

- 판독자: `/root/cross_domain`. **같은 모델 계열 내부 별도 판독, 외부인 독립 검토 아님.** 해당 Homebrew 자료의 최초 수집에는 참여하지 않았으나, 이번 보고서는 수집자의 판정과 근거 위치를 본 뒤의 비맹검 재판독이다.
- 판독 완료 UTC: 2026-11-22T05:37:39Z 이후 기록. 아래 원문 재열람은 이번 내부 판독 세션에서 수행했다.
- 입력: `collectors/homebrew/upstream.json`, `chains.json`, `verdicts.json`, `future-sources.json`, `release-archive-receipt.json`; `collectors/homebrew-b/`의 B-H02 사례 및 해당 출처 행.
- 쓰기 범위: 이 판독 파일. 수집자의 파일은 수정하지 않았다. 아래 중복 재열람 자료는 원문 최소수에 추가하지 않는다.

## 판정 요약

| 검토 대상 | 판독 결과 | 통합본에 필요한 처리 |
| --- | --- | --- |
| A-H02 kitty 자산 시각 | 현재 자산 메타데이터와 수정된 배포 소스의 존재는 확인. `created_at`–`updated_at`이 최초 공개 배포의 엄밀한 2초 구간이라는 의미는 확인하지 못함 | **필수:** 수치의 의미를 메타데이터 차이로 한정. 최초 배포 지연의 적격 관측이나 통계적 구간 검열에 산입하지 말 것. 해당 배포판의 내용 확인과 실제 CI/사용자 효과는 계속 분리 |
| A-H01 fish/cppcheck | 2019 호출과 현재 패키지의 정적 부적합을 당시의 오류 또는 현재 fish의 실패로 넘기지 않은 `UNDECIDABLE`은 타당 | 2024 원문이 직접 보이는 것은 기여 문서에서 C++/cppcheck 안내를 삭제한 사실임을 유지. 현재 fish 전체의 모든 호출 부재까지 단정하지 말 것 |
| A-H06 qutebrowser | `pyqt@5` 수정 커밋 뒤 v2.5.3 고정판에도 이전 명령이 남음. 소스 수정과 대응 배포를 구분한 판정은 타당 | `pyqt@5`의 첫 대응 배포일은 미확인 유지. 후속 Qt6 판을 Qt5 정정의 배포일로 대체하지 말 것 |
| B-H02 Borg/Python | Homebrew 설치 문서의 다른 수정은 Python 참조 정정의 증거가 아님. 수집자가 이를 제외한 처리는 타당 | cask→formula/FUSE/지연 보고를 Python 변경의 실패·정정·효과로 전이하지 말 것. 소스 커밋 기준 365일 임시 검색 범위를 정식 시행 후 창/우측 검열과 구분 |

## 직접 다시 연 원문과 확인 위치

| 재열람 ID / 수집 출처 ID | 원문 URL·고정판 | 직접 확인한 위치와 내용 | 제한 |
| --- | --- | --- | --- |
| IR-H01 / H-R01 | <https://api.github.com/repos/kovidgoyal/kitty/releases/tags/v0.38.0> ; 공개 표시 <https://github.com/kovidgoyal/kitty/releases/tag/v0.38.0> | `published_at=2024-12-16T01:40:10Z`; `assets[id=213583777]`의 `state=uploaded`, `created_at=2024-12-16T01:41:05Z`, `updated_at=2024-12-16T01:41:07Z`, `size=8927688`, `digest=null`, `browser_download_url` 확인 | 현재 API 응답은 고정 과거 응답이 아니다. 이 재판독에서는 archive를 다시 내려받지 않고 수집자의 H-R02 다운로드 영수증을 읽었다. 현재 `uploaded` 상태 자체가 그 상태로 전환된 시각을 제공하지는 않는다 |
| IR-H02 / H-C02 | <https://github.com/fish-shell/fish-shell/commit/59922d0859781ea9202f8312da8f43c7c15cd192> ; API 동일 SHA `/commits/…` | `CONTRIBUTING.rst` diff `@@ -8,7 +8,7`, `@@ -27,7 +27,6`, `@@ -91,36 +90,6`: Rust/C++ 표현을 Rust로 바꾸고 C++11 요구 및 cppcheck·`lint`/`lint-all`·custom rules 설명을 삭제 | 문서 목적의 변화는 확인한다. 현재 저장소 모든 호출부 또는 역사판 재현 지원 정책의 전수 증거는 아니다 |
| IR-H03 / H-C06 | <https://github.com/qutebrowser/qutebrowser/commit/7b53f648141dd9b604fc01a8603faa55021576e7> ; API 동일 SHA `/commits/…` | `doc/install.asciidoc` diff `@@ -388,21 +388,10`: `brew install qt` 및 수동 PyQt/PyQtWebEngine 지시를 `brew install pyqt@5`로 교체 | 커밋 내용은 배포 사실/시각이나 실행 성공의 증거가 아니다 |
| IR-H04 / BH-S08 | <https://github.com/borgbackup/borg/commit/e632f2659e09c83881afcd4cdc3b034247776a91> ; API 동일 SHA `/commits/…` | `docs/installation.rst` diff `@@ -48,7 +48,7`, `@@ -72,7 +72,7`: Borg 설치를 cask에서 formula로 바꿈. `@@ -223,16 +223,16`: Homebrew가 의존성을 자동 설치한다는 설명으로 바꾸지만 수동 명령 `brew install python3 openssl`은 그대로 | 제목 “Update Homebrew install instructions”만으로 Python 변경 대응이라 분류할 수 없다. 다른 FUSE 커밋·issue 본문은 이번 재판독에서 새로 열지 않고 수집자의 기록 범위만 검토 |
| IR-H05 / H-F07 (보강 원문) | <https://github.com/qutebrowser/qutebrowser/blob/2fe78b7644605c1e6622573935e7a2404922cbcd/doc/install.asciidoc> ; raw 동일 SHA 직접 GET | v2.5.3 고정 파일 L374–390, 특히 L377–383: 여전히 `brew install qt`, PyQt/PyQtWebEngine 수동 빌드 및 Homebrew 미제공 안내 | 이 판에는 수정이 없다는 관측. 모든 웹 문서·nightly·다른 배포 경로에도 없었다는 뜻은 아니다 |
| IR-M01 (날짜 의미 보강, 원문 최소수 제외) | <https://docs.github.com/en/rest/releases/assets?apiVersion=2022-11-28> | “Get a release asset” 응답 예시; “Update a release asset”의 수정 가능성 및 `name`, `label`, `state` 인수; “Upload a release asset”의 성공 응답·`starter` 상태 설명. 조회 렌더링 L78–104, L238–269, L295 | 현재 공식 API 문서다. 과거 운영 구현의 불변 사양이 아니며, `created_at`/`updated_at`을 최초 공개 접근 구간으로 보장하는 문장은 여기서 확인하지 못했다 |

## 1. A-H02: 존재·내용 확인과 최초 공개 시각을 분리해야 한다

H-R01의 세 시각은 재열람 결과와 일치한다. 수집자의 H-R02 영수증에는 `kitty-0.38.0.tar.xz` 8,927,688바이트, SHA256 `96fe79a645ec57a378295cdf16204265768091338d77efb058977b60209bb8ff`, 내부 `kitty-0.38.0/Brewfile`에서 직접 `pkg-config` 행이 빠진 내용이 적혀 있다. 이 자료는 **현재 내려받은 해당 공식 소스 배포물에 수정된 인용이 포함된다**는 주장을 지원한다. 2024-11-23T14:18:05Z의 소비자 수정 커밋으로부터 자산의 두 메타데이터 시각까지 계산한 22.4743056일과 22.4743287일도 산술값으로 남길 수 있다.

그러나 `tc_to_tr_interval.censoring = interval-bounded upload metadata`와 `eligible_for_same_reference_source_release_delay = true`는 그 수치가 정식 배포 지연 구간으로 읽힐 수 있다. IR-M01은 자산 수정 API와 현재 상태 필드를 제공하지만 두 날짜 필드를 최초 공개 가용성의 하한·상한으로 정의하지 않는다. 현재의 `uploaded` 상태와 마지막 수정 시각만으로 당시 첫 공개 접근을 2초 구간에 가두는 논리는 추가 증거가 필요하다. 업로드 기록이 배포 경로 전체의 첫 배포를 포괄하는지도 별도 문제다.

필수 수정 권고는 다음과 같다.

1. 메타데이터 필드와 두 산술차는 보존하되 이름을 `source edit → asset record created_at/updated_at offsets` 또는 같은 뜻의 한국어로 한정한다. “정정이 사용자에게 도착한 시간”, “최초 배포의 2초 구간”, 통계적 구간 검열이라고 부르지 않는다.
2. 정식 `Tc→최초 Tr` 적격성은 미확인으로 둔다. `first_matching_corrected_release`도 전 배포 경로를 소거하지 않았다면 “이번에 확인한 대응 소스 배포판”으로 제한한다. v0.37.0과 v0.38.0의 내용 비교는 보존한다.
3. 현재 배포물의 내용 확인을 삭제할 필요는 없다. CI 수정 효과·설치 성공·실제 사람의 피해/회복을 미확인으로 둔 기존 처리는 적절하다.

판정을 바꿀 최소 자료는 당시 asset ID와 내용 해시를 연결하는 업로드 성공 응답/공개화 로그, 또는 해당 타임스탬프의 역사적 의미를 보장하는 1차 명세와 첫 해당 배포 경로를 확인할 목록이다. 그 전에도 릴리스 페이지 게시일과 소스 자산 시각을 **별도 관측**으로 나열할 수 있다.

## 2. A-H01: 역사판의 재현 위험을 당시 잘못으로 소급하지 않았다

수집 기록은 옛 fish의 `--rule-file` 호출(H-F02), 현재 Homebrew의 `HAVE_RULES=OFF`(H-U08/H-U15), 해당 기능이 없을 때 실패하는 파서(H-U18)를 연결하되 실제 패키지 실행은 하지 않았다고 적었다. 이는 “오늘의 해당 조합으로 과거 목적을 재현하려면 기능 호환성 점검이 필요하다”는 정적 판정이다. 2019년 당시 설치물이 잘못되었다거나 현재 fish 사용자가 실패했다는 증거가 아니다.

별도 재열람한 H-C02는 2024년 기여 안내에서 C++와 cppcheck 규칙 설명을 삭제한다. 따라서 이 소비자의 현재 목적을 2019 목적과 자동으로 같게 놓고 정정 지연을 재는 것을 거절한 판단은 타당하다. 다만 “현재 fish는 해당 기능이 전혀 없다”보다 “재열람한 기여 문서의 해당 목적 안내가 먼저 제거됐다”가 원문에 맞는 범위다. 역사판 재현을 의도해 보존했는지 여부는 여전히 미확인이다.

## 3. A-H06: main의 정정 커밋은 다음 안정판 내용과 같지 않다

H-C06에서 `pyqt@5`로 고친 사실과 H-F07의 v2.5.3에는 그 변경이 없다는 사실을 각각 직접 확인했다. 후자는 소스 커밋일 뒤의 릴리스 날짜만으로 도달 시점을 채우는 방법의 구체적 반례다. 수집된 v2.5.4 및 v3.0.0 비교를 이번 판독에서는 새로 원문 재열람하지 않았다. 수집자가 v3.0.0의 `pyqt@6`을 다른 세대라고 구분하고 `pyqt@5`의 첫 대응 배포를 null로 둔 처리는 유지해야 한다.

정정이 전혀 배포되지 않았다고 단정할 수도 없다. 당시 문서 사이트 빌드, nightly 또는 `pyqt@5` 줄이 들어간 공개 배포 아카이브가 발견되면 이 셀을 바꿀 수 있다. CLI/GUI 실행 성공과도 별도로 검증해야 한다.

## 4. B-H02: 설치 문서의 다른 변경은 Python 사건의 정정이 아니다

BH-S08은 같은 문서에서 Borg 설치 경로와 의존성 설명을 바꾸지만 선택된 참조 `python3`는 유지한다. 이 diff를 Python3 기본 버전 전환의 후속 정정으로 세면 분석 단위가 다른 기능으로 이동한다. 수집자가 이 편집, 이후 FUSE 관련 편집, 다른 시점의 성능 보고를 선택한 Python 참조의 실제 실패·정정 효과에 산입하지 않은 점은 적절하다.

`python3`가 허용한 버전 범위와 텍스트상 들어맞는다는 판단 역시 모든 Borg 코드·바이너리의 실행 성공 보장은 아니다. 상류 실제 시행일을 찾지 못한 상태에서 소스 커밋 후 365일을 검색 보조 범위로만 쓴다면 가능하지만, 이를 정식 Tu 이후 365일 무수정이나 우측 검열로 집계하면 안 된다. 현 수집 기록의 `Tu=null`, 효과 미확인, 정식 창과 임시 검색 끝의 구분을 통합본에서도 유지해야 한다.

## 판독의 제한과 후속 확인

이 판독은 지정된 네 쟁점의 논리적 전이와 근거 범위를 점검했다. Homebrew A 전체의 모집틀, 모든 경로 이력, 릴리스 목록 전수조사, 패키지 실행 또는 사용자 재현 실험은 하지 않았다. 핵심 원문 4건과 qutebrowser 고정판 1건을 직접 재열람했고, 날짜 의미 때문에 공식 API 문서 1건을 추가 확인했다. 별도 판독자가 같은 모델 계열이라는 한계와 수집자 설명을 먼저 본 영향을 남긴다. 통합 RESULT의 분모·검열 집계는 별도 최종 판독 대상으로 남는다.

현재 우선 후속은 A-H02의 숫자를 **메타데이터 차이**와 **최초 배포 지연 미확인**으로 분리해 통합하는 한 건이다. 나머지 세 사례의 보수적인 범위 제한은 유지하는 것이 원문과 맞는다.
