# HANDOFF — AF-RES-221
상태: **PARTIAL** (직접 열람/정적 판별 완료, 독립 기대/실행 부족). 
결과판 SHA (HANDOFF 직전, 고정 재열람): eefc1be2a41ab96a6ce024d86ca9d39394fc545e
branch: work/research-af-res-221; owned_path: docs/workstreams/research/AF-RES-221/
start: f3895893e32e2c055cefde446d34f1467fa27b4c; plan fc095c323d0177401d34f1daa7b4d1c529e2351f +5/-0; central only changed +264/-9. AGENTS/STATE/DOT_AUTOMATION/RESEARCH_WORKFLOW read, control blob recovery confirmed only depends_on AF-RES-210, its result_commit 097948b68f3be1802c06c15c7beccaeb5478c06c and HANDOFF (PARTIAL), RESULT, pairs, predictions read. 216–218 excluded. 
Representative fixed files:
- [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/eefc1be2a41ab96a6ce024d86ca9d39394fc545e/docs/workstreams/research/AF-RES-221/RESULT.md) — mandatory two tables, Q1–Q7, 3 weaknesses.
- [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/eefc1be2a41ab96a6ce024d86ca9d39394fc545e/docs/workstreams/research/AF-RES-221/sources.jsonl) — 33 records, 24 counted P3 M5 I5 E7 D4; 9 excluded.
- inputs.csv; predictions.csv (28 rows, exposure tracked); mechanisms.csv; cards.md; COUNTEREXAMPLES.md; SELF_CHECK.md; SCOPE.md + SCOPE_ADDENDUM.md. M/P/I freeze commits cf4c203ea5745d4f16f92fe5263eb6b3c91f0490, 52a60e2e9cfbf7e1f1acfd4290a700b083b51404, f466ff4854cfbe98c529c4cfc5186aa79f389aac.
- Result exact SHA reopened all 15 paths with connector, inspected ledger 24 counts/33 total, seven inputs and 28 stage rows, freeze contents, RESULT tables/Q1–7/end three rows, source limitations and counterexamples. Compared start→result: 18 commits ahead, 15 added files, all owned_path, zero others; central control untouched. No code execution, no independent evaluator. HANDOFF last-only commit.
 
## 핵심 판정
A=N–W+E–S, B=N–E+S–W, C=E–W. Coordinates array-based. C1 ski A/CP A/bilinear A; C2 A/B/B; C3 A/B/A; C4 A/A/cross (paper branch B under positive marked diagonal, not equivalent to exact crossing); C5 C/C/C. C3 (8,−4,1,−3) center +.5 vs saddle (8−12)/16=−.25, so document center and paper continuous bilinear choose opposite pairs. C2 shows fixed low policy vs bilinear. These are static predictions, not run outputs. P01 original p85 scan numerator +, matrix derivative gives − confirmed by P02 Eq2/P03 p7 face test; source-version/erratum unresolved. No assertion of historical adoption. Binary mask preserving connectivity: M01 first. Continuous bilinear saddle with four crossed edges: add P01 §2 and P02/P03 corrected formula; exact API behavior requires I02/I04, not paper alone.
 
## 미달 / 다음 첫 행동
R1 test_binary input/ref co-exposed; public E–S selected quad only, nondefault orientation. R2 test_convert_lines first literal-grid under selected directory rule, relative comparison no exact expected pair. Earlier generated configs may qualify under different rule; whole repository lex completeness unconfirmed. E03 separate fixed expected not substitute. 5 controls prospective M/P/I (15), 2 real retrospective M/P/I (6), E (7): 1 public exact selected pair, 1 relative assertion, 5 no exact expected. Independent accuracy denominator 0, runtime 0. P02 screenshot HTTP400 27MB; text read. Exact per-source access UTC missing. Next first action: open pinned inputs.csv and predictions.csv at result SHA, have independent worker use input-only then M/P/I/E reveals, and Codex run below with the exact versions. Confirm R2 selection and absolute pair by reading whole pinned test tree plus test_config baseline image or executing original tests. No automated verification was performed by web worker; instructions below are **proposed, not executed**.
 
## Codex reproducible checks (unexecuted)
Use preinstalled isolated environment with exact versions, or install only if separately authorized. In disposable checkout only, no common path writes. Record versions, stdout and exit; compare edge-pair sets (not ordered polylines). Proposed shell:
```sh
python -c 'import skimage,contourpy; print(skimage.__version__,contourpy.__version__); assert skimage.__version__=="0.25.2" and contourpy.__version__=="1.3.3"'
# With upstream repositories available at their pinned tags:
# git -C /tmp/scikit-image checkout v0.25.2
# git -C /tmp/contourpy checkout v1.3.3
# python -m pytest /tmp/scikit-image/skimage/measure/tests/test_find_contours.py -k 'binary or mask'
# python -m pytest /tmp/contourpy/tests/test_convert.py -k test_convert_lines
# python -m pytest /tmp/contourpy/tests/test_dechunk.py -k test_dechunk_lines
# python -m pytest /tmp/contourpy/tests/test_z_interp.py -k saddle
python - <<'PY'
import numpy as np, skimage, contourpy
from skimage.measure import find_contours
assert (skimage.__version__,contourpy.__version__)==("0.25.2","1.3.3")
cases={"C1":(1,-2,1,-2),"C2":(3,-1,3,-1),"C3":(8,-4,1,-3),"C4":(2,-2,2,-2),"C5":(2,2,-1,-1)}
expected={"C1":("A","A"),"C2":("A","B"),"C3":("A","B"),"C4":("A","A"),"C5":("C","C")}
def arr(t):
    a,b,c,d=t
    return np.array([[a,b],[d,c]],dtype=float)
def edge(xy):
    x,y=xy
    e=[k for k,w in (("N",y),("E",x-1),("S",y-1),("W",x)) if abs(w)<1e-10]
    return e[0] if len(e)==1 and -1e-10<=x<=1+1e-10 and -1e-10<=y<=1+1e-10 else None
def pairset(lines):
    return frozenset(frozenset((a,b)) for z in lines
                     for a,b in [(edge(z[0]),edge(z[-1]))]
                     if a and b and a!=b)
mapping={frozenset(map(frozenset,[("N","W"),("E","S")])):"A",
         frozenset(map(frozenset,[("N","E"),("S","W")])):"B",
         frozenset([frozenset(("E","W"))]):"C"}
def both(z,L=0):
    sk=[v[:,::-1] for v in find_contours(z,L)] # row,col -> x,y
    cp=contourpy.contour_generator(z=z,name="serial").lines(L)
    return sk,cp
for k,t in cases.items():
    z=arr(t)
    sk,cp=both(z)
    got=tuple(mapping.get(pairset(x),str(pairset(x))) for x in (sk,cp))
    print(k, "expected",expected[k],"observed",got,"vertices",sk,cp)
    print("orientation high",find_contours(z,0,positive_orientation="high"))
    print("fully_connected high",find_contours(z,0,fully_connected="high"))
    print("quad_as_tri",contourpy.contour_generator(z=z,name="serial",quad_as_tri=True).lines(0))
    print("flip LR",both(np.fliplr(z)), "flip UD",both(np.flipud(z)), "sign",both(-z))
for eps in [-1e-6,0,1e-6]:
    print("C4 perturb",eps,both(arr((2+eps,-2,2,-2))))
z=arr(cases["C3"]); mask=np.ones((2,2),bool); mask[0,0]=False
print("ski mask",find_contours(z,0,mask=mask))
for cm in [False,True]:
    print("CP mask",cm,contourpy.contour_generator(z=np.ma.array(z,mask=~mask),name="serial",corner_mask=cm).lines(0))
# Full real fixtures; locate consecutive segment within first array cell.
a=np.ones((8,8),dtype=np.float32); a[1:-1,1]=0; a[1,1:-1]=0
b=np.array([[1,0,0,0,0,0,0],[0,0,2,0,0,0,0],[0,2,0,0,0,0,0],[0,1,1,0,0,0,0],[0,0,0,0,0,0,1],[0,2,2,0,0,0,0],[0,0,0,0,1,0,1]],float)
def first_quad_pairs(lines):
    return [tuple(sorted((edge(x),edge(y)))) for line in lines
            for x,y in zip(line[:-1],line[1:]) if edge(x) and edge(y) and edge(x)!=edge(y)]
for label,z in [("R1",a),("R2",b)]:
    sk,cp=both(z,.5)
    print(label,first_quad_pairs(sk),first_quad_pairs(cp),"vertices",sk,cp)
# Log contrast (not default and not signed controls)
z=np.array([[1.,100.],[100.,1.]])
for level in [9.9,10,10.1,50.5]:
    for mode in ["Linear","Log"]:
        print("log contrast",level,mode,contourpy.contour_generator(z=z,name="serial",z_interp=mode).lines(level))
PY
```
Observed values in this handoff: none from new software. Predicted R1 first cell E–S, R2 N–W; C3 default CP B vs bilinear A. A swapped after LR/UD expected label permutation; sign change on C4 tie does not imply invariant pair; C4 eps positive center/saddle B for CP/bilinear, negative A (ski always A for same sign pattern). Check tie output actual vertex/connected component, CP quad_as_tri coincident center may change representation. Log expected geometric threshold 10 vs linear 50.5; preserve values. If got differs, inspect input ordering, version, corner mask, numeric equality and reference cases; do not interpret no run as failed run. Save test output separately from predictions, append independent status only if actually executed.
 
## 색인 반영 제안
Link from 210's "원전이 실제 선택을 좁히는 때" to conditional 221 card: (1) binary connectivity policy, (2) center-vs-bilinear sign mismatch, (3) Q=0 crossing vs tie contract, (4) original scan equation discrepancy and later confirmation. Record PARTIAL, result SHA above, independent expected/run missing; do not mark DONE on source count alone. Do not modify dot-control.json or any index here.
