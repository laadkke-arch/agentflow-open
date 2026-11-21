# AF-RES-020 재검사와 미충족 재개 입력

## 1. 현재 읽기 전용으로 재생 가능한 검사

저장소 루트에서 실행한다. 고정 Git 객체를 입력으로 읽으며 네트워크 검색·원 실험·외부 서비스 실행을 다시 하지 않는다. 다음 명령의 종료 0은 구조 및 집계 대조 성공이다. 미충족 연구 조건이나 공통 manifest gate를 통과했다는 뜻은 아니다.

```bash
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-020/evidence/audit-late.py --check-only
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-020/evidence/validate-assembly.py --post-handoff
```

첫 명령은 AF-RES-011~016의 46개 고정 파일에서 허용된 구조·집계 필드를 읽는다. 011의 질문 본문·기존 요약을 출력하지 않는다. 두 번째 명령은 최종 HANDOFF 단독 커밋 이후에 사용한다. 인계 전에 수행한 기록은 `validation-report.json`에 있으며, `--post-handoff`와 `--output`은 함께 쓸 수 없다. 인계 후 검사로 작업 트리를 바꾸지 않는다.

입력 SHA는 [fixed-inputs.json](fixed-inputs.json), 주장·2단계 파일 위치는 [CLAIM_CHECK.json](../CLAIM_CHECK.json), 파일별 본문 해시는 [sources.json](../sources.json)에 있다. 파일이 없으면 저장소의 공개 origin에서 해당 고정 SHA를 fetch한 뒤 같은 명령을 실행한다. 새 작업 017~019는 입력에 없다.

## 2. 통과하지 못한 공통 작업 계약

당시 실행은 exit 2, `dependency changed: work/research-af-res-013`이었다. 입력은 `eb569f07a3a34ffacf114384ae9b06ad062f5396`, 당시 원격 branch HEAD는 `d720777ed8e446a84ccfe628efe7447a2525ce2a`였다. 그 결과 `manifest.json`은 생성되지 않았고 `check --fetch`도 통과하지 않았다.

아래는 축약 기록을 12개 의존 입력으로 펼친 재현 명령이다. **현재 계약을 확인하기 위한 입력이며 성공을 기대하는 우회 명령이 아니다.** 실행하면 원격 추적 ref를 정상 fetch하고, 같은 차이가 남아 있으면 다시 실패한다. HEAD를 과거로 위장하거나 의존 입력을 최신 값으로 바꾸지 않는다.

```bash
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session start af-res-020 \
  --allow docs/workstreams/research/AF-RES-020/ \
  --output docs/workstreams/research/AF-RES-020/manifest.json \
  --fetch \
  --dependency work/research-af-res-001=4d6208c08f6f2657865ba000d6768f6537e832b6 \
  --dependency work/research-af-res-002=62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1 \
  --dependency work/research-af-res-003=b13db3931b4021ff9e1ac6e404590c09526c3087 \
  --dependency work/research-af-res-004=2b798c7d2b7355b649691c18de196104ceabb0f0 \
  --dependency work/research-af-res-009=7f627a81199f06da7f7b15f979e7fef25dd17602 \
  --dependency work/research-af-res-010=0603f0d2990c7a501dbdfc45fbbba79155f505fc \
  --dependency work/research-af-res-011=478c301b693896e2c6d777f46ac441f071bfdfe8 \
  --dependency work/research-af-res-012=cb602858378db90adb1f085953016267f9afbd6d \
  --dependency work/research-af-res-013=eb569f07a3a34ffacf114384ae9b06ad062f5396 \
  --dependency work/research-af-res-014=42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9 \
  --dependency work/research-af-res-015=e39d23c9a7307ba83c974580f60115d90e221084 \
  --dependency work/research-af-res-016=3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc
```

공통 `workbench/session.py`의 `dependency_errors`는 각 의존 브랜치의 현재 원격 HEAD와 입력 SHA의 정확한 일치를 요구한다. `--integration-ref`는 통합 기준만 바꾸며 역사 의존을 승인하는 옵션이 아니다. 공식 help, 고정 코드 및 `test_session.py`의 의존 변경 실패 검사를 읽었다. 근거는 `sources.json` G11~G13이다.

**다음 첫 행동:** 공통 계약을 담당하는 별도 범위에서 현재 HEAD 의존과 역사적 `result_commit` 자료 의존을 구별하는 승인된 표현을 정한다. 이번 고정 입력 12개를 유지할 수 있는 계약이 마련된 후 새 작업 계약을 만들고 아래 검사를 실행한다. 현재 연구는 공통 파일을 수정할 권한 범위가 아니므로 manifest를 손으로 생성하거나 검사기를 변경하지 않았다.

```bash
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-020/manifest.json --fetch
```

위 check의 선행 입력은 승인된 계약으로 실제 생성된 manifest다. 없는 manifest를 대상으로 실행한 실패를 검증 결과로 세지 않았다. 새 계약으로 연구를 재개하면 기존 마지막 HANDOFF를 수정하기 전에 새 커밋 묶음과 재인계 순서를 정해야 한다.

## 3. 발견하지 못한 수치 충돌 반례

요구된 다섯 번째 반례인 ‘같은 주장이 두 묶음에 서로 다른 수치로 들어간 경우’는 현재 표집에서 발견하지 못했다. 73개 전달행과 명시 공유 3개 주장군, 010의 7/9, 013의 두 146, 012/014의 N, 015의 14/195와 5/83, 016의 다른 관측 단위 등을 대조했다. 차이는 정의·분모·관측 창·처치로 설명됐으며, 이를 실제 수치 오류로 이름 붙이지 않았다.

추가 입력은 현재 12개 고정 결과에서 아직 표집하지 않은 정량 주장의 목록이다. 각 행에 `task, sha, path, locator, target, denominator, observation_window, condition, rater, value`를 넣고 같은 의미 키의 중복을 조인한다. 동일 키에서 서로 다른 값이 있는 최소 1쌍을 발견하면 해당 원 evidence 파일까지 대조해 실제 충돌인지 판정한다. 존재하지 않는 오류를 만들거나 조건이 다른 숫자를 합치면 안 된다. 조사 전체는 여전히 고정 입력 범위이며 이전 외부 연구의 재수행을 요구하지 않는다.

이 조건은 자료 부재로 미충족이다. ‘찾아봤음’을 ‘반례를 찾음’으로 바꾸지 않는다. 현재 기록은 [counterexample-search.json](counterexample-search.json)의 CE05다.

## 4. 되돌릴 수 없는 절차상 이탈

추가 발견 19개 호스트의 익명 응답 코드 확인이 본문 읽기 뒤에 이뤄졌다. 첫 커밋 전이라는 과거 시점은 사후 요청으로 복구할 수 없다. 차기 작업은 첫 커밋 전에 필요한 호스트를 확인하고, 조사 중 새 호스트가 생기면 본문 열람 전에 응답 코드를 기록한다. 개별 실패 주소·코드·재개 명령은 [PROGRESS.md](../PROGRESS.md), `external-network-check.json`, `sources.json`의 excluded에 있다. 차단된 주소를 우회하지 않는다.

011 CASES의 초기 `outcome` dict 집계 출력에는 기존 요약 필드가 부수적으로 노출됐다. 이 경계 이탈 역시 사후에 없애지 않는다. 근거는 구조·집계에 한정했고 텍스트를 새로운 사례 분석이나 산출물 복사에 사용하지 않았다. 이후 검사는 §1의 `--check-only`처럼 허용 필드를 먼저 투영해 출력한다.

## 5. 결론을 바꿀 다음 연구의 최소 입력

| 질문 | 필요한 자료 | 제안한 최소 규모와 판단 경계 |
| --- | --- | --- |
| role을 고정하고 proposed_use만 바꾸면 H/T가 달라지는가 | 같은 문제·후보·설정·제공 근거에서 사용 방식이 달라지는 쌍, 원 코드북, 판정자별 이유 | RESULT §4.1의 쌍 설계로 시작한다. 용도 축을 버려도 된다는 결론은 문서 요약만으로 내리지 않는다. |
| 역할 정의와 qrel의 차이가 어떤 검색 결론을 뒤집는가 | 동일 항목·동일 cutoff의 별도 판정, 양성 교집합/합집합, 역할별 분모, 불일치 이유 | RESULT §4.2의 동일 입력 재판정 규모를 사용한다. 높은 전체 일치율이 낮은 양성 일치를 가리지 않게 한다. |
| C0·C1·C2 중 어느 조건에서 추가 기록 비용이 상쇄되는가 | 같은 실제 과제, 판정 오류·검토 시간·수정/이행 비용, 원 질문과 근거 판의 보존 여부 | RESULT §4.3의 비교 규모와 실패 신호를 사용한다. 현재 자료에는 구성 간 실제 비용·효과 비교군이 없다. |

위 연구의 실행은 이번 문서 감사에서 수행하지 않았다. 구체 질문·자료·최소 규모는 [RESULT.md §4](../RESULT.md#§4-가장-중요한-불일치약점-3건과-다음-조사-제안)와 [DECISIONS.md](../DECISIONS.md)에 있다. 017~019가 답할 선택은 계속 ‘대기 중인 입력’으로 남긴다.
