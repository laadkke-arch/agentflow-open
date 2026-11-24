# 원자료 취득 및 선정 영수증

| 범위 | 입력 | 실행 및 도구판 | UTC | 종료 및 누락 |
| --- | --- | --- | --- | --- |
| 시작 계약 | 통합 `ff2302a9c02fe72eea915dc1612d1791d5c780ec`, 선행 `12eb394eff4c556b47925f791d8aa42d7b09d86a` | [SCOPE](../SCOPE.md)의 `python -m workbench.session start … --fetch`, Python 3.12.14, Git 2.52.0 | 2026-11-24 16:53:27Z | 0, 원격 확인 및 [계약 지문](../session.json) 기록. 이전 두 시도는 연구 시작 전 전진한 통합판을 반영 |
| 범위 원격 확인 | `0b545f949368c509fcec388b9952fdd1ebd02ed1` | `git ls-remote --heads origin work/research-af-res-157`, GitHub connector SHA 파일 열기 | 16:54–16:55Z | 0 / 읽기 성공. `SCOPE.md` blob `001daa044b9c0c6698fc05b30e052da51063c1fd` |
| Sketchy 목록·README | `brownhci/sketchy-1.0` master, `f01bb57fbc7f5f14b6bd057b01221f5c3618f69e` | `git clone --depth 1 --single-branch --branch master https://github.com/brownhci/sketchy-1.0.git sketchy`, `git ls-tree -lr HEAD data` | 16:55:22–16:55:24Z | 0. CSV blob `e2a18ceca7542a754ba2c039ad4c9ed33c921ac5`와 README blob `c89d7ed513afbf54c89720b220471802929f76c5`. 저자 코드 checkout에 별도 DB 없음 |
| Sketchy 정규 raw | [raw 고정 URL](https://raw.githubusercontent.com/brownhci/sketchy-1.0/f01bb57fbc7f5f14b6bd057b01221f5c3618f69e/data/pilot_data/sketchy_dec6_dec13_peeks_updated.csv) | `curl -fLsS --max-time 35`, curl 8.14.1, `sha256sum`, `git hash-object`, `cmp` | 16:55:57–16:56:00Z | 모두 0, HTTP 200, 15,062,721 B, 1.187371s 전송, 두 사본 `aec34f174ac350448b62a2223a859303ae496f99ba526775e027e914a4a1afbc`. 파일럿 헤더의 25열 확인 |
| 연결과 선행 원자료 규모 | 동일 CSV; 위 SHA-256과 고정 헤더 | `python docs/workstreams/research/AF-RES-157/replay/pilot.py /tmp/af-res-157/a03/pilot.csv` 및 동일 명령에 `--selection` | 17:00:43Z 관측 종료 | 둘 다 0. [전수 구조](pilot-metadata.json)와 [선정 봉인](../selection.csv). 비식별 숫자 키와 논리 행 위치만 이용. 필수 과제/시계/전후판 누락 |
| 외부 보관소 | [archive.csv](../archive.csv)의 A03–A23 | curl 8.14.1, 공개 web open/search, 기관 및 저자 경로. 명령 및 응답은 각 행 | 16:55:22–17:00:58Z | 셸의 미허용 호스트는 proxy 403 및 client exit 22. 웹의 timeout/403/content-size·404는 별도. 대체 논문·목록 확인, 해당 ZIP 및 OSF 전체 전송 0 |
| Desktop 확인 | Cambridge 정규 item UUID, shared Chromium | Cloud Desktop, Browser Use 시도 후 native Chromium 정보·스크린 확인 | 16:56–16:58Z | Browser Use could not read requirements. Native Chromium AT-SPI provider unavailable로 주소 탐색 완료 확인 불가. 독립 다운로드 성공 없음 |

공개 web 도구는 HTML 또는 PDF의 판독 범위와 접근 오류를 보고했다. 셸 종료와 별개다. 초 단위가 없는 도구에서 시작·종료 범위 안에 있는 열람은 원장 `checked_utc`를 관련 배치의 관측 시각으로 사용하며 요청별 HTTP 수신 시각은 얻지 못했다. 민감 정보가 있을 수 있는 Mongo 컬렉션은 복원·실행하지 않았다. 자료 추가 조사에서는 저자 공개 비식별 export인지 먼저 확인한다.

## 정확한 보관소 명령

아래 명령의 출력 위치는 저장소 바깥의 임시 폴더다. 실제 실행 시에는 [archive.csv](../archive.csv)의 URL마다 `curl -fLsS --max-time 35 --max-filesize 80000000 -w '%{http_code} %{size_download} %{time_total}\n' URL -o TEMPFILE`을 적용했다. 포워드 연결이 성립하지 않아 curl `http_code`가 `000`, 오류 본문은 HTTP proxy 403을 보고했다. DOI·REST·정규 화면에서 실제 bitstream UUID를 얻기 전의 레거시 URL은 별도 후보일 뿐이다.

재취득 시 Apollo item → 다운로드 링크 → 파일크기·SHA-256 → `python -m zipfile -l delftdata.zip` → `python -m zipfile -t delftdata.zip` 순서로 검사한다. ZIP 안 PDF는 작품 내용보다 페이지/과제 코드부터 확인한다. OSF에서는 node JSON, `/files/`, `/files/osfstorage/`, 분할 페이지 `links.next`, provider 및 개별 `links.download`에서 공개 파일을 따라간다. 파일 목록과 해시를 작게 남기고 본문은 반출하지 않는다.

## 입력 지문

```text
aec34f174ac350448b62a2223a859303ae496f99ba526775e027e914a4a1afbc  pilot CSV / 15062721 bytes
cc0c811effddb2ece5808ab6bf0ae80f3e98cbbca3d68f5ad26af911b9992554  Git data/README / 752 bytes
```
