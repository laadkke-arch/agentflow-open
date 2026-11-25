# AF-RES-251 HANDOFF

## 1. 식별과 결과

- **자체 상태 완료, 통합 검토 준비됨.** Audacity 3.4.2와 3.5.0의 정식 Linux GUI Labels 내보내기 16/16, 출력 WAV 28/28을 판독했다. 별도 프로필의 대표 기본 재실행 2/2와 무음 B 2/2도 완료했다. 자체 검토 시행, 별도 검토자 검토 미실시.
- AF-RES-251 시도 1, Codex Cloud, Debian 13.6/x86-64, 저장소 `laadkke-arch/agentflow-open`, 작업 브랜치 `work/research-af-res-251`, 소유 경로 `docs/workstreams/research/AF-RES-251/`.
- 착수 GitHub 통합 SHA `d1353701530ffd4c68587276c15d988d2cc92972`. 계약 원격 재조회 통합 SHA `933a0f7d534314470c083b0aa284044a9ad45443`. 선행 AF-RES-230 결과 `896b13e51f18738e60d63977e999c0aa25027057`, 중앙 DONE, 자체 PARTIAL. 230의 원작성자 산출과 alpha 인과는 미확인 상태다. [착수 범위](SCOPE.md) · [고정 세션 계약](session.json)
- 마지막 결과 SHA **`8037f33f7e48668a116d237f731d8d13ffd6959b`**. GitHub에서 새로 받아 실제 확인했다. 이 문서는 결과 SHA 다음의 단독 인계 커밋이다. [고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/8037f33f7e48668a116d237f731d8d13ffd6959b/docs/workstreams/research/AF-RES-251/RESULT.md)
- 고정 결과 검사 종료 2026-11-25T00:35:25Z. 첫 화면 캡처 일부의 숫자 표시를 보완한 16회까지 포함한 결과다.

## 2. 판단

두 판에서 첫 라벨 트랙은 파일 경계를 정했다. 기본 `A · L · B · K`에서 L13/L35 두 파일은 B가 아래에 있어도 440 Hz와 880 Hz를 모두 포함했다. B를 L 위로 옮긴 출력은 기본과 WAV 바이트가 동일했다. B mute는 파일 수와 경계를 유지하고 880 Hz만 없앴다. L/K 교환은 K24 [2,4) 한 파일로 줄였고 공통 시간대의 두 음은 유지했다. 모든 본표 WAV는 44,100 Hz, mono signed PCM16, 88,200 frames다. 정수 초별 원음 구간과 샘플 차이 0 LSB로 일치했다. [RESULT.md](RESULT.md) · [runs.csv](runs.csv)

두 판에 동봉된 매뉴얼은 위쪽에 있는 wave track들의 믹스를 설명한다. 이 문장을 아래쪽 제외로 읽은 예측은 기본·교환 8/16회와 12/28 WAV에서 반전됐다. 위쪽 라벨의 경계 선택과 위에 둔 wave track의 포함은 매뉴얼과 양립한다. unmuted 무음 B의 WAV는 mute-B와 바이트가 같았다. 따라서 신호 성분을 근거로 트랙 자체의 음소거 상태를 해석할 때 원음과 화면을 함께 봐야 한다. Inkscape 1.4는 같은 100×80 bbox에서 id-only 추가 후 겹친 픽셀을 포함해 8,000개 중 2,500개가 바뀌었다. [반례 및 정정](counterexamples.md) · [별도 재실행](receipts/replay/comparison.json) · [SVG 픽셀](receipts/svg/pixels.json)

## 3. 결과 파일과 커밋

| 파일 | 내용 |
| --- | --- |
| [SCOPE.md](SCOPE.md), [inputs.json](inputs.json), [session.json](session.json) | 사전 판정, 합성 입력과 라벨의 SHA, Git 원격 계약 |
| [sources.jsonl](sources.jsonl) | 열람 94행, 성공 76/실패 18, 직접 원저작 30 및 lineage 13. AF-RES-230 4, 정확판 릴리스·코드 11, PR·회귀·매뉴얼 7, 판독 도구 3, Inkscape 4, Ardour 1 |
| [RESULT.md](RESULT.md), [runs.csv](runs.csv), [SELF_CHECK.md](SELF_CHECK.md) | 16주행, 4비교, 약점 3건, Q1–Q7, 원영수증과 자체 점검 |
| [receipts/](receipts/), [measure.py](measure.py), [replay.md](replay.md) | 제품 WAV, 화면, 명령·stdout/stderr·exit, 두 판의 release/AppImage/ELF 지문, decoders, 다시 실행하는 실제 순서 |

① 사전 봉인 `9c076cd4792a4abc176020bed82bbba223d4ecb3` → ② 원장·배포 지문 `2a45a3b6ca2e81448c3e2daca7e2e876d5be0ade` → ③ 두 표·주관측 `95a82e63450886d706a815ad879e91a5fb9d3a31` → ④ 반례·정정 `188a408a9dbf1771bfc4b022b12d1534db2674eb` → ⑤ 결과·점검 `21b5e2199cc707a6954ec54f017d1c42aac9849b` → 원장 E02/E02b에 Q3 연결을 보정한 고정 결과 `8037f33f7e48668a116d237f731d8d13ffd6959b` → ⑥ 이 인계.

## 4. 고정 결과 재확인

| 실제 명령·검사 | 8037f33 결과와 포함 범위 |
| --- | --- |
| `python -m workbench.session check docs/workstreams/research/AF-RES-251/session.json --fetch` | exit 0, `remote_checked`. 작업 기점·계약·의존 SHA와 허용 경로 검증. manifest 외 501 변경 경로, 이탈·충돌·오류 0. |
| `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | exit 0, 시작과 종료 clean. doctor, acceptance, reference-audit discovery, original smoke, sessions 하위 호출 모두 exit 0. acceptance가 `scripts/check.py --require-git`으로 공통 55개, 두 lab 7개/9개, demo·독립 export·Git bundle 복원을 검사했다. |
| `check-all --fetch`의 실제 공통 검사 범위 | `no_active_sessions`, count 0, freshness `not_checked`. 이 작업의 `session.json`은 소유 경로에 있으며 위 개별 명령으로 remote check했다. |
| GitHub 새 checkout 재판독 | 결과 502파일, 원장 94행과 30저작/13계보, 상대 링크 187개, 두 필수 표 16/4행과 마지막 약점 3행 및 열 수, Q1–Q7을 대조했다. 봉인한 범위·입력·측정기 Git blob이 같고 변경 경로는 모두 소유 경로다. |
| PCM 및 SVG 재판독 | 총 36회분 Audacity WAV 64개를 커밋에서 꺼내 세 판독 경로와 지문·창 원값을 대조했다. 사전 교정 PCM 4개 해시가 일치했다. SVG 출력 2개의 크기와 2,500/8,000 변화도 다시 계산했다. |

개별 계약 확인 UTC 2026-11-25T00:35:14Z. 계약 stdout SHA-256 `16e0477165bf85043fd6da66e6497b25ed8b20feab45c894076f9711221421fd`, cloud stdout `9a168dc29ffbc2a515da87703dc6267e0cfad74e1614354a35f88ce9b657110d`, cloud JSON `54a7ca55c3f1d8ab93b769b5ec12904d6c16cc5a1dd060056e834fee6f76d683`. 두 runner stderr는 0 bytes였다. 현 Cloud의 저장소 검사는 Workbench의 Git·환경·lab 범위이며 제품의 외부 주장을 확인하는 범위 밖이다.

3.4.2 첫 기본은 실제 완료 화면과 WAV 둘을 읽어 성공으로 확인했다. 설정/완료 창 이름이 같아 처음 드라이버 exit 1은 보존했다. 라벨 편집기 초기 화면의 숫자 누락을 보완해 같은 16회를 별도 프로필에서 다시 찍었고 그 28개 WAV가 모두 기본 자료와 바이트까지 일치했다. Debian ABI에 맞게 호스트 libmount·libselinux·Pango를 우선 로드한 이유와 관련 실패는 원영수증에 있다. 다른 OS·stereo·solo·point label, 하드웨어 재생, 별도 독립 검토는 미확인이다. [초기 완료 화면](receipts/3.4.2/base-r1/failure.png) · [화면 재실행](receipts/screen-repeat/comparison.json) · [복구 영수증](receipts/diagnostics/)

## 5. 다음 첫 행동과 색인 제안

1. 통합 담당은 GitHub에서 `work/research-af-res-251`의 최신 HEAD와 이 문서의 고정 결과 SHA를 재조회하고 마지막 커밋 경로가 HANDOFF 하나인지 확인한다.
2. 별도 검토자는 고정 결과에서 3.4.2/3.5.0의 base·mute-b·swap-labels 원 WAV 및 숫자 화면을 비교한다. 새 폴더에 저장하는 GUI 단계와 `python verify_wav.py WAV_폴더`의 실제 입력은 [replay.md](replay.md)에 있다. 다른 플랫폼을 넓혀 검정할 때는 같은 네 fixture와 동일 임계·구간을 유지하고 [RESULT 마지막 표](RESULT.md)의 반전 조건을 먼저 본다.
3. 색인 제안은 **AF-RES-251 · Audacity Labels의 시간 경계와 믹스**, 자체 완료/독립 검토 대기, 3.4.2·3.5.0 공식 Linux PCM16 16회/28 WAV, AF-RES-230 의존 및 `8037f33f7e48668a116d237f731d8d13ffd6959b` 고정 근거다. 검색 축은 `top label track`, `audible wave tracks`, `mute`, `frame origin`, `Inkscape bbox/export-id-only`를 쓴다.
