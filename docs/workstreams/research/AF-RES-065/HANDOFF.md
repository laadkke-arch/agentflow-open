# AF-RES-065 · PARTIAL HANDOFF

## 상태 및 고정 판

**부분 인계. 완전 수용 불가.** 읽은 후보와 설명 가능한 대응은 있지만 첫20 모집의 원순번, 기간 내 명시 인용 사건 4자리, 역사적 채택 결정/배포 연결, 같은 입력·판 출력, 원저작 독해 최소20은 완료되지 않았다. 이 결손을 부재·실패 증명으로 일반화하지 않는다.

- 작업 저장소/브랜치: laadkke-arch/agentflow-open · `work/research-af-res-065`.
- 실제 읽은 foundation HEAD: `374dc309454e8847603c133c4c1d1029d63c0c92`. 계획 통합 기준: `028d16fee1121f5862efd410b78ec1d79d7080f2` (둘은 다름).
- 선행 인계: [AF-RES-061@bf9f27e](https://github.com/laadkke-arch/agentflow-open/blob/bf9f27eb67b1f72b243297c1672bea9b2524e4e4/docs/workstreams/research/AF-RES-061/HANDOFF.md). 선행 본문: `1ea731294c57c233ae164e3c31cd69c57b8896aa`.
- **고정 결과 커밋:** `796e7127babc7440fa3b1a0f2a400fee67b33326`. GitHub connector에서 해당 SHA로 [필수 표](https://github.com/laadkke-arch/agentflow-open/blob/796e7127babc7440fa3b1a0f2a400fee67b33326/docs/workstreams/research/AF-RES-065/RESULT.md), [수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/796e7127babc7440fa3b1a0f2a400fee67b33326/docs/workstreams/research/AF-RES-065/evidence/acceptance-evidence.json), [모집표](https://github.com/laadkke-arch/agentflow-open/blob/796e7127babc7440fa3b1a0f2a400fee67b33326/docs/workstreams/research/AF-RES-065/frame.csv)를 다시 fetch하여 각각 blob SHA `0fbc1504cc768c09a4f4a3deaad5a62921c648d5`, `9b9aacb9b008cafae45b6097ca30ed6961d34efd`, `0d1e5d25f66f100ea97fd0f4c32d3793b1d568cd`를 확인했다. 이 확인은 원장 전체의 의미/수치 검사나 실행 검사 아님.
- **첫 재개 파일:** [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/796e7127babc7440fa3b1a0f2a400fee67b33326/docs/workstreams/research/AF-RES-065/SCOPE.md) 다음 [frame.csv](https://github.com/laadkke-arch/agentflow-open/blob/796e7127babc7440fa3b1a0f2a400fee67b33326/docs/workstreams/research/AF-RES-065/frame.csv). 먼저 원순번을 확정하고 그 후 결과 표를 수정.

## 실제 분모와 판정

| 단위 | 실측/상태 |
|---|---|
| 요구 우선 계획 자리 | 8; 후보 원본문 8건 읽음, *첫 적격*으로 검증된 자리 0/8 |
| 인용 우선 계획 자리 | 4; 기간 내 적격 원 사건 0/4 확보, 공석 유지 |
| 후보/확정 고유 사건 | 후보 8건 / 모집 규칙 충족 확정 0 / 두 층 중복 미확인 |
| sources.jsonl | 15행. 여기에는 같은 프로젝트의 안내 자료, 원논문 일부 텍스트가 포함되며 **완결된 독립 원저작 독해20건이라고 셀 수 없음** |
| 인용 명시 / 당대 선택 이유 / 코드 diff→release / 동판 원출력 | 역사적 사건 기준 각각 확보 0. 검색 범위에서 발견 못함이지 실제 0이라는 단정 아님 |
| 같은 판 독립 실행 | 미실시 |
| 검사 | `workbench.session start` 미실시; `workbench.session check` 미실시, 종료 코드 해당 없음 |
| 검토 | 자체 점검만 수행; 독립 검토 0 |

## 주된 지식과 사용 경계

- [React Photo Album README](https://github.com/igordanchenko/react-photo-album#how-it-works)는 Knuth–Plass에서 영감을 얻은 행 분할 DAG를 명시. 이것은 최신 문서의 *직접 귀속*이지 선정 기간 중 인간 결정 사건의 입증이 아니다.
- [Verovio #113](https://github.com/rism-digital/verovio/issues/113)의 하나의 강제 `sb` 문제 및 [#515](https://github.com/rism-digital/verovio/issues/515)의 배치 후 전체 폭 맞춤 왜곡과 [MuseScore #23792](https://github.com/musescore/MuseScore/issues/23792)의 의도적 고정 페이지 요구는 보편 DP 추천의 반례/한계 후보.
- 다른 프로젝트의 원전을 사용자에게 돌려주려면 (a) 구현이 선택 변수/목적을 실제 공유하는지, (b) 강제/수동 제약을 어떻게 다루는지, (c) 원전 귀속·실제 수정의 증거가 있는지를 분리해야 함. 사용자 효과 실험은 미실시.

## 재개 첫 행동과 명령

Git checkout이 있는 실행 주체가 아래 시작 계약을 **실제로 실행하고 출력/exit code/HEAD**를 `evidence/` 아래 기록. 현재 GitHub 파일 쓰기 도구만으로는 Python workbench 실행이 불가능했다. 공통 진행표/색인은 배정 담당만 수정.

```sh
git fetch --prune origin
git switch work/research-af-res-065
python -B -m workbench.session start af-res-065 --allow docs/workstreams/research/AF-RES-065/ --dependency work/research-af-res-061=bf9f27eb67b1f72b243297c1672bea9b2524e4e4 --output docs/workstreams/research/AF-RES-065/manifest.json --fetch
# 원자료+수용 표 채운 후
python -B -m workbench.session check docs/workstreams/research/AF-RES-065/manifest.json --fetch
```

다음 최소 입력: 네 원 이슈 추적기의 기간별 `created_at`·ID·원본문으로 최초 적합 가능 20건씩 판정, 수신자의 원전 직접 인용 사건 찾기, 초기 commit/PR·merge·tag·fixture 연계. 검색 기록을 갱신한 다음 독립 원저작20 이상 **직접 본문 읽기** 완료. 이 인계는 검사가 끝난 결과물이라는 주장이 아니라 결손을 명시한 부분 인계다.

## 커밋과 정정

SCOPE → frame → search-log → sources → decisions → mechanisms → cards → SELF_CHECK → acceptance → RESULT 순으로 파일 단위 커밋했으며 결과 고정 SHA는 위 참조. 실제 원순번과 시각이 확인되지 않아 ‘선정된 최초 사건’으로 기록하지 않고 전부 ‘provisional’로 후퇴시킨 것이 중요한 보수적 정정이다. 이번 대화에서 새 결과로 과거 AF-RES-061의 예측 수치를 변경하지 않았다.

**색인 반영 제안:** AF-RES-065 / 인쇄 문단 전체 분할→사진 행·악보 시스템의 대응과 이탈 / 부분 인계 / 결과 `796e7127babc7440fa3b1a0f2a400fee67b33326` / 고정 대상 Flickr justified-layout, React Photo Album, Verovio, MuseScore / 주결손 최초모집 검증·인용 사건·동시대 결정연쇄·동판 출력 / 첫 파일 SCOPE + frame.

## 가장 중요한 불일치·약점 3건 및 다음 조사

1. **원순번이 미확정:** 선후 모집의 표본 선택편향. [Flickr 이슈 목록](https://github.com/flickr/justified-layout/issues)과 나머지 3개 tracker의 기간 내 created_at/ID 정렬 첫20을 직접 판정; 8자리가 교체되면 표1 다시 산출.
2. **현재 README 인용 vs 당시 결정:** [React Photo Album How It Works](https://github.com/igordanchenko/react-photo-album#how-it-works)의 실제 최초 추가 SHA·작성자·시점을 Git blame/PR과 비교; 인용이 기능 구현보다 늦으면 역사적 채택 주장을 버림.
3. **실제 출력·비용 검증 없음:** [Verovio #515](https://github.com/rism-digital/verovio/issues/515)의 원 명령과 태그·fixture·이미지를 고정해 원 출력/대안 출력을 대조; 같은 input의 사용자 목표를 측정해야 수신 결정의 유효성 판정 가능.
