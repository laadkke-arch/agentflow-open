# AF-RES-081 역사판과 사전 관측 약속

배정 계획 SHA는 `e7a777f2c13b626532b5828591d6388743688b34`다. 배정 브랜치가 원격에 없음을 `git ls-remote`와 GitHub 브랜치 조회로 확인했다. 2026-11-23 UTC 실제 출발점은 그 후손이자 확인 당시 통합판 `f736bd557fa4c40aecb6833165823196cfa42af2`다. 해당 GitHub 통합판의 AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, RESEARCH_BRIEF 및 AF-RES-081 진행표 항목을 읽었다. `work/research-af-res-081`의 이 경로에만 결과를 둔다. [실제 출발점](https://github.com/laadkke-arch/agentflow-open/commit/f736bd557fa4c40aecb6833165823196cfa42af2)

`python -B -m workbench.session start af-res-081 --allow docs/workstreams/research/AF-RES-081/ --dependency work/research-af-res-077=a6338ffd6bc04d45f97e211031bd22aa870fbba0 --output docs/workstreams/research/AF-RES-081/manifest.json --fetch`가 exit 0을 반환했다. 의존 결과는 077의 인계, RESULT Q4–Q8, CASEBOOK의 MS, TESTS MS-N/E/X, ERRATA E3/E5/E6, native RUNBOOK이다. 077의 두 판독은 L 계열을 골랐고 고정된 세 입력에서 G와 같은 예상을 냈다. 077의 MuseScore 목표 실행은 0/3이었다. TEI는 077이 고정한 4.8.0의 지정 부분을 직접 다시 열며 신규 원전 검색을 생략한다. [077 인계](https://github.com/laadkke-arch/agentflow-open/blob/a6338ffd6bc04d45f97e211031bd22aa870fbba0/docs/workstreams/research/AF-RES-077/HANDOFF.md)

## 비교 원형

| 표기 | Git commit / tree | 용도 |
| --- | --- | --- |
| 부모 1 / U | `f4fcf53ff65c56f0efb616a3af209d3faba9b342` / `c69a857919e8c44677df1d93e39e14919914d0d7` | 2019-03-07 09:41:37 UTC, 3.1.0 unstable. 세 빌드 공통 소스 |
| 부모 2 | `3cfc174c665b01e57ef374fbb990c8f36910019a` / `bc274172b0c4028ed72410dbb93723eb3b86c004` | ericfont의 선택 비트 변경, 작성 2019-01-16 04:57:06 UTC |
| 병합 / G의 패치 원전 | `16851045c9e50eafb016c5cf4f2733f974e841bf` / `3d3a5877c9a5ff53a666a29bba49d9426e4a7efd` | 2019-03-07 09:53:22 UTC. 부모 1 기준 `libmscore/element.cpp` 한 줄 추가 |
| L | U에 여기서 구현한 생성 경계 패치 | 새 part score에 속하는 방문 요소와 spanner의 SELECTED만 파트가 반환되기 전에 정리 |
| 077의 v3.0.1 | `06a66a2206fc5f3c2c33d7ee4123badf496bc4dd` / `c21d5c276341f2f14715994446d1cf1c8d9fae4d` | 2019-01-15 tag. 01-08 신고 후, 01-16 PR 전 |
| 신고판 후보 태그 v3.0 | `c1a5e4c882b9687fead02a017513f17b6c1521a3` / `af8a71e4e2ac3e554227bc7ee97959d3585f8e15` | tracker의 Reported version 3.0과 같은 표기. reporter binary 지문 미확인 |
| 신고판 후보 태그 v2.3.2 | `45924076871483cb96b859cc374c5fbdbf76ba53` / `76b448c3969da62937db86221f6dca5166e08f54` | tracker 본문에서 별도로 언급한 판. reporter binary 지문 미확인 |

서로 다른 tree SHA를 동일 소스로 묶지 않는다. G는 첫 부모 diff 한 줄만 사용하는 연구 빌드다. G의 패치 내용, L의 연구 구현, 공통 native 테스트 타깃 및 현대 의존 환경을 따로 검산한다. [PR 원문](https://github.com/musescore/MuseScore/pull/4590) · [두 부모와 변경 파일](https://github.com/musescore/MuseScore/commit/16851045c9e50eafb016c5cf4f2733f974e841bf) · [v3.0.1 릴리스](https://github.com/musescore/MuseScore/releases/tag/v3.0.1)

원 tracker #281441의 직접 열람은 403을 반환했다. 작성자·2019-01-08·두 신고 버전은 077이 읽은 부분 캐시와 이번 PR 원문을 근거로 쓰고, 첫 revision과 전체 이력은 미확인으로 둔다. 원 조건은 master에서 노트를 선택한 채 새 part를 만들 때 선택 목록 없이 선택 표시가 남지 않는 것이다. 링크, 별도 part의 음·배치, undo, 저장·재열기는 연구 보존 조건이다. [tracker](https://musescore.org/en/node/281441) · [077 ERRATA E5](https://github.com/laadkke-arch/agentflow-open/blob/a6338ffd6bc04d45f97e211031bd22aa870fbba0/docs/workstreams/research/AF-RES-077/evidence/ERRATA.md#e5--재개에서-확보한-musescore-tracker의-부분-캐시와-시간-순서)

## 입력과 비교 단위

- 여섯 자리 모두 독자 작성한 `two-parts.mscx` bytes를 사용한다. SHA-256은 `c88ee55c6cb5fce96eca83f643a8569d909fd8029d27f23e6cf54a812f339991`이다. 마스터의 Flute는 track 0, C4=60과 fingering 1이다. Oboe는 track 4, G4=67과 offset 0.75 spatium이다. 첫 마디 4/4, tick 0, whole note 하나씩이다. P2(Oboe)를 먼저 생성하는 공통 준비 직후 해당 조작의 입력 상태를 만든다. 복제 P1(Flute)은 생성 전 공석이다.
- 음표 위치 키는 score 역할(마스터 또는 excerpt 제목), 첫 마디의 tick 0, track, Chord의 음 순번 0이다. `Fingering`은 그 음의 첫 동종 자식이다. `C1`은 E05의 마스터 track 1 새 음이다. pitch나 포인터 주소를 재열람 식별자로 쓰지 않는다. 주소는 동일 프로세스에서 객체, 선택 목록, 링크 상대를 맞추는 데 쓴다. 저장 전후 비교는 위치와 링크 상대의 역할을 사용한다.
- 시작, `createExcerpt` 또는 `cloneVoice` 반환 직후(명령 종료 전), 명령 종료 후, 적용되는 편집/undo, 저장 직전, 재열기 뒤를 기록한다. 선택 비트, Selection 상태·전체 목록·해당 객체 membership, mark, 원색/curColor, printing·drop target·visibility를 동시에 읽는다. 음 높이와 tpc, offset, link peer, 두 악보의 관계를 별도로 확인한다. mark가 없는 형식은 필드 적용 불가로 기록한다.
- 새 part 중첩 선택을 점검하는 E03은 Chord→Note→Fingering을 방문한다. E05는 일반 비링크 `cloneVoice` 하위 API의 두 번째 성부 출력이며, 독립 메뉴나 Ctrl+C/V를 눌렀다는 증거로 계산하지 않는다. E06은 실제 sequencer가 쓰는 `setMark`로 주입하는 표시 대조다. 시각 입력 없이 같은 mark 조건을 고정한다. E01–E04는 UI가 호출하는 모델 경계에 대한 native 실행이다.
- 예상 G/L 동일은 E01–E04·E06, 상이는 E05다. E01·E03·E04의 U는 원 비트를 계승할 것으로 예상한다. E03의 신고 범위 확장은 자식 coverage 조건이다. E06에서 세 빌드의 mark와 선택색이 남아도 selection ghost로 채점하지 않는다. 저장된 재열기 음·링크가 같은 것만으로 생성 직후 동일이라고 채점하지 않는다.
- 입력 순서 E01–E06 안에서 U·G·L 순번 01–18, 각 2회가 계획 분모 36이다. 모델 조작 층 12셀/24회, API 대조 층 6셀/12회, 화면 조작은 별도 층이다. 기록 상태는 실행 완료, 실행 실패, 미실행을 구분하고, 누락 필드는 별도로 집계한다. 종료 코드·출력과 위치 키·피치·링크·선택을 검증한 뒤 비교한다. 반복 원시 주소와 경로를 정규화하며 원 출력은 그대로 보존한다.
- 차이가 있어도 양쪽의 결함 여부는 계약 근거로 좁힌다. 원 신고 위반은 E01·E04의 새 part 음표에서 flag=1/membership=0이면서 선택색일 때이다. 외부 clone의 차이는 기존 consumer가 해당 비트에 의존하는지 별도 근거가 있어야 요구 우열을 부여한다. 값이 동일한 경우와 필요한 필드가 빠진 경우도 구분한다.

예상과 최소 반증은 [cases.csv](cases.csv)에 봉인한다.
