# AF-RES-016 진행 상태

- 브랜치: `work/research-af-res-016`
- source_commit: `24b22f8a068d02fa5be2aaaa0df50d241f7602a4`
- 이 기록을 작성할 때의 마지막 원격 커밋: `e78a067a6aeecf46b3f9f4a3ec4becda82b4cd07` (묶음7: VOCAB_MAP·RESULT)
- 완료한 묶음: 코드북/범위 → 체계 → 표본 → A동결 → B원응답 → 일치도/영향 → 어휘/결과.
- 이 기록과 함께 커밋할 묶음8: SELF_CHECK, validation, 내부 별도 수치 감사, acceptance evidence.
- 다음 묶음9: HANDOFF.md만 단독 커밋하고 원격 본문을 다시 읽어 로컬과 비교한다.

## 막힌 부분과 상태

198단위×3안의 내부 이중 코딩과 지정4표,30개 문서 영향 감사는 작성·동결했다. 수치·보존·구조 검증72개는PASS다. 그러나 Hooper1965·Markey1984의 지정 원문 본문은 추가32검색/10URL 보강 뒤에도 미확인이다. 정확한 차단·실패·한계와 최소 추가 확인은 SELF_CHECK §3 및 evidence/reliability-supplement.json에 있다. 전체요청을 무조건 완료로 표시하지 않는다.

## 재개 명령과 입력

저장소 루트에서 현재 커밋과 상태를 먼저 읽는다.

```bash
git log -9 --oneline work/research-af-res-016
git status --short
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/validate_delivery.py
```

분석 재현의 입력은 동결 CODEBOOK, sample/units.json, sample/baseline.json, coding/coder-a.json, coding/coder-b.json이다. 고정 선행 Git 객체는 manifest.json와 sample/selection.json의7개 SHA다. 새 코딩으로 덮어쓰지 않는다.

```bash
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/analyze.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/build_impact.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/toy_counterexamples.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/vocab-inventory.py
```

원문 공백의 다음 첫 행동은 정상 공개 IBM/FID Hooper 스캔 또는 Markey1984 저자/기관판의 실제 URL을 확보하는 것이다. 확보되면 원표지/판과 방법·결과를 직접 읽고, 먼저 sources.json 원장에 확인 범위와 한계를 추가한다. 반복 후속 인용만으로 원문 열람 상태를 예로 바꾸지 않는다.

HANDOFF가 이미 존재하고 마지막 커밋이라면 이 파일의 ‘다음 묶음’ 설명은 이전 시점의 기록이다. 최종 상태는 HANDOFF와 원격 HEAD를 우선한다.
