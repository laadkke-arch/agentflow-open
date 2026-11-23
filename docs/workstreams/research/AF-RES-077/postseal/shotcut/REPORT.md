# Shotcut 사후 검산 — B 봉인 뒤 공개

대상은 `v20.09.13@0898bdf3fc0f9f3fbf78336bad21d5506e19c118`. 요청은 [#910](https://github.com/mltframework/shotcut/issues/910), 보조층이다. 여기서 확인한 결과를 A/B 판독자에게 소급 제공하지 않았다.

## 원 보고와 실제 결말

11개 공개 댓글과 전체 반환 timeline을 읽었다. 작성자 johnnydepup는 같은 길이·이름의 낮은 해상도 영상으로 바꿨다고 설명했다. ddennedy는 탐색/시작 시점/스트림 순서 가능성을 차례로 제시하고 Timeline Replace 및 XML의 audio_index/video_index 제거를 제안했다. 작성자는 마지막 [699527361](https://github.com/mltframework/shotcut/issues/910#issuecomment-699527361)에서도 검은 영상이 지속된다고 답했다. 종료 이벤트는 2020-09-26T07:44:43Z이며, 닫힘을 재현 성공이나 수정 배포로 간주하지 않는다. 직접 읽은 댓글에는 재현 영상/프로젝트 첨부, 실행 가능한 원시험, 성공 출력이나 연결 PR이 없다.

이 결과는 프록시 연결 오류가 원인이었다는 확인이 아니다. 스트림 인덱스/시간축 등 다른 원인이 제안됐고, 실제 원인은 미확인이다. 저자가 약 두 시간의 편집 작업을 언급한 것은 이 사건의 자기 보고이며, 본 연구가 그 시간을 절약했다는 증거가 아니다. timeline에는 최초 body의 역사적 내용이 없으므로 최초판 요구문은 여전히 미확인이다.

## 고정판 코드가 가르는 것

1. [UnlinkedFilesDialog::lookInDir](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/dialogs/unlinkedfilesdialog.cpp)은 아직 비어 있는 replacement row에 대해 hash 일치 **또는** basename 일치로 첫 후보를 기록한다. filename만 같으면 경고 아이콘이다. 그 row에 hash가 들어가면 뒤의 더 좋은 후보를 다시 비교하지 않는다. SC-E가 지정한 BLUE→RED 순서에서 BLUE가 경고와 함께 제안된다는 것은 소스 조건의 결과다. 실제 파일 열거가 이 순서였다는 GUI 관측은 없다.
2. [MainWindow::checkFile의 unlinked 분기](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/mainwindow.cpp)는 `dialog.exec() == QDialog::Accepted` 뒤에만 checker 재검사와 repaired XML 저장을 한다. 따라서 후보 제안을 자동 오연결 완료라고 쓰면 틀린다. 봉인 입력의 “human identity confirmation 없음”이 일반 OK도 누르지 않는 뜻인지, 경고를 보고 OK는 누르는 뜻인지는 명세만으로 고정되지 않았다. A0의 조건부 예상을 사후 확정 성공/실패로 바꾸지 않는다.
3. [MltXmlChecker::fixUnlinkedFile](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/mltxmlchecker.cpp)은 missing **전체 경로**가 일치하는 row를 사용하고 hash/caption 및 stream-index 처리를 이어간다. 전체 프로젝트의 모든 동명 파일을 무차별 바꾸는 구현이라고 단정하면 안 된다.
4. [Util::getFileHash/getHash](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/util.cpp)는 2,000,000바이트 초과에서 첫/끝 각각 **1,000,000바이트**를 MD5에 넣는다. 파일 길이는 분기 조건이며 digest 입력에 따로 이어붙이지 않는다. `getHash`는 저장된 hash가 있으면 재사용한다. 코드에 Kdenlive에서 복사한 루틴이라는 주석이 있어 두 제품을 독립 알고리즘 증거로 세지 않는다.
5. `MltXmlChecker::checkForProxy`는 저장된 hash로 proxy filename을 찾고 원래 resource를 별도 property로 남긴다. 이 경로만 보면 외부의 unsampled-middle 교체를 검출하는 장치는 없다. 실제 디코더/GUI의 결과까지 실행한 것은 아니다.

## 원시험·환경·실행 분리

고정 commit recursive tree에서 test/README/build 경로를 검색했다. 반환된 시험명에는 EDL JavaScript 시험과 GL widget가 있었지만 proxy/relink 회귀 입력·출력은 찾지 못했다. 이 한정 검색을 저장소 전체에 시험이 없다는 명제로 확대하지 않는다. 공개 원시험 실행 영수증은 0건이다. SC-N/E/X 대상 GUI 실행은 0/3이다.

Python 보조 실행은 `evidence/auxiliary/`에 별도 기록한다. 원 Qt 코드를 실행한 것이 아니라 동일 조건/해시 읽기 범위를 재현한다. SC-X의 두 실제 바이트열은 동일 sampled MD5와 다른 full SHA256을 만들지만, 영상 컨테이너가 아니므로 재생 성공/실패를 말하지 않는다. SC-E 보조 결과도 후보 row 조건이며 dialog 수락·저장·재열기 결과가 아니다.

## 실행 재개

고정 README의 실제 빌드 흐름은 Qt5/MLT 등 의존성 설정 후 `qmake PREFIX=/usr/local/`, `make`, `./src/shotcut`이다. `shotcut.pro`는 Qt5.9 이상을 요구한다. 현재 환경에서 qmake wrapper는 있지만 `qmake -v`는 종료1이며 Qt 설치를 찾지 못한다. target binary 및 개발 pkg-config가 없고 빌드는 시도하지 않았다.

다음 실행자는 같은 SHA와 당시 MLT/Qt/FFmpeg 조합을 준비하고 SC-E 후보 열거 순서·OK 동작을 명시한 harness를 먼저 만들어야 한다. 입력은 `packets/SC-common.json`, 관찰은 replacement model의 path/hash/icon → 수락 여부 → repaired XML → 활성 producer → 실제 decoded frame identity 순이다. SC-X는 봉인 바이트 시험을 그대로 보존하고, 실제 영상의 중간 변화 fixture는 별도 후속 행으로 추가한다. 성공 전까지 0/3을 유지한다.

## 비용과 범위

root가 B 봉인 뒤 추가한 public HTTP 요청은 comments/timeline/tree 3건과 source 5건, 모두 HTTP200이다. `fetch-receipts.json`, `source-receipts.json`에 URL·UTC·bytes·SHA256을 남겼다. 새 5개 파일은 기존 SC-CODEBASE 계보, 댓글은 SC-REQUEST-910 계보이며 독립 저작 수를 늘리지 않는다. code mainwindow는 해당 분기와 proxy-toggle 부분만 읽었고 전체 188769바이트를 모두 이해했다는 주장은 하지 않는다.
