# AF-RES-087 #1 인계 · REVIEW_READY

## 1. 식별

- 작업 ID AF-RES-087, 시도 1. Codex Cloud에서 GitHub checkout과 별도 O/N venv로 조사·재현했다.
- 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-087`. 계획 기준은 `184137d2f257f5d1a7ef584e0f3a6b35f3d280cd`, 실제 시작과 검사 시 통합 기준은 `9dcae48a47b05d7ba2a1320444be28f5d0fcd739`다. 계획판 중앙표에는 087 행이 아직 없었고, 최신판에서 배정 행과 작업 브랜치 부재를 확인했다.
- 마지막 확인한 결과 SHA와 원격 재열람 SHA는 모두 **`263fe7581cf45eadd1f05139aacaadb27290b86e`**다. 2026-11-23 15:11:05 UTC 계약 검사 종료 0, 15:11:09 UTC 원격 Git blob 92/92 일치, 15:11:21 UTC 원격 checkout 자가검산 47/47. PR 주소는 미생성이다.
- 이 파일은 마지막 단독 커밋이다. 자신의 SHA는 [이 파일 Git 이력](https://github.com/laadkke-arch/agentflow-open/commits/work/research-af-res-087/docs/workstreams/research/AF-RES-087/HANDOFF.md) 및 최종 기록에서 확인한다.

| 단계 | 원격 커밋 |
|---|---|
| ① 범위·입력·양 계약·예측 봉인 | `e1b4a0f27ff8ab35505064840ad556d78af062be` |
| ② 두 환경·네 파일 생성·footer | `798d4c488c4ff4fe5ab65615446e574f85f640aa` |
| ③ 16자리·원 시험·반례 | `aca6173dea4898da45536941d01a0df66f33bae2` |
| ④ 결과·권고·출처·자가검산 | `263fe7581cf45eadd1f05139aacaadb27290b86e` |
| ⑤ 인계 | 이 파일만 추가, 부모는 ④ |

## 2. 사용자 요구와 작업 범위

목표는 옛 GeoPandas 안내를 새 Parquet 파일 독자에게 반환할 판·인코딩·출력 기준을 판별하는 것이다. O는 0.14.4의 `60c9773e44fff8a35344c2a74431e00c5546a4ee`, N은 1.0.0의 `d8e14e1be3ecbef6f75a1142f85561ff652ed3d1`다. 쓰기 범위는 `docs/workstreams/research/AF-RES-087/`이며, 다른 같은 회차 결과와 독립이다. 유일한 입력 의존은 `AF-RES-083@f9be0dacdb51603c72f30abd452ce9d349d0ca3b`의 G04-1/G04-2와 재현 입력이다. [통합판](https://github.com/laadkke-arch/agentflow-open/tree/9dcae48a47b05d7ba2a1320444be28f5d0fcd739) · [083 인계](https://github.com/laadkke-arch/agentflow-open/blob/f9be0dacdb51603c72f30abd452ce9d349d0ca3b/docs/workstreams/research/AF-RES-083/HANDOFF.md).

## 3. 실제 변경

| 파일 | 변경 사항 | 검사 |
|---|---|---|
| [RESULT.md](RESULT.md) | 지정 세 표와 분모, Q1–Q7, 주요 약점 세 건 | 동일 bytes의 실행행·원문·반대 입력 대응 |
| [SCOPE.md](SCOPE.md), [manifest.json](manifest.json), [fixtures/input.json](fixtures/input.json) | 범위와 의존 SHA, 고정 matrix·예측·비교 계약 | ① 봉인 hash 및 workbench 검사 |
| [files.csv](files.csv), [fixtures/](fixtures), [environments.json](environments.json) | 실제 writer 환경, 입력, 출력 및 제3 footer SHA | 4/4 생성·판독, 3/3 pair diff · import 확인 |
| [runs.jsonl](runs.jsonl), [reproduce.md](reproduce.md), [evidence/](evidence) | 프로세스 16개와 upstream 48개, 보조 최종 20개, 정상 거절과 실패 원 출력 | 16/16 같은 SHA, 원 선택 및 상세 출력 |
| [sources.jsonl](sources.jsonl), [attempts.jsonl](attempts.jsonl), [SELF_CHECK.md](SELF_CHECK.md) | 55 산입행/51 원문 URL/35 계보, 범위와 미확인 | 출처 하한, 역방향 근거 및 47항목 정합성 |

[고정 결과 전체](https://github.com/laadkke-arch/agentflow-open/tree/263fe7581cf45eadd1f05139aacaadb27290b86e/docs/workstreams/research/AF-RES-087).

## 4. 실제 검증 결과

| 명령/행동 | 대상 | 종료/검사 범위 |
|---|---|---|
| `python -B -m workbench.session start af-res-087 --allow docs/workstreams/research/AF-RES-087/ --output docs/workstreams/research/AF-RES-087/manifest.json --dependency work/research-af-res-083=f9be0dacdb51603c72f30abd452ce9d349d0ca3b --fetch` | 실제 시작 9dcae48 | 0, 계약 v2 및 의존·허용 경로 |
| `python -B docs/workstreams/research/AF-RES-087/build_matrix.py /tmp/af087 docs/workstreams/research/AF-RES-087` | ① 계획·해시 | 0, 두 환경과 네 파일·footer |
| `python -B docs/workstreams/research/AF-RES-087/read_matrix.py /tmp/af087 docs/workstreams/research/AF-RES-087 docs/workstreams/research/AF-RES-087` | ② 파일 SHA 4개 | 0, 16자리 완료. reader 개별 0 열넷·20 둘 |
| 원 pytest 네 프로세스 | O/N 고정 checkout과 포함 fixture | 각각 0, 16/30/1/1 통과. [명령 및 영수증](evidence/upstream/receipts.json) |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-087/manifest.json --fetch` | **263fe7581cf45eadd1f05139aacaadb27290b86e** | **0**, `passed / remote_checked`, 범위 밖·미통합·오류 각각 0 |
| `python -B docs/workstreams/research/AF-RES-087/audit.py` | **263fe7581cf45eadd1f05139aacaadb27290b86e** 로컬 및 GitHub 새 checkout | 둘 다 **0**, 47/47. manifest를 포함한 92개 blob과 Git tree 일치 |

보조 F의 첫 시도에서 pandas 메타데이터를 필수 키로 취급한 footer 계기가 reader 호출 전 종료 1이었다. 적절한 optional 처리 뒤 **동일 payload hash**로 O/N을 재실행해 모두 0을 관측했다. 초기 오류 2개는 주 격자 집계에서 제외하고 로그와 함께 보존했다. [초기 오류](evidence/attempts/F-before-footer-fix.json) · [실제 F](evidence/auxiliary/F-no-pandas-meta.json).

**미확인 및 미실시.** 원 작성자의 역사적 resolved lock과 G04 인용을 실제 적용한 하류 소비 이력은 미확인이다. 다른 GEOS/PROJ/Arrow 스택, 새 디스플레이·AT 실측, GDAL 과거 writer의 새 실행은 범위 밖이다. 원 시험의 GDAL 공개 bytes에 대한 GeoPandas 읽기는 실시했다.

### 결과 SHA 검사 영수증

```json
{
  "checked_at": "2026-11-23T15:11:05.535511+00:00",
  "checked_out_commit": "263fe7581cf45eadd1f05139aacaadb27290b86e",
  "task_base_commit": "9dcae48a47b05d7ba2a1320444be28f5d0fcd739",
  "integration_commit": "9dcae48a47b05d7ba2a1320444be28f5d0fcd739",
  "scope_base_commit": "9dcae48a47b05d7ba2a1320444be28f5d0fcd739",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "exit": 0,
  "status": "passed",
  "freshness": "remote_checked",
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "checked_changed_paths": 91,
  "changed_paths_sorted_newline_sha256": "be6a39364dbee702f36bd64b495334cb384bb8e0d224002dad2f96776293d260",
  "stderr_bytes": 0,
  "stdout_sha256": "37de71c23464af9325b55ac746df4f5e7337dc1c47a7bd2b27ce2c3a975604f6"
}
```

`check_task`의 변경 경로 목록은 manifest 자체를 제외한다. 별도 Git diff의 92개 모두 소유 경로에 속하고 원격 Git blob 전체를 다시 읽었다. tree는 `4a7f5c8335416ab43d7ab20c6060eddf65ed26c4`다. 감사 stdout SHA-256은 `c27cd0f04aad0f93b0f2a0483bf8ed651b3c11474ee3eb1adbccaa80a1775150`이며 stderr는 비어 있었다. [계약 checker](https://github.com/laadkke-arch/agentflow-open/blob/263fe7581cf45eadd1f05139aacaadb27290b86e/workbench/session.py#L205-L239).

| 원격 재열람 표본 | SHA-256 |
|---|---|
| RESULT.md | `bea1fcc5d4c65cde303c9d4a06a07fb5857f2724763b77ed4805bee959c4cf53` |
| SELF_CHECK.md | `972beba9ca616776318f5aa6a8a157df1d02f80b2599e477f912806401cd2327` |
| runs.jsonl | `0a608db05f76af6898e8c4b175077114d87e3911fc223707db37d2969f61f5f2` |
| sources.jsonl | `44005bfce30e873888ad685100db4b741e11615f45478eae2bbad8415730a738` |
| manifest.json | `2b6d18ec8fbc97d76b5f1d2916873b2b805a27b748450f9939a386ca5602a450` |
| files.csv | `457ba2ff873d9f494fd05867a3586d2cbd69c01d6a4a7a14e545dfb8c53e12db` |
| fixtures/F4.parquet | `c8eddc72bf703a19d6e8ac452de58c7f28a804048f91d202630a28e5d419be7e` |

## 5. 판단과 근거

**REVIEW_READY.** F1–F3 WKB는 O/N 12/12에서 보존됐다. F4 native는 N 2/2 보존, O 2/2 정상 거절이다. 성공 14자리는 공간 및 엄격 속성 계약을 모두 통과했다. 같은 1.1.0이라도 F3와 F4의 결과가 갈린다. N native도 혼형 Point/MultiPoint의 원 타입을 바꿀 수 있으므로 반환 조건에는 geometry 요구를 붙인다. B와 F는 공간 결과가 유지되어도 엄격 스키마가 달라지는 사례다. 원 발행자의 필수 정정 여부는 실제 하류 인용 사례가 필요하다. [세 결과표](RESULT.md) · [자가검산](SELF_CHECK.md).

중앙 색인 제안 한 줄

> AF-RES-087 · REVIEW_READY · 결과 263fe7581cf45eadd1f05139aacaadb27290b86e · 동일 SHA 4파일/8셀/16회, 공간·엄격 보존 14·O native 명시 거절 2, 원 시험 48/48, 독립 근거 35 · WKB 1.0 검증 범위 유지, 1.1 native는 reader·geometry 계약을 붙여 반환.

## 6. 다음 대화의 첫 행동

1. 원격 브랜치 최신 SHA에서 이 인계만 바뀌었는지 확인하고 결과 SHA `263fe7581cf45eadd1f05139aacaadb27290b86e`의 [표 2](RESULT.md)와 [manifest](manifest.json)를 연다. 위 종료값은 이 결과판 대상이다.
2. **첫 후속 연구 행동.** 고정 `fixtures/F3.parquet`, `fixtures/F4.parquet`와 C 파일의 SHA로 같은 O/N에 한 번에 의존판 하나만 교체하는 짝을 만든다. [재현 명령](reproduce.md)의 동일 입력 SHA에서 예외·활성 geometry·CRS 축·dtype 및 C의 None/EMPTY를 대조한다. 실제 G04 하류 인용이 확보되면 별도의 정확 파일과 환경으로 재생해 안내의 필수 수정 여부를 판단한다.
3. 입력 의존은 [AF-RES-083 고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/f9be0dacdb51603c72f30abd452ce9d349d0ca3b/docs/workstreams/research/AF-RES-083/HANDOFF.md)다. 격자 내 검토에서 해결하지 못한 나머지 조건은 [RESULT의 마지막 세 조사](RESULT.md#주요-약점과-판단을-바꿀-조사-3건)에 있다.
