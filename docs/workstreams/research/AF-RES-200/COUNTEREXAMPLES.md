# 반례 및 타 분야 대조 (04)

## 반례 찾기와 보정 이력
- 초기 가설: 전체 판이 철회되면 모든 파일/OS에서 같은 실행 위험. 반증: [D01 PyPI 3.9.1 banner](https://pypi.org/project/matplotlib/3.9.1/)는 남은 source/macOS/manylinux가 작동한다는 유지자 판단과 downstream packager에게 yank하지 말라는 요청을 포함한다. [M01 issue](https://github.com/matplotlib/matplotlib/issues/28551)와 [C01](https://github.com/contourpy/contourpy/pull/406) Windows 관측은 전체 환경 고장 증거가 아니다. 수정: release eligibility, per-file availability, affected runtime condition을 독립 필드로 관리. musllinux는 목록에 있지만 사유에서 정상으로 명시하지 않아 미확인.
- 초기 가설: exact pin이면 언제나 과거판 설치 가능. 반증: Windows official wheel은 삭제됨; [R01 PEP 592](https://peps.python.org/pep-0592/)는 installer가 모든 yanked 후보를 거부할 재량을 허용하며, mirror가 파일을 누락할 수도 있다. [R06 24.0 factory](https://github.com/pypa/pip/blob/24.0/src/pip/_internal/resolution/resolvelib/factory.py#L304-L325) all_yanked and pinned는 resolver 후보가 있는 조건에서만 의미. [R07 tests](https://github.com/pypa/pip/blob/24.0/tests/functional/test_install.py#L2176-L2288) unpinned, exact, all-yanked error의 별도 시험 코드(미실행). 수정: pin, 호환 태그, 실제 artifact 가용성, 인덱스/설치기 정책을 각각 확인.
- 초기 가설: successor가 원판과 동일한 문제를 모두 고친다. 반증: [M03 #12069](https://github.com/pytest-dev/pytest/issues/12069) Mar10 bwoodsend와 nicoddemus 답변은 private call_runtest_hook이 복구되지 않았다고 명시; M04는 두 deprecated path API만 복구했다. 수정: 8.1.1은 그 두 제거에 대한 수정 후보, 다른 내부 API는 별도; 3.9.1.post1은 Windows wheels 재등장과 날짜로 연결하되 실질 수리 확인은 보류. [R04](https://packaging.python.org/en/latest/specifications/version-specifiers/)에 의해 3.9.1.post1은 3.9.1 exact를 만족하지 않음.
- 초기 가설: 철회 뒤 아무도 원판을 쓰지 못하거나 사용하면 안 된다. 반증: M03 2024-03-09 nicoddemus의 exact wheel 설치 transcript(캐시 사용 포함)와 edgarrmondragon의 Poetry lock 보고(동일 thread), Mar10 bluetech가 plugin 호환 확인용 철회판 테스트를 권하는 사례. 수정: 설치 성공/현재 runtime 성공/새 추천을 분리. 실제 pip/Poetry 버전 및 기존 lock 파일 내역은 미확인.
- 날짜 보정: notices N15 구값 "2024-03 thread; exact day 미확인" → 2024-03-09, nicoddemus (M03 #19). N18 구값 미확인 → 2024-06-28 reference event (M03 #30, C04 actual diff; author timestamp는 미확인). 첫 flag 시각으로 소급하지 않음. source R07 추가로 F09 실패를 대체하되 실패 행 보존.
- 초기 가설: 오래된 원문이 살아 있으면 지금도 같은 용도로 추천 가능. 반증: [X04 PLOS original](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0237597)와 [X05 retraction](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0311387) 별 DOI/명시적 철회. [X06 original](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0291840)와 [X07 correction](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0313792)는 특정 figure/data/문장 수정이며 전체 결론을 여전히 지지한다는 편집자 평가. 원문 abstract와 correction 내용은 같이 읽어야 함. 수정: 원 객체 ID와 notice relation을 보존하고 목적별 영향 판단. 원문 존속 자체가 권고 유효성은 아님.

## 관점별 비용
배포 관리자: R05 whole-release UI와 D01 소스 fallback 문제; 파일만 삭제할 때의 의도하지 않은 파급. 설치기 제작자: R01, R06, R07; reproducibility와 fresh selection의 충돌 및 호환 파일 부재. 특정 OS 사용자: C01/C02는 Windows, C03은 Ubuntu에서 플러그인 훅 검증 문제; 동일 yanked flag로 위험 정도를 계산할 수 없음. 기존 환경 설명자: 당시 버전/파일/hash(아는 경우)와 지금 status를 나란히, 바꾸지 말 것. 편집자: X01/X02/X03은 원문에 상태/공지 링크 유지, 별 notice 식별자. X04/X05는 철회 후 계속 제공; X06/X07 정정 후 원문 일부 주장 수정. 전자는 새 설치 후보 배제와 비슷하나 학술 논문은 해석·인용 신뢰 문제이며 설치 프로그램은 resolution policy와 플랫폼별 코드/bytes 실행이라는 차이가 있다.

[Crossmark policy X01](https://www.crossref.org/services/crossmark/), [X02 registration](https://www.crossref.org/documentation/register-maintain-records/maintaining-your-metadata/registering-updates/), [X03 PLOS policy](https://journals.plos.org/plosone/s/corrections-expressions-of-concern-and-retractions)는 규칙, 두 실제 출판 계보는 관측. Crossmark 로고만으로 개별 레코드 최신성 보증하지 않으며, 철회→대체 DOI를 무조건 가정하지 않는다. 타 분야 전이 가능: notice linkage, event date, scope, preserved object. 전이 불가: paper status가 pip resolution/run outcome을 정한다는 주장.

## 재조합 대안
1. Release-only badge: 저비용/HTML로도 가능, 신규 범위 요청에서 적합; OS 과경고와 fixed historical 혼동. 
2. File-level index plus conditional notice: index file metadata와 affected context를 분리, 정확한 대상 가능하나 파일 수와 index recheck 비용 증가. raw API 미확인이라 본 과제에서 완결 구현/평가 불가.
3. Purpose-aware routing: first link는 역사적 원판 또는 지원 가능한 후보, notice companion 제공. 환경/핀 입력이 없으면 특정 수정판을 강제하지 말고 "환경/제약 미확인"으로 보류. release-only 신호와 조합 가능.
4. 시점 이력: checked_at, uploaded_at, yank observed date, observed notice date, deleted file, supersession relation의 분리. 현재 관측을 과거 이력에 복사하지 않음. 추가 비용은 조회·저장·재검증 횟수, 이 과제는 비용 실측 없음.

반례 검토는 자체 검토이며 독립 리뷰/새 설치·벤치마크 없음. F01–F08 raw flag 접근 한계 유지.
