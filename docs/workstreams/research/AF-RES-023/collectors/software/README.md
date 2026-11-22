# Homebrew 조사 묶음

이 묶음은 AF-RES-023의 소프트웨어 분야 원문 수집 결과다. 본표본은 **5건**, 이유 미확인 alias 취소 **1건**과 원 프로젝트·포크 병렬 등록 **1건**은 보충이다. 본표본의 직접 원자료는 중복을 제외하여 사건 5, 정책 3, 독립 소비자 3으로 **11건** 산입했다. 수집자는 부모와 같은 실행의 자료 준비 담당이며 독립 맹검 판정자가 아니다.

## 파일과 범위

| 파일 | 내용 | 분모에서의 처리 |
| --- | --- | --- |
| `sources.json` | 25개 원문·연결 자료의 주소, 읽은 위치, 확인·한계·계보 | `counted=true` 11건 |
| `events.jsonl` | SW01–SW06의 전후 ID, 편집 사유, 기능·판·복원 범위 | SW01/02/03/05/06의 5건; SW04 제외 |
| `citations.json` | SW-D01–03, 서로 다른 소비자의 수정·오류 보고 | 독립 소비자 3건; issue와 그 fix는 하나 |
| `http-observations.json` | 개별 GET 15회, 정확한 주소·시각·응답 | 원문 개수에 추가하지 않음 |
| `SEARCH_LOG.md` | 질의, 연 편집 ID, 반증·접근 실패·배제 | 조사 범위 설명 |
| `fork-supplement.json` | SW-F01, 포크 추가·원 formula 유지·upstream 고정판 3자료 | 본표본과 최소 개수에 추가하지 않음 |

## 복원 판단에 쓰는 핵심 차이

| 사건 | 확인한 변경 | 구 링크를 다시 읽을 때 필요한 조건 |
| --- | --- | --- |
| SW01 TinyFugue | 기존 패키지와 중복인 새 formula를 삭제하고 alias로 연결 | 같은 배포물을 찾는 목적은 alias가 맞는다. 다른 설치 옵션과 패치를 쓴 옛 recipe 재현은 고정판이 필요하다. [편집](https://github.com/Homebrew/homebrew-core/commit/7f379ed5e4135654176204310ae0f24af0826eaa) |
| SW02 libxml++3 | 3.2.4 source와 SHA256을 유지한 이름 변경 | major 3 계열 wrapper를 찾는 목적에는 rename mapping이 맞는다. 옛 파일의 현재 404와 고정판의 내용 존재를 분리한다. [편집](https://github.com/Homebrew/homebrew-core/commit/eb1463eb72712952a10ecdfc201592ca4d24a20a) |
| SW03 readline | gnu-readline으로 바꾼 canonical 이름을 다시 readline으로 복원 | alias와 설치 keg의 대응이 작업을 깨뜨렸다는 편집자 설명이 있다. 파일명만 복원한 것과 외부 인용 복구는 별도다. [되돌림](https://github.com/Homebrew/homebrew-core/commit/8c2998215320942b1329f5b073fad7bfa33e9976) |
| SW05 postgresql | unversioned 이름을 major 14 전용 formula로 전환 | old→@14 관계만으로 소비자의 최신판 요구를 재현하지 못한다. Rails는 뒤에 @16과 libpq를 선택했다. [실제 소비자 수정](https://github.com/rails/rails/commit/27cb8c618ca3a96a2817e412bfe48dc29a6acfa3.patch) |
| SW06 tree-sitter | 한 formula가 설치하던 library와 CLI를 별도 formula로 분리 | 현재 옛 URL이 200이어도 library만 가리킨다. CLI 목적이라면 successor뿐 아니라 요구판도 확인해야 한다. [분리 편집](https://github.com/Homebrew/homebrew-core/commit/e5e819e64a3104cabb55d46ea8e80d69aaf76d5b), [0.25.x 요구 소비자](https://github.com/salesforce/agentscript/issues/33) |

현재 정책은 [Rename-A-Formula](https://docs.brew.sh/Rename-A-Formula), [Versions](https://docs.brew.sh/Versions), [Formula-Cookbook](https://docs.brew.sh/Formula-Cookbook)을 직접 읽었다. 이 문서들은 recipe·설치판·이름변경·versioned formula의 범위를 설명하지만 과거 사건 당시의 정책 준수를 입증하지 않는다.

## 포크 반례 보강

SW-F01에서는 Homebrew가 2021-08-30에 yt-dlp 2021.08.10을 새 formula로 추가했고, 같은 tree에 원 youtube-dl 2021.6.6 formula가 유지됐다. 따라서 이 편집에서 프로젝트 계보는 공유해도 catalog entity와 배포물은 분리되어 있다. 이를 실제 병합 거절 토론으로 부르지는 않는다. [추가 commit](https://github.com/Homebrew/homebrew-core/commit/3e32b083e96a38b8bd09b3516898e77dc05bd518)과 [같은 tree의 원 formula](https://github.com/Homebrew/homebrew-core/blob/3e32b083e96a38b8bd09b3516898e77dc05bd518/Formula/youtube-dl.rb)를 직접 읽었다.

해당 yt-dlp 배포판의 README는 포크 계보를 밝히며 파일명, 다운로드 형식의 정렬, 오류처리 기본값 차이를 설명한다. 동영상 다운로드라는 넓은 용도의 대체 후보와 과거 자동화의 출력을 보존하는 동일 대상은 다른 판단이다. [고정 README의 19행, 119–129행](https://github.com/yt-dlp/yt-dlp/blob/418964fa91b1c44e8f6e5fc323932f952cd558b7/README.md)을 근거로 삼으며 실제 실행은 하지 않았다. 이 포크는 SW06의 같은 upstream 배포판에서 library·CLI를 분리한 패키징 사건과도 구별된다.

## 남은 약점과 인계 입력

- SW03 최초 rename 해시는 되돌림 원문에 남지만 직접 객체를 확보하지 못했다. 대신 공식 revert의 parent에서 gnu-readline formula를 읽었다. 원 사건 ID, 접근 실패, 확보한 전판 주소는 원장에 그대로 있다.
- SW04는 alias를 추가했다가 6분 7초 뒤 삭제했다는 변경만 확인했다. 이유·오병합·소비자 피해가 미확인이므로 성공 정정 분자로 세지 않는다.
- 소비자 3건 가운데 SW-D03은 구 formula가 CLI를 제공하지 않아 빌드 명령이 실패했다는 사용자 보고이며, SW-D01/02는 실제 수정 diff다. 셋을 모두 이번 실행에서 재현한 사용자 피해라고 합산하지 않는다.
- HTTP 404는 대상의 역사적 부재가 아니다. 반대로 200은 기능·판의 연속성을 보장하지 않는다. 간헐적 503·connector 성공·web open 실패는 서로 다른 관측으로 남겼다.
- 본표본은 변화의 유형과 반례를 찾은 목적 표집이다. 오병합률·자동 복원률이나 Homebrew 전체 품질을 추정하지 않는다. 실행이 필요한 다음 입력은 각 고정 formula와 해당 시점 Homebrew runtime이며, 설치·업그레이드 실험은 이번 범위에 포함하지 않았다.

부모는 source/event/consumer ID를 통합 원장에 연결하고, 동일 자료를 본 ①②③ 보기를 사후 정답과 구분하여 구성한다. 이 수집자가 이미 정정 원문을 읽었으므로 이 자료에 대한 복원 답안은 자기 점검이다. 소유 경로 밖 변경이나 commit/push는 수행하지 않았다.
