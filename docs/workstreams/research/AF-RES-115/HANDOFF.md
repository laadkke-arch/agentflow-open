# AF-RES-115 최종 인계

**PARTIAL.** Excalidraw와 MuseScore 공개 원글을 각각 생성순 60건으로 고정했다. 산입한 1차 저작은 원 요청 6, 원 구조·공식 구현 8, 별도 반례 7, 타 분야 규격·실데이터 4의 25개다. 1,454개의 열람·시도 행과 1,441개 출처 주소는 서로 다른 분모다. 본 자연 입력은 작동한 1/6로 비교 3/18, 본 변형은 0/12로 비교 0/36이다. 원본 파일 접근 실패와 없는 필드를 보류 성공으로 세지 않았다. [결과](RESULT.md) · [질문별 자체 검토](SELF_CHECK.md) · [수용 증거](evidence/acceptance-evidence.json)

E05의 382자 B/C는 같은 사각형을 받았고 바꿀 text ID와 실행판은 없었다. A/B/C 모두 보류다. M60은 원글이 링크한 공식 테스트 자료로 보조층에 뒀다. 같은 주소의 두 blob을 대조했고 저자의 후속 변경은 `TBox[1]/Text[1]`의 한 바이트다. C++ 비교값은 선행판부터 이미 19였다. M60에서는 B/C 모두 412자로 같은 저장 범위를 지지했다. 동일 문자수 C 단독 지지는 별도 합성 CE·CM에만 있었다. 동명·방향·효과의 과신을 확인하기 위해 조건 누락 대조를 분리했고, 실제 편집 앱의 영향 범위는 미확인이다. [보기](views.jsonl) · [비교기 입력과 출력](evidence/replays.json) · [패치와 누락 대조](evidence/provenance.json)

## 식별과 검사

저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-115`, Codex Cloud 실행이다. 계획판 `670ecde1dab07aede6760618a7d907f0cdff185a` 이후 진행표에 추가된 3커밋을 확인하고 실제 분기 `581b863dfb9f90106c2a07fb749d0cada51b0a25`에서 시작했다. 첫 원격 head는 `3839d730271a9a7f2f909be9cca5526299a4d929`였고 checkout 전 바뀌었다. 운영 선행 `c49eb343ca0f74006cd3f748a1ec48b67615cedf`의 인계와 검사판 `cf01f72e7b9837661efc3a70bb29ef924a52ad29`의 RESULT, gold, links, verification을 먼저 읽었다. 계약의 허용 경로는 `docs/workstreams/research/AF-RES-115/` 한 곳이다. [시작 기록](SCOPE.md) · [manifest](manifest.json)

검사 결과 SHA `0da8f40d4aff86a85c559d2851e5e38acff4f380`. 2026-11-24 04:28 UTC 무렵 GitHub에서 새 checkout을 열어 36파일을 Git blob과 대조했고 커넥터로 대표 5파일을 읽었다. 원글 7곳의 opening SHA가 맞았다. 고정 원본에서 보기와 재생, 검산 JSON, 첫 세 표를 다시 만들었다. 두 경로의 45자리씩 모두 동일하다. MusicXML XSD 3건, NGA·Sakay 행, M60의 byte diff도 재현했다. [고정 결과판](https://github.com/laadkke-arch/agentflow-open/tree/0da8f40d4aff86a85c559d2851e5e38acff4f380/docs/workstreams/research/AF-RES-115) · [실행 명령](reproduce.md)

`workbench.session check … --fetch`와 저장소 공통 검사가 종료 0이었다. 공통 55, 기존 lab 7·9 검사도 통과했다. 공통 검사의 기본 manifest 검색은 `no_active_sessions`였고 owned path의 manifest는 별도 명령으로 검증했다. 판독은 같은 작업자가 독립 후처리 코드로 대조했다. 다른 판독자, Windows 및 원 앱 실행은 미실시다. [수용 영수증](evidence/acceptance-evidence.json)

| 묶음 | 커밋 | 먼저 읽은 내용과 원격 재열람 |
| --- | --- | --- |
| ① 계약과 모집 규칙 | [94688a38659879cc5020aae93b532d58ebc50126](https://github.com/laadkke-arch/agentflow-open/commit/94688a38659879cc5020aae93b532d58ebc50126) | 통합 자료·AF-RES-111 인계/검사판 읽기 뒤 원격 manifest 확인 |
| ① 모집 결과 | [73b244dd406abcb2005e8b9f3f8a05559c93d1d5](https://github.com/laadkke-arch/agentflow-open/commit/73b244dd406abcb2005e8b9f3f8a05559c93d1d5) | 생성순 opening과 첨부 응답 뒤 원격 frame.csv 확인 |
| ② 원 파일 지문·보기 | [f0215c62e234f4622be95bd587bf71f38c9af36e](https://github.com/laadkke-arch/agentflow-open/commit/f0215c62e234f4622be95bd587bf71f38c9af36e) | E05 JSON·M60 앞뒤·정의 읽기 뒤 원격 inputs SHA 확인 |
| ③ gold 봉인·반례 | [93633ac15f936d49905b9ece22b108fbb3a67e5d](https://github.com/laadkke-arch/agentflow-open/commit/93633ac15f936d49905b9ece22b108fbb3a67e5d) | 전체 파일·공식 절 판독 뒤 재생 전에 원격 봉인 확인 |
| ④ 재생 | [12fbd3f9c184153589fa531202c5eb5c45da1333](https://github.com/laadkke-arch/agentflow-open/commit/12fbd3f9c184153589fa531202c5eb5c45da1333) | 두 입력 접근 감사 뒤 원격 runs SHA 확인 |
| ⑤ 검산·고정 결과 | [0da8f40d4aff86a85c559d2851e5e38acff4f380](https://github.com/laadkke-arch/agentflow-open/commit/0da8f40d4aff86a85c559d2851e5e38acff4f380) | 세 표·원장·Q별 점검 뒤 새 checkout 및 원문 재열람 |
| 수용 증거 | [4afad1531c08517357d00218f26d2d65cc26b25e](https://github.com/laadkke-arch/agentflow-open/commit/4afad1531c08517357d00218f26d2d65cc26b25e) | 고정 결과의 검사 후 영수증을 원격에서 재열람 |
| 인계 | 이 파일의 단독 커밋 | 결과·검사 영수증의 원격 확인 뒤 작성 |

## 막힌 입력과 다음 첫 행동

첫 행동은 [frame-notes.md](frame-notes.md)의 E08/E16/M01/M03/M04 줄과 [첨부 요청 원장](evidence/attachment-attempts.jsonl)을 열고, 같은 공개 원본을 받을 수 있는 환경에서 아래와 같이 M01 ZIP을 받는 것이다. GitHub 사용자 ZIP은 `objects.githubusercontent.com`으로 이동했고 여기서는 터널 403을 받았다. Excalidraw 공유 장면의 JSON endpoint와 MuseScore 원 첨부도 접근하지 못했다. Cloud 환경의 Networking 절로 확인한 호스트 제한에 해당한다. 웹 원경로 및 가능한 공개 대체 URL도 본 시도에 포함했다. 원 저자와 동일 판의 바이트가 있어야 적격 순위·변형 자리·저장 영향의 결손을 줄일 수 있다.

```sh
af115_retry_dir=$(mktemp -d /tmp/af115-originals.XXXXXX)
curl -fLsS --max-time 45 \
  'https://github.com/musescore/MuseScore/files/7887546/lyrics-test.zip' \
  -o "$af115_retry_dir/lyrics-test.zip"
sha256sum "$af115_retry_dir/lyrics-test.zip"
python -B -m zipfile -l "$af115_retry_dir/lyrics-test.zip"
```

E08의 share scene은 원 URL에서 앱으로 복원하고 로컬 `.excalidraw` 및 선택 표시의 지문을 별도로 보관한다. E16과 나머지 M 원본은 원글의 링크·실제 판·의존 파일을 재검사한다. E05의 실제 앱 빌드와 추가 텍스트, M60의 아카이브에 연결 가능한 repeat runner가 확보되면 [네이티브 재현 명령](reproduce.md)으로 이어간다. 현 보관판의 CMake는 `tst_repeat.cpp`를 제외한다.

색인 제안 — AF-RES-115 · 부분 구조에서 공식 조작 링크의 대상·보존 범위 · PARTIAL · [결과](RESULT.md) · AF-RES-111 고정 인계 의존.

| 가장 중요한 불일치·약점 | 다음 조사·직접 열 자료 | 어떤 관측이면 판단이 바뀌나 |
| --- | --- | --- |
| 본 자연 5건과 본 변형 12건의 입력이 비었다. | [모집과 후보 주소](frame-notes.md) 및 [M01 원 ZIP](https://github.com/musescore/MuseScore/files/7887546/lyrics-test.zip)부터 원본 바이트를 연다. | 첫 적격 사건 세 건씩의 원 데이터와 정확 판이 확보된다. |
| 같은 길이에서 C만 지지한 두 건은 합성이다. | [보기 층](views.jsonl)과 [독립 판독용 원장](truth.csv)을 열고, 확보한 자연 자료에서 조건에 가린 판독을 추가한다. | 자연 요청에서도 정확히 복원한 직접 관계가 늘고 동명·역방향의 오확정이 함께 늘지 않는다. |
| M60은 주석만 변경된 diff까지 확인했다. 편집과 repeat 실행 효과는 미확인이다. | [상류 C++ 테스트](https://github.com/musescore/MuseScore/blob/ee7506f7a877b79f905fc15b3f0051e468d397de/src/engraving/tests/tst_repeat.cpp#L153-L174) 및 [타깃 설정](https://github.com/musescore/MuseScore/blob/ee7506f7a877b79f905fc15b3f0051e468d397de/src/engraving/tests/CMakeLists.txt#L21-L45)을 열고 같은 판에서 전후 입력을 실행한다. | 계산된 재생 순서·화면·저장 레코드를 나란히 비교해 공동 변화 여부를 확정한다. |
