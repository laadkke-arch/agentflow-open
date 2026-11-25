# AF-RES-244 HANDOFF — PARTIAL
## 실제 상태와 결과
- 착수 통합 SHA 8e1000cd9446909bc06cb2905c89c8bc78e99beb, 진행표 blob 4c5470fdbf34e703241c29416518fb0cd9939c9e. AF-RES-231 중앙 DONE/자체 PARTIAL, 의존 e55fd8c9df7fdd45259346aeb8884a7d3586594b. 238–242 미사용. 본인 배정 branch work/research-af-res-244, owned path docs/workstreams/research/AF-RES-244/ 이외 편집 없음.
- 고정 결과 SHA (HANDOFF 직전): 659cc8a613e2ee49e1b2f6e3833ac8346f9bb794. [고정 결과 경로](https://github.com/laadkke-arch/agentflow-open/tree/659cc8a613e2ee49e1b2f6e3833ac8346f9bb794/docs/workstreams/research/AF-RES-244).
- 정확한 공식 문서판 1.6.1, 실제 제목 Gallery examples. publisher commit 34aafaf61b4a20a7520817c02a5924baf026e3fe; 원 HTML 8/8 blob 재확인. tag f159b78dc59f250cdde8fe391a21f0bc871960ad. 13개 전체 href 중 first 2 unique per symbol: 예정6, 관측5, 정상 공석1, 접근 결측0, 중복0. 배포 script와 tag 5/5 동일. 엄격한 전체 목적 직접 0/5, 조건부5/5; G connectivity 직접2/2, distance 직접0/2. API 자체 N/C 직접, G 부분. 두 면에서 N/C 3/5 직접은 API 자체 근거; gallery의 증분 효과나 인과 효과로 해석 금지.
- 84 원장행, 산입38 독립 work_id, 10 lineage_id, API3 / example/test9 / generator9 / implementation12 / NLM guidance5 / NLM direct XML0. 실패17, 기타 미산입29. 두 역사적 PubMed XML main record 사본을 직접 읽어 DescriptorName MajorTopicYN 및 qualifier 반례를 기록했으나 원제공 응답 직접 접근 0/2. 엄격 원자료 21 총량은 넘겼으나 자료별 XML 2개 하한 미달이므로 **PARTIAL**. 정확 SG build version, exact membership _codeobj, figure pixel/실행 미확인; 외부 독립 검토 및 실제 runtime tests 미실시. 자체 점검만 수행.
- 대표 파일: RESULT.md 두 필수 표/Q1~Q7/약점3; SCOPE.md 사전 기준+정정; gallery.csv 슬롯, gallery-all.csv 전체 DOM href; uses.csv 소스→호출→소비; sources.jsonl 84행; index-controls.md 반례+MeSH 원행+실행 입력; SELF_CHECK.md 근거 ID별 검토.
- 커밋 경로: ① efe2305fbc984cb79e361c30a900b54b4f342edb 사전 기준; ba841dc530afdcc597f5186947bbdc37def42ec3 여섯 슬롯 seal 전 예제 열람 안 함; ② 2ea66baa9ed83b317e8c993c5b1901b8664cd851 원장; ③ 17aac5ec8187beb68520cc9bbf57bd549b7b7f53 uses; 554d7b724340833fd270cb6952a08bb2e1e0c46e 본표; ④ b4c4e3bee9170b47cfbb4fb133fbaaf61ab6df4a index-controls; 70eb40c0c26d7f1137c925a3460788fc6b00a120 전체 anchor; 5fe637899fa390033c20a34aa007cf23662530cc SCOPE clarification; eda2b9ba1051fff34378adafb68e917474c30adb selection rule; 7c8889ba3640fffaea4aa2d1bc881079cea82e61 uses line correction; 9b21765d689a1b226b3ce3d1298f054d5df2f4fe pinned ledger; ⑤ bf53952d0bb5f1ffecd37a535feb3b85e2ccdcef RESULT final and 859f65559ea4c409860232d69dc5a17c4c7a0856 Q3/Q4 headings; 659cc8a613e2ee49e1b2f6e3833ac8346f9bb794 SELF_CHECK; ⑥ 이 HANDOFF 단독 커밋.
- 고정 result SHA 원문 자체 재조회 8/8 성공. CSV widths gallery 11×6, gallery-all 8×13, uses 15×6 데이터행(헤더 제외); 슬롯/href/원위치/source ID 매칭 true; JSONL 84 parse, unique source_id 및 전행 필수 필드 true; 38 work/10 lineage/17 fail 확인. RESULT 첫/둘/마지막 표 데이터행 6/3/3, 폭 5/5/4, Q1–Q7 heading 모두, 마지막 필수 4열 제목 일치. integration→result compare ahead14 behind0, 8 files 모두 owned path, HANDOFF 아직 없었음. 이 구조·링크·원소스 판독은 독립 검토/실행 결과가 아님.

## 다음 첫 행동 — NLM 원 XML 두 기록 (미실행; 재개 담당)
정상 NCBI 공개 API 연결 환경에서, 12091962 및 11748933을 각각 요청. 웹 접근 실패 F1–F8과 다르게 raw XML과 HTTP 상태/시간 보존. 기존 사본은 덮어쓰지 말고 owned path receipts/retry-<UTC>/에 추가. API 정책 준수; 무인증/키 없음. 아래는 재개 명령이며 이번에는 실행하지 않았다.
```bash
git fetch origin work/research-af-res-244
git switch work/research-af-res-244
git rev-parse HEAD
P=docs/workstreams/research/AF-RES-244
R="$P/receipts/retry-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$R"
for pmid in 12091962 11748933; do
  date -u +%FT%TZ > "$R/$pmid.before.utc"
  curl --get --compressed --connect-timeout 15 --max-time 60 --fail-with-body -sS \
    -D "$R/$pmid.headers" -o "$R/$pmid.xml" \
    'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi' \
    --data-urlencode db=pubmed --data-urlencode "id=$pmid" --data-urlencode retmode=xml \
    2>"$R/$pmid.stderr"
  rc=$?
  printf '%s\n' "$rc" > "$R/$pmid.exit"
  date -u +%FT%TZ > "$R/$pmid.after.utc"
  test "$rc" -eq 0 || break
  sleep 1
done
sha256sum "$R"/*.xml > "$R/xml.sha256"
python - "$R" <<'PY'
import pathlib,sys,xml.etree.ElementTree as E
r=pathlib.Path(sys.argv[1])
for pmid in ("12091962","11748933"):
    p=r/(pmid+".xml")
    root=E.parse(p).getroot()
    found=[a for a in root.findall(".//MedlineCitation") if a.findtext("PMID")==pmid]
    assert len(found)==1,(pmid,len(found))
    c=found[0]
    print("PMID",pmid,"owner",c.attrib,"revised",E.tostring(c.find("DateRevised"),encoding="unicode") if c.find("DateRevised") is not None else None)
    for h in c.findall("./MeshHeadingList/MeshHeading"):
        d=h.find("DescriptorName")
        if d is None: continue
        print(d.text, d.attrib, [(q.text,q.attrib) for q in h.findall("QualifierName")],sep="\t")
PY
```
원 XML 2 응답/HTTP 성공/각 PMID 실제 descriptor field 관측을 먼저 확인. expected historical: PMID12091962 Humans N, Prisoners Y; PMID11748933 Sperm Motility Y, Cryopreservation N + methods Qualifier Y. 현재값이 달라도 실제 관측에 따라 기록하고 historical과 다름을 명시. 원본에 descriptor 없으면 정상 결측/레코드 상태로 분리, 복사본에서 보완하지 않음. 성공 이후 sources.jsonl에 원 응답 별 source_id/receipt/hash/time/판을 추가하고 Q6 및 counts 갱신, 별도 독립 판독자 검토 필요. 원제공의 과거 제공시점과 현재 내용 차이도 별도. 직접 XML 요청이 다시 실패하면 exit/HTTP/stderr를 보존하고 PARTIAL 유지.

## Codex 실행 인계 — exact sklearn fixture
기존 허용된 실행 환경의 1.6.1 및 dependencies 사용, 새 설치나 시스템 변경 금지; checkout은 별도 scratch에서 tag commit 검증. 실제 실행하지 않았다. checkout 경로에서:
```bash
git rev-parse HEAD
python -c 'import sklearn,numpy,scipy; print(sklearn.__version__,numpy.__version__,scipy.__version__); assert sklearn.__version__=="1.6.1"'
python -m pytest -q sklearn/neighbors/tests/test_neighbors.py -k 'test_kneighbors_graph or test_precomputed_sparse_invalid or test_pairwise_boolean_distance'
```
정확 입력/출력 검증 (원래 예제와는 별도 control, stdout/stderr/exit 및 input 코드 보존):
```python
import numpy as np
from sklearn.neighbors import NearestNeighbors,KNeighborsClassifier,kneighbors_graph
X=[[0.,0.,0.],[0.,.5,0.],[1.,1.,.5]]
dist,ind=NearestNeighbors(n_neighbors=1).fit(X).kneighbors([[1.,1.,1.]])
print(dist.tolist(),ind.tolist()); assert dist.tolist()==[[0.5]] and ind.tolist()==[[2]]
c=KNeighborsClassifier(n_neighbors=3).fit([[0],[1],[2],[3]],[0,0,1,1])
labels=c.predict([[1.1]]); print(labels.tolist()); assert labels.tolist()==[0]
X=np.array([[0,1],[1.01,1.0],[2,0]])
a=kneighbors_graph(X,1,mode="connectivity",include_self=True)
b=kneighbors_graph(X,1,mode="distance",include_self=False)
print(a.format,a.shape,a.toarray(),b.format,b.shape,b.toarray())
assert a.format==b.format=="csr" and a.shape==b.shape==(3,3)
np.testing.assert_array_equal(a.toarray(),np.eye(3))
np.testing.assert_allclose(b.toarray(),[[0,1.01,0],[1.01,0,0],[0,1.40716026,0]])
for mode in ("connectivity","distance"):
    g=kneighbors_graph(X.T,1,mode=mode,include_self=False)
    print("feature graph",mode,g.shape,g.toarray())
    assert g.shape==(2,2)
```
C2 별도 보강: E3 script에서 pipeline.fit 이후 동일 X_test에 y_hat=clf.predict(X_test), labels array 및 clf.score와 np.mean(y_hat==y_test) 확인; 원본에는 이 줄이 없다. 결과와 KNC 열만 연결해서 저장. G1/G2 공개 figure 수치를 확인할 때 해당 HTML image asset, 코드 소스, local result를 각각 분리하며 전체 그림이 graph 결과로 생성되었다고 단정하지 않는다. 실제 run 금지된 이번 turn에서 실행/계측 미수행.

## SG 정확판 검증과 반전 조건
먼저 S2 min 0.17.1이 아니라 1.6.1 실제 release build env manifest/lock/CI log로 SG exact 버전을 확정. 못 하면 v0.17.1 비교 실험으로만 명시. 정확판 checkout에서 `python -m pytest -q sphinx_gallery/tests/test_backreferences.py`; test input/expected는 S6 L181–279. 별도 scratch minimal gallery: config extensions=['sphinx_gallery.gen_gallery'], sphinx_gallery_conf={'examples_dirs':'examples','gallery_dirs':'auto_examples','backreferences_dir':'backrefs','doc_module':('sklearn',),'inspect_global_variables':False,'plot_gallery':False}; examples/GALLERY_HEADER.rst 또는 해당 판 필수 README.rst, index.rst에는 auto_examples/index toctree와 `.. minigallery:: sklearn.neighbors.NearestNeighbors`. 아래 6 source 각각 제목/구문으로 파일을 만든 후 `python -m sphinx -b html . _build/html`; Sphinx/SG/sklearn version, command, exit, *.examples, HTML anchors, logs 저장. 설치/빌드 조건 허용 전에는 실행하지 않음.
1. plot_unused.py: docstring title + from sklearn.neighbors import NearestNeighbors
2. plot_access.py: 동일 import + print(NearestNeighbors)
3. plot_role.py: docstring title + :class:`~sklearn.neighbors.NearestNeighbors` (import 없음)
4. plot_plain.py: docstring title + 평문 NearestNeighbors
5. plot_discard.py: import + NearestNeighbors(n_neighbors=1).fit([[0],[1]]).kneighbors([[0.2]]) (반환 폐기)
6. 별도 minigallery explicit path 'examples/plot_plain.py' (이름 관계 없이 선택).
예상 2,3,5 name positive, 1,4 negative; 6 explicit inclusion. E1 실제 role 삭제 후 rebuild에서 유입 사라지면 명시 역할 가설 지지, 남으면 다른 route를 조사. _codeobj pickle은 신뢰할 수 없는 외부 데이터를 역직렬화하지 말고 동일 자체 생성 산출물 또는 text/AST receipt를 사용. 비교 실험과 원 빌드 동일성 분리.

## 색인 제안 (dot-control 미수정)
AF-RES-244 = PARTIAL / result 659cc8a613e2ee49e1b2f6e3833ac8346f9bb794 / handoff branch HEAD / 1.6.1 6 slots 5 observed 1 vacant / strict full 0/5, connectivity 2/2 / API alone N,C direct / exact call+consumer+result/mode/axis separate from backref / historical MeSH Y/N qualifier contrast; direct XML 0/2 missing / next public EFetch two raw records. 기존 link는 관계 탐색층으로 유지하며 목적별 반환 소비를 근거 위치와 버전으로 추가 표시. 채택 확정 아님.
