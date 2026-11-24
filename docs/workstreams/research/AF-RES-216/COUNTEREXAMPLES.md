# AF-RES-216 반례와 정정

## 먼저 고친 판단

| 대상 | 이전 값과 출처 | 검산 후 값과 적용 조건 |
| --- | --- | --- |
| 두 대상판 파일 표시 | B01·B04 파일 원값 0/88. 배너로 릴리스 상태만 확인 | 88/88 파일 원값. V02/I01 24개, V05/I02 2개가 같은 사유로 철회됐고 인접 62개는 명시적 false. 현재판 카드와 파일표도 일치. [파일 조인](files.csv) |
| 3.9.1 Windows 삭제 집단 | B01 D01/N07에 당시 이름·수·시각 미확인 | 유지자가 2024-08-04T00:55:14Z에 삭제를 이미 보고했고 01:05:41Z 댓글에서 5개 이름·해시를 열거했다. 세 현 표면에서 그 다섯 이름이 없다. 정확한 삭제 이벤트 UTC와 당시 파일별 철회 플래그는 미확인. C03에 CPython 3.12 이름 하나의 당시 다운로드·설치 로그도 있다. [M01 삭제 공지](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1#issuecomment-2267223102) · [M01 열거](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1#issuecomment-2267225291) · [C03 L385–418](https://github.com/PyO3/maturin/issues/2141) · [삭제 파일 표](history-deleted.csv) |
| 배너 날짜와 최초 관측 | B02/N08과 N14에 날짜만, N15에 캐시 경고 날짜 | H02/H05의 현재 Key dates가 각각 2024-08-05T01:44:21+0000 및 2024-03-04T15:13:02+0000을 담는다. 별도 결정 댓글은 같은 날 각각 01:43:21Z 및 15:12:02Z였다. P 캐시 경고를 담은 댓글 작성 UTC는 2024-03-09T21:51:30Z다. 첫 API 전파·로그 발생 순간은 미확인이다. [M01 결정](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1#issuecomment-2268018494) · [M02 결정](https://github.com/pytest-dev/pytest/issues/12069#issuecomment-1976808605) · [M02 경고](https://github.com/pytest-dev/pytest/issues/12069#issuecomment-1986989847) |
| post1 수정 | B04와 N09는 후판 제공과 수정 목적·성공 근거 결손을 남김 | M03의 수정 목적, M05에서 인용 자료만 바뀐 소스 태그 diff, M01의 새 wheel과 양립 가능한 조합 및 여전히 실패한 조합을 확보했다. 전달할 표현은 Windows wheel 재빌드 후속판과 조건부 호환이다. DLL 조합 가설 M06의 추가 확인은 원 빌드 로그 F02 및 후속 로그 F03·F04 접근 실패로 남는다. [M03 tag](https://github.com/matplotlib/matplotlib/releases/tag/v3.9.1.post1) · [M05 diff L1,43,57](https://github.com/matplotlib/matplotlib/compare/44be14cc3a866e28a9ad22f36abfe8c0623cc6ac...9c9792a66900de7740fa6428f7fe59edb5083c60.diff) · [M01 post1 비교](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1#issuecomment-2273144251) · [M06 L163–191](https://github.com/adang1345/delvewheel/issues/52) |

## 실제 반례

- 현재 4개 인접판 HTML도 페이지의 릴리스 이력에 대상판 Yanked 카드를 담는다. 해당 판의 h1·상단 배너·`release--current`를 함께 읽어서 키워드 검색의 오탐 4개를 피했다. 판별기가 해당 네 판에도 철회 경고를 붙이면 현재 카드 위치를 다시 검토한다. [H01·H03·H04·H06 원응답](receipts/html/http.json)
- 3.9.1의 sdist, macOS 및 manylinux도 인덱스에서 철회 표시를 받는다. 유지자 사유는 Windows 출시 wheel의 조건부 세그폴트와 삭제 뒤 소스 빌드 경로를 구분한다. 소스 빌드 자체가 성공했던 로컬 대조와 실패한 CI도 있다. 원래 파일 설명에는 공급 계보와 환경 경고를 둔다. musllinux 동작은 미확인이다. [H02 배너 L346–355](https://pypi.org/project/matplotlib/3.9.1/) · [M01 원문 L215–227, L480–552](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1)
- post1은 Windows wheel을 제공하지만 8월 7일 nightly ContourPy wheel과 함께 실행한 시험에서는 성공, ContourPy 자체 빌드와 BertJorissen의 별도 프로그램에서는 실패가 보고됐다. DLL 이름 때문에 더 오래된 번들 DLL이 로드된다는 M06 가설을 해당 조합에서 검증할 근거가 필요하다. [M01 L1032–1073](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1) · [M06 L163–191](https://github.com/adang1345/delvewheel/issues/52)
- pytest 설치 로그는 당시 캐시 wheel의 경고·성공을 보인다. 같은 릴리스의 ixmp 플러그인은 Ubuntu에서 hook 검증에 실패했다. 8.1.1에서 되돌린 것은 두 공개 변경이고 사용자 기록에서 내부 `call_runtest_hook` 의존은 여전히 문제다. 설치 성공이나 비철회만으로 런타임 대체를 결정하면 경고가 빠진다. [M02 L349–401, L447–478](https://github.com/pytest-dev/pytest/issues/12069) · [C01 L455–475](https://github.com/pytest-dev/pytest/issues/12061) · [M04 L66–80](https://docs.pytest.org/en/8.1.x/changelog.html#pytest-8-1-1-2024-03-08)
- PyPI 배너의 최신판 제안은 3.11.2와 9.2.0이었다. 예시의 `>=3.9,<3.10` 및 `>=8,<9`는 각 제안을 배제한다. 탐색기는 링크를 유지하면서 실제 범위에 맞는 별도 후보를 제공할 수 있다. [H02 배너 L353](https://pypi.org/project/matplotlib/3.9.1/) · [H05 배너 L353](https://pypi.org/project/pytest/8.1.0/) · [R07 매칭 L546–562](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-matching)

## 합성 입력과 추가 확인

`controls.json`은 연구자 작성 두 시나리오다. 타입 9개 사례의 기대를 먼저 명시하고, digest/태그 충돌, JSON만·Simple만, 원목록 양쪽 부재, 신규, 동일 파일명의 잘못된 버전, 중복, 한쪽 취득 실패를 추가했다. 정확 키 집합과 범위 밖 post1 유사 이름 제외도 비교했다. 총 20/20 비교가 일치했다. [합성 입력](controls.json) · [기대·실제 비교](receipts/controls-result.json) · [실행 기록](receipts/controls-run.json)

- 형을 검증하면 빈 문자열이 false로 내려가는 오판과 릴리스 `info.yanked`를 결측 파일에 복사하는 오판을 피한다.
- 잘못된 판의 정확히 같은 filename은 별도 키로 남는다. 조인 결과에 `filename_identity_mismatch`가 있고 원래 버전의 JSON 누락도 유지된다.
- 읽기에 실패한 API와 파일 목록이 비어 있는 API는 다른 관측이다. 두 쪽에서 읽지 못한 파일의 최신 삭제는 판정 보류다.
