# 반례와 정정

## 같은 파일 길이에서 880 Hz만 사라지는 경우

기본 배치와 B mute는 모두 L13·L35 두 파일에 88,200 프레임씩이다. 두 판·두 반복에서 mute 후 B 성분이 부재로 분류됐고, 각 출력이 A의 해당 시간 slice와 샘플 오차 0 LSB였다. B를 L 위로 이동한 경우에는 기본 배치와 같은 PCM SHA였다. 따라서 파일 개수나 길이로는 B가 들어갔는지 판정할 수 없다. [3.4.2 기본](receipts/3.4.2/base-r2/analysis.json) · [3.4.2 mute](receipts/3.4.2/mute-b-r2/analysis.json) · [3.5.0 기본](receipts/3.5.0/base-r2/analysis.json) · [3.5.0 mute](receipts/3.5.0/mute-b-r2/analysis.json)

## 같은 믹스 성분에서 파일 수가 줄어드는 경우

K를 첫 라벨 트랙으로 올리면 L13·L35 두 파일 대신 K24만 생성됐다. K24는 프로젝트 [2,4)초의 A+B와 샘플 오차 0 LSB였다. 프로젝트 [2.25,2.75)에서 기본 L13과 K24의 진폭이 같고, [3.25,3.75)에서 기본 L35와 K24의 진폭이 같았다. 조건을 바꿔 음 조합은 그대로인 채 파일 범위만 바뀔 수 있다. [3.4.2 K24](receipts/3.4.2/swap-labels-r2/analysis.json) · [3.5.0 K24](receipts/3.5.0/swap-labels-r2/analysis.json)

## 음소거하지 않은 무음 B

별도 폴더에서 새 프로젝트를 만들고 B.wav를 0으로 채운 220,500프레임의 `Silence.wav`로만 교체했다. 화면에 B가 있고 mute는 꺼져 있다. 두 판에서 두 파일 모두 본표 mute-B의 PCM 및 A 참조와 일치했다. 880 Hz 부재만으로는 B가 음소거됐는지, 신호가 0인 트랙이 믹서 입력으로 들어갔는지 구분되지 않는다. 구분에는 프로젝트 상태와 원음이 필요하다. 해당 대조의 WAV 4개는 본표 분모 밖이다. [무음 원음](fixtures/Silence.wav) · [대표 재실행과 대조 지문](receipts/replay/comparison.json)

## 매뉴얼의 범위 해석과 Tracks 회귀

동봉된 두 매뉴얼의 Labels 절은 상단 라벨 트랙이 시간 경계를 정한다고 명시한다. 위쪽에 여러 wave track이 있을 때 그 트랙들이 섞인다는 조건절도 있다. 이 조건절을 아래쪽 트랙의 배제 규칙으로 해석하면 기본·라벨 교환의 8개 실행과 맞지 않는다. 조건절의 위쪽 트랙 포함 주장 자체는 위치 이동에서 관측한 값과 양립한다. 실제 WAV로 입증한 것은 두 Linux 고정판의 아래쪽 비음소거 mono 트랙 포함이다. [동봉 매뉴얼 위치 M01–M01b](sources.jsonl) · [온라인 Labels 절](https://manual.audacityteam.org/man/export_multiple.html#Split_files_based_on)

#5302와 #5305는 별개의 요청 경로인 Tracks에서 분리 파일에 믹스가 들어가던 회귀를 기록한다. PR의 한 줄 수정은 `selectedOnly`를 task builder에 전달한다. 이 이력은 Labels의 두 음 결과를 Tracks 안내에 그대로 쓰면 안 되는 실제 사례다. 알파 바이너리와 그 파일의 재생성은 범위 밖이다. [회귀 #5302](https://github.com/audacity/audacity/issues/5302) · [원 PR diff](https://github.com/audacity/audacity/pull/5305/files)

## PNG 대조와 반대 문구

Inkscape 1.4는 `target`의 bbox를 120,120에서 100×80 px로 찾았다. 두 PNG는 동일 크기였고, `--export-id-only` 추가로 겹친 [35,19]가 RGBA [0,0,255,255]에서 [255,0,0,255]로 바뀌었다. 타 객체만 덮는 [65,52]의 알파는 255에서 0으로 바뀌었다. 타 객체 사각형에 해당하는 2,500/8,000 픽셀이 달랐다. 고정 man의 `--export-id` 항목에 있는 타 객체 배제 문구는 단독 옵션의 이 관측과 맞지 않는다. PNG 구현은 별도의 `export_id_only` 플래그에서 객체 벡터를 전달한다. [PNG 원값](receipts/svg/pixels.json) · [고정 man](https://gitlab.com/inkscape/inkscape/-/raw/INKSCAPE_1_4/man/inkscape.pod.in#L302) · [고정 PNG 구현](https://gitlab.com/inkscape/inkscape/-/raw/INKSCAPE_1_4/src/io/file-export-cmd.cpp#L798)

## 복구가 필요했던 도구 동작

- 3.4.2 최초 출시품 호출은 Debian host의 `libgio`가 요구한 `MOUNT_2_40` 심볼 때문에 실패했다. 호스트 libmount·libselinux를 먼저 로드한 뒤 실행 준비까지 진행했다. 새 임시 경로와 Pango의 호스트 버전을 지정하고 다시 시작한 뒤 정상 GUI를 확보했다.
- 3.4.2 기본 1회는 내보내기 설정 창과 완료 창의 제목이 모두 `Export Audio`여서 감시기가 timeout으로 exit 1을 냈다. [실제 성공 화면](receipts/3.4.2/base-r1/failure.png) 및 WAV 둘을 직접 확인해 관측에 포함했다. 이후 창 ID를 대조했다. 다음 준비에서 저장된 Multiple Files 패널이 다른 높이로 열려 절대 좌표 조작이 실패했다. 내보내기 전 화면의 원점을 읽게 고친 후 새 프로젝트에서 성공했다.
- 3.5.0의 첫 준비에서는 Music Import와 `Export to computer` 위치 선택 화면을 각각 처리하지 않아 WAV가 없는 두 시도가 생겼다. 템포 변경은 No, 내보내기는 컴퓨터 저장을 택했다. 두 UI 경로의 원영수증은 이후 실행에도 남겼다.
- 새 폴더 재실행에서 3.4.2는 패널 높이 변화가 늦었고, 3.5.0 무음 대조의 첫 시도는 템포 화면이 늦게 떠 키 입력이 다른 창에 적용됐다. 소리 장치 오류가 나서 오류 전송을 닫고 빈 프로젝트를 다시 열었다. 최종 driver는 패널 확장, picker 제목, 첫 원음 직후 템포 창을 기다린다. 준비·복구 로그는 [receipts/diagnostics/](receipts/diagnostics/)에 있다. 이 시도들은 실험 성공 분모에 포함하지 않았다.
- 일부 본표 Label Editor 그림은 창 제목이 보인 직후에 잡혀 숫자가 비어 있었다. 별도 프로필에서 대화상자 그리기를 기다려 16회 모두 다시 찍었다. 3.4.2의 마지막 재촬영 준비 중 X11 active window가 일시 공석이었으므로 선택 전환을 기다리는 처리를 더해 새 프로젝트에서 내보내기를 완료했다. 16개 재촬영 결과는 원래 28개 WAV 바이트와 일치했다. [X11 전환 시도](receipts/diagnostics/342-screen-swap-r2-active-window/gui.json) · [재촬영 비교](receipts/screen-repeat/comparison.json)
