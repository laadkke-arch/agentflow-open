# AF-RES-229 범위와 실행 전 예측

## 착수 고정점

| 단위 | 고정값·확인 |
| --- | --- |
| 계획 시점 통합판 | [`fc095c323d0177401d34f1daa7b4d1c529e2351f`](https://github.com/laadkke-arch/agentflow-open/blob/fc095c323d0177401d34f1daa7b4d1c529e2351f/docs/automation/dot-control.json). AF-RES-216은 RUNNING, `result_commit`은 null이다. 이 판의 `tasks` 배열에는 AF-RES-229가 아직 없다. |
| 선행 완료 게이트 | [`2a32cb8a661539308320cf985fc5584588203d52`](https://github.com/laadkke-arch/agentflow-open/blob/2a32cb8a661539308320cf985fc5584588203d52/docs/automation/dot-control.json), 2026-11-24 22:00:55 UTC 통합판. 216을 DONE으로 바꾸고 아래 인계 SHA를 기록했다. 229 배정 항목은 이 판에도 아직 없다. |
| 실제 착수 | [`f3895893e32e2c055cefde446d34f1467fa27b4c`](https://github.com/laadkke-arch/agentflow-open/blob/f3895893e32e2c055cefde446d34f1467fa27b4c/docs/automation/dot-control.json), 22:09 UTC 원격 `chore/workspace-foundation`. 계획판 이후 5커밋의 변경 경로는 `docs/automation/dot-control.json` 하나다. 216 완료 외에 `d013602`에서 229를 배정했고, `f389589`에서 229를 RUNNING으로 올렸다. 최신 항목의 `depends_on`은 [AF-RES-216], `result_commit`과 `source_commit`은 null이다. |
| 작업 계약 | 원격 `work/research-af-res-229`가 없는 것을 확인하고 위 착수 SHA에서 만들었다. 소유 경로 `docs/workstreams/research/AF-RES-229/`, 계약 2. [고정 계약](session.json) · [시작 명령과 출력](receipts/session-start.json) |
| 직접 의존 | AF-RES-216 브랜치 원격 head와 중앙 `result_commit`이 [`9a306b74e785dc98cb82fa000a10e497208309a6`](https://github.com/laadkke-arch/agentflow-open/blob/9a306b74e785dc98cb82fa000a10e497208309a6/docs/workstreams/research/AF-RES-216/HANDOFF.md)로 같다. 216 인계가 지목한 선행 실증 결과판은 `e2b767089a72c2e58c1a360d524f2b0d71df8ca9`이다. AF-RES-200은 216의 선행이자 역사 맥락이다. |

질문은 같은 공개 파일의 철회 속성을 바꾸었을 때 고정한 소비자의 **선택**, **사용자에게 나온 경고**, **종료** 중 무엇이 어떻게 바뀌는가다. 216의 V04–V06 `/urls/0`과 I02 `/files/309,311,313`을 원응답 지문까지 먼저 대조했다. 세 wheel의 `Requires-Python`은 `>=3.8`이고 파일명 태그는 `py3-none-any`다. 표본은 이 세 wheel로 고정한다. 최대판 8.1.1, sdist 0개, 외부 후보 0개가 목표다.

## 조작, 분모, 분류

- HTML Simple 페이지의 세 파일 링크에 SHA-256 fragment와 `data-requires-python`을 두고, URL은 같은 읽기 전용 loopback wheel 파일을 향한다. 기준은 8.1.0에만 216의 사유 문자열을 넣는다. `unmarked`는 이 속성 하나를 삭제한다. `empty`는 같은 속성 값을 빈 문자열로 두고, `missing`은 해당 링크 한 개만 뺀다. 사양에 따르면 미러는 원 신호를 보존하거나 링크를 생략할 수 있다. `unmarked`는 실험용이며 운영 미러의 허용 동작으로 제시할 수 없다.
- Python 3.12.14, pip 24.0 소스 태그 `ef78c129b1a966dbbbdb8ebfffc43723e89110d1`. 각 시행은 새 venv, 같은 버전의 pip, 초기 pytest 미설치 상태에서 한다. `python -m pip install --dry-run --ignore-installed --no-deps --only-binary=:all: --no-cache-dir --report …`와 로컬 단일 `--index-url`을 고정한다. 외부 소스나 캐시 가능성을 줄이기 위해 상속 pip 설정·프록시를 선택 실행의 환경에서 제외하고 `PIP_CONFIG_FILE`에 OS null 장치를 지정한다. pip 자체의 버전 조회를 끄고 로컬 페이지 외에 후보 주소를 주지 않는다. wheel 입수는 그 실행과 분리한다.
- 기본은 요구 4개 × 페이지 2개 × 깨끗한 반복 2회 = 16회(보고 표의 요청·페이지 셀 8개)다. 보조는 정확 요청 × 빈 사유/대상 링크 부재 = 2회다. 반복 1은 각 요청에서 기준 뒤 통제, 반복 2는 역순으로 예정한다. 재생은 동일한 18개 조건을 별도 임시 출력에 다시 실행하고 URL의 localhost 포트·시각·임시 경로를 떼고 비교한다. 재생과 문헌 수는 기본 실험 분모 밖에 둔다.
- 선택은 report 설치 배열 한 건의 `metadata.version`, `download_info.url`, `archive_info.hashes.sha256`, `is_direct`, `is_yanked` 및 HTTP 요청과 일치해야 한다. 경고는 같은 실행의 stderr에 선택 파일·버전과 연결된 선택 경고 및 바로 뒤 사유 줄을 확인하고 stdout도 읽는다. 성공·무경고는 실패·무선택과 구별한다. 요구 해석 실패, 파일 준비 실패나 서버/환경 실패는 원인별로 남긴다. 출구만으로 선택, 경고, 실설치를 판정할 수 없다.
- 문헌 하한은 직접 중복 제거 22개다. 선행·원응답·발행 6, 규격·사용 문서 5, pip 24.0 코드·회귀시험 6, 당시 당사자 2, 출판 3이다. 같은 파일의 여러 표면은 각 원값을 기록하되 산입할 때 계보를 묶는다. 독립 사례 사건과 자료 수를 따로 센다. 실패·미열람·범위 밖·관측된 0을 구분한다.
- 링크 안내의 적용 대상은 정확판 재현 사용자, 새 범위 사용자, 인덱스 운영자다. 실제 runtime, 플러그인 호환성, 다른 pip 판·Python·OS·인덱스, 당시 캐시 사용자, matplotlib Windows 삭제 복원과 216 전수 재집계는 범위 밖이다. 동시성·네트워크 결과의 재현성은 여기서 고정한 로컬 HTTP와 새 환경에 한정한다.

## 실행 전 봉인한 예측

| 선택 식 | 기준 `baseline` | 상태 속성 제거 `unmarked` |
| --- | --- | --- |
| `pytest==8.1.0` | 8.1.0, report `is_yanked=true`, stderr 선택 경고와 216 문자열, 종료 0 | 8.1.0, `false`, 선택 경고 0, 종료 0 |
| `pytest>=8.0.2,<8.1.1` | 8.0.2, `false`, 선택 경고 0, 종료 0 | 8.1.0, `false`, 선택 경고 0, 종료 0 |
| `pytest>=8.0.2,<=8.1.1` | 8.1.1, `false`, 선택 경고 0, 종료 0 | 8.1.1, `false`, 선택 경고 0, 종료 0 |
| `pytest==8.1.1` | 8.1.1, `false`, 선택 경고 0, 종료 0 | 8.1.1, `false`, 선택 경고 0, 종료 0 |

정확 `==8.1.0` 보조 예측은 `empty`에서 8.1.0 선택, `is_yanked=true`, stderr 선택 경고와 `<none given>`, 종료 0이다. `missing`에서는 8.0.2 및 8.1.1만 노출되므로 resolver 거절, report·wheel 요청·선택 경고 0, 종료 1을 예상한다. 모든 성공 시행에서 해당 pytest 파일 하나의 wheel GET과 report SHA-256 일치를 예상한다.

실행 전 근거는 non-yanked 적용 후보를 우선하는 [PEP 592 Installers](https://peps.python.org/pep-0592/#installers)와 [현행 File Yanking](https://packaging.python.org/en/latest/specifications/file-yanking/#installers), 적용 후보 필터의 [pip 24.0 factory.py L296–339](https://github.com/pypa/pip/blob/ef78c129b1a966dbbbdb8ebfffc43723e89110d1/src/pip/_internal/resolution/resolvelib/factory.py#L296-L339), 선택 후 경고의 [resolver.py L160–176](https://github.com/pypa/pip/blob/ef78c129b1a966dbbbdb8ebfffc43723e89110d1/src/pip/_internal/resolution/resolvelib/resolver.py#L160-L176), [업스트림 설치 회귀시험](https://github.com/pypa/pip/blob/ef78c129b1a966dbbbdb8ebfffc43723e89110d1/tests/functional/test_install.py#L2223-L2289)과 [dry-run report 시험](https://github.com/pypa/pip/blob/ef78c129b1a966dbbbdb8ebfffc43723e89110d1/tests/functional/test_install_report.py#L67-L117)이다. [pip CLI](https://pip.pypa.io/en/stable/cli/pip_install/#obtaining-information-about-what-was-installed)와 [report 설명](https://pip.pypa.io/en/stable/reference/installation-report/#specification)은 계측에 사용한다.

경쟁 설명은 버전 정렬만으로도 범위 판정이 같다는 설명, 사유가 비면 유효 상태가 풀린다는 설명, 철회가 링크 제거와 같다는 설명, report flag가 stderr 또는 실제 설치를 뜻한다는 설명이다. 이 예측이 틀린 경우 입력 지문·링크 파싱·resolver 분기·실제 요청 경로를 그 순서로 다시 읽는다.

## 자료 노출 순서

통합 규칙·중앙 기록과 AF-RES-216 고정 원값을 먼저 받았다. 규격과 소스·업스트림 시험의 관련 절을 읽었고, 위 기대를 첫 커밋에 봉인한다. 이 시점까지 대상 wheel 입수·로컬 pip 선택 실행·해당 실행의 report/로그 열람은 0회다. 다음 묶음은 추가 직접 자료 및 입력/fixture 봉인, 그 다음은 16회와 1차 판독, 그 다음은 두 반례 실행과 양성·음성 재생, 마지막 결과판은 자체 점검과 함께 고정한다. 작성자가 입력을 알고 실행한다. 독립 검토와 블라인드 실험은 별도 관측으로 취급한다.
