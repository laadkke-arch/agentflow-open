# AF-RES-216 | PyPI 철회 배너와 파일 메타데이터

| 판·파일 | HTML 배너 | JSON 원 플래그·사유 | Simple 원 플래그·사유 | 지문·주소 | 차이·미확인 |
| --- | --- | --- | --- | --- | --- |
| matplotlib 3.9.0 / 29 | 현재판 없음 | `false` / `null` ×29 | `false` ×29 | [H01 현재판 L5773](https://pypi.org/project/matplotlib/3.9.0/) · [V01 `/urls/0..28`](https://pypi.org/pypi/matplotlib/3.9.0/json) `25285edc` · [I01 `/files/1881..1909`](https://pypi.org/simple/matplotlib/) `39beadba` | 의미 일치. 이력 카드에 3.9.1 철회 표시가 따로 있다. |
| matplotlib 3.9.1 / 24 | Yanked, Key dates `2024-08-05T01:44:21+0000` | `true` / 원문 M ×24 | 문자열 M ×24 | [H02 배너 L346–355·Key dates L578](https://pypi.org/project/matplotlib/3.9.1/) · [V02 `/urls/0..23`](https://pypi.org/pypi/matplotlib/3.9.1/json) `25033013` · [I01 `/files/1910..1933`](https://pypi.org/simple/matplotlib/) `39beadba` | 표시는 전체 일치. Windows wheel 0, 실제 고장 조건은 당시 원기록 참조. |
| matplotlib 3.9.1.post1 / 29 | 현재판 없음 | `false` / `null` ×29 | `false` ×29 | [H03 현재판 L5725](https://pypi.org/project/matplotlib/3.9.1.post1/) · [V03 `/urls/0..28`](https://pypi.org/pypi/matplotlib/3.9.1.post1/json) `f21cee1c` · [I01 `/files/1934..1962`](https://pypi.org/simple/matplotlib/) `39beadba` | 의미 일치. Windows wheel 5, 환경별 수정 범위는 당시 시험 참조. |
| pytest 8.0.2 / 2 | 현재판 없음 | `false` / `null` ×2 | `false` ×2 | [H04 현재판 L2185](https://pypi.org/project/pytest/8.0.2/) · [V04 `/urls/0..1`](https://pypi.org/pypi/pytest/8.0.2/json) `6221b3d5` · [I02 `/files/309..310`](https://pypi.org/simple/pytest/) `9f95351f` | 의미 일치. 이력 카드에 8.1.0 철회 표시가 따로 있다. |
| pytest 8.1.0 / 2 | Yanked, Key dates `2024-03-04T15:13:02+0000` | `true` / 원문 P ×2 | 문자열 P ×2 | [H05 배너 L346–355·Key dates L633](https://pypi.org/project/pytest/8.1.0/) · [V05 `/urls/0..1`](https://pypi.org/pypi/pytest/8.1.0/json) `ac505502` · [I02 `/files/311..312`](https://pypi.org/simple/pytest/) `9f95351f` | 두 사유 문자열이 정확히 같다. |
| pytest 8.1.1 / 2 | 현재판 없음 | `false` / `null` ×2 | `false` ×2 | [H06 현재판 L2122](https://pypi.org/project/pytest/8.1.1/) · [V06 `/urls/0..1`](https://pypi.org/pypi/pytest/8.1.1/json) `02fbc945` · [I02 `/files/313..314`](https://pypi.org/simple/pytest/) `9f95351f` | 의미 일치. 플러그인별 결과는 별도 근거가 필요하다. |
| matplotlib 3.9.1 / 삭제 집단 1 | 배너 사유에 Windows wheel 삭제 | 현재 해당 객체 부재 | 현재 해당 객체 부재 | [H02 배너 L346–355](https://pypi.org/project/matplotlib/3.9.1/) · [M01 삭제 목록 L441–468](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1) | 과거 삭제 5개는 현재 88개 분모 밖이다. 개별 삭제 이벤트 시각과 당시 API 플래그는 미확인. |

| 판·분모 | 양쪽 일치 | 한쪽만·신규·삭제 | 업로드 대 조회시각 | 역사적 근거 |
| --- | --- | --- | --- | --- |
| matplotlib 3.9.0 / 29 | 29 | 0·0·0 | 2024-05-15 23:37:04.927481–23:38:15.591949Z / [API V01](https://pypi.org/pypi/matplotlib/3.9.0/json) 2026-11-24 21:32 UTC | [M01 본문 L144–180](https://github.com/matplotlib/matplotlib/issues/28551) 비교 시험 |
| matplotlib 3.9.1 / 24 | 24 | 0·0·0 현존, 별도 집단 1 | 2024-07-04 07:15:25.890006–07:16:41.501768Z / [API V02](https://pypi.org/pypi/matplotlib/3.9.1/json) 2026-11-24 21:32 UTC | [M01 삭제·결정 L441–468, L702–721](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1) |
| matplotlib 3.9.1.post1 / 29 | 29 | 0·0·0 | 2024-08-06 22:00:11.114595–22:01:24.863361Z / [API V03](https://pypi.org/pypi/matplotlib/3.9.1.post1/json) 2026-11-24 21:32 UTC | [M03 tag L184–189](https://github.com/matplotlib/matplotlib/releases/tag/v3.9.1.post1) · [M01 시험 L1018–1073](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1) |
| pytest 8.0.2 / 2 | 2 | 0·0·0 | 2024-02-24 22:21:27.561174–22:21:30.762987Z / [API V04](https://pypi.org/pypi/pytest/8.0.2/json) 2026-11-24 21:32 UTC | [M04 8.0.2 L82–89](https://docs.pytest.org/en/8.1.x/changelog.html#pytest-8-0-2-2024-02-24) |
| pytest 8.1.0 / 2 | 2 | 0·0·0 | 2024-03-03 21:23:38.040582–21:23:43.502406Z / [API V05](https://pypi.org/pypi/pytest/8.1.0/json) 2026-11-24 21:32 UTC | [M02 결정·캐시 로그 L227–267, L349–401](https://github.com/pytest-dev/pytest/issues/12069) · [C01 환경 L455–475](https://github.com/pytest-dev/pytest/issues/12061) |
| pytest 8.1.1 / 2 | 2 | 0·0·0 | 2024-03-09 11:51:04.858193–11:51:08.012236Z / [API V06](https://pypi.org/pypi/pytest/8.1.1/json) 2026-11-24 21:32 UTC | [M04 문서 일자 03-08·복원 2항목 L11–15, L66–80](https://docs.pytest.org/en/8.1.x/changelog.html#pytest-8-1-1-2024-03-08) |
| 합계 / 기존 88, 현재 88 | 88 | 0·0·0, 역사 집단 1 | UTC API 21:32:16–18, HTML 21:32:40–43 | 첫 파일별 플래그 노출 시각 미확인 |

| 사용자 목적 | 유지·경고·대체·보류 | 직접 지지하는 파일 | 경쟁 설명·반례 |
| --- | --- | --- | --- |
| matplotlib 정확 재현 | 유지+경고, Windows wheel 필요 시 보류 | [V02 `/urls`](https://pypi.org/pypi/matplotlib/3.9.1/json) 중 sdist 포함 24 | 5개 삭제와 소스 대체 경로는 [M01 L441–552](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1) |
| matplotlib 신규 범위 | 태그·Python·범위 허용 시 대체 후보, 문제 조합은 보류 | [V03 `/urls`](https://pypi.org/pypi/matplotlib/3.9.1.post1/json) 중 Windows 5 | [M01 L1032–1073](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1)의 조건부 실패 |
| matplotlib 기설치 설명 | 당시 링크 유지, 날짜 있는 경고 | [V02 `/urls`](https://pypi.org/pypi/matplotlib/3.9.1/json) 또는 M01 삭제 해시 | [M01 L215–227](https://github.com/matplotlib/matplotlib/issues/28551?timeline_page=1) conda-forge 별도 계보 |
| pytest 정확 재현 | 유지+경고, 변경 시 명시적 핀 | [V05 `/urls`](https://pypi.org/pypi/pytest/8.1.0/json)의 wheel과 sdist | [M02 L349–401](https://github.com/pytest-dev/pytest/issues/12069) 캐시 wheel 성공과 [C01 L455–475](https://github.com/pytest-dev/pytest/issues/12061) hook 실패 |
| pytest 신규 범위 | 호환 시 대체 후보, 좁은 범위는 보류 | [V06 `/urls`](https://pypi.org/pypi/pytest/8.1.1/json)의 wheel과 sdist | [M02 L447–478](https://github.com/pytest-dev/pytest/issues/12069) 내부 API 의존 |
| pytest 기설치 설명 | 당시 링크와 플러그인 조건 유지 | [V05 `/urls`](https://pypi.org/pypi/pytest/8.1.0/json)의 wheel과 sdist | [M02 L349–401](https://github.com/pytest-dev/pytest/issues/12069) 설치 성공과 런타임의 별개 관측 |

위 지문은 응답 SHA-256 접두사다. 원문 M·P는 각 대상 파일의 `json_reason_raw`와 `simple_yanked_raw`에서 문자열 그대로 확인할 수 있다. HTML 비교는 고정판의 상단 배너와 현재 카드 구간을 사용했다. [files.csv](files.csv) · [API HTTP 기록](receipts/api/http.json) · [HTML HTTP 기록](receipts/html/http.json) · [1차 집계](receipts/reconciliation.json)
