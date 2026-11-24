# AF-RES-211 — HANDOFF

**실제 상태: PARTIAL.** 핵심 버전별 코드 지원 판별 및 22개 하한 달성. 실제 HTTP·redirect·HTML fragment와 과거 도착지 확인이 결손이므로 완료로 승격하지 않는다.

- branch: work/research-af-res-211; 시작 SHA 87ffc1539bcf33da0fccf45eb15982a02d93e409, 계획 bb146773bbffba5e724e8c842951e2c25198c2da 대비 ahead 5 behind 0, dot-control만 차이. AF-RES-200 중앙 DONE, 인계 1ae3b56d3f445188109c343b00a1b67516f683ce의 실제 PARTIAL 전제 사용.
- **마지막 결과 SHA(이 인계 직전): 456f63aabd3f77f90ac4f1cef5d3db08a2de0701**. 5개 결과 묶음 SHA: 78bd44ff1d66cb33701276cc01b23267b84059be / c64ffcd3222fce03280583615caa365e7c3656d0 / 00f8c6cf31d72f0e54bc1f4012eedff992a33273 / acc2201c3f117879c1a42b45e78ada9a81a974e2 / 456f63aabd3f77f90ac4f1cef5d3db08a2de0701. 마지막 HANDOFF는 별도 커밋.
- 고정 결과에서 10개 파일 직접 readback: RESULT, SELF_CHECK, SCOPE, frame, sources, versions, destinations, citations, TABLE_DRAFT, COUNTEREXAMPLES. JSONL 59행/고유 ID 59/산입 38/고유 work 38; fixed 8, publisher 4, consumer 5, hosting 9, standard 3, supplement 9. frame 77×8, versions 4×12, destinations 18×16, citations 8×11 (헤더 제외), 열 수 일관, destinations source ID 결손 없음. 시작 대비 5 commits, 10 added files 전부 owned_path. 자체 검토 수행, 독립 검토 없음; repo 전체 테스트 및 Python 런타임 미실시.
- 18자리 모두 기록, 15자리 본문·SHA 읽음, 3자리 P numeric 실패. Raw HTTP/HTML id 0/12 rendered slots; 역사 슬롯 실제 당시 도착지 0/6, 소비자 href 8개 당시 archive 없음. DNS exit 6, HTTP 000은 404가 아님. Y03–Y06 RTD success 실제 build logs 확인; F03–F06 shell-only 기록 보존 후 정정.
- 대표 파일: [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/456f63aabd3f77f90ac4f1cef5d3db08a2de0701/docs/workstreams/research/AF-RES-211/RESULT.md), [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/456f63aabd3f77f90ac4f1cef5d3db08a2de0701/docs/workstreams/research/AF-RES-211/SELF_CHECK.md), [destinations](https://github.com/laadkke-arch/agentflow-open/blob/456f63aabd3f77f90ac4f1cef5d3db08a2de0701/docs/workstreams/research/AF-RES-211/destinations.csv), [sources](https://github.com/laadkke-arch/agentflow-open/blob/456f63aabd3f77f90ac4f1cef5d3db08a2de0701/docs/workstreams/research/AF-RES-211/sources.jsonl), [COUNTEREXAMPLES](https://github.com/laadkke-arch/agentflow-open/blob/456f63aabd3f77f90ac4f1cef5d3db08a2de0701/docs/workstreams/research/AF-RES-211/COUNTEREXAMPLES.md).
- 색인 반영 제안(반영하지 않음): 기능 문서 alias vs exact version vs commit source; U/P old API 지원 및 history role; 목적별 18자리; PARTIAL(raw navigation/history). 연결 AF-RES-200(관측·상태·시점 분리). 216 설치 관련 제외 유지.
- 핵심: U 1.26.18과 P 9.5.0에서 old deprecated but supported; U2.0.0/P10.0.0에서는 제거; 새 이름은 두 지정판 모두 존재하나 U1.25.8 역반례. stable 최신 페이지에 이름이 없어도 old pinned 호출 무효 아님, history old 이름이 있어도 현재 지원 아님. 고정판 HTML 불가 시 SHA 문서 원본+source fallback. 역사 인용은 원 href 보존, 현재 자료와 날짜 표시.

## 첫 재개 행동 — Codex 검증 (미실행)

아래 네트워크 probe는 기존 문서 읽기 제한을 우회하지 않고 공개 인터넷에 접근 가능한 정상 환경에서 수행. 허가되지 않은 인증, 설치, 외부 업로드 금지. 임시 파일은 /tmp; 새 결과를 커밋한다면 owned_path에만. 새 환경에서 start SHA/계정 권한을 확인하고 branch drift가 있으면 중단·재검토.

```bash
git fetch origin work/research-af-res-211
git switch work/research-af-res-211
git rev-parse HEAD
git status --short
git diff --name-only 87ffc1539bcf33da0fccf45eb15982a02d93e409 HEAD
python3 - <<'PY'
import csv, pathlib, subprocess, tempfile, datetime, json
from urllib.parse import urldefrag, unquote
from html.parser import HTMLParser
p=pathlib.Path('docs/workstreams/research/AF-RES-211')
class Probe(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.title=[]; self.in_title=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        if tag=='a' and a.get('name'): self.ids.add(a['name'])
        if tag=='title': self.in_title=True
    def handle_endtag(self,tag):
        if tag=='title': self.in_title=False
    def handle_data(self,data):
        if self.in_title: self.title.append(data)
inputs=[]
with (p/'destinations.csv').open() as f:
    inputs.extend((r['slot'],r['input_url']) for r in csv.DictReader(f) if r['path']!='sha')
with (p/'citations.csv').open() as f:
    inputs.extend((r['citation_id'],r['original_href']) for r in csv.DictReader(f))
inputs += [('P-root-9','https://pillow.readthedocs.io/en/9.5.0/'),('P-root-10','https://pillow.readthedocs.io/en/10.0.0/'),('W01','https://www.w3.org/TR/2018/REC-WCAG21-20180605/#dfn-single-pointer'),('W02','https://www.w3.org/TR/WCAG21/#dfn-single-pointer'),('Y07','https://www.w3.org/TR/2025/REC-WCAG21-20250506/#dfn-single-pointer')]
with tempfile.TemporaryDirectory() as d:
    for i,(slot,url) in enumerate(inputs):
        page,frag=urldefrag(url)
        body=pathlib.Path(d)/f'{i}.html'; hdr=pathlib.Path(d)/f'{i}.headers'
        now=datetime.datetime.now(datetime.timezone.utc).isoformat()
        r=subprocess.run(['curl','-sS','-L','--max-time','30','--max-redirs','10','-D',str(hdr),'-o',str(body),'-w','%{http_code} %{url_effective}',page],capture_output=True,text=True)
        parser=Probe()
        if body.exists(): parser.feed(body.read_text(errors='replace'))
        print(json.dumps(dict(slot=slot,utc=now,input_url=url,sent_url=page,fragment=frag,exit=r.returncode,final=r.stdout,error=r.stderr,headers=hdr.read_text(errors='replace') if hdr.exists() else '',title=''.join(parser.title),fragment_found=(unquote(frag) in parser.ids if frag and r.returncode==0 else None)),ensure_ascii=False))
        # Before temporary cleanup, manually inspect body and heading surrounding exact id;
        # rerun a specific input with -o /tmp/af-res-211-page.html if needed.
PY
```

For every raw request, retain actual status+redirect chain, final URL (query retained), header date vs observed time, exact HTML id (or legacy name), adjacent heading and call-support text; distinguish server redirect fragments from client fragment. Failure status 000/DNS remains unknown; do not equate to 404. Deduplicate URL requests for efficiency but map outcomes back to all 18 positions. A 2xx response that is a generic error page is not confirmation. On valid numeric P page, promote exact doc and retain SHA as supporting link; on old anchor present, remove proposed anchor change, not the version warning. If no successful old numeric build found, search public RTD versions/build records or upstream docs policy, and record no-result rather than assert never existed. For historical cases use citations.csv UTC and original_href; check publicly available contemporaneous archived snapshots/RTD build records around dates; snapshot date and title must be independently visible, latest observation is not substitute. No source acquisition bypass.

### Runtime verification (only if pre-existing isolated exact environments available; no installation authorized)

Run these commands with the appropriate environment's Python for each 1.26.18/2.0.0 and 9.5.0/10.0.0; verify version first, use local object calls only (no HTTP requests). Capture warning/exception and return type/values. Consult existing pinned repository tests before executing any newly written test. Expected old U accepted with warning / TypeError, new accepted both, both keywords ValueError on 1.26.18; total default 10. Expected old P alias warns / AttributeError, new enum LANCZOS 1 both, BICUBIC 3 both. Difference reverses static inference and is recorded, not overwritten. Quality equivalence not inferred from enum alone.

```bash
python - <<'PY'
import urllib3, warnings
from urllib3.util import Retry
print(urllib3.__version__)
for kw in (dict(method_whitelist={'GET'}),dict(allowed_methods={'GET'}),dict(method_whitelist={'GET'},allowed_methods={'GET'}),dict(total=10)):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        try:
            x=Retry(**kw); print(kw,x.total,x.allowed_methods,[(type(v.message).__name__,str(v.message)) for v in w])
        except Exception as e: print(kw,type(e).__name__,str(e))
PY
python - <<'PY'
import PIL, warnings
from PIL import Image
print(PIL.__version__)
im=Image.new('RGB',(64,64))
for name in ('ANTIALIAS','Resampling.LANCZOS','Resampling.BICUBIC'):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        try:
            x=Image
            for part in name.split('.'): x=getattr(x,part)
            print(name,int(x),im.resize((32,32),x).size,[(type(v.message).__name__,str(v.message)) for v in w])
        except Exception as e: print(name,type(e).__name__,str(e))
PY
```

Current task conclusion remains PARTIAL until raw observations or documented failure reason are independently verified; no claim of archive success or runtime execution. Follow-up must preserve earlier values and source IDs. 
