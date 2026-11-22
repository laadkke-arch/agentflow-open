# AF-RES-027 · B·타 분야 별도 내부 판독

## 범위와 독립성

- 판독자: `/root/conda_a`. A의 conda-forge 수집을 맡았지만 이번 대상 B·타 분야 수집에는 참여하지 않았다.
- 이것은 **같은 표시 모델 안의 별도 내부 판독**이다. 외부 전문가 검토, 다른 모델의 독립 판독, 맹검 검토가 아니다.
- 대상: `collectors/homebrew-b`의 B-H02, `collectors/conda-b`의 B-C01–03, `collectors/cross`의 X-BIB01·X-LIB01. 원장·사례·한계를 읽고 중요 원문을 다시 열었다.
- 원문 재열람·검산일: **2026-11-22 UTC**. 판독 시 기존 결과 HEAD는 `17229e1bde153aaf29290dceae4dad9172fe987f`였다. 이 SHA의 B-C02 문구와 이후 통합 담당자가 고친 working tree를 별도로 비교했다.
- 본 판독자는 원수집 파일을 수정하지 않았다. 이 파일만 작성했다. 새로 읽은 동일 원문을 기존 최소 원문 수에 다시 더하지 않는다. MARC 005 설명서는 보조 확인이며 최소수에 산입하지 않는다.
- 패키지 설치, 과거 solver, CI 실행을 재현하지 않았다. 아래 재실행은 공개 레코드 바이트 확인과 날짜 뺄셈에 한정된다.

## 결론

**수정이 필요한 논리 오류 1건을 찾았으며, 통합 담당자가 수정한 working tree를 확인했다.** BC-S16의 최초 관측 상태만으로 이전 전환의 존재를 가정해 좌측 검열로 분류했던 문구다. 최종 수용은 수정된 통합 커밋과 원격 원문에서 재확인해야 한다.

나머지 사례에서는 주요 구분이 이미 기록되어 있다. 특히 B-C03의 보조 수리 구간을 원래 2022년 분리 사건의 정정 지연으로 합치지 않고, Harvard의 파일명·레코드 시각·미러 수정 시각을 구별한다. 다만 집계나 요약에서 이 조건이 탈락하면 결론이 바뀌므로 아래 보존 조건을 명시한다.

## 발견 사항과 필요한 처리

| ID·영향 | 확인한 위치·원문 | 판독 | 처리·수용 조건 |
| --- | --- | --- | --- |
| REV-F01 · 수정 필요, 검열 분모 영향 | 기존 HEAD의 `collectors/conda-b/cases.json`, B-C02.secondary_attempts[0]; BC-S16. [최초 수입 코드](https://github.com/conda/conda-libmamba-solver/blob/f93d38a190d912902ec90729304ea2936dd0976b/conda_libmamba_solver/solver.py), 1–4행·36행 | 기존 문구는 “Transition is left-censored, not observed post-split correction.”이었다. 그러나 첫 코드가 `libmambapy`를 쓰고 `mamba` import를 금한다는 사실만으로 이전 mamba 참조나 전환 사건의 존재가 성립하지 않는다. 처음부터 새 API로 작성됐을 가능성이 남는다. | “최초 관측부터 후계 API 사용; 이전 참조·전환 존재와 시점 미확인; 통계적 좌측 검열 산입 보류”로 수정. 05:45–05:47 UTC에 수정된 cases/source/notes를 읽었다. 선행 `conda/conda` 코드의 실제 옛 참조를 확보하기 전 좌측 검열 수에 넣지 않는다. 원수집자 또는 통합 담당자의 수정이며 본 판독자가 고친 것이 아니다. |
| REV-F02 · 범위 탈락 시 큰 오류, 현재 구분은 적절 | B-C03.consumer와 auxiliary_repair; BC-S20–27. [옛 test.sh](https://github.com/spyder-ide/qtpy/blob/b784f035bb9aad24f37614327d9f2c0d44166c19/.github/workflows/test.sh), 20·22행; [PR397](https://github.com/spyder-ide/qtpy/pull/397), 제목·본문 | 원래 참조에는 Qt 5.12 시험 경로가 있다. 12월 Python 3.11/PyQt 5.15 행의 실패·우회와 1월 수리는 같은 요구가 아니다. R2의 약 5.47시간은 2023년 해당 수리 업로드→소스 편집 간격이다. 2022년 분리→옛 5.12 목적 정정 지연으로 옮기면 단위가 바뀐다. | R1의 `dates_eligible_for_original_correction_delay=false`를 유지한다. R2는 한 B 탐색의 부수 사슬이며 새 B 시도나 A 성공을 늘리지 않는다. 약 75.09일의 끝점은 최초 확인한 **공개 소스 릴리스**이며 CI 실제 적용일로 쓰지 않는다. |
| REV-F03 · 독립성 범위 제한 | B-C03.independent_consumer_limit; [상류 수리 diff](https://github.com/conda-forge/qt-feedstock/commit/275058548203f5d3bdb563930d6ad8bee7c475e0), CODEOWNERS·recipe-maintainers; [PR235](https://github.com/conda-forge/qt-feedstock/pull/235)와 [PR397](https://github.com/spyder-ide/qtpy/pull/397) | 상류의 과거 maintainer 목록에는 ccordoba12가 있다. 소비자와 유지관리 계보가 겹친다는 제한은 타당하다. 다만 수리 PR235 작성자는 hmaarrfk이고 복귀 PR397 작성자는 CAM-Gerlach다. 유지관리자 겹침을 이 두 변경의 동일 작성자라는 주장으로 강화하면 안 된다. 같은 실패 보고가 상류 이슈에 재게시된 것도 두 독립 실패가 아니다. | “별도 소비자 프로젝트이나 인적 계보의 독립성은 보장되지 않음”을 유지한다. 봇 merge author, PR 작성자, 기존 maintainer 역할을 따로 쓴다. PR·커밋·원문·재게시 보고를 각각 독립 사건으로 세지 않는다. |
| REV-F04 · 시간·식별자 역할 범위 제한 | X-LIB01.consumer_snapshot_label / consumer_record_005 / mirror_file_modified; [고정 위치 레코드](https://openlibrary.org/show-records/harvard_bibliographic_metadata/20220215_017.bib.mrc:295257330:2338), 001·005·043·651·852; [MARC 005 공식 설명](https://www.loc.gov/marc/bibliographic/bd005.html) | `20220215`는 파일명 표기, `20020606163548.3`은 레코드 최신 transaction 시각, 2026-03-12는 현 미러 파일의 수정 시각이다. 005는 특정 651 필드의 변경일이 아니다. 현행 해시가 과거 2022년 공개 사실을 증명하지 않는다. | “2022 고정판”을 쓰면 “2022-02-15로 이름 붙은 덤프 파일의 현재 확인 바이트”라는 한계를 붙인다. 원래 공개 영수증·같은 001의 전후판 없이 소비자 정정일이나 1993→2022 지연을 계산하지 않는다. |
| REV-F05 · 직접 후계 관계 오독 방지 | X-LIB01.old_identifier / successors; [LC Bulletin 60](https://www.loc.gov/aba/publications/FreeCSB/CSB_060.pdf), 인쇄 2–4쪽 | 지리 코드 e-cs/e-xr/e-xo, name authority n90718759/n50075233, 역사 subject sh85035319는 역할과 ID 종류가 다르다. Bulletin은 시기·목록 역할별 사용 규칙을 뒷받침한다. sh85035319가 두 name authority ID로 직접 분리됐다는 관계나 그 URI가 1993년 전부터 연속 보존됐다는 사실은 확인되지 않았다. | “옛 지리 범위를 보존한 표현이 이 책의 주제에 맞음”으로 한정한다. 서로 다른 namespace 사이의 직접 replacement edge를 만들지 않는다. 구체 subject URI의 생성·변경 이력은 별도 미확인으로 유지한다. |

## 직접 재열람한 중요 원문

아래 확인일은 모두 2026-11-22 UTC다. 각 원문의 같은 커밋 렌더링·API·본문을 재확인한 것이며 새 사건 수가 아니다.

| 판독 근거 ID | 원문·정확한 위치 | 재확인한 내용 | 한계 |
| --- | --- | --- | --- |
| REV-O01 / BC-S16 | [solver.py@f93d38a](https://github.com/conda/conda-libmamba-solver/blob/f93d38a190d912902ec90729304ea2936dd0976b/conda_libmamba_solver/solver.py), 모듈 설명 1–4행·import 36행 | 최초 확인 코드는 libmambapy API를 사용한다. mamba를 import하지 말라는 역할 구분이 있다. | 선행 코드와 옛 참조를 읽지 못했으므로 API “전환”은 미확인이다. |
| REV-O02 / BC-S20 | [QtPy test.sh@b784f03](https://github.com/spyder-ide/qtpy/blob/b784f035bb9aad24f37614327d9f2c0d44166c19/.github/workflows/test.sh), 14·20·22·61행; 같은 판 ci.yml의 conda-forge 설정 | 당시 CI의 Python 입력과 Qt 기본값 5.12, PyQt/PySide 분기, pytest 호출이 확인된다. | 파일에 설치 명령이 있다는 사실은 실행 성공이나 실제 선택한 배포 빌드를 보장하지 않는다. |
| REV-O03 / BC-S24 | [qt-feedstock 수리 2750585](https://github.com/conda-forge/qt-feedstock/commit/275058548203f5d3bdb563930d6ad8bee7c475e0), recipe/meta.yaml의 version·requirements.run 전후 diff | qt 버전 5.15.4→5.15.6, qt-main 버전 연동, qt-webengine을 동일 세부 버전에서 5.15 계열로 완화한 수정이다. | recipe 병합 시각만으로 패키지 업로드나 소비자 실행 시각을 대체할 수 없다. |
| REV-O04 / BC-S26 | [QtPy PR397](https://github.com/spyder-ide/qtpy/pull/397), 제목·본문·created_at·merged_at·merge_commit_sha | 소비자가 이전 우회의 후속임을 밝히고 상류 issue234/PR235를 이유로 제거한다. 작성자 CAM-Gerlach, 생성 2023-01-12 21:06:16Z, 병합 2023-01-13 15:33:04Z다. | 이 PR은 2023년 수리 사슬의 근거다. 2022년 원래 5.12 목적의 실패 증거가 아니다. |
| REV-O05 / X-S01–03 | [PLOS 정정 공지](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0165166), Notice of Republication·Supporting Information·Reference; [실제 후속 PeerJ PDF](https://jevinwest.org/papers/Piwowar2018peerj.pdf), 인쇄 5쪽의 Ottaviani 논의·22쪽의 해당 참고문헌 | 정정 공지의 공표는 2016-10-21, 공지가 말하는 재발행은 2016-09-06이다. 소비자는 연구 결과를 인용하며 연구 DOI .0159614를 사용한다. | 이번 재열람도 S1/S2 PDF 바이트 전후 비교를 완성하지 못했다. 후속 인용의 최초 삽입일·변경일이나 공지를 읽었다는 사실은 미확인이다. |
| REV-O06 / X-S04 | [LC Bulletin 60 PDF](https://www.loc.gov/aba/publications/FreeCSB/CSB_060.pdf), 인쇄 2쪽 descriptive heading, 3쪽 subject practice, 4쪽 geographic area codes | 옛 국가 전체의 역사적 범위와 현재 국가·지역 세분의 범위를 구별한다. Slovak Republic (Czechoslovakia)는 descriptive 사용과 subject 사용의 허용 범위가 다르다. e-cs도 옛 전체 범위를 위해 유지한다. | 1993-05-24는 해당 code 시행 근거다. 모든 표목과 subject URI의 정확한 시행일로 일반화할 수 없다. |
| REV-O07 / X-S05·보조 | [Harvard 레코드 렌더링](https://openlibrary.org/show-records/harvard_bibliographic_metadata/20220215_017.bib.mrc:295257330:2338), 001·005·043·245·260·505·651·852·876; [MARC 005](https://www.loc.gov/marc/bibliographic/bd005.html), Field Definition and Scope | 1968년 책의 1938/1968 역사 주제와 e-cs, 실제 WID 소장 정보를 확인했다. 005의 의미는 레코드 transaction이지 subject 수정일이 아니다. | 동일 URI의 과거 생성·수정 이력과 2022년 최초 공개 영수증을 제공하지 않는다. LC·UKM·Harvard의 공유 목록 계보를 독립 인적 검증으로 세지 않는다. |
| REV-O08 / X-S12 | [IA 공개 manifest](https://archive.org/metadata/harvard_bibliographic_metadata)와 [원래 MARC 파일](https://archive.org/download/harvard_bibliographic_metadata/20220215_017.bib.mrc), 파일 항목·HTTP Range 295257330–295259667 | 05:46:16.998649Z에 manifest를, 05:46:34.275771Z에 2,338바이트를 다시 받았다. 아래 영수증이 기존 수집값과 일치한다. | 전체 357,206,833바이트 파일의 MD5/SHA1을 직접 다시 계산한 것은 아니다. manifest와 현 레코드 해시는 과거 공개 시각을 검증하지 않는다. |

## 표집·중복·목적 유지 판정

| 대상 | 별도 판독 결과 | 집계에 남겨야 할 제한 |
| --- | --- | --- |
| B-H02 · Borg/Python | 원장의 Python 기본 minor 이동과 Borg의 Python 최소 버전 목적을 구별한 판정은 타당하다. 후속 Borg cask/formula·FUSE 수정은 같은 Python 참조의 정정으로 세지 않는다. | 공식 시행일이 없으므로 source committer+365를 **임시 확인 범위**로만 유지한다. 이를 정식 365일 창이나 우측 검열로 바꾸지 않는다. 버전 하한을 만족한다는 추론과 실제 Borg 설치 성공은 다르다. |
| B-C01 · Xarray/Matplotlib | 2019년 선택 사건은 recipe 최상위 이름 정리이며 소비자가 부르는 출력명은 유지된다. 범위 밖 2018년 실제 분리로 사건을 교체하지 않았다. 문서 환경에서 직접 참조가 없어지는 일과 2020년 시험 환경에서 matplotlib-base로 바뀌는 일도 분리했다. | 문서 참조 폐기는 경쟁하는 참조 변화다. 실제 설치된 간접 의존성이 미확인이므로 “계속 유지”나 “오류 정정”으로 채우지 않는다. 문서 목적을 테스트 목적으로 바꾸어 시간 쌍을 만들지 않는다. |
| B-C02 · Snakemake/Mamba | CLI 산출물 유지와 라이브러리 분리를 나누는 해석은 타당하다. 최초 공개 소비자 릴리스가 같은 명령을 유지해도 실제 모든 플랫폼 실행 성공은 확인되지 않는다. | API 보조 소비자의 이전 참조는 미확인이다. REV-F01 수정 후 이 보조 관측을 좌측 검열 숫자나 독립 B 시도로 추가하지 않는다. |
| B-C03 · QtPy/Qt | 옛 버전 시험·새 Python 시험·수리 후 기존 이름 복귀를 세 수준으로 나눈 현재 원장이 적절하다. 소스 ancestry에 우회 커밋이 있어도 중간 공개 태그에 우회 코드가 실제 실렸다는 뜻은 아니다. | R1/R2 범위와 소스 편집/병합/소스 릴리스/실제 CI 적용을 분리한다. R2의 계산 가능성이 R1 완전 사슬을 만들지 않는다. 동일 보고자·공통 유지관리 계보도 보존한다. |
| X-BIB01 · PLOS/PeerJ | 연구 결과를 지시하는 인용에는 연구 DOI를 계속 쓰는 것이 맞을 수 있다. 정정 공지 DOI는 공지 자체의 식별자다. 이 사례는 자동 교체에 대한 조건부 반례가 된다. | 2018년 인용은 2016년 공지 이후의 관측이다. 이전 소비자 판이 없으므로 수정 시점이나 전달 지연의 양 끝이 아니다. 연구의 모든 본문·결론이 전후 동일하다는 검증도 아니다. |
| X-LIB01 · LC/Harvard | 1938/1968 역사 책을 찾는 목적에는 옛 지리 범위가 적절하다. 한 현 국가로 치환하면 범위를 줄일 수 있다. | 특정 URI의 지속 보존 이력까지 입증한 것은 아니다. 책 출판연도·국가 분리일·code 시행일·MARC 005·덤프 파일명·미러 시각을 따로 유지한다. |

이 판독은 B-H01·H03 전체를 다시 조사하지 않았다. 전체 B의 6회 시도 완료 여부는 통합 원장이 검산한다. 본 판독 범위의 B 4건, 보조 관측, 타 분야 2쌍 중 어느 것도 A의 참조 수·성공 수·전파율에 추가해서는 안 된다. 원문 재열람 수와 독립 사건 수 역시 따로 센다.

## 실행 영수증과 숫자 검산

### Harvard 레코드 재확인

2026-11-22 05:46:34.275771 UTC의 직접 HTTP 응답:

```text
status: 206
Content-Range: bytes 295257330-295259667/357206833
retrieved_bytes: 2338
record_sha256: 6ce2142a32f7fe98f815cc62de767efdf6312571da20814c65a1fb6170d5e4e6
manifest file: 20220215_017.bib.mrc
manifest mtime: 1773287290 = 2026-03-12T03:48:10Z
manifest md5: b2ebb2d2a54b9e48589e8e5f459920e3
manifest sha1: 34e06a9a1c3cbdc680bc23819574955297f47abb
```

이 일치는 **현재 공개 레코드 바이트의 재현 확인**이다. 전체 덤프 해시의 재계산, 2022년 공개 증명, 2002년 특정 주제 수정 증명이 아니다.

### B-C03-R2 산술

UTC ISO 시각을 Python `datetime.fromisoformat`으로 파싱해 뺄셈을 재실행했다.

| 시작 → 끝 | 재계산 초 | 허용되는 해석 |
| --- | ---: | --- |
| 2023-01-12 15:27:37.161 → 20:55:58 | 19,700.839 | 선택 Linux wrapper 수정 업로드 기록→복귀 소스 편집 |
| 같은 업로드 → 2023-01-13 15:33:04 | 86,726.839 | 업로드 기록→기본 브랜치 병합 |
| 2023-01-12 20:55:58 → 2023-03-28 23:06:05 | 6,487,807 | 복귀 소스 편집→최초 확인한 공개 소스 릴리스 |

산술은 일치한다. 재계산은 날짜 출처의 완전성이나 해당 빌드가 CI에서 선택됐다는 사실을 추가 검증하지 않는다. 실제 사용자 피해와 수정 효과는 보고된 개발 CI 범위를 넘어 확장하지 않는다.

## 통합 담당자에게 남기는 최소 후속 확인

1. REV-F01 문구 수정과 좌측 검열 집계 제외가 같은 통합 커밋에 들어갔는지 확인하고, 원격 SHA의 cases/source/notes 및 최종 집계에서 다시 읽는다. API 전환을 다시 주장하려면 `conda/conda` 선행 코드의 같은 목적 옛 mamba 참조와 첫 libmambapy 참조를 불변판으로 확보한다.
2. B-C03-R2의 모든 숫자에 보조 참조 ID·2023년 수리·선택 플랫폼·소스 끝점을 붙인다. 2022년 5.12 시험 실패나 실제 CI 적용을 입증하려면 원래 Actions run 3718737526/job 6307127310의 보존 로그와 당시 repodata가 필요하다.
3. X-LIB01을 요약할 때 ID 종류와 날짜 역할을 유지한다. 실제 수정 전파를 묻는 다음 조사는 같은 001의 더 이른 고정판과 원 배포자의 공개 영수증 한 쌍이다. 현재 바이트를 다시 확인하는 것만으로 이 빈칸은 채워지지 않는다.

