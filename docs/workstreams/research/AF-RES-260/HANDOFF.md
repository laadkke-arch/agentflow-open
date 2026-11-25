# AF-RES-260 HANDOFF — 자체 상태 PARTIAL
- **고정 결과 SHA: f2e12227571aae21c4860e44c774bd3b3eefc674** (SELF_CHECK까지, HANDOFF 직전). [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/f2e12227571aae21c4860e44c774bd3b3eefc674/docs/workstreams/research/AF-RES-260/RESULT.md) · [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/f2e12227571aae21c4860e44c774bd3b3eefc674/docs/workstreams/research/AF-RES-260/SELF_CHECK.md) · [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/f2e12227571aae21c4860e44c774bd3b3eefc674/docs/workstreams/research/AF-RES-260/SCOPE.md).
- 작업 브랜치 work/research-af-res-260, start integration becd6b705eebf9c5b77d04ff2bc0f19e11e85415, 현재 control blob d59c3f75026b59e8937615126164860389e46acc의 AF-RES-260 RUNNING, owned_path 정확. AF-RES-247 DONE result 72657241644860b35c01c5ab7a68ff2e9b7db6b5 (own PARTIAL; result/handoff 고정판 read). 기준 계획 933a0f7d534314470c083b0aa284044a9ad45443. control/다른 경로 변경 없음. GitHub compare start..result: ahead 17, behind 0; changed files 10, 모두 owned_path.
- 완료: 2 아이콘×3 자리 정적 파일·요소·목적 연결 6/6, 정확 ordered path 3/3 match, viewBox/attributes/title 구분, 3 목적×3 모드 제거 대비 9/9 설계, X1–3/O4, 추가 X5. sources.jsonl 58 rows / 34 distinct counted (12/5/9/5/3; 하한 6/5/6/3/2 충족). 실제 GDAL binary bytes/record 판독. 필수 표/약점 및 자체 반증.
- 핵심: original alarm 689B, arrow-right311B, pinned sprite1,098,145B ASCII text; 2050 symbols 중 ID 두 개. original path tags exactly same in selected symbol; original fill=currentColor, selected symbol fill 없음. A/B host red expected, C isolated document CanvasText (black은 조건부). A host-only, B host+sprite/ID, C host+개별 SVG; 둘 동시 여섯 자리 4 files. 형상 편집 원 SVG 별도 링크, cached files 제외. 실제 픽셀/요청 미확인. GDAL SQL x와 binary byte는 이름/last_change 다름, matrix 동일 수치. Binary byte z0,col0,row0 712B PNG.
- 미달: release ZIP/npm archive bytes vs tag files 대조 미확인, 공식 OGC guide artifact 74984 미수신(다른 공식 GDAL binary/SQL 확보, 별도 표본), WPT 실행/실제 지정 6자리 browser receipts 0/6, 물리 제거/합성 통제 미실행. 웹 역할이 신규 browser 실행을 하지 않는다는 제약 준수; PARTIAL을 DONE으로 올리지 않음. 독립 검토 없음.

## 산출물 링크 (결과 고정판)
- [원자료 원장 sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/f2e12227571aae21c4860e44c774bd3b3eefc674/docs/workstreams/research/AF-RES-260/sources.jsonl)
- [icons.csv](https://github.com/laadkke-arch/agentflow-open/blob/f2e12227571aae21c4860e44c774bd3b3eefc674/docs/workstreams/research/AF-RES-260/icons.csv) 3 path rows/21 cols, exact d 및 전체 태그, blob.
- [contexts.csv](https://github.com/laadkke-arch/agentflow-open/blob/f2e12227571aae21c4860e44c774bd3b3eefc674/docs/workstreams/research/AF-RES-260/contexts.csv) 6 rows/15 cols, host/base/URI/선택/색·필요 파일.
- [fixture.html](https://github.com/laadkke-arch/agentflow-open/blob/f2e12227571aae21c4860e44c774bd3b3eefc674/docs/workstreams/research/AF-RES-260/fixture.html) 여섯 실제 HTML 자리, 내장 CSS/MIT 고지; 작성만, 실행 없음.
- [bundles.md](https://github.com/laadkke-arch/agentflow-open/blob/f2e12227571aae21c4860e44c774bd3b3eefc674/docs/workstreams/research/AF-RES-260/bundles.md) 목적별·제거·통제·Geo 비교.
- [counterexamples.md](https://github.com/laadkke-arch/agentflow-open/blob/f2e12227571aae21c4860e44c774bd3b3eefc674/docs/workstreams/research/AF-RES-260/counterexamples.md) 가설/정정 전후.
- [gpkg_byte_evidence.json](https://github.com/laadkke-arch/agentflow-open/blob/f2e12227571aae21c4860e44c774bd3b3eefc674/docs/workstreams/research/AF-RES-260/gpkg_byte_evidence.json) GDAL binary의 header/schema root/page/cell/serial type/overflow/PNG header static evidence; independent SQL check pending.

## 후속 첫 행동 — Codex 독립 검산 (아래 명령은 미실행)
허용된 Codex 작업공간에서 결과 SHA와 원자산 SHA를 고정하고 정확한 파일을 확보한다. 사용자 PC/다른 저장소 경로 변경 금지. 아래는 명령·입력·예상·반전 기준이지 실행 영수증 아님. 실제 브라우저/Playwright 준비되어 있지 않으면 도구/권한 blocker 기록하고 임의 설치하지 않는다.

```bash
set -eu
WORK=$(mktemp -d)
export WORK
git clone --no-checkout https://github.com/laadkke-arch/agentflow-open.git "$WORK/af"
git -C "$WORK/af" checkout --detach f2e12227571aae21c4860e44c774bd3b3eefc674
git clone --no-checkout https://github.com/twbs/icons.git "$WORK/icons"
git -C "$WORK/icons" checkout --detach 8d88686c03c3768a2d82ba4f20c3c4e1b100fa29
git -C "$WORK/icons" rev-parse HEAD
git -C "$WORK/icons" hash-object icons/alarm.svg icons/arrow-right.svg bootstrap-icons.svg
wc -c "$WORK/icons/icons/alarm.svg" "$WORK/icons/icons/arrow-right.svg" "$WORK/icons/bootstrap-icons.svg"
git -C "$WORK/af" diff --name-only becd6b705eebf9c5b77d04ff2bc0f19e11e85415 f2e12227571aae21c4860e44c774bd3b3eefc674
curl -fL --retry 2 https://github.com/twbs/icons/releases/download/v1.11.3/bootstrap-icons-1.11.3.zip -o "$WORK/release.zip"
curl -fL --retry 2 https://registry.npmjs.org/bootstrap-icons/-/bootstrap-icons-1.11.3.tgz -o "$WORK/npm.tgz"
sha256sum "$WORK/release.zip" "$WORK/npm.tgz"
unzip -Z1 "$WORK/release.zip"
tar -tzf "$WORK/npm.tgz"
python3 - <<'PY'
import os, pathlib, zipfile, tarfile, hashlib, xml.etree.ElementTree as E
w=pathlib.Path(os.environ["WORK"]); root=w/"icons"
ns={"s":"http://www.w3.org/2000/svg"}
z=zipfile.ZipFile(w/"release.zip"); t=tarfile.open(w/"npm.tgz")
paths=["icons/alarm.svg","icons/arrow-right.svg","bootstrap-icons.svg"]
for p in paths:
    b=(root/p).read_bytes()
    # ZIP may distribute standalone SVGs at the archive root; suffix fallback for individual SVG names.
    n=[n for n in z.namelist() if n==p or n.endswith("/"+p)]
    if not n and p.startswith("icons/"):
        n=[n for n in z.namelist() if n==p.split("/")[-1] or n.endswith("/"+p.split("/")[-1])]
    m=[m for m in t.getmembers() if m.isfile() and (m.name==p or m.name.endswith("/"+p))]
    assert len(n)==len(m)==1,(p,n,[x.name for x in m])
    for name,data in [("git",b),("zip",z.read(n[0])),("npm",t.extractfile(m[0]).read())]:
        print(p,name,len(data),hashlib.sha256(data).hexdigest(),data==b)
s=E.parse(root/"bootstrap-icons.svg").getroot()
sy=s.findall("s:symbol",ns)
print("symbols",len(sy))
for name in ["alarm","arrow-right"]:
    a=E.parse(root/"icons"/(name+".svg")).getroot()
    bs=[v for v in sy if v.get("id")==name]; assert len(bs)==1
    x=bs[0]
    assert a.get("viewBox")==x.get("viewBox")=="0 0 16 16"
    assert [p.attrib for p in a.findall("s:path",ns)]==[p.attrib for p in x.findall("s:path",ns)]
    print(name,a.attrib,x.attrib,len(a.findall("s:path",ns)))
    print("external href-like attrs",[(e.tag,k,v) for e in a.iter() for k,v in e.attrib.items() if k.split("}")[-1]=="href" or "url(" in v])
PY
```

예상 blob alarm 27160b3bf128f9a28b69c6ca2ef49fd2fae54a00, arrow 23629043909280839d225410276e26c53303d36e, sprite b7d55a8e2671b2907d23dc9a799626949528f5d8. 예상 counts 689/311/1098145, symbols2050, d 순서/attrs 3/3. archive 동일 바이트이면 동판 배포 근거 강화; 차이 있으면 각 파일의 root/path/ID 비교로 분리(동일성 철회). 다운로드 실패는 미수신 유지. 

## 실제 슬롯/제거/통제 실행 입력 (미실행)
고정 fixture, local-only HTTP, cold context, system font, 16×16, device_scale_factor=1, viewport=800×600, color_scheme=light, forced_colors=none. 설치된 Playwright 버전과 browser.version 기록, chromium/firefox/webkit 각각 지원될 때 실행. `python -m playwright --version`, `python -m pip show playwright Pillow`. 브라우저 binaries/패키지 없으면 허가된 환경 확보 후 재개, 추측하지 말 것. 다음 Python은 독립 temp bundle을 만드는 **작성 계획 코드**. 파일 제거는 cache가 아니라 실제 누락으로 테스트.

```bash
python3 - <<'PY'
import os, pathlib, shutil
w=pathlib.Path(os.environ["WORK"])
fixture=(w/"af/docs/workstreams/research/AF-RES-260/fixture.html").read_text()
for name in ("baseline","no_host","no_sprite","no_alarm","no_arrow","missing_id","decoy","unused_defs","no_b_fill"):
    d=w/"cases"/name
    (d/"page").mkdir(parents=True,exist_ok=True)
    (d/"assets/icons").mkdir(parents=True,exist_ok=True)
    for p in ("bootstrap-icons.svg","icons/alarm.svg","icons/arrow-right.svg"):
        shutil.copyfile(w/"icons"/p,d/"assets"/p)
    h=fixture
    if name=="missing_id":
        h=h.replace("bootstrap-icons.svg#alarm","bootstrap-icons.svg#af-res-260-missing",1)
    if name=="decoy":
        (d/"assets/alt/icons").mkdir(parents=True)
        shutil.copyfile(w/"icons/icons/arrow-right.svg",d/"assets/alt/icons/alarm.svg")
        h=h.replace('src="icons/alarm.svg"','src="alt/icons/alarm.svg"',1)
    if name=="unused_defs":
        i=h.index("<svg",h.index('id="A1"')); j=h.index(">",i)+1
        h=h[:j]+'<defs><g id="unused"><image href="never.svg" width="16" height="16"/></g></defs>'+h[j:]
    if name=="no_b_fill":
        i=h.index("<svg",h.index('id="B1"')); j=h.index(">",i)
        h=h[:i]+h[i:j].replace(' fill="currentColor"','')+h[j:]
    if name!="no_host":
        (d/"page/index.html").write_text(h)
    remove={"no_sprite":"bootstrap-icons.svg","no_alarm":"icons/alarm.svg","no_arrow":"icons/arrow-right.svg"}.get(name)
    if remove: (d/"assets"/remove).unlink()
PY
cat > "$WORK/probe.py" <<'PY'
import os, json, pathlib, threading, functools, http.server, traceback
from playwright.sync_api import sync_playwright
w=pathlib.Path(os.environ["WORK"]); out=w/"receipts";out.mkdir(exist_ok=True)
slots=("A1","B1","C1","A2","B2","C2")
with sync_playwright() as pw:
    for eng in ("chromium","firefox","webkit"):
        try: browser=getattr(pw,eng).launch()
        except Exception as e:
            (out/(eng+"-BLOCKED.json")).write_text(json.dumps({"engine":eng,"error":str(e)}));continue
        for d in sorted((w/"cases").iterdir()):
            server=http.server.ThreadingHTTPServer(("127.0.0.1",0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(d)))
            th=threading.Thread(target=server.serve_forever,daemon=True);th.start()
            origin=f"http://127.0.0.1:{server.server_port}"
            ctx=browser.new_context(viewport={"width":800,"height":600},device_scale_factor=1,color_scheme="light",forced_colors="none",service_workers="block")
            page=ctx.new_page();receipt={"engine":eng,"browser_version":browser.version,"case":d.name,"origin":origin,"events":[],"slots":{}}
            def gate(route):
                if route.request.url.startswith(origin+"/"): route.continue_()
                else: route.abort()
            ctx.route("**/*",gate)
            page.on("request",lambda r:receipt["events"].append({"request":r.url,"type":r.resource_type}))
            page.on("response",lambda r:receipt["events"].append({"response":r.url,"status":r.status}))
            page.on("requestfailed",lambda r:receipt["events"].append({"failed":r.url,"reason":r.failure}))
            try:
                res=page.goto(origin+"/page/index.html",wait_until="load")
                receipt["host_status"]=res.status if res else None
                page.evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
                receipt["document_base"]=page.evaluate("document.baseURI")
                for sid in slots:
                    loc=page.locator("#"+sid)
                    if not loc.count(): continue
                    receipt["slots"][sid]=loc.evaluate("""e=>({hostColor:getComputedStyle(e).color,childColor:getComputedStyle(e.firstElementChild).color,childFill:getComputedStyle(e.firstElementChild).fill,href:e.querySelector("use")?.getAttribute("href"),src:e.querySelector("img")?.currentSrc,complete:e.querySelector("img")?.complete,naturalWidth:e.querySelector("img")?.naturalWidth})""")
                    loc.screenshot(path=str(out/(eng+"-"+d.name+"-"+sid+".png")),animations="disabled")
                page.screenshot(path=str(out/(eng+"-"+d.name+"-full.png")),animations="disabled")
            except Exception as e: receipt["exception"]=traceback.format_exc()
            finally:
                (out/(eng+"-"+d.name+".json")).write_text(json.dumps(receipt,indent=2))
                ctx.close();server.shutdown();server.server_close()
        browser.close()
PY
python3 "$WORK/probe.py" 2>&1 | tee "$WORK/probe.log"
```

예상/반전 기준:
- baseline: A1/B1 red same shape candidate, A2/B2 red same shape candidate; C1/C2 CanvasText in image doc, controlled ordinary light UA black candidate (not universal). actual pixel arrays compare Pillow convert RGBA, alpha/background/antialias separately; don't compare PNG compressed file bytes as pixel equality. A1 vs B1, A2 vs B2, A vs C geometry silhouettes; each slot screenshot and decoded color histogram. img DOM box color is not inner SVG paint. 
- no_host: host 404, no slots; no_sprite: B1/B2 no icon, A/C unchanged; no_alarm: C1 fails/alt fallback, A1/B1 unchanged; no_arrow analog C2; expected request 404 vs browser actual logs. 
- missing_id: sprite resource available (network response may share B2 fetch) but B1 no target/icon; HTTP success not proof of pixels. decoy: C1 displays arrow-shaped input; compare C2 crop ignoring alt text if success. unused_defs: A1 intended unchanged; never.svg requested or not is separate measured dimension; request failure without visual change supports distinction. no_b_fill: B1 red changes to default black fill expected, host color unchanged. Each scenario fresh context and separate local server root/port. If expected fails, preserve actual receipt, record engine/version, contrast X1–X5 rather than discard.
- Receipt format: immutable input SHA and SHA256 of all case files, exact host URL/base/ID, browser engine/version, Playwright/OS, request URL/status/resource type/failure + HTTP server log, decoded PNG pixel stats and full/crop screenshot hashes/files, exception and timestamps; executed/failed/missing distinct. Use `find "$WORK/cases" -type f -print0 | sort -z | xargs -0 sha256sum`, `sha256sum "$WORK"/receipts/*`, save metadata. WPT published expectations kept separate; run selected cases with pinned WPT repo (db19ea407e861bab8158d86f07823aec5a490a4e) in authorized environment using its runner and record actual product/version, runner commands, report. No WPT execution receipt in this work.

## GeoPackage independent next input
```bash
curl -fL --retry 2 https://raw.githubusercontent.com/OSGeo/gdal/6d7a6388745ef760b68d3ea460d700f4be5479c4/autotest/gdrivers/data/gpkg/byte.gpkg -o "$WORK/byte.gpkg"
curl -fL --retry 2 https://raw.githubusercontent.com/OSGeo/gdal/6d7a6388745ef760b68d3ea460d700f4be5479c4/autotest/gdrivers/data/gpkg/byte.gpkg.sql -o "$WORK/byte.gpkg.sql"
sha256sum "$WORK/byte.gpkg" "$WORK/byte.gpkg.sql"
python3 - <<'PY'
import os,sqlite3,pathlib,json
w=pathlib.Path(os.environ["WORK"]);db=sqlite3.connect((w/"byte.gpkg").as_uri()+"?mode=ro",uri=True)
print("sqlite version",sqlite3.sqlite_version)
for q in ["PRAGMA integrity_check","PRAGMA application_id","SELECT * FROM gpkg_contents","SELECT * FROM gpkg_tile_matrix_set","SELECT * FROM gpkg_tile_matrix","SELECT id,zoom_level,tile_column,tile_row,length(tile_data),hex(substr(tile_data,1,24)) FROM byte"]:
 print(q,db.execute(q).fetchall())
print("SQL fixture contents:")
d=sqlite3.connect(":memory:");d.executescript((w/"byte.gpkg.sql").read_text())
for q in ["SELECT * FROM gpkg_contents","SELECT * FROM gpkg_tile_matrix_set","SELECT * FROM gpkg_tile_matrix","SELECT id,zoom_level,tile_column,tile_row,length(tile_data),hex(substr(tile_data,1,24)) FROM x"]: print(q,d.execute(q).fetchall())
PY
curl -fL --retry 2 'https://portal.opengeospatial.org/files/?artifact_id=74984' -o "$WORK/ogc-74984.gpkg"
file "$WORK/ogc-74984.gpkg"
sha256sum "$WORK/ogc-74984.gpkg"
```
예상 G06 actual byte not x; table_name joins, extent and matrix from gpkg_byte_evidence.json, tile id1,z0,col0,row0,length712, PNG256×256. G02 x 별도. independent SQL mismatch이면 정적 decode 수정. OGC artifact가 실제 SQLite인지 header 확인 후 read-only schema/contents/matrix_set/matrix/user table 키를 기록, 아카이브/HTML이면 미수신/형식 불명으로 기록. 지도 실행·OGC 1.4 conformance와 구분.

## 색인 제안
색인에는 AF-RES-260을 'SVG asset → consumed element → style context → minimal delivery bundle → evidence level'로 등록. AF-RES-247의 inventory/request/render 분리 및 GeoPackage table selector 대비 연결. 242/251/254/255 의존 추가하지 않음. 재사용 키: repo+version+blob; document URL/base; href/src; fragment/symbol or root; path/edit locator; consumer mode; style context; required/declared/selected/requested/rendered flags; evidence provenance and expectation/observation status. 사용자 중앙 작업표 수정하지 않음.
