# Shotcut 재개 검토 — 두 구현 경계의 보완

## 범위와 판정

검토한 연구 체크포인트는 `2f7e07542b4a59839556e00c9e266179150b21a3`이다. 재개 검토자는 부모 문맥을 상속한 같은 모델 계열의 별도 작업자이며, 기존 판독·사례집·정정표를 읽은 **사후 검토자**다. 새 독립 A/B 판독자 또는 맹검 표본으로 세지 않는다. 봉인된 모집·입력·원문 발췌·선택·예측은 변경하지 않았다.

기존 Shotcut 결론은 유지된다. 주 표본은 0/1, 세 봉인 입력의 native 실행은 0/3, 그 입력의 공개 원시험 실행 영수증은 0건이다. 두 보기에서 선택한 핵심 방식은 producer 범위의 내용 근거 확인과 불충분한 legacy 근거의 거부다. 외부 원전이 동종 문서보다 그 방식을 추가로 만들었다거나 실제 복구를 성공시켰다는 증거는 없다.

결과판에는 다음 두 사항을 우선 보완해야 한다.

| ID | 보완할 주장 | 확인 근거 | 필요한 수정과 적용 한계 |
|---|---|---|---|
| SC-R1 | producer별 바인딩 필드와 XML 경로를 고치면 범위 밖 producer 보존까지 구현된다는 인상 | 고정판 [ProxyReplacePostJobAction::doAction](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/jobs/postjobaction.cpp#L88-L107)은 완료 뒤 `MAIN.replaceAllByHash(m_hash, producer, true)`를 호출한다. [MainWindow::replaceAllByHash](https://github.com/mltframework/shotcut/blob/0898bdf3fc0f9f3fbf78336bad21d5506e19c118/src/mainwindow.cpp#L4558-L4587)는 현재/저장 producer를 비교하고 playlist와 timeline의 hash 기반 교체를 호출한다. | A1/B-F의 변경 심벌 목록에는 이 공개·전파 경로가 빠져 있다. Q4의 추가 구현 전제에 post-job action, MainWindow 함수, downstream `replaceClipsWithHash`를 명시한다. 후속 함수 본체는 이번 검토에서 열지 않았다. frozen p2의 hash는 다른 값이므로 이 정적 경로만으로 p2가 실제 바뀌었다고 판단할 수 없다. |
| SC-R2 | 같은 선택 또는 예상 상충0이라는 표현을 완전한 동작 동등성으로 읽는 경우 | 봉인 `readers/SC-A.json`의 SC-X는 rebuild 필요와 완료까지 preview 보류를 말한다. `readers/SC-B.json`의 SC-X는 명시적 recovery decision을 기다린다고 쓴다. | ‘같은 **정규화된 핵심 방식**’과 ‘현재 봉인 관찰 지점에서 반대의 성공/실패 예측을 확인하지 못함’으로 한정한다. 재생성 시작의 사용자 선택·자동 실행 정책이 바이트 단위로 같다는 증거는 없다. A가 자동 재생성을 확정했다는 반대 주장도 하지 않는다. |

SC-R1은 새 native 실패 관측이 아니라 **제안에서 아직 구체화되지 않은 변경 범위**다. SC-R2는 연구 결과의 집계 해상도를 명확히 하는 수정이며 봉인 선택을 소급 변경하지 않는다.

## 직접 다시 확인한 원문과 고정판

[릴리스 태그](https://api.github.com/repos/mltframework/shotcut/git/ref/tags/v20.09.13)는 다시 읽었을 때도 commit `0898bdf3fc0f9f3fbf78336bad21d5506e19c118`을 직접 가리킨다. 작성자가 실행한 정확한 binary와 의존성 조합을 증명하지는 않는다.

[이슈 #910의 현재 본문](https://github.com/mltframework/shotcut/issues/910)과 [공개 댓글 11개](https://api.github.com/repos/mltframework/shotcut/issues/910/comments?per_page=100)를 다시 읽었다. 작성자는 Windows10/20.09.13, 같은 이름으로 외부에서 해상도를 낮춘 영상, Source에서는 재생되지만 timeline에서는 검은 화면이라는 현상을 설명한다. 마지막 작성자 댓글 [699527361](https://github.com/mltframework/shotcut/issues/910#issuecomment-699527361)은 XML 변경 제안 후에도 검은 화면이 남았다고 한다. 사건 종료를 성공 출력으로 바꿀 수 없다. 원본 이동이나 서로 다른 폴더의 동명 클립 오연결은 확인되지 않았다. 현재 본문을 최초 작성판으로 부를 근거도 추가되지 않았다.

다음 파일의 GitHub blob SHA와 저장된 로컬 원문에 `git hash-object`를 적용한 값이 일치했다. 일부 구간만 원격으로 다시 열었으며 SHA는 도구가 반환한 전체 파일 blob 식별자다.

| 파일 | 직접 읽은 심벌·구간 | 원격/로컬 공통 blob SHA |
|---|---|---|
| `src/util.cpp` | `getFileHash/getHash`, 380–430 | `ee934954acfc4c73c839c5ebe753034c3c782f53` |
| `src/dialogs/unlinkedfilesdialog.cpp` | 수동 지정 및 `lookInDir`, 46–150 | `31b1a700dacb1f78a49b26a8930198217149e84c` |
| `src/mainwindow.cpp` | unlinked 수락 gate와 hash 전파, 1064–1097/4558–4587 | `65e097149a4efc41abcdfb0a4707c81eec414575` |
| `src/jobs/postjobaction.cpp` | `ProxyReplacePostJobAction::doAction`, 88–107 | `8a498e509875734f9498e55ba13b5890a897f097` |

이를 통해 기존 [ERRATA.md](ERRATA.md)의 SC 해시 정정과 수락 gate 한계를 확인했다. 크기는 digest에 추가되지 않으며, 2,000,000바이트 초과에서 양 끝 각각 1,000,000바이트를 읽는다. 비어 있지 않은 저장 hash는 다시 읽지 않는다. `lookInDir`의 filename 또는 hash 일치는 후보 row를 채우지만, 실제 repaired XML 적용에는 dialog 수락이 필요하다. 소스의 조건을 읽은 것과 실제 열거 순서·UI 선택·재열기·decoded frame을 관측한 것은 다르다.

## 공여 원전과 동종 대조의 범위

darktable 공식 4.8 계열 commit `9d2c663bbe2a3390fd3750fdce780025933a5045`의 [sidecar 본문](https://github.com/darktable-org/dtdocs/blob/9d2c663bbe2a3390fd3750fdce780025933a5045/content/overview/sidecar-files/sidecar.md)과 [duplicate manager 본문](https://github.com/darktable-org/dtdocs/blob/9d2c663bbe2a3390fd3750fdce780025933a5045/content/module-reference/utility-modules/darkroom/duplicate-manager.md)을 직접 다시 읽었다. sidecar blob은 `f3276cd29fe5b38e60ba8570cf2c616f16c55a44`, duplicate blob은 `cf27bcd32f667ce34e349719db2ffaa3761ecc81`이다.

원전은 공통 입력 이미지와 편집본별 metadata/history, database와 sidecar의 우선순위 및 충돌 선택을 설명한다. 독립된 편집 history가 공통 입력 bytes를 변경 전 상태로 보관해 준다는 뜻은 아니다. whole-file digest, stable snapshot, proxy에서 원본을 복원하는 역변환, 여러 파일의 atomic commit은 이 두 절에서 확보하지 못했다. 이를 연구자 공학적 추론으로 표시한 기존 사례집의 귀속은 타당하다. 해당 판의 duplicate 파일 front matter에는 applicable-version3.6이 있으므로, 그 문자열을 최신판4.8이라는 주장과 혼동하지 않는다. 이번 고정의 근거는 제공된 공식 release 계열 commit이다.

[Kdenlive Proxy Settings](https://docs.kdenlive.org/en/project_and_asset_management/project_settings/proxy_settings.html)와 [Using Camera Proxy Clips](https://docs.kdenlive.org/en/tips_and_tricks/useful_info/using_camcorder_proxy_clips.html)를 현재 웹 원문에서 다시 열었다. 제목은26.08이며 편집용 proxy/렌더용 원본 구분과 상대 폴더·prefix/suffix로 대응을 찾는 규칙을 확인했다. 현재 반환 텍스트에서 종전 기록의 문서 revision8a74558을 따로 확정하지는 못했다. 현재 페이지의 일치가 과거 Shotcut 동작이나 당시 개발자의 열람을 증명하지 않는다. `getFileHash`의 Kdenlive 복사 주석 때문에 두 제품의 그 루틴을 독립적인 알고리즘 증거로 세지 않는 규칙도 유지한다.

## 시험 판정과 최소 후속 확인

| 입력 | 현재 가를 수 있는 것 | 아직 가르지 못한 것 | 다음 첫 확인 |
|---|---|---|---|
| SC-N | 기존 resource 복원 코드와 A1/B-F의 같은 정상 예상 | 실제 저장·재열기와 decoded media identity; 추가 필드 보존 | 고정 target와 실제 원본/proxy/MLT project를 준비해 disable→save→reopen을 실행하고 XML와 프레임 identity를 함께 보존 |
| SC-E | 주어진 후보 순서의 filename-first 제안, selected A1/B-F의 legacy 거부 예상 | native QDir 순서, 일반 OK와 identity confirmation 구분, repaired XML, p2 보존 | 후보 순서와 dialog accept/cancel을 명시한 harness를 만들고 model→gate→XML→active producer를 각각 관측. post-job hash 전파 경로를 별도로 확인 |
| SC-X | 커밋된 보조 영수증의 두 비영상 바이트열에서 sampled digest 같음/full digest 다름 | 실제 영상의 stale proxy 재생·원인 판정, 과거 digest가 없는 상황의 변화 검출, 재생성 시작 정책 | 기존 비영상 입력은 유지. 실제 영상의 변경 전 bytes와 신뢰 가능한 과거 digest를 확보한 **별도 후속 행**을 준비 |

기존 보조 실행 영수증은 읽었지만 이번 검토에서 다시 실행하지 않았다. Python의 동일 해시 조건 검사는 native GUI 실행으로 세지 않는다. current full digest 하나로 과거 내용을 복원하거나 mutation을 증명할 수 없다는 한계도 유지한다. 새로운 valid-media fixture를 만든다면 이미 봉인된 SC-X의 성공으로 소급하지 않는다.

원 실행 환경을 준비한 뒤 고정판 README가 제시한 build 흐름은 `qmake PREFIX=/usr/local/`, `make`, `./src/shotcut`이다. Qt/MLT/FFmpeg 조합과 실제 media 입력을 먼저 고정해야 하며 이 명령만으로 frozen9 시험이 자동 수행되지는 않는다. 핵심 첫 개발 확인은 `rg -n 'replaceAllByHash|replaceClipsWithHash|ProxyReplacePostJobAction::doAction' src`로 실제 target의 completion 경로와 호출자를 찾고, proposed producer identity가 어느 호출 경계까지 전달되는지 조사하는 것이다.

## 비용·독립성과 기록

[resume-review-shotcut.json](resume-review-shotcut.json)에 직접 원격 재열람 시도15개를 남겼다: GitHub 호출10회, 웹 open URL5개(2개 batch, Kdenlive2절 반복 포함). PROV-DM의 첫 웹 접근은 도입 텍스트가 반환된 예비 접근으로만 남겼으며 §5.2.1의 새 완전 판독으로 세지 않았다. substantive 재열람 계보는 기존 SC-CODEBASE·SC-REQUEST-910·DARKTABLE-MANUAL·KDENLIVE-MANUAL뿐이고 **독립 원저작 추가0**이다. 봉인 A/B reader의 추가 노출도0이다.

처음5회와 마지막2회의 GitHub 호출에는 실제 포착한 UTC를 남겼다. 중간3회와 웹5개 URL은 정확한 호출별 UTC가 포착되지 않아 인접 timestamp 사이의 구간과 그 이유를 기재했다. 없는 정밀 시각·비용·토큰·native 종료값을 만들지 않았다. 이번 파일은 새 사후 검토이고, 원 연구의 조사자와 재판독자가 완전하게 독립이라는 증거로 사용하지 않는다.

