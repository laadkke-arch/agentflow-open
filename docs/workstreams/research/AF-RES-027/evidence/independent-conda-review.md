# AF-RES-027 · conda 사례 별도 내부 판독

## 판독 성격·입력

- 판독자: `/root/homebrew_a`. Homebrew A를 수집했으며, 이 문서에서 검토한 conda A의 수집자는 아니다.
- **같은 모델 계열 안의 별도 내부 판독**이다. 외부 독립 연구자·독립 기관·맹검 평가가 아니며, 전체 프로젝트 판단의 독립 재현으로 부르지 않는다.
- 범위: collectors/conda의 `upstream.json`, `chains.json`, `verdicts.json` 중 C04(Pandas/NumPy), C06(Spyder/applaunchservices); C01/C02의 경로 이행·라벨·검열 해석. 역사 원장, source 원장, path 추적 기록도 대조했다.
- 직접 재열람: 2026-11-22T05:40–05:42 UTC. 아래 중요한 원문 **4묶음, 7개 GET URL**을 읽었다. 같은 고정 commit의 여러 파일과 같은 PR의 본문/merge diff는 각각 묶었으며, 원문 최소수에 다시 더하지 않는다.
- 판독 기록 시각: 2026-11-22T05:43:13Z.
- 읽은 수집 파일 SHA256: upstream `affbf19d69fa063eb54b8c267dec10d52a87735109e20443dee4df72283a211e`; chains `c3392edb9a068ff1bdeadb51793947641dd128a1971bf48b2b69873ef7cc2a82`; verdicts `346c067c55c81027e5a429568c09372b26f4e9e3c883b1c7b2ac578284b1c27a`.
- 수집자 파일은 수정하지 않았다. 이 판독문만 작성했다.

## 판단

**C04/C06의 직접 실패 보고와 소비자 source 수정 연결은 원문에 부합한다. 실제 사용 artifact·최초 정상화·운영 배포까지 확인했다고 표현하지 않는 한, 부분 사슬이라는 판정은 타당하다.**

필수 수정 1건이 있다. C06 upstream의 “최소판 상향은 수정된 metadata를 보장한다”는 문구를 아래처럼 좁혀야 한다. 이는 확인된 version-floor diff보다 강하고, 같은 행의 실제 artifact/architecture 미확인과 맞지 않는다.

> 0.3.0 미만을 배제하고, 유지관리자가 의존성을 수정했다고 설명한 최소판을 요구한다. 검토한 conda-forge 0.3.0 recipe/artifact metadata의 변경과 실제 소비자 solve·실행 성공은 구별한다.

Root가 이 축소 권고를 수용했으며 통합 단계에서 원 수집 문구도 고치겠다고 알렸다. 이 문서는 **수정 적용 자체를 재검증한 영수증은 아니다**.

C04의 Tu→Tc와 C06의 실제 노출→수정 지연을 부적격으로 둔 `latency_eligible=false`는 유지해야 한다. source release 관련 시각은 공개된 source 판의 후보/포함 여부·발표 시각이며 실제 CI, 문서 서버, GUI installer, 사용자의 정상 실행 시각으로 승격하면 안 된다.

## 직접 재열람 근거

| 판독 ID·기존 근거 | 원 URL·고정판·직접 읽은 위치 | 확인한 내용 | 한계·최소수 |
| --- | --- | --- | --- |
| IR-C04-OLD / C-F53·C-S04 | [2019 CI](https://raw.githubusercontent.com/pandas-dev/pandas/35ba6b0dc0d49dbe5abe44eee62ea6276a1f7276/.github/workflows/ci.yml) L9–10,L99–121; [같은 판 setup_env](https://raw.githubusercontent.com/pandas-dev/pandas/35ba6b0dc0d49dbe5abe44eee62ea6276a1f7276/ci/setup_env.sh) L94–104; [같은 판 environment](https://raw.githubusercontent.com/pandas-dev/pandas/35ba6b0dc0d49dbe5abe44eee62ea6276a1f7276/environment.yml) L1–8,L28–34,L75 | 고정 2019판이 ENV_FILE=environment.yml을 지정한다. Ubuntu web_and_docs가 setup_env.sh로 그 파일을 conda env create에 전달하고 pandas-dev를 활성화한 뒤 warnings-as-errors 문서를 빌드한다. 환경에 NumPy>=1.15, Python=3.7, Sphinx, Matplotlib가 있다. | 정적 source 연결이다. 실제 conda solve나 실행 로그는 아니다. 봉인 뒤 Q2 보강이라는 표시가 맞다. 같은 2019 commit 1묶음이며 원문 최소수에 추가하지 않음. |
| IR-C04-PR / C-F16·C-F15 | [Pandas PR35312](https://api.github.com/repos/pandas-dev/pandas/pulls/35312) title/body/created_at/merged_at; [merge diff cd5e17c](https://api.github.com/repos/pandas-dev/pandas/commits/cd5e17c1a537a8ce8e786d308cebc64e1a2c6bda) environment.yml와 requirements-dev.txt | 유지관리자는 NumPy 경고가 Matplotlib를 거쳐 master 문서 빌드를 실패시키며 Matplotlib 3.3.0을 기다리는 임시 pin이라고 설명한다. 실제 diff가 같은 environment.yml의 NumPy 하한에 <1.19.0을 추가한다. 이때 Python 조건은 2019의3.7이 아니라 `python=3`이다. | 당사자 실패 보고와 source correction을 확인. 실제 실패에 쓴 Python minor/build, 첫 성공한 CI, 문서 서버 배포는 이 원문에 없음. 같은 수정 1묶음, 최소수 추가 없음. |
| IR-C06-REPORT / C-F28 | [applaunchservices issue1](https://api.github.com/repos/impact27/applaunchservices/issues/1) created_at/body/traceback | 2022-04-29T01:24:04Z 보고. pip/virtualenv에서는 editable Spyder 실행이 되지만 conda에서는 pyobjc 배포 의존성이 없다는 오류로 시작하지 못한다고 설명한다. traceback은 Python3.10 환경을 보여 준다. | 0.3.0 공급/수정에 앞선 문제 보고다. CPU architecture와 설치된 정확한 conda build는 알 수 없다. 파일 열기 등록 기능을 실제로 실행해 본 결과도 아니다. 생산자/소비자 유지관리자 계보가 겹치므로 독립 외부 소비자로 중복 산입하지 않음. |
| IR-C06-FIX / C-F25 | [Spyder c185384](https://api.github.com/repos/spyder-ide/spyder/commits/c1853843ace0f7b9347d74b9c8636f48d12c2537) commit message; requirements/macos.yml,setup.py,spyder/dependencies.py diff | 2022-07-03T19:56:02Z source commit이 applaunchservices 최소판을 >=0.1.7에서 >=0.3.0으로 바꾼다. setup.py의 Darwin 조건은 유지된다. commit 설명은 해당 새 버전의 Pyobjc 의존성이 수정됐다고 말한다. | >=0.1.7도0.3.0을 허용하므로 이 commit 전 모든 설치가 실패했다는 뜻은 아니다. version floor만으로 정확한 channel/build/정상 GUI 실행이 확정되는 것은 아니다. 테스트 파일 수정은 실행 성공 기록이 아니다. 최소수 추가 없음. |

모든 직접 재열람은 공개 원문 읽기였다. 패키지 설치, conda solve, CI 재실행, GUI 실행은 수행하지 않았다. API/원문에 있는 명령이나 코드도 실행하지 않았다.

## C04 · 같은 목적과 시간쌍

### 확인된 연결

2019판의 source 연결은 단순히 “NumPy가 개발환경에 있었다”보다 강하다. environment.yml을 실제로 생성 입력으로 쓰는 setup_env.sh, 같은 환경을 활성화하는 Ubuntu 문서 작업, warnings-as-errors 호출을 같은 SHA에서 모두 확인했다. 따라서 이후 PR35312가 설명하는 문서 빌드 목적을 옛 참조와 연결하는 것이 타당하다. 이 보강을 A 선정 시 이미 알고 있었다고 소급하지 않는 현행 표기도 적절하다.

2020 correction diff는 이 같은 environment.yml을 고치며, PR 본문은 문서 빌드라는 구체적 용도를 직접 설명한다. import만 성공하는지 또는 패키지 이름이 유지되는지만 보면 이번 문제를 놓친다는 해석은 원문에 맞는다. 그러나 모든 NumPy 사용이 부적합했다는 뜻은 아니다.

### 유지해야 하는 제한

- **2019 Python3.7과 2020 Python=3은 다르다.** 과거 고정판에3.7이 명시됐다는 사실로 2020 실패 artifact를 py37로 확정하면 안 된다. 재열람한 correction diff 자체가 Python=3을 보여 준다.
- Linux CPython3.6/3.7/3.8 artifact upload 시각은 공개 공급 후보의 기록이다. 실제 실패 CI가 어떤 minor/build/channel을 골랐는지 확인되지 않았다. 따라서 5.27–5.32시간 산술은 조건부 metadata 계산이며, 확정 Tu→Tc 지연이 아니다.
- C04 `To`는 처음 찾아낸 직접 실패 보고다. 최초 발생 시각/최초 피해자 시각을 증명하지 않는다.
- `Tr`의 rc0 source-release 후보, 뒤 stable source에 pin이 포함됐다는 사실, 실제 dev-docs 서버 배포는 서로 다르다. 현재 chain의 `strict_ordered_five_point_complete=false`, `latency_eligible=false`, 실제 배포 미확인은 적절하다.
- PR/commit 원문과 수집 원장에서 “첫 성공 CI”가 확인되지 않았으므로 정정 효과나 피해 감소량은 미확인이다.

원문에 부합하지 않는 C04의 확정 인과·실제 지연 주장은, 검토한 collector 세 파일의 제한 문구를 포함해 읽는 범위에서는 발견하지 못했다. 최종 표가 이 제한을 삭제하면 같은 판단을 유지할 수 없다.

## C06 · 보고 순서·허용 범위·배포

직접 보고는2022-04-29이고, 수집 원장의 상류 source 수정은2022-05-20, 기록한0.3.0 rollout은05-24~05-29다. 따라서 이번 관측은 “새 upstream 배포가 하류를 처음 망가뜨렸다”는 순서가 아니다. 기존 의존성 문제가 보고되고 upstream이 수정한 뒤 소비자 최소판이 정리되는 사슬로 읽어야 한다. 이 순서 차이를 chain에 보존한 것은 타당하다.

새 하한은0.3.0 미만을 차단하지만 옛>=0.1.7 범위도0.3.0을 포함한다. 최소판 변경 이전에도 resolver가 새 artifact를 골랐다면 수정된 metadata를 받을 수 있었으므로, 소비자 commit 날짜가 모든 사용자의 최초 정상화 날짜라는 결론은 성립하지 않는다. 반대로 해당 commit 뒤라도 정확한 architecture/build와 실제 실행을 읽지 않았으므로 GUI 성공을 확인했다고 할 수 없다.

verdict가 macOS editable launch와 별도 plugin 검사 보고로 범위를 제한한 점은 적절하다. 이번 재열람은 그 중 **editable launch 보고**를 직접 확인했으며, plugin issue 원문은 재열람하지 않았다. 둘을 같은 기능의 독립 실패자로 중복 합산하면 안 된다. Python 파일 열기 등록의 source 목적과 앱 시작 단계 의존성 실패도 구별해야 한다.

v5.3.2 source에 새 하한이 들어 있다는 연결은 수집 원장에 기록돼 있다. 이번 별도 판독에서 release archive/installer를 직접 열지는 않았다. 따라서 source commit→공개 source-release 시각의 산술을 실제 conda package·GUI installer 배포 또는 첫 정상 실행 지연으로 일반화할 수 없다. collector가 그 범위를 미확인으로 둔 것은 유지해야 한다.

## C01/C02 · 경로 이행에 대한 별도 일관성 점검

이 두 행은 `chains`, `verdicts`, source rows C-F08/C-F10/C-F58, 공개 path 추적 기록의 대응을 읽었다. **위4묶음의 직접 외부 재열람에는 포함하지 않았다.** 따라서 아래는 수집 원장의 경로·판정 일관성 점검이며 해당 diff를 독립적으로 다시 확인했다는 주장은 아니다.

| 행 | 기록한 경로 이행 | 판독 판단 | 남은 한계 |
| --- | --- | --- | --- |
| C01 | AppVeyor environment.yaml 삭제 → GitHub Actions가 environment-3.6.yaml을 참조. 새 파일은 원래 Travis 경로에서 옮겨 온 것으로 기록 | workflow replacement를 옛파일의 단순 Git rename이라고 부르지 않은 것이 맞다. Python3.6 시험 목적의 source 유지와 뒤 지원 정책 변경을 상류 식별자 정정과 구별한다. | 실제 AppVeyor/Actions solve·성공은 미확인. “경로 삭제=미수정” 또는 “같은 Python 이름=실제실행유지”로 요약하면 안 됨. |
| C02 | docs/environment.yml → pip requirements.txt → 다시 conda environment.yml | 같은 Sphinx 문서 목적을 유지해도 공급 경로는 바뀌었다는 판정이 맞다. 창 끝의 동일 패키지명만으로 중간 상태가 불변이었다고 하지 않은 점이 적절하다. | RTD 렌더링·배포 성공을 뜻하지 않음. 이후 복귀는 공급자 identifier 정정으로 확인되지 않았으므로 corrective latency로 세면 안 됨. |

C02 복귀 기록은 source row C-F58에 정확한2020-10-19T21:28:18Z가 있고 chain에는 날짜 정밀도만 보존돼 있다. 날짜 정밀도 표기가 있으므로 오류는 아니며, 최종 표에서 정확 시각이 필요하면 같은 source row를 사용하면 된다.

## 통합 시 필요한 처리

1. **필수 수정**: C06 upstream의 metadata “보장” 문구를 version floor와 검토한 recipe 범위로 축소한다. 실제 solve·실행 보장은 미확인으로 유지한다.
2. **필수 유지 조건**: C04/C06의 artifact/exposure 불명, Tu→Tc 부적격, source-release와 실제 CI/GUI 배포의 구별, 전체 strict-chain 미완성을 최종 표·계산 파일에도 전달한다. source release 시각이 있는 셀에는 그 종류를 표시한다.
3. **검토 범위 표시**: C04/C06은 직접 원문 재판독, C01/C02는 원장 일관성 점검이라는 차이를 유지한다. 이 리뷰를 외부 독립 검토나 전체 12행 실행 재현으로 부르지 않는다.

현재 남은 최소 보강은 C04의2020-07-16 정확한 conda explicit list와 첫 성공 docs 배포 기록, C06의 실패한 Python3.10/CPU/build 및 첫 정상0.3.0 실행 기록이다. 이 자료가 없으면 관측 상태 자체를 보류 사슬의 결론으로 인계하는 것이 맞다.

