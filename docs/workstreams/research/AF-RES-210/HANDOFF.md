# AF-RES-210 HANDOFF

- 실제 상태: **PARTIAL** (조사·설계와 원장 저장 완료; 독립 예측 효과/실행 결손).
- 작업 브랜치: work/research-af-res-210.
- 계획 SHA bb146773bbffba5e724e8c842951e2c25198c2da; 시작 SHA 87ffc1539bcf33da0fccf45eb15982a02d93e409. 기준 대비 +5/-0, dot-control만 변경. AF-RES-199 중앙 DONE, 결과 80db1b64c7fa9e6c1ccaf131813a0f10cd879aca 자체 HANDOFF PARTIAL; 지정 전제만 재사용.
- **최종 결과 SHA(이 HANDOFF 직전): 9c1c8fa669247f859381370759fd35eb8107165d**.
- 대표 파일: [RESULT.md](RESULT.md), [SELF_CHECK.md](SELF_CHECK.md), [pairs.csv](pairs.csv), [predictions.csv](predictions.csv), [mapping.csv](mapping.csv), [COUNTEREXAMPLES.md](COUNTEREXAMPLES.md), [frame.csv](frame.csv), [sources.jsonl](sources.jsonl), [SCOPE.md](SCOPE.md).
- 고정 결과 SHA에서 9파일 다시 열어 SHA·원장·프레임·입력·예측·반례·RESULT 표/약점 3행·자체검토를 대조함. GitHub compare 시작→결과 +10/-0, 9파일 모두 owned_path 아래 added, dot-control 및 타 경로 변경 없음. 이 인계는 별도 마지막 커밋. 독립 검토 없음.

## 핵심 판정
카드 pile/LIS 원전은 순서 보존 anchor chain의 길이·증인 복원을 좁힌다. R2 root 8 후보 중 길이7, return 1; 제외. C2 길이1 두 해에서 Git은 A 순회/B rank, Breezy는 B 순회/A rank이므로 보존 앵커가 달라지는 소스 기반 예측(B02/D02/D03). C1에서 Git patience는 classic fallback, Breezy는 no unique/no equal edges로 전체 replace 예측. R3 공통 자체 없음은 Git 직접 changed. Histogram은 A 빈도·연속 블록·희소도 개선으로 별도 정책. R2에 Git patience/histogram 같은 공개 expect, C04 CE3에 default difflib/명시 patience 다른 공개 expect, C05/C06에 hunk emission/indent 반례. 원전을 더한 독립 정답률 향상 입증 0건(효과 자체 미확인); 구체 tie/fallback/hunk는 구현이 필요. 더 읽기 좋다는 선호 및 카드→Git 역사적 채택 인과는 주장하지 않음.

## 분모와 막힌 이유
- 직접 열람 산입 27(목표22), A3/3 B11/7 C6/6 D5/4 E2/2, C05/C06 사후 보강 2건 제외 시 지정 시험 범위 C4/6(총25). 같은 inline helper의 입력/expect를 별도 파일로 중복 산입하지 않음. 원장 34행 중 비산입 7. A01/A02 동일 저자·계보, A03 타 기관 원논문 facsimile 한 번.
- Git 15 valid static calls/3 unique; Breezy nonempty line-list/file 12/5; 합계 27/8, 반복19, 선택4/상한제외4. 실제 시험 4 + 합성4 고정. 스칼라/Unicode/tuple/empty는 별도 그룹 제외; 행 목록 eligibility가 본문 노출 후 명료화돼 모집 범위의 사전성 결손. 정적 호출 수이지 실행 수 아님.
- 원본 기대: R1 grep only, R2/R3 full hunk expected, R4 matching pairs, C1–4 없음. 시험 source와 expect가 한 파일이고 Breezy source도 같은 열람 묶음에서 열려 M baseline 선노출; P/I/E는 재구성. 예측 원값은 M 커밋 이후 4단계 32행으로 보존. stdout 0, 독립 검토 0, 사람 실험 0. 실제 Git/Myers tie 및 최종 compaction trace 미확인. 따라서 DONE 아님.
- **첫 재개 행동:** 9c1c8fa669247f859381370759fd35eb8107165d의 pairs.csv를 읽고 아래 동일 판 실행으로 C2/C1의 반례를 우선 확인. 원전 증가분은 별도 세션에 입력/매뉴얼만 주고 기대/원전/구현을 순차적으로 격리. 지정 시험 파일 추가 2개가 실제 존재하는지 공통 helper 참조 관계로 찾아보고, 모두 inline이면 결손을 유지.

## Codex 검증 항목 — 명령은 미실행
임시 작업공간에서만 소스 확보/빌드. 비용·설치 권한이 있는 환경에서 시행하고 owned_path 외 저장소 파일 변경 금지. 아래는 깨끗한 임시 환경 기준. 먼저 프로젝트 checkout 또는 고정 결과판에서 pairs.csv 경로를 절대경로로 설정. 실행 날짜, tag 실제 commit SHA, OS, compiler/Python version, stderr/exit status 및 stdout을 저장. Git diff exit 1은 차이 있음, >1은 오류. 네트워크/빌드가 막히면 그 이유와 첫 실패 명령 기록.

```bash
# agentflow-open work branch or exact result SHA checkout
export PAIRS="$(pwd)/docs/workstreams/research/AF-RES-210/pairs.csv"
test -r "$PAIRS"
export TMP210="$(mktemp -d)"
git clone --depth 1 --branch v2.43.0 https://github.com/git/git.git "$TMP210/git"
git clone --depth 1 --branch v0.2.13 https://github.com/breezy-team/patiencediff.git "$TMP210/breezy"
git -C "$TMP210/git" rev-parse HEAD
git -C "$TMP210/breezy" rev-parse HEAD
make -C "$TMP210/git" -j2
export GIT210="$TMP210/git/git"
"$GIT210" --version
(cd "$TMP210/git/t" && sh ./t4033-diff-patience.sh)
(cd "$TMP210/git/t" && sh ./t4050-diff-histogram.sh)
(cd "$TMP210/git/t" && sh ./t4032-diff-inter-hunk-context.sh)
(cd "$TMP210/git/t" && sh ./t4061-diff-indent.sh)
# Breezy pure Python first; separately record optional C build/backend
PYTHONPATH="$TMP210/breezy" python -m unittest patiencediff.test_patiencediff
(cd "$TMP210/breezy" && python setup.py build_ext --inplace)
PYTHONPATH="$TMP210/breezy" python -m unittest patiencediff.test_patiencediff
```

동일 입력 비교(정규화 R4만 원래 list 요소에 LF를 붙임, 원래 matching test는 별도 직접 list로 검증). 실제 출력은 공개 expected와 별도 열에 기록하고, -U0와 default context, indent on/off를 분리한다.

```bash
cd "$TMP210"
PYTHONPATH="$TMP210/breezy" python - <<'PY'
import csv, json, os, pathlib, subprocess
import patiencediff
from patiencediff._patiencediff_py import PatienceSequenceMatcher_py
try:
    from patiencediff._patiencediff_c import PatienceSequenceMatcher_c
except ImportError:
    PatienceSequenceMatcher_c = None
env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
print('breezy version/backend', patiencediff.__version__, patiencediff.PatienceSequenceMatcher)
for row in csv.DictReader(open(os.environ['PAIRS'], encoding='utf-8')):
    case = row['case_id']
    a, b = [json.loads(row[k]) for k in ('a_lines_json','b_lines_json')]
    aa, bb = [x+'\n' for x in a], [x+'\n' for x in b]
    pa, pb = pathlib.Path('a'), pathlib.Path('b')
    pa.write_bytes(''.join(aa).encode('utf-8'))
    pb.write_bytes(''.join(bb).encode('utf-8'))
    print('CASE', case)
    for policy in ('myers','minimal','patience','histogram'):
        for mode in (['-U0','--no-indent-heuristic'], ['-U3','--indent-heuristic']):
            cmd = [os.environ['GIT210'],'--no-pager','diff','--no-index',
                   '--no-ext-diff','--no-textconv','--color=never',
                   '--diff-algorithm='+policy,*mode]
            if case == 'R1':
                cmd.append('--ignore-space-at-eol')
            v = subprocess.run(cmd+['--',str(pa),str(pb)],env=env,capture_output=True,text=True)
            print(policy,mode,'exit',v.returncode,v.stdout,v.stderr)
    for cls in (PatienceSequenceMatcher_py,PatienceSequenceMatcher_c):
        if cls is None:
            continue
        print(cls.__name__,cls(None,a,b).get_matching_blocks())
        for n in (0,3):
            print(''.join(patiencediff.unified_diff(aa,bb,n=n,sequencematcher=cls)))
    print('default difflib', ''.join(patiencediff.unified_diff(aa,bb,n=0)))
PY
```

검증 기대·반전 조건:
1. C2 Git/Breezy 서로 다른 root 선택(소스상의 순회 방향); 실제 출력이 같다면 compact/emit이 차이를 지웠는지, root trace가 반대인지 분리. xpatience의 find_longest_common_sequence·walk_common_sequence와 Breezy unique_lcs/recurse_matches에서 1-based/0-based 변환 후 anchor trace를 별도 로깅할 필요. instrumentation은 임시 clone에서만.
2. C1 Git fallback에서 공통 3행 가능, Breezy no match; histogram 3행 후보. 만약 실제 root/final 차이가 반대라면 B02/B03/D02/D03의 분기·등호·범위 및 compaction을 재추적. R3 all changed가 fallback 호출과 혼동되지 않도록 trace 확인.
3. R2 default context 공통 expect와 +10/-11 비교, R1 grep plus-X 확인, R4 원래 list pair와 LF 정규화 Git 차이 구별. 원래 R4 public expected (0,0),(2,2),(4,4); hunk 기대값은 없음. C3 방향 반전도 실행하고 A-only count가 결과를 바꾸는지 체크. CE6 --anchored=A와 plain, CE7 minimal vs patience를 추가 별도 입력으로 검사.
4. 별도 blind worker에 8개 입력만 전달해 M 예측 커밋, 이후 A01 Lemma1만 공개 P 커밋, 이후 고정 B/D 소스 I 커밋, 마지막 C 기대와 새 stdout을 평가. 기존 작성자는 정답에 노출되어 독립 평가자 역할 불가. 더 좁힌 후보/실제 정확 anchor/hunk/틀린 반례를 분리. 성능/읽기 효용은 사용자 과제 성공·시간·오류, merge는 base/ours/theirs 및 충돌/오병합으로 별도.

## 색인 반영 제안 (직접 수정하지 않음)
AF-RES-210: PARTIAL, 핵심 연결: patience sorting/LIS(길이·증인) ↔ 구간별 양쪽 유일 줄의 순서 보존; Git vs Breezy tie orientation와 fallback, histogram A-frequency 및 hunk compaction/context 별도. 판별 근거 RESULT 표1–3, pairs/predictions/mapping/COUNTEREXAMPLES, 고정 결과 SHA 위 참조. 199의 동일 이름≠동일 연산 전제를 재사용하되 HDR 재조사 없음. 독립 효과 및 실행 결손 포함.
