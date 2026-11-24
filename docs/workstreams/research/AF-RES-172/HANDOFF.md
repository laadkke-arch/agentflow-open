# AF-RES-172 HANDOFF

## 자기 판정: PARTIAL (중앙 상태 미변경)

- 작업: 기성 부품의 그대로 사용·어댑터 수정·직접 작성 비교를 위한 노동/검수 기록지와 판정 규칙 설계.
- 결과 본문 고정 SHA: `e0dd973a4f79c8c8faa9390b70bb4deceb2ef47d` (RESULT.md 및 SELF_CHECK.md 포함). 이 인계 파일은 그 뒤의 독립 커밋에 포함된다. 인계 커밋 자신의 SHA는 이 파일 안에 자기참조하지 않으며 브랜치 HEAD/외부 인계 기록에서 확인한다.
- 브랜치: `work/research-af-res-172`. 허용 경로: `docs/workstreams/research/AF-RES-172/`. 중앙 dot-control.json은 수정하지 않았다.
- 고정 계획 통합판: `53eaa286136019510f052179f5f51d901bdac858`. 시작 통합판: `2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc` (계획판 대비 2 ahead, 0 behind; dot-control.json 변경만 확인). AGENTS.md, STATE.md, DOT_AUTOMATION.md, RESEARCH_WORKFLOW.md, 진행표 항목을 확인했다.
- 선행 입력: AF-RES-164 `df07150fcb13ab153e6472490787f3f970173a35`, HANDOFF.md와 lattanzi-raw.csv. 중앙 DONE과 작업자 자체 PARTIAL 구분. R1/R9/R17은 145/65/75 원척도, A−B=+33.125, A−C=−17.5는 기존 평균을 서식 점검에만 사용; 새 추정이나 물리 단위 환산을 하지 않았다.

## 실제 저장 묶음

| 순서 | SHA | 대표 파일과 확인 |
|---|---|---|
| ① | ded04def7d2ed25e4f45552df9c0e3e96290c874 | SCOPE.md 재열람: 모집 조건, 예정 분모, 판정 규칙 |
| ② | e4e1dde47f8768352e10075d52af2f49814990d8 | sources.jsonl/frame.csv 재열람 |
| ③ | 0acb885debc9e7390d24369aef9afda8e7d69615 | PROTOCOL.md, effort-form.csv, worked-cases.csv 재열람 |
| ④ | ad5bd94776de126c5c46b7b1c1d0cb9b9c4a44e5 | 추가 원문·반례, 수정 SCOPE/PROTOCOL, 원장 분모 대조 |
| ⑤ | e0dd973a4f79c8c8faa9390b70bb4deceb2ef47d | RESULT.md, SELF_CHECK.md 재열람 |
| ⑥ | 별도 인계 커밋 | HANDOFF.md (이 파일) |

대표 파일: PROTOCOL.md(두 과제·세 경로·수용 기준·비용식), effort-form.csv(빈 서식+설계 예시), worked-cases.csv(실제 자료와 가상 수치 분리), RESULT.md(세 필수 표), SELF_CHECK.md(분모와 미충족).

## 실제 판독 및 남은 것

- 원장 57행(S 52, F 4, D 1): 직접 판독 40행(신규 39, 선행 1), 실패 16행, 초록만 1행. 신규 work_id 24(보충 포함). 17 lineage 후보명은 독립 관측 수로 확정할 수 없다. 동일 연구 패키지는 중복 산입하지 않았다.
- 엄격 범주별 후보 18/22: SW 원보고 5/6, 독립 저자 패키지 3/6, 프로토콜 4/4, 번역 3/3, 기록물 3/3. 하한 최소 4 부족(도메인 모델 제작을 제외하면 5 부족), 번역·기록물의 원표/시간/최종 품질 결합 조건까지 적용하면 미충족은 더 많다. 후보 산입을 모든 조건 충족으로 읽지 말 것.
- 원 모집 24 예정 자리 전부 미확인: Zenodo API 실패, OSF 403, ACM 403, IEEE 접근 제한. 보충층을 원 모집 순번 대신 채우지 않았다. 검색 결과 일부 노출 및 질의/클릭 이력 전량 미보존으로 완전한 블라인드 모집이 아니다. 실패 16행 중 일부(대소문자 경로)는 재열람 해결; 원장 그대로 보존.
- W01–W19: 관측/전사/보고 14행, 설계 예 5행. 신규 원행 적용 계보 METR, OC, Echoes, CITR, Frattini 5; 물리 시간 단위 명시 3(METR/OC/CITR); 배정 전원·동일 기능·활동 인시·독립 검수 완전 비교 0. 연구 효과를 재사용 절감률로 바꾸지 않았다.
- X/Y 과제: CSV 파싱 계약(기성 reader 사용 가능 문서 근거)과 2열 고정 폭 예외 계약(그대로 사용 불가 예상). Python 3.12.10은 설계 선택이며 해당 런타임에서 실행하지 않았다. Y-B가 불가능하다는 문서 기반 판단은 실행 확인 전 조건부이다. 배정 전 불가능 확인이면 sentinel N=0(합격률 없음), 배정 이후에는 실패/중단을 N에서 제외하지 않는다.
- 같은 사람 활성 구간의 합집합, 다른 사람 합산, 경과/기계/회고 구분. 전체 배정 품질 분모와 노동 결측 분모 분리, 성공자 평균은 보조. 선행 제작자/도입/유지/검수 비용을 누락값 0으로 놓지 않음. 반복 N회 식은 조건부. 새 참가자 모집, 처치 배정, 코드 실행, 실측 절감은 하지 않았다.
- 자체 점검만 수행했다. 독립 검토, 자동화 검산, 실험 수행 없음.

## 다음 첫 행동 및 후속 검산 입력

1. **모집 복구 먼저**: SCOPE의 2015–2025 기간/정렬/동률/제외 규칙 그대로 적용. Zenodo/OSF/ACM·IEEE 원 목록 대신 보충 검색 결과 순위를 쓰지 말 것. DOI·최초 공개일·자료 존재만으로 후보 확정 후 원 결과를 읽고 sources.jsonl/frame.csv를 추가 보정 커밋. 최소 부족: 보고서 1 및 별도 저자 패키지 3(엄격 실행 과제 조건이면 보고서 2); METR prereg 주소 및 OC 논문/부록, Piantadosi figshare 접근, Echoes v1/패키지 버전 대응부터 확인. Q6은 같은 입력의 TM 직접 번역/후편집과 이중입력/교정의 역할별 시간 및 최종 품질 원표를 별도로 회복.
2. 다음 명령은 Codex Cloud에서 **검산 권한이 있고 공개 비식별 자료가 확보되었을 때** 실행한다. 이번에는 실행하지 않았다. 기존 파일을 덮어쓰지 않는다.

```sh
git fetch origin work/research-af-res-172
git checkout --detach e0dd973a4f79c8c8faa9390b70bb4deceb2ef47d
git diff --name-only 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc HEAD
cd docs/workstreams/research/AF-RES-172
python3 - <<'PY'
import csv, json
from collections import Counter
from pathlib import Path
s = [json.loads(x) for x in Path("sources.jsonl").read_text().splitlines() if x.strip()]
with open("frame.csv", newline="") as f: frame = list(csv.DictReader(f))
with open("worked-cases.csv", newline="") as f: work = list(csv.DictReader(f))
print("source", len(s), "frame", len(frame), "cases", len(work))
print("source fields", sorted(s[0]))
print("case fields", list(work[0]))
assert len(s) == 57 and len(work) == 19
PY
```

3. 고정 런타임 확인은 별도 실행 허용 후 아래 입력 및 PROTOCOL.md X1–8/Y1–11 전체 fixture를 그대로 대조한다. Docker 이미지/tag 접근과 digest 기록은 실행 담당자 확인 사항. 아래 스모크 입력은 대표 사례만이며 전체 시험 대체가 아니다.

```sh
docker run --rm -i python:3.12.10 python - <<'PY'
import csv, io
def b(s):
    return list(csv.reader(io.StringIO(s, newline="")))
def c(s):
    rows = b(s)
    if any(len(row) != 2 for row in rows): raise ValueError("width")
    return rows
assert b('a,b\r\n"c,d",e\r\n') == [["a","b"],["c,d","e"]]
assert b('a,b,c\n') == [["a","b","c"]]
assert c('a,b\n') == [["a","b"]]
try:
    c('a,b\nx,y,z\n')
except ValueError as exc:
    assert str(exc) == "width"
else:
    raise AssertionError("width check not triggered")
PY
```

4. 공개 전원 배정표·개인별 시간 구간(역할/단위/clock/활동/중복)·시험별 합격표·중단/교차·검수/후속 수정 원행이 확보된 후에만 effort-form 컬럼에 매핑한다. 분모 및 합집합 검산을 Codex에 별도 인계. 알려진 30인분, 결측 한 사람 최대 180인분, N=2의 범위 [15,105]; 동일인 [0,30)∪[20,40)=40 및 다른 사람 30 → 70인분; 예제값은 원관측과 별도 테스트. 공개 원행 없이는 새 사람 실험이나 효과 추정으로 넘어가지 않는다.

## 색인 제안(중앙 파일 수정 없음)

AF-RES-172 | PARTIAL | 부품 채택 노동 측정: X/Y 과제·전원 배정 분모·활동 인시 합집합·역할별 비용·실제 원행 적용 5계보; 원 목록 24자리 미복구/후보 18÷22/엄격 Q6·실행 미확인 | docs/workstreams/research/AF-RES-172/RESULT.md, PROTOCOL.md, HANDOFF.md
