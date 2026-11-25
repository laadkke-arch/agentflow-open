# HANDOFF — AF-RES-249

**자체 상태: DONE (평가 절차·설계 문서에 한정).** 실제 개발자 모집·배정·추적·CPython 실행·독립 채점·인수·효과 측정은 미실시. 중앙 진행표는 작업자가 변경하지 않았다. 실험이 성공했다거나 링크가 개인별 설계 변경을 일으켰다는 주장은 하지 않는다.

## 고정 입력과 결과
- 시작 통합 SHA: `7b8b008dcc460f15cbc75348bb9527d1b95085cf`; control blob `070ec5ee27df91589e0f76ebf47d175288b00127`; 실제 AF-RES-249 RUNNING attempt1, depends_on AF-RES-236/237 중앙 DONE(자체 PARTIAL). 통합 HEAD에서 AGENTS.md, STATE.md, DOT_AUTOMATION.md, RESEARCH_WORKFLOW.md, control 항목 확인. 계획 입력 SHA `7369707441e2eb70e84004ca6cb3bfeefc8b4061`과 착수판 구별.
- 고정 의존 인계 및 결과/원표: 236 `538cb1f04c83ae2dbf79be7d4fc91b27f818baef` HANDOFF/RESULT/chain/rivals; 237 `0cd0389a47514c81d95ed2b2cd7e42e1efe84ba5` HANDOFF/RESULT/cohort/evaluation. 225는 brief와 236 보고만 사용. 238–242 입력/결과/정답 미사용. Godot/pandas 추가 모집, METR 회귀 재실행 없음.
- 브랜치: `work/research-af-res-249`; 지정 소유 경로 `docs/workstreams/research/AF-RES-249/`.
- **고정 결과 SHA (HANDOFF 직전): `8c8c7b760c65dbca32fbe1094418eda47454b602`**. 이 HANDOFF는 마지막 단독 커밋. 결과 SHA에서 재판독 후 작성하였다.

## 대표 산출물
- [RESULT.md](RESULT.md): 두 필수 표, Q1–Q7, 비용·대안·가장 중요한 세 약점.
- [SCOPE.md](SCOPE.md), [sources.jsonl](sources.jsonl), [SELF_CHECK.md](SELF_CHECK.md): 사전 봉인·원자료/실패 원장·자체 검토.
- [protocol.md](protocol.md), [stimuli.md](stimuli.md), [forms.md](forms.md), [event-dictionary.csv](event-dictionary.csv), [verify_vectors.py](verify_vectors.py): 6분 baseline + 24분 작업, E 즉시/L 12분 뒤 공개, 양쪽 동일 카드/탐색 규칙, 순서균형, 1기 주분석, A/B 7/8 벡터, 빈 양식과 실행 담당용 코드.
- [worked-traces.csv](worked-traces.csv), [worked-events.jsonl](worked-events.jsonl), [trace-artifacts.jsonl](trace-artifacts.jsonl), [trace-source-fixtures.jsonl](trace-source-fixtures.jsonl), [OBSERVATIONS.md](OBSERVATIONS.md), [revisions.md](revisions.md): 4개의 완전 합성 행동기록, 가상 시간/인수·코드 bytes/해시, 최초 판정·반증 및 정정 이력.

## 결과와 판정 경계
- 실제 자료: 원장 41행, 산입 24 distinct work/file, 17 lineages, 종류 7/4/4/4/5. D04(예제 평가) 및 P01(자료사전)을 빼는 보수적 기준에서도 22 = 6/3/4/4/5. 원자료 범주 하한 충족. 논문/별도 프로토콜·데이터는 artifact 단위이지 독립 실험 수가 아님. 실패 X01/X05/X06, D05/F01 일부 PDF 화면 실패(원문 텍스트 열람), 2025 CONSORT CAPTCHA로 2010 직접 원문 사용; P03 대형 archive 미열람; P06 현재 공개 자극의 당시 연구 판 일치 미확인. 전체 파일·전수 코드·원 저작 전체 판독이라는 주장 없음.
- 사전 지식 네 차원(이름/원리/조건/적용) 각각 K/N_CONSISTENT/U. 무응답은 미인지 증명이 아님. 제공·보임·열람·이해·시도·동일 작성자 구현 교체·최종 retained·독립 품질/인수는 각기 별도. 링크 개인 인과 및 새 원리 학습 단정 금지.
- K: groupby 이미 앎, 유지. N: 수동 upper-bound에서 right로 실제 구현 교체(합성), 이름의 새 발견과 부합하나 원리는 이미 앎. R: Counter 열람 후 적합성 판단하여 거절. F: bisect_left로 교체, 동률 반례로 불합격/인수 거절. revisions C1–C8·8 reversal(사전 코드, 자력 노출, 다른 actor, 보조 코드, rollback, reviewer code, known 이름/새 조건, missing pre). 합성에서만 3 인수 가정, 71 person-min/3; 실제 비용이 아님.
- 예정 24명 × 2과제 = 48배정, 1기 24 주분석·2기 24 탐색. 실제 0명/0배정/0실험 사건. 실제 분모·결측률·효과/비용 모두 미측정. 합성 4 case, 78 events, 12 snapshots, 4 mock source fixtures. 관측된 0 vs U vs NA vs VACANT 구분.
- 고정 결과 재판독 영수증: 15/15 파일 GitHub에서 다시 열었음; 41 고유 source_id 및 요구 metadata/HTTP(S) URL 모두 nonempty; 24 산입 22 strict 및 범주 하한 재확인; dictionary 65행×6열, worked-traces 4행×26열, 78 unique event_id 전부 synthetic/not_observation, 12 checkpoint 참조 해시·participant/assignment/session/artifact 일치, 4 mock fixture, actor active_seconds 합 K15/N20/R17/F19. RESULT 첫 표 4행×6열, 둘째 4행×5열, Q 7절, 마지막 약점 3행×4열, SELF_CHECK Q1–Q7 재확인. base→result 비교 ahead18/behind0, 변경 15파일 전부 소유 경로 안 추가, 밖 0 및 dot-control 무변경. 자체 검토와 별도 독립 검토 구별: 자체만 시행.
- ① 766a3f95004b9cd6dfe656dc45595a85950aabec 사전 범위/판정 봉인; ② 82ddbd1dd30ff939d443a74a4409ae54e8b3fea9 원장 초기, 05c894ae834f798935558b7538eb3f162c533c5b 보충; ③ 2e2c618ab5cbf21fdd6e229ad9bb24c5f8d8980e 첫 판정 표, 앞선 protocol/stimuli/runner/dictionary/traces 커밋 포함; ④ f8fc0af1bdac4f71341934097fc17a82459f2a6a 정정 및 28bbff32f23ca5a1a94f9998e6346544315c04d5 추가 자극 원자료, dbbb6b56e2212eee0f50f367b501186c1a7379e6 합성 event 정정, 3f84edc3062a51b5f9483388dcc999e75bfad240 양식; ⑤ 14144273298126fbd6ff7e2724a8436a3771bdf9 RESULT, 8c8c7b760c65dbca32fbe1094418eda47454b602 SELF_CHECK 별도.

## 미실시 검사: 다음 담당자 첫 행동
실제 사용자는 모집하지 말고, 승인된 격리 실행 환경에서 아래 synthetic fixture만 dry-run. 작업 트리는 별도 임시 checkout, 저장소의 다른 경로 수정 금지. 다음 명령은 실행 예정이지 이번에 실행한 영수증이 아니다.

```sh
git fetch origin chore/workspace-foundation work/research-af-res-249
git diff --name-only 7b8b008dcc460f15cbc75348bb9527d1b95085cf 8c8c7b760c65dbca32fbe1094418eda47454b602
git checkout --detach 8c8c7b760c65dbca32fbe1094418eda47454b602
cd docs/workstreams/research/AF-RES-249
python3.12 -VV
python3.12 -c 'import sys; assert sys.version_info[:3] == (3,12,0), sys.version'
python3.12 - <<'PY'
import hashlib, json, pathlib, subprocess, sys, tempfile
rows = [json.loads(l) for l in pathlib.Path("trace-artifacts.jsonl").read_text().splitlines()]
fixtures = [json.loads(l) for l in pathlib.Path("trace-source-fixtures.jsonl").read_text().splitlines()]
for row in rows + fixtures:
    assert hashlib.sha256(row["source_utf8"].encode("utf-8")).hexdigest() == row["sha256"], row
runner = pathlib.Path("verify_vectors.py").resolve()
with tempfile.TemporaryDirectory() as td:
    for row in rows:
        case, phase = row["case_id"], row["phase"]
        task = "A" if case in {"K", "R"} else "B"
        f = pathlib.Path(td) / (case + "_" + phase + ".py")
        f.write_bytes(row["source_utf8"].encode("utf-8"))
        p = subprocess.run([sys.executable, str(runner), task, str(f)], capture_output=True, text=True, timeout=10)
        print(json.dumps({"case":case,"phase":phase,"hash":row["sha256"],"python":sys.version,
                          "exit":p.returncode,"stdout":p.stdout,"stderr":p.stderr},ensure_ascii=False))
        expected = 1 if (case, phase)==("F","t24") else 0
        assert p.returncode == expected, (case,phase,p.returncode)
        verdicts=[json.loads(line) for line in p.stdout.splitlines()]
        assert len(verdicts)==(7 if task=="A" else 8)
        assert {v["id"] for v in verdicts if not v["pass"]} == (
            {"B2","B3","B6","B7"} if expected else set()), (case,phase,verdicts)
PY
```

정확한 원영수증 단위: case×phase×artifact hash×Python patch×runner hash×vector ID, expected/got/type_ok/unchanged/pass/exception/exit/stdout/stderr. A2·A5 비연속 반전, B2·B3·B6·B7 tie 반전, 빈 입력, A1/B1 공개 예시; 기대: K,N,R 전체 pass, F t0/t12minus pass, F t24 네 실패. 다르면 코드/기대/판 규격 재검토하고 원래 결과를 덮어쓰지 말 것. 비신뢰 참가자 파일은 권한 없는 별도 샌드박스에서만 실행. 실제 파일/문서 캡처 bytes와 SHA256, 출처 resolved URL+first-visible 영역, actor/provenance, reviewer/acceptor independent receipt는 pilot 전에 준비. 실제 사람을 쓰는 단계는 별도 승인/동의/데이터 보존 조건이 필요. 별도 독립 코더 2인 판정 불일치면 U, adjudication 기록. 결과가 다르면 PARTIAL로 재판정.

## 색인 제안
AF-RES-249: delayed link-release / prior-knowledge dimensions / same-author artifact provenance / Python groupby and bisect tie reversal / independent quality & acceptance / all-assigned labor / synthetic adjudication. 지정 경로 RESULT.md 및 이 인계 링크를 통합 색인에 제안만 함; 중앙 파일 직접 수정 없음.
