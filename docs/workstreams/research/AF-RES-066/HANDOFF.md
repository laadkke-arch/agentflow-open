# AF-RES-066 인계 — 부분 인계(PARTIAL_HANDOFF)

## 상태·고정 결과

**완전 수용 아님.** 이번 작업에서 GitHub 브랜치 `work/research-af-res-066`를 `chore/workspace-foundation`에서 생성하고, `docs/workstreams/research/AF-RES-066/` 경로에만 파일을 작성했다. `docs/automation/dot-control.json`과 공통 색인은 수정하지 않았다. 원장·명제 규칙을 본문 판독 이전에 먼저 고정했다. 인계 전 원격에서 RESULT와 acceptance를 실제 재조회했다.

- **고정 결과 커밋**: [`d736df8b3108451ab183ab0a09656a2d719bae12`](https://github.com/laadkke-arch/agentflow-open/commit/d736df8b3108451ab183ab0a09656a2d719bae12) (이 HANDOFF 추가 직전 결과 SHA)
- **필수 표 1** (24개 권고): [RESULT.md, 첫 표](https://github.com/laadkke-arch/agentflow-open/blob/d736df8b3108451ab183ab0a09656a2d719bae12/docs/workstreams/research/AF-RES-066/RESULT.md)
- **필수 표 2** (정오·판 분모): 위 RESULT.md 두 번째 표
- **첫 재개 파일**: [evidence/acceptance-evidence.json](https://github.com/laadkke-arch/agentflow-open/blob/d736df8b3108451ab183ab0a09656a2d719bae12/docs/workstreams/research/AF-RES-066/evidence/acceptance-evidence.json), 미충족 항목 C05–C15부터 검사. 이어 [versions.csv](https://github.com/laadkke-arch/agentflow-open/blob/d736df8b3108451ab183ab0a09656a2d719bae12/docs/workstreams/research/AF-RES-066/versions.csv)에서 역사판 미확인 URL을 순회한다.
- **계획 통합 기준**: `028d16fee1121f5862efd410b78ec1d79d7080f2`. 실제 분기 시 통합 SHA는 GitHub branch-create 성공을 확인했지만 SHA 자체를 회수하지 못했다. 이 값을 계획 SHA로 대체하지 않는다.
- **완료된 의존성**: AF-RES-062@`36e50408139d35022c2fe527ff2f05216f24516c`; 인수 내용 SHA `bb3c627bf94f16418e3d71f56b7838b0c60d5e04`. 두 파일의 내용/전사 인수는 GitHub connector 직접 읽음.

## 현재 확보한 것과 의미

| 측정 단위 | 계획/실제 | 해석 |
|---|---:|---|
| 실험 질문 | 12/12 | 의미기반 ID; 공개 앱 원문 ID 아님 |
| 저자 정·오 선택 | 24/24 | 저자 답키에 종속, 외부 정답키 재판정 아님 |
| 출처 자리 | 72/72 | 각 3자리와 선택값 연결·커밋 |
| 고유 원주소 | 67/67 | 원장 중복 제거. 5개 URL은 같은 문항 반대 권고에 재사용 |
| 과거/현재 URL 버전 행 | 134/134 | 표를 만들었음; **134개 본문 검증을 뜻하지 않음** |
| 자리×버전 명제 행 | 144/144 | 초기 원자명제 P0/기록 상태; 모든 명제 독해 완료 아님 |
| 링크 3개 결합으로 완전 검증된 권고 | 관측 0/24 | 완료된 감사가 0; 실제 지지0이라는 뜻 아님 |
| 기록한 자료 | 34 JSONL 행 | 일부 재사용/2차자료/부분 절; **34개 엄격한 독립 완전본문 읽기 합격을 입증하지 않음** |
| 과거 본문 선행 검증 | 3/67 원URL | USGS·NLM·NASA AF062 검증 재사용; 나머지 64원URL 미확인 |
| HTTP·본문 해시 검산 | 0/134 판 | 도구가 원문 HTTP·타임스탬프/해시를 제공하지 않아 미충족 |
| session start/check 실행 | 0/2 | **미실시**; 종료코드·검사대상 SHA 미확인 |

핵심은 한쪽 수치만 있는 NASA 달 보행자 12명을 달/심해 비교 전체의 증거로 쓰지 못한다는 점, USGS의 폐·피부 비율과 NLM의 선천 무지문증이 일부 **오권고를 오히려 반박**한다는 점, 동일 URL 5쌍이 양쪽 반대 문장에 붙는다는 점이다. Port Royal의 2025 UNESCO 등재·보호 문서는 사후판이며 잠수 가능 여부의 개별 허가를 의미하지 않는다. [RESULT Q1–Q7](RESULT.md), [실제 카드](cards.md), [자체검토](SELF_CHECK.md).

## 커밋 영수증과 고정판 재열람

| 묶음 | 커밋 SHA | 역할/정정 |
|---|---|---|
| ① 원자판정 규칙 | `2e7003b587ce7cc51755a924873569e881530cdd` | SCOPE 선행 고정 |
| ① 슬롯 원장 | `e5d96b7f03ea8452e948650931049ccff90c4715` | 72 원URL/선택 연결 |
| ② 원문 단위 원장 | `c84853c6c1e9ea2f355cabb3781a2033bf24aff6` | 출처·위치·한계 32행 시작 |
| ② 과거/현재 URL 행 | `516a08cf3af4b5d86fe8d410de86e0537948c7c7` | 67×2, 미확인 보존 |
| ③ 명제/권고 행 | `1977b5f0e9b5180db5c245874cd8ba96c275d398`, `8293493cb1487f5aee17e1ea75aba666741c103e` | 144명제 행, 24권고 |
| ④ 필수 표 | `a01535a7ea5a38e31fc3b62ec41d472744b80611` | 24권고 두 표와 Q1–Q7 |
| ④ 카드·검토·실패 | `04ec9049cc216401688130ddf21ddc44c804e8f9`, `090c2063127070d0e3bea22ccc137130d57151b3`, `069b9e60f8a828f13e783c8af8cd791dd01bfa87` | 표현 경계/실패 기록 |
| ④ 두 추가 원문 | `7a3918ae6514c3b9f046add29798a7a9d9451125` | Villmoare 2022, UNESCO 결정 |
| ④ 수용 원장 | **`d736df8b3108451ab183ab0a09656a2d719bae12`** | 명시된 부분 수용 |

커밋 시각 UTC의 독립 로그 조회는 **미실시**; 채팅 기록의 순서와 커밋 SHA를 보존했다. 마지막 고정 결과의 GitHub 원격 재열람은 AI GitHub connector가 직접 실시했다. 읽힌 blob SHA: RESULT `e5aeab9bb5419517a99d5794ef34287ec5cd95b5`, acceptance `a91b420e5aa46a126d34259c4029677d95fd5f23`, slots `4c5f47badc25dbeec15257a6415360ec87afd0a8`. CSV 행 수는 72/134/144/24, RESULT 표1은 24행으로 재확인. 이것은 **계약 검사나 독립 판독**이 아니다.

## 도구 제한과 다음 첫 행동

연결 환경은 GitHub 파일 커밋·원격 fetch와 일반 웹 원문 열람만 제공했다. 이 작업의 Git 작업 사본에서 Python `workbench.session`을 실행할 수 없어 `manifest.json`을 만들어 실행했다고 주장하지 않는다. 저장소 기본 경로 `chore/workspace-foundation`에 대한 AGENTS/STATE/DOT_AUTOMATION/RESEARCH_WORKFLOW는 직접 읽었으나 대형 `dot-control.json`의 특정 AF-RES-066 내용은 GitHub fetch에서 빈 응답으로 나와 원 항목 대조 미충족. 원 브리프는 이 대화의 배정 내용으로 보존.

**첫 행동**: Git 작업환경에서 지정 브랜치를 fetch하고 실제 분기 통합 SHA, dot-control 항목과 소유 경로/의존 SHA를 확인한 다음 정확히 아래를 실행한다. 기존 파일이 있으면 덮어쓰기 전에 비교한다.

```bash
git fetch origin
 git switch work/research-af-res-066
python -B -m workbench.session start af-res-066 --allow docs/workstreams/research/AF-RES-066/ --dependency work/research-af-res-062=36e50408139d35022c2fe527ff2f05216f24516c --output docs/workstreams/research/AF-RES-066/manifest.json --fetch
python -B -m workbench.session check docs/workstreams/research/AF-RES-066/manifest.json --fetch
```

실제 exit code·대상 SHA·UTC·검사기 출력을 별도 영수증으로 커밋하라. 그 다음 실제 모집 가능 날짜 구간에 맞춰 67 URL의 시간 양옆 원문 캡처·HTTP·본문 해시를 채우고 `claims.csv` 원자명제를 근거 절마다 분리, `advice.csv` 전체 결합을 재계산한다. 이번 실행 중 가진 상태 표지 '미확인'을 임의로 '관측0' 또는 '해당없음'으로 바꾸지 않는다.

## 색인 담당에 제안

`AF-RES-066 | 같은 정오 답에 첨부된 3개 링크의 본문함의와 과거판 비교 | 부분 인계: 12질문/24권고/72자리/67URL 인덱스; 본문·시점/원자료·Git contract 미충족 | work/research-af-res-066, docs/workstreams/research/AF-RES-066/RESULT.md | AF-RES-062@36e5040..., 현시점 근거≠실험시점 근거`를 **편집 담당이 검토 후** 등록한다. 소유 경로 밖 직접 변경 안 함.

## 가장 중요한 불일치·약점과 다음 조사 — 정확히 3건

1. **시점/본문 67URL 미완전**: 전URL 당시판이라고 잘못 표기될 위험 → 원URL별 Wayback 실제 캡처 본문·날짜·HTTP·hash를 쌍으로 가져오고 원래 연구 모집창과 비교하라.
2. **비교 명제 미완전/재인용**: NASA 12명·사람 머리카락 수만으로 두 대상 우위를 판정할 위험 → 다른 쪽의 동일 단위·기준일 원자료와 중복계보를 연결한 뒤 명제×판 재코딩하라.
3. **저자키와 사후판 충돌**: 2021/2022/2023 뇌크기 논쟁, 2025 Port Royal 제도, 인구 연도 업데이트를 저자키와 혼동할 위험 → 당시 원자료·정정·허가규정과 실제 시험 기준일을 연결해 독립 판정하고, 반대방향이 전체 증명인지 일부 반박인지 나누라.
