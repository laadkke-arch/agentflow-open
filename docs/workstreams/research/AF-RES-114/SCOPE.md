# AF-RES-114 모집과 판정 계획

봉인 1. 한국어 표기가 후보를 조사 목록에 넣는 효과와, 읽은 절의 대상 역할을 확인해 표시 순서를 바꾸는 효과를 같은 24자리에서 비교한다. 자료집의 직접 답 공급, 조사 12, 표시 3을 각각 추적한다. 이슈 검색과 순위 실행 전 계획이다.

## 시작과 선행 읽기

- 계획판 `670ecde1dab07aede6760618a7d907f0cdff185a`. 첫 GitHub 조회는 `3839d730271a9a7f2f909be9cca5526299a4d929`였다. 생성 직전 조회한 통합 HEAD와 실제 시작판은 `581b863dfb9f90106c2a07fb749d0cada51b0a25`였다. 계획판 이후 `2d23de9`, `3839d73`, `581b863`의 변경 파일은 모두 중앙 진행표다. 앞의 두 커밋에서 작업 추가와 Codex 배정 상태를, 세 번째에서 같은 회차 Pro 작업의 상태 갱신을 확인했다.
- [시작 규칙](https://github.com/laadkke-arch/agentflow-open/blob/581b863dfb9f90106c2a07fb749d0cada51b0a25/AGENTS.md), [상태](https://github.com/laadkke-arch/agentflow-open/blob/581b863dfb9f90106c2a07fb749d0cada51b0a25/STATE.md), [Dot 규칙](https://github.com/laadkke-arch/agentflow-open/blob/581b863dfb9f90106c2a07fb749d0cada51b0a25/docs/DOT_AUTOMATION.md), [제품 브리프](https://github.com/laadkke-arch/agentflow-open/blob/581b863dfb9f90106c2a07fb749d0cada51b0a25/docs/product/RESEARCH_BRIEF.md), [연구 규칙](https://github.com/laadkke-arch/agentflow-open/blob/581b863dfb9f90106c2a07fb749d0cada51b0a25/docs/RESEARCH_WORKFLOW.md), [진행표 AF-RES-114·110 행](https://github.com/laadkke-arch/agentflow-open/blob/581b863dfb9f90106c2a07fb749d0cada51b0a25/docs/automation/dot-control.json), [시작 안내](https://github.com/laadkke-arch/agentflow-open/blob/581b863dfb9f90106c2a07fb749d0cada51b0a25/docs/START_HERE.md)를 읽었다. AF-RES-114 행은 RUNNING, 시도 1, 직접 선행은 AF-RES-110이다.
- AF-RES-110의 진행표 상태는 DONE이고, `281b661f9b17e07483f20834859fa157b4846c75` [인계](https://github.com/laadkke-arch/agentflow-open/blob/281b661f9b17e07483f20834859fa157b4846c75/docs/workstreams/research/AF-RES-110/HANDOFF.md)는 최초 제출본과 독립 판독의 결손으로 연구 수용 범위를 PARTIAL로 한정했다. 검증 대상 `4e7c060377669896ca3e03446ce386ba053a1b16`의 [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/4e7c060377669896ca3e03446ce386ba053a1b16/docs/workstreams/research/AF-RES-110/RESULT.md), [truth](https://github.com/laadkke-arch/agentflow-open/blob/4e7c060377669896ca3e03446ce386ba053a1b16/docs/workstreams/research/AF-RES-110/truth.csv), [ranks](https://github.com/laadkke-arch/agentflow-open/blob/4e7c060377669896ca3e03446ce386ba053a1b16/docs/workstreams/research/AF-RES-110/ranks.csv), [summary](https://github.com/laadkke-arch/agentflow-open/blob/4e7c060377669896ca3e03446ce386ba053a1b16/docs/workstreams/research/AF-RES-110/evidence/summary.json), [검사 기록](https://github.com/laadkke-arch/agentflow-open/blob/4e7c060377669896ca3e03446ce386ba053a1b16/docs/workstreams/research/AF-RES-110/evidence/acceptance-evidence.json)을 GitHub에서 가져와 읽었다. truth 144행의 직접 적격은 Q-PA/PA-G2 1개, ranks는 864 조사 슬롯 행이다. 한국어 메모로 새로 표시한 세 자리는 충돌이었다. 파일 헤더와 UI 모듈 헤더, 산출 코드의 Python 판과 빌더 런타임 판이 달랐다. 이슈·영어 순위·마침표는 이번 재생 입력에서 제외한다.
- 의존 SHA와 쓰기 경로는 [manifest](manifest.json)에 고정했다. 같은 회차의 다른 세 결과를 입력으로 삼지 않는다.

## 후보 모집

문서 기준은 `2026-11-24T00:00:00Z` 이전 발행 안정판이다. 배정에 별도 시각이 없어 해당 UTC 날짜의 시작을 사용했다. Blender 5.3과 Krita Manual 5.3.0의 언어별 발행판과 원본 계보를 확인한다. Blender dev/5.4 및 Qt 기반 Krita 앱 패치번호를 매뉴얼 판과 별도로 기록한다. 상위판에서 두 언어판 대응 증거가 결손이면 확인한 쌍과 조사 자리 둘 다 보존한다.

| 프로젝트 | 층 | 영어 목차 구획 | 추출 단위 |
| --- | --- | --- | --- |
| Blender | 마스크·레이어 | [Compositing → Mask Nodes](https://docs.blender.org/manual/en/5.3/compositing/types/mask/index.html) | 목차에 나오는 실제 노드. 레거시와 현행은 구현 심벌/입력이 별개일 때 각각 한 기능 |
| Blender | 합성·출력 | [Compositing → Filter Nodes](https://docs.blender.org/manual/en/5.3/compositing/types/filter/index.html) | 노드 소구획을 원순서 깊이 우선으로 펼치고 조작 없는 제목은 건너뛴다 |
| Krita | 마스크·레이어 | [Reference Manual → Layers and Masks](https://docs.krita.org/en/reference_manual/layers_and_masks.html) | 목차 항목별 특유의 편집 조작. 일반 소개 링크는 제외 |
| Krita | 합성·출력 | [Reference Manual → Render Animation](https://docs.krita.org/en/reference_manual/render_animation.html) | 위에서 아래로 General, Export as Image Sequence, Export as Video의 조작/설정 항목. First/Last는 한 프레임 범위 조작의 두 매개변수. 명명, 경로, 번호, 프레임 선택은 별도 사용자 조작 |

구획별 첫 여섯 고유 조작을 유지한다. 미번역, 실제 답의 유무, 유명세, 결과 순위, 접속 실패 때문에 뒤 항목으로 교체하지 않는다. 고유 키는 프로젝트·경로·노드/설정이다. 원 절의 영어 키와 한국어 PO의 msgid·문서 경로를 대조한다. fuzzy, 빈 msgstr, 다른 키, 원 PO 미확인, 배포 HTML 불일치 상태를 남긴다. 검색 별칭의 1차 분석에는 같은 키·역할과 해당 판의 실제 한·영 표시를 확인한 비공백 한국어 표제만 넣는다. 영어 UI 심벌은 영어 본문에서 확인한 형태를 기록한다.

## 요청 모집과 노출

- 공식 `blender/blender`의 Issues와 KDE Bugzilla product `krita`의 공개 요청에서 생성 UTC `[2023-01-01, 2026-01-01)`를 사용한다. PR, 댓글만의 일치, 문맥상 대상 없는 시스템 로그를 배제한다. 영어 제목 또는 최초 작성자 게시물의 공개 현재판에서 유니코드 단어 경계 기준 `mask(s|ed|ing)?`, `layer(s|ed|ing)?`, `composit(e[sd]?|ing|or[s]?|ion[s]?)`, `export(s|ed|ing|er[s]?)`을 대소문자 없이 찾는다. 서버가 댓글/변경 시각도 검색하면 작성자 본문과 생성 UTC로 다시 거른다. 프로젝트별 첫 40개, 동시각은 정수 ID순이다. 원문의 동작·대상과 독립 보존 조건이 함께 관측된 첫 세 건을 선발한다. 읽을 수 있는 처음 목록과 40/41 경계의 범위를 기록한다. 순서를 입증하지 못한 발견 표본은 탐색 층에만 두며 예약 자연 슬롯을 비워 둔다.
- 카드와 후보 모집을 우선 봉인한다. 이후 공개 요청 게시물만 열어 조작과 보존 조건을 영어로 단문화한 다음 카드·PO를 다시 펼치기 전에 한국어로 옮긴다. 같은 작성자가 앞서 카드를 보았음을 기록한다. 한국어 문장을 한국어 실사용 요청으로 집계하지 않는다. 최초 게시판 revision이 확인되면 그 때만 최초 표현으로 표기한다.
- 고정 예제의 직접 적격 대조 2개와 같은 이름의 입출력·편집/표시 충돌 대조 2개는 별도 섹션이다. 대조의 정답 근거와 문장을 자연 요청 원장의 적격 수와 독립 집계한다.
- 순위 계산 전 가능한 모든 자연 슬롯 × 후보 슬롯의 동작과 보존을 따로 판독한다. 둘 다 입증하면 직접, 사용 가능한 하위 동작만 입증하면 일부, 고정 근거로 요구 동작·보존을 거스르면 충돌, 관련 절 부족이면 미확인으로 둔다. 모집 공석은 별도 표시한다. 분모 0일 때 recall은 계산 불가다.

## 검색 조건과 교란 확인

| 코드 | 별칭 조회 | 역할로 재정렬 |
| --- | --- | --- |
| A0R0 | 꺼짐 | 꺼짐 |
| A1R0 | 켜짐 | 꺼짐 |
| A0R1 | 꺼짐 | 켜짐 |
| A1R1 | 켜짐 | 켜짐 |

영어 URL, 제목, 한 줄 메모 24자리의 고정 SQLite 입력을 사용한다. 네 조건에 유니코드 NFKC·casefold, 문자/숫자 단어, 고정 영어 기능어 제외 규칙을 적용한다. 조사 점수는 유일한 질의 단어에 대해 제목 3, 메모 2, URL 1, 검증 한국어 표제 단어 3을 합산한다. 같은 단어의 필드 반복은 필드별 한 번으로 센다. 양수만 후보가 되고 점수 내림차순 다음 기능 ID 오름차순으로 12개까지 가져온다. 역할 스위치는 앞 12개에서 명시 충돌 수 오름차순, 기존 조사 순서 오름차순이다. 둘 다 비교 근거가 있을 때만 역할 충돌을 세고 불명은 그대로 보관한다. 허용 역할은 input, output, edit, display. 같은 개념을 뽑았지만 후보가 제공 가능한 역할과 요구 역할이 어긋나는 경우를 기본 비교한다. 대응 개념도 닫힌 조건도 읽히지 않은 경우는 유보한다. 역할 필드는 독립 원절/요청 위치를 가리킨다. 별칭은 조회용이며 역할 혹은 적격 증거의 대용으로 쓰지 않는다. 랭커에는 정답표, 프로젝트별 정답 ID, 요청별 순위 조정 규칙을 넣지 않는다. 표시 3자리와 조사 12자리의 공석을 모두 출력한다.

주 실행에서 한·영 각각 네 방식을 고정 DB 두 개에서 반복한다. 실측의 질의 수, SQL 수, 증분 바이트와 토큰 행, 준비 문서 수, 입력과 순위 지문을 분리한다.

| 비교 | 고정할 변화 | 볼 관측 |
| --- | --- | --- |
| 띄어쓰기 | `이미지 시퀀스`와 `이미지시퀀스` | 같은 의미의 두 형태 중 어느 쪽이 조사에 들어가는가 |
| 조사 | `레이어`와 `레이어를` | 형태소 분석 없는 본 조회의 경계 |
| 영문 UI | 현행·레거시의 영문 노드명이나 기호를 한국어 대조문에 유지 | 한국어 표지가 미확인인 실제 양성이 조사에 들어오는가 |
| 동명·역할 | 동일 표제 또는 같은 핵심어가 명시된 후보에서 edit/display, input/output 반대 | 순위 하락, 상위 슬롯 교체, 실제 적격의 하락 여부 |
| 한 기능 번역 교체 | Krita Clone Layers의 해당 판 한국어 별칭을 제거. 확인된 별칭이 없으면 null→null을 보존하고 결측 차분은 미측정 | 자료집과 역할을 유지했을 때 조사/표시 차이 |
| 역할 태깅 누락 대조 | 주 실행 이후 구조상 역할이 여러 개인 직접 적격의 역할 하나를 빼는 구성 실험 | 옳은 후보가 아래로 가는 반례, 사실 판정은 고정 |

음악에서는 기보음·실음 표준과 출판 예, 서지에서는 원표제/번역표제 규칙과 실제 레코드를 원 문맥에서 읽는다. 대응이 맞더라도 관점·파일 출력·표지의 귀속을 잘못 잡을 수 있는지 비교한다. 제품 후보에는 추가하지 않는다.
