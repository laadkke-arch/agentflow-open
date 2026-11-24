# Inoreader에서 FreshRSS로 옮길 때 확인할 링크

검증한 조합은 공개 비식별 Inoreader 유래 파일 두 개와 FreshRSS 1.29.1 SQLite의 CLI다. 파일이 어디에서 왔는지와 수신 후 어떤 행이 생겼는지를 연결하면 목적별로 필요한 조건을 확인할 수 있다.

| 목적 | 첫 링크와 수신 쪽 링크 | 확인할 값 |
| --- | --- | --- |
| 구독 목록을 넘기기 | [Inoreader의 Download OPML file](https://www.inoreader.com/help/basic/preferences-customization/can-i-export-my-subscriptions-and-content)와 [고정판 FreshRSS Import](https://github.com/FreshRSS/FreshRSS/blob/b2c50115baa36c217e939ee3ea8ecfae52f91abd/docs/en/users/04_Subscriptions.md#import) | 피드 URL 및 필요한 폴더. 이번 SQLite 주실험은 별표 파일만 실행했다. 구독 필드의 경계는 [AF-RES-215의 고정표](https://github.com/laadkke-arch/agentflow-open/blob/58102fdacb7ac32ffcdacc08a55025612fdc7ebc/docs/workstreams/research/AF-RES-215/fields.csv) 참조 |
| 저장해 둔 별표 글을 다시 열기 | [Inoreader의 Read later 발신 메뉴](https://www.inoreader.com/help/basic/preferences-customization/can-i-export-my-subscriptions-and-content), [검증한 두 파일의 지문·원값](inputs.json), [고정판 CLI](https://github.com/FreshRSS/FreshRSS/blob/b2c50115baa36c217e939ee3ea8ecfae52f91abd/cli/import-for-user.php#L23-L44) | `streamId`, 기사 `id`, alternate, 별표 토큰, label. 원형 관측에서 세 라벨 관계의 이름과 다섯 별표가 저장됐다. 파일 이름과 URL 충돌의 조건은 [통제 기록](controls.csv)에 있다 |
| 읽음과 안읽음의 과거 근거를 보존하기 | [Inoreader 항목의 상태 토큰 설명](https://www.inoreader.com/developers/stream-contents_)과 [FreshRSS의 reception 값 및 parser](https://github.com/FreshRSS/FreshRSS/blob/b2c50115baa36c217e939ee3ea8ecfae52f91abd/app/Controllers/importExportController.php#L441-L472) | explicit read는 보존됐다. reception을 끄면 누락 항목은 0, 켜면 1로 채워진다. 토큰이 없는 원항목의 상태를 확인해야 하는 경우 발신 근거가 더 필요하다. 수신 UI의 [reception 체크박스 코드](https://github.com/FreshRSS/FreshRSS/blob/b2c50115baa36c217e939ee3ea8ecfae52f91abd/app/views/configure/reading.phtml#L368-L377) |
| 이미 사용 중인 수신 DB에 같은 파일을 다시 넣기 | [동일 바이트 재수입 표](observed.csv)와 [수신에서 바꾼 필드의 전후](receipts/C5-state-drift.json) | ID 외에 read, favorite, 태그 관계와 lastSeen을 비교. 작업용 복제본에서 기존 사용자 수정 값과 추가 태그의 결과를 먼저 확인할 수 있다 |

별표 파일에 두 피드가 같은 GUID를 쓰거나 canonical만 있는 글이 있다면 자료 사본에서 원항목과 수신 URL을 대조한다. 정상 종료여도 하나의 글이 다른 피드에 붙거나 link가 빈 채로 행이 남을 수 있다. 이 사례는 고정판 합성 통제에서 관측했다. [GUID 충돌·분할](controls.csv), [원형 및 링크 통제](RESULT.md).

## 고정 표본을 다시 실행하는 명령

연구 브랜치의 checkout에서 실행한다. Docker와 Python 3가 필요하다. 공개 FreshRSS 소스와 런타임 구성은 인터넷에서 받아오며, 실제 import는 외부 통신을 차단한 일회용 컨테이너에서 수행된다. 영수증의 이미지 ID와 패키지 버전을 비교하면 사용한 환경의 차이를 알 수 있다.

```sh
study=docs/workstreams/research/AF-RES-228
fresh_src=$(mktemp -d /tmp/af228-src.XXXXXX)
fresh_run=$(mktemp -d /tmp/af228-run.XXXXXX)
git -C "$fresh_src" init
git -C "$fresh_src" remote add origin https://github.com/FreshRSS/FreshRSS.git
git -C "$fresh_src" fetch --depth=1 origin b2c50115baa36c217e939ee3ea8ecfae52f91abd
git -C "$fresh_src" checkout --detach FETCH_HEAD
docker build -f "$study/runtime.Dockerfile" -t af-res-228-runtime:20261124 "$study"
python "$study/run.py" main --source "$fresh_src" --output "$fresh_run/main"
python "$study/run.py" controls --source "$fresh_src" --output "$fresh_run/controls"
python "$study/run.py" replay --source "$fresh_src" --output "$fresh_run/replay"
```

판정에 사용한 입력은 저장소에 고정된 두 바이트 사본이다. 패키지 저장소 시점이 달라져 런타임 버전도 달라진 재생은 별도로 표시한다. OS·PHP·SQLite·cURL·bundled SimplePie와 이미지 지문은 영수증에 있다. [기준 런타임](receipts/runtime-main.json), [컨테이너 호출](receipts/container-main.json).
