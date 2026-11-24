# AF-RES-218 HANDOFF · DONE

## 작업과 판정

- 시도 1, Codex Cloud의 Linux x86_64. FITS 실행은 CPython 3.11.15, NumPy 1.26.4, Astropy 6.0.1 W03의 해시 잠금이다. 데이터는 overlayfs의 임시 폴더에서 생성한 무스케일 PrimaryHDU만 사용했다. [환경](receipts/runtime.json) · [wheel 대조](receipts/wheel-check.json) · [입력](inputs.json)
- 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-218`, 소유 경로 `docs/workstreams/research/AF-RES-218/`. 시작 SHA `87ffc1539bcf33da0fccf45eb15982a02d93e409`. 계획 기준 `bb146773bbffba5e724e8c842951e2c25198c2da`와의 차이와 의존 AF-RES-205 `3853289f5189ad8af242c0f62d6cad566f31bc66`의 착수 판정은 기록에 있다. [범위](SCOPE.md) · [계약](session.json) · [205 고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/3853289f5189ad8af242c0f62d6cad566f31bc66/docs/workstreams/research/AF-RES-205/HANDOFF.md)
- 마지막 결과 SHA는 이 인계 직전 `9403bd6c5bf2bde59f8a1d9ada2a77fd77e7e04f`다. GitHub에서 가져온 별도 checkout으로 표·출처 원장·반례·실행 영수증을 다시 대조했다. [고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/9403bd6c5bf2bde59f8a1d9ada2a77fd77e7e04f/docs/workstreams/research/AF-RES-218/RESULT.md) · [고정 자체점검](https://github.com/laadkke-arch/agentflow-open/blob/9403bd6c5bf2bde59f8a1d9ada2a77fd77e7e04f/docs/workstreams/research/AF-RES-218/SELF_CHECK.md)

| 완료 근거 | 실제 관측 | 대표 파일 |
| --- | --- | --- |
| 선행 호출 | 205의 첫 적격 `A01-A1.false` 두 원영수증에서 원 ndarray `0.0 → 99.0`, 출력 m/s. 같은 호출의 네이티브 float64·big-endian 힙과 FITS 매핑 양립을 확인 | [R02 예비 원출력](receipts/preflight.json) · [선행 연결](inputs.json) |
| 본시험 12자리×2 | 24/24에서 메모리 HDU `0.0 → 99.0`. 같은 경로는 `update` 8회에서 대입 직후부터 종료 뒤까지 `99.0 m/s`, `readonly`·`copyonwrite` 16회에서 `0.0 m/s`와 기준 바이트. 별도 reader 84회 모두 종료 0 | [집계](persistence.csv) · [R03 본시험 원영수증](receipts/matrix.jsonl) |
| FITS 통제와 외부 분야 | 새 경로만 99.0, 헤더 해시만 변경, 깊은 사본, 무쓰기 close, 매핑 없는 update의 flush 뒤 가시성, 기존 파일 저장 거부. SQLite의 WAL 읽기 스냅샷과 rollback journal의 커밋 재시도 합성 2건 | [반례·정정](COUNTEREXAMPLES.md) · [R05 FITS 통제](receipts/controls.jsonl) · [R06 SQLite 영수증](receipts/sqlite-command.jsonl) |
| 직접 원자료 | 33/22, 종류별 11/4·10/8·4/4·4/3·4/3. 원장 59행 및 고유 계보 8 | [원장](sources.jsonl) · [모집표](frame.csv) |

완료 조건의 부족 항목은 0이다. 파일 잠금·경쟁 쓰기·크래시 및 전원 상실, 다른 OS·스케일·압축 영상은 미검사다. 작성자가 자체 검토했다. 독립 연구자 검토는 미실시다. 초기 uv 설치의 정확한 시작 UTC는 미기록이며 출력의 마지막 쓰기 시각과 종료코드를 남겼다. [자체점검](SELF_CHECK.md) · [설치 영수증](receipts/setup.jsonl)

## 고정 결과 검사

2026-11-24 21:57 UTC, 깨끗한 GitHub checkout `9403bd6c5bf2bde59f8a1d9ada2a77fd77e7e04f`에서 확인했다. 기준 FITS의 SHA-256은 `0036084179bc9c0b4d7d7ec5c57eac218bdca3d931be05343201a4a7a81bd720`이다. 24행과 통제 6행을 원로그에서 재생하고 저장 CSV와 두 번의 `cmp` 종료 0으로 일치시켰다. 표의 첫 세 묶음, Q1–Q7, 마지막 약점 3행, 내부 링크와 원장·반례를 대조했다. [재현 명령과 입력](receipts/README.md) · [R07 본시험 재생](receipts/matrix-replay.jsonl) · [R08 통제 재생](receipts/controls-replay.jsonl)

```sh
python -m workbench.session check docs/workstreams/research/AF-RES-218/session.json --fetch
python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

- 개별 계약은 exit 0, `passed`와 `remote_checked`. 확인 통합 SHA는 `fc095c323d0177401d34f1daa7b4d1c529e2351f`였고 그 시점까지 시작점 이후 통합판의 차이는 진행표 한 파일이었다. 의존 SHA와 공통 계약 지문 일치, 허용 경로 밖 변경·충돌 0. stdout SHA-256 `b965f2d86da5e123c17903d6f6b18d19433cae8674bd57ada3ef084968edd20c`.
- 공통 Cloud 검사는 exit 0, Python 3.12.14/Git 2.52.0에서 공통 55개와 두 lab 7·9개, smoke와 Git bundle 복원을 통과했다. 전체 manifest 목록은 `no_active_sessions`였고 이 과제는 위 개별 계약으로 확인했다. stdout SHA-256 `618c4a18afdff80710bc9e124db5479bdc9b22377aa7c1f4caaf3f1672dcd1f3`. 두 검사 모두 stderr가 비었다.

## 다음 첫 행동과 색인 제안

통합 담당은 `work/research-af-res-218`의 마지막 커밋에서 이 인계를 읽고, 고정 결과의 [persistence.csv](persistence.csv)와 [반례의 새 경로·헤더 통제](COUNTEREXAMPLES.md#같은-초기-fits에서-관측한-반례)를 대조한다. 확인 뒤 아래 사례를 현재 색인에 반영할 수 있다. 스케일이 있는 새 사례를 이어받으면 `inputs.json`의 정확 환경 아래 별도 합성 파일에서 BSCALE/BZERO와 원시·물리 픽셀을 먼저 고정한다. 기존 재실행의 입력과 명령은 [영수증 안내](receipts/README.md)에 있다.

**색인 제안** · AF-RES-218 DONE · Astropy 6.0.1에서 동일 HDU 수정의 원경로 재열람 및 새 파일 경계 · [RESULT](RESULT.md) · 의존 AF-RES-205 `3853289f5189ad8af242c0f62d6cad566f31bc66`.

## 커밋

1. `766003f1af2cfb6983a874951b04a8dd5eb206fc` 범위·판정·작업 계약
2. `b6f1f3212d7d43a5cbb8d6d3c5b2c249610a2b3d` 모집표·직접 근거
3. `49d7efb21a3bd5d8d6a3a2c709d271b82188d405` 본시험·표 초안·영수증
4. `1f417a1ea08cf0955d65fd6307b46017852bbce5` 반례·SQLite·정정
5. `9403bd6c5bf2bde59f8a1d9ada2a77fd77e7e04f` 결과·자체점검
6. 이 인계 문서
