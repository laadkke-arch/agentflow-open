# AF-RES-157 HANDOFF · PARTIAL

실제 예시 개봉과 같은 참가자·과제의 전후 영속판을 조인한 엄격 확인은 **0/8쌍, 0/2연구**다. Sketchy 파일럿 196행을 전체 받아 원판, 구조, 스냅샷을 검사했다. 해당 CSV에는 직전 저장, 정확한 개봉 시계, 과제 키가 없다. Sketchy의 저자 DB, Delft ZIP과 VIS OSF 원파일은 취득이 막혀 내부 적격 수가 미확인이다. 원자료 기반의 개인 변경·실제 무변경·효과 방향은 보류한다.

- 작업 `AF-RES-157` #1, 단일 Codex Cloud 작업자. 자기검산 수행, 독립 검토 미실시.
- 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-157`. 허용 경로 `docs/workstreams/research/AF-RES-157/`. 실 시작 `ff2302a9c02fe72eea915dc1612d1791d5c780ec`. 계획판 `ff5a037d4926e5c3ce6032bfa22c75b62f3c6aa8`보다 4커밋 앞이고 차이는 진행표 한 경로다. 이번 브랜치 diff는 허용 경로 안에서 확인했다. [SCOPE](SCOPE.md)
- 선행 핀은 `work/research-af-res-153@12eb394eff4c556b47925f791d8aa42d7b09d86a` 하나다. [선행 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/12eb394eff4c556b47925f791d8aa42d7b09d86a/docs/workstreams/research/AF-RES-153/HANDOFF.md)
- **결과판 `b82bafda1355a6e5160b58db70019e5a8c6fa4d4`.** [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/b82bafda1355a6e5160b58db70019e5a8c6fa4d4/docs/workstreams/research/AF-RES-157/RESULT.md)와 [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/b82bafda1355a6e5160b58db70019e5a8c6fa4d4/docs/workstreams/research/AF-RES-157/SELF_CHECK.md)를 확인했다. 인계판은 그 다음 별도 HANDOFF 커밋이고 원격 확인 SHA는 응답에 표시한다.

## 원격에서 확인한 묶음

| 묶음 | 커밋 SHA | 직접 다시 연 대표 파일과 blob |
| --- | --- | --- |
| ① 범위·규칙 | `0b545f949368c509fcec388b9952fdd1ebd02ed1` | SCOPE.md `001daa044b9c0c6698fc05b30e052da51063c1fd` |
| ② 취득·선정 봉인 | `e2131c1447d9fe541aad5cd9bc61492b9ed5ec15` | selection.csv `b1987f703854c97c7b8f5838633ddb0db825ee2f`, archive.csv `16fe71b26b546aeba18924308f432605bc46bf27` |
| ③ 판독·본 관측 | `e9aeda09ce752fbeae4e7c83f1dc17e0e60e4e8e` | pairs.csv `9b4dd89c571dd198d1da90caa2caec9fe43ed8d0`, pilot-snapshots.json `c19b733a100c77d4eabe8533e27352fbe89cacec` |
| ④ 대조·반례·비용 | `f9a75ff4cdd1f65d7a5a108db9ced8acaf9ea047` | contrasts.csv `ff4fa62b8c679535de6032005dcf171fabb97409`, production-before-after.json `d5d397e90a90fac9df0a7f61dfffb5e86f08b1f3` |
| ⑤ 결과·자기검산 | `b82bafda1355a6e5160b58db70019e5a8c6fa4d4` | RESULT.md `dc002ae8827909d7e721e5475f407da0c6dc6a8c`, SELF_CHECK.md `efe5334af5c4e019ad4fb198518ba588424b77b2` |

## 관측한 근거와 시험 범위

- 파일럿의 숫자 참가자×완료 참조 57개 모두 과제와 세 사건의 증명이 결측이다. 같은 완료 참조의 추가 139행과 양쪽 역할의 배열이 같은 62행은 직접 관측했다. 실제 사람이 동일 작품을 다시 저장했는지는 미확인이다. Fig. 7의 before/예시/after 위치 4개는 저자 레이블·캡션에 있고 원행 ID 및 픽셀 판독은 미확인이다. 보충 VIS 및 확장 B04/B06/B09의 개인 원자료도 미확인이다. [pairs.csv](pairs.csv), [내용 집계](evidence/pilot-snapshots.json)
- 82자료행을 재계수하고 고유 1차 저작 20개를 산입했다. 실험 8, 독립 버전·이벤트 기록 4, 실제 예시 원작·제작 4, 유전비평판 2, 공개 제작 타임라인 2다. 스토리보드 분야는 제작 전후 파일의 실제 편집 구조를 읽은 두 건이다. 그림 보드 개정판 자체만 인정하면 18이다. B07의 저자 업로드 제3자 호스트, 확인하지 못한 Blender Studio 판, 목록·중복판은 제외했다. [sources.jsonl](sources.jsonl)
- 두 독립 임시 공간의 [④ 재생 A](evidence/replay-fresh-A.json)와 [④ 재생 B](evidence/replay-fresh-B.json)에 전체 명령·UTC·종료·지문이 있다. ⑤ 결과판을 다시 두 새 클론에 checkout하고 2026-11-24T17:33:54–17:34:06Z에 동일 재생과 계약을 실행했다. 플랫폼 Linux, Python 3.12.14, Git 2.52.0, curl 8.14.1. 각 공개 raw GET은 200과 15,062,721 B, SHA-256 `aec34f174ac350448b62a2223a859303ae496f99ba526775e027e914a4a1afbc`. 파일럿 엄격 0, 인공 기준 2/민감도 2, 선정·후보·원장·스크립트 지문과 재생 출력 6개의 바이트가 모두 일치했다. 원장 SHA-256 `9a17bcd41a1dc0dcb45dd2bea7bb0a20b680f8a1fe67480109d424b5558adea9`.
- ⑤ 양쪽에서 `python -m workbench.session check docs/workstreams/research/AF-RES-157/session.json --fetch` 종료 0, `remote_checked`, 통합 `ded3420249a3d60ebbb578a8432cf262d3ffa7d7`, 계약 SHA-256 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`, manifest 지문 `456163570fdd1fcf8e28298b247355632fe4ed37ecb0146f0da13da6dd36a5e2`. ⑤ 한 새 클론에서 `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` 및 그 안의 doctor/acceptance/research-case/original-smoke/sessions 종료 모두 0. 공통 `check-all`은 `docs/tasks` 위치에서 활성 세션 없음으로 표시했다. 소유 경로 안의 manifest 확인은 위 명시 명령 결과를 사용했다. Windows/Actions, 외부 원파일 미취득본 재생, 새 독립 검토 미실시. 결과판에는 29개 파일이 있고 manifest 제외 보고 변경 경로 28, 외부 경로 0이다.

색인 제안 · AF-RES-157 PARTIAL — Sketchy 파일럿 전수 구조/스냅샷 재생, Delft·OSF·DB 취득 미해결, 엄격 0/8, AF-RES-153@12eb394 의존, 결과 `docs/workstreams/research/AF-RES-157/RESULT.md`.

## 다음 첫 행동과 재개 입력

공개 아카이브에 연결되는 실행 환경에서 **Apollo item의 ORIGINAL bundle과 정상 Download 링크부터 열기**. [Apollo item](https://www.repository.cam.ac.uk/items/e7dd30c8-2262-4d11-86ea-5d59dc347498)과 [DOI](https://doi.org/10.17863/CAM.69091)의 도착점, 실제 바이트, SHA-256, ZIP test를 기록한다. 이 시도의 관리형 셸에서 해당 호스트·OSF·Drive는 proxy 403으로 curl 22, 웹은 timeout/403/size limit, Desktop은 Browser Use requirements 및 Chromium AT-SPI 오류였다. 파일 미취득 상태는 확정했고 원자료 공개 자체의 부재는 미확인이다. [실패 원장](archive.csv)

이후 OSF 할당의 공개 목록·파일을 받고, 저자 DB가 접근되면 비식별 참가자·과제·이벤트·판의 export를 확인한다. 이름·설문·계정 정보가 섞인 백업은 원형 게시와 실명 조인 없이 비식별 입수판을 확인한다. 재취득 후 실제 과제·열기·저장 키를 확인한 뒤 앞선 선정판과 별도 보정 커밋을 남긴다. Q7의 신뢰 수준을 올리려면 동일 컷 렌더와 무예 조건을 별개로 확인한다.

```sh
git clone --single-branch --branch work/research-af-res-157 https://github.com/laadkke-arch/agentflow-open.git af-res-157-replay
cd af-res-157-replay
git checkout --detach b82bafda1355a6e5160b58db70019e5a8c6fa4d4
AF157_DIR=docs/workstreams/research/AF-RES-157
python -m workbench.session check "$AF157_DIR/session.json" --fetch
python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
python -B "$AF157_DIR/replay/check_ledgers.py"

AF157_TMP="$(mktemp -d)"
curl -fLsS 'https://api.repository.cam.ac.uk/server/api/core/items/e7dd30c8-2262-4d11-86ea-5d59dc347498/bundles' -o "$AF157_TMP/apollo-bundles.json"
curl -fLsS 'https://api.osf.io/v2/nodes/sbp2k/files/' -o "$AF157_TMP/osf-providers.json"
curl -fLsS 'https://api.osf.io/v2/nodes/sbp2k/files/osfstorage/' -o "$AF157_TMP/osf-files.json"
```

Apollo의 실제 ORIGINAL 묶음에 열리는 bitstream 링크를 쓰고 `sha256sum delftdata.zip`, `python -m zipfile -l delftdata.zip`, `python -m zipfile -t delftdata.zip` 순으로 검사한다. OSF는 응답의 공개 provider와 개별 `links.download`를 따라간다. CSV 고정 다운로드·선정·인공 조인 입력과 동일성 검사 명령은 [replay/README](replay/README.md)에 있다.

| 불일치·약점 | 영향을 받는 결론 | 다음 조사·자료 | 결론을 바꿀 관측 |
| --- | --- | --- | --- |
| 미취득 DB/ZIP/OSF 및 파일럿 세 사건 결측 | 실제 엄격쌍 수와 변경 여부 미확인 | 공식 소스의 공개 비식별 파일·지문과 전후 버전 키 | 2독립 연구에서 실제 개봉과 직전·직후 판을 4쌍씩 연결 |
| 저장 시계·대조·기저·탈락 원표 결측, 작품이 예시 선택을 선행 | 개인 자발 열람 연관과 배정 효과 방향 미확인 | 시간 보정, 실제 개봉, 무예/지연 원표, 같은 과제의 기저와 사후 | 동률·다중 자극과 결측을 제외한 재생에서 대조 방향이 유지되거나 뒤집힘 |
| 선택 사례, 동일 배열, 제작판은 실제 동기·기능과 서로 다른 근거 | 작동 이식·독자 및 사용자 효과를 말할 범위 제한 | 열기/설계 원판, 상태·보존값 확인을 위한 실행 또는 렌더 | 원래 같은 선택이 있던 판, 실제 사용의 기록 또는 재생 결과의 기능 차이가 발견됨 |
