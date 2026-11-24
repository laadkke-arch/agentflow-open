# AF-RES-235 HANDOFF

상태: **PARTIAL**. 지정 6셀의 날짜판 본문, W3C 정오표/원결정, 고정 소비자 원파일 및 시험 기대, 옛 감사/새 수정의 차이, RFC 대조와 반례까지 확보. 자료 최소수 충족. 다만 실제 HTML target id/name 0/6 확인(문서 절 6/6 관측)으로 요청의 링크 판정 전부를 완료했다고 하지 않는다. 2.0 #13 개별 정정일, 최초 2.2 공개 초안 정확판, 실제 사용자/runtime도 미확인. 독립 검토 0, 자체 점검 수행.

## 고정 입력과 결과
- 착수 610bcdf35a3dc04bc7f55ce1ecf0a339d9d881e6; 계획판 914dbfa789ebec97063ed97130ea2a71c2e9f503에는 AF-RES-235 항목 없음(최신 6 commits ahead); 최신 dot-control blob 71109adf1dc9cdc9b8b46464861f0af7a55b23ed의 RUNNING/brief/depends_on 확인. AF-RES-222 중앙 DONE/고정 HANDOFF fe41449d156eb5e723c254a0530863468c084480 자체 PARTIAL 유지; HANDOFF, RESULT, history.csv, names.csv 확인. 227–229 불필요.
- 브랜치 work/research-af-res-235. 소유 경로 docs/workstreams/research/AF-RES-235/.
- ① 25dd5d790d6ebab0a3ca884039a3f9803b6db26f 사전 범위/예측 봉인
- ② ba4343144b945518de681a6f473d71db1947f38f 원자료 원장
- ③ 964dc644438200847b3504475b2ddbbb86e6e6fc 필수 표·정적 관측
- ④ b86f6683ee2a910b29d9f3e096bc34c60ea683bd 반례·원결정 추가·정정
- ⑤ **결과 SHA 9d698c3e01b67fee6f189d0452efa4ccb3e2b572** RESULT.md·SELF_CHECK.md
- ⑥ 이 HANDOFF.md 단독 커밋(자기 SHA는 커밋 본문 자체로 확정할 수 없으므로 별도 branch head 확인).

대표: [RESULT.md](RESULT.md) 첫 표 1/2, Q1–Q7, 마지막 약점 3행; [sources.jsonl](sources.jsonl), [timeline.csv](timeline.csv), [consumer.csv](consumer.csv), [citations.csv](citations.csv), [rfc-controls.md](rfc-controls.md), [COUNTEREXAMPLES.md](COUNTEREXAMPLES.md), [SCOPE.md](SCOPE.md), [SELF_CHECK.md](SELF_CHECK.md), TABLES.md(중간표). 결과 SHA에서 10개 전부 다시 fetch_file로 열고 JSONL parse/ID 중복 0, Q1–Q7 headings 7, 끝 약점 3, C1/C2/C3, exact table header 및 근거 주소 확인. F77는 source ID가 아닌 기법명(G05/G06 연결; 기계 정규식 오탐 제외), 나머지 사용된 단일 source ID 모두 존재. CSV 22/8/3 데이터행. RESULT blob 6968c86e5bee9c0d9076ae4dd7fd1cca122b3559; SELF_CHECK blob 54fccd129ab5ccda2934b82ca584ee4fa5d05ed0; 원장 blob b97bb6c70d5027bab048d3f114843a6938bf638b. GitHub compare base→result ahead=5, behind=0, 파일 10개 모두 owned_path의 추가. dot-control 및 타 경로 변경 없음. 
- 원장 71 rows: 62 opened, 9 failed, 46 고유 산입(W3C 9, WG 11, axe 16, RFC 10; 각 요구 7/4/6/5). 16 repeat 제외. 선택한 변경 사건 묶음 11(통계 독립 아님). 6 최초 본문 관측, target 0/6 미확인, 4 rule×2 tags 정적 8/8, duplicate expected 6/6, runtime 0, 사용자 감사 자료 없음. 정확한 첫 UTC 대신 실제 조회 시간창 표기. 

## 결론
2.0 원문 유지+editorial #13, 2.1 원문+HTML/XML 충족간주 노트, 2.2 번호/제거 표지만. 2.2 제거 G10 2022-11-16 제안, G09 11-22 결의/11-23 병합, 2023-01-05/12 CfC, 10-05 발행. 2.0/2.1 2023-04-04 회의/4-18 정오표·PR/7-17 병합/2.1 9-21 재발행. 현행 2.1 2025-05-06, 2.2 2024-12-12. 4.8.0 2023-09-06에서는 두 rule 비활성·deprecated, aria는 4.1.2/reviewOnFail; 표준 최종판보다 먼저 도구 출시. 1.1.1 핵심 존속(2.0 cross-ref 정정), image-alt mapping 유지. RFC update와 obsoleted 및 verified errata 구별. 
옛 감사 citation은 보존, 현행 안내는 별 revision 및 적용 범위/다른 SC로 연결. ARIA 관계 결함은 실제 name/relationship 확인 없이 자동 failure로 결정하지 않는다.

## 다음 첫 행동 및 Codex 검증 인계
**1순위:** 네트워크 접근이 가능한 허용 환경에서 아래 정확 6 URL을 standard library로 직접 읽어 HTML id/name/heading 확인. 이번 세션은 raw DNS 실패; 아래 명령 미실행. HTTP 결과 및 fragment 실패를 구별하며 원본 해시/최종 URL/UTC를 owned_path 내 새 receipt에 보존. 기존 답의 candidate 링크를 검증 성공 시에만 verified로 바꾼다.

```bash
python - <<'PY'
from urllib.request import Request,urlopen
from urllib.parse import urldefrag
from html.parser import HTMLParser
from hashlib import sha256
from datetime import datetime,timezone
import json
pairs=[
 ('https://www.w3.org/TR/2008/REC-WCAG20-20081211/','ensure-compat-parses','text-equiv-all'),
 ('https://www.w3.org/TR/2018/REC-WCAG21-20180605/','parsing','non-text-content'),
 ('https://www.w3.org/TR/2023/REC-WCAG22-20231005/','parsing','non-text-content')]
class Targets(HTMLParser):
 def __init__(self, keys):
  super().__init__(); self.keys=keys; self.hits=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('id','name') and v in self.keys:
    self.hits.append({'tag':tag,'attribute':k,'target':v,'line':self.getpos()[0],'attrs':attrs})
for url,*keys in pairs:
 try:
  with urlopen(Request(url,headers={'User-Agent':'AF-RES-235/1.0'}),timeout=30) as res:
   b=res.read(); parser=Targets(keys); parser.feed(b.decode(res.headers.get_content_charset() or 'utf-8',errors='replace'))
   print(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'url':url,'final':res.geturl(),'status':res.status,'sha256':sha256(b).hexdigest(),'targets':{k:[h for h in parser.hits if h['target']==k] for k in keys}},ensure_ascii=False))
 except Exception as e: print(json.dumps({'url':url,'error':str(e),'status':'unobserved'}))
PY
```
예상: 각 후보가 1개 대상 또는 legacy name anchor에 대응하고 해당 SC 절에 도달. 0/복수/다른 절이면 명시적으로 후보 수정/불확실 표시; HTTP 오류는 0 대상 아님. raw source의 hit 주변 HTML과 브라우저 scroll/heading을 추가 대조. 2.0 #13은 W04 정오표 revision/archive 및 2022-12-13 회의, CR history, 2.0/2.1 CfC를 이어 확인. 2.2 첫 외부 공개 초안 정확판 확인. F05 EID499 개별 날짜 미확인은 원 레코드 경로 회복시 재검토.

**2순위:** 실제 브라우저 및 axe runtime 비교는 승인된 기존 Node/Playwright·브라우저·두 고정 빌드가 있는 경우에만. 설치/빌드 필요 시 별도 승인. 정확 checkout 두 SHA(A01–06)와 빌드 provenance 및 파일 SHA-256 기록, version assertion. 예: 기존 빌드 절대 경로 AXE_OLD_JS / AXE_NEW_JS를 환경에 지정, Node의 정상 공개 진입점 axe.run 사용. 입력은 C1/C2/C3과 active 대조, 같은 browser+DOM; 결과 종류/노드 target 확인. 여기서는 실행하지 않았다.

```bash
# 두 checkout에서 git rev-parse HEAD: b4f78df8fe5393efa0292f621c5dbca28eaa268c / 712026eb791ccd6469b4fa8934f819852c9949fc
# AXE_OLD_JS=/absolute/pinned-4.7.2/axe.min.js, AXE_NEW_JS=/absolute/pinned-4.8.0/axe.min.js (기존 빌드)
test -f "$AXE_OLD_JS" && test -f "$AXE_NEW_JS" || exit 1
sha256sum "$AXE_OLD_JS" "$AXE_NEW_JS"
node <<'JS'
const {chromium}=require('playwright');
const inputs={
 plain:'<p id="x">A</p><p id="x">B</p>',
 active:'<button id="a">A</button><button id="a">B</button>',
 aria:'<span id="n">Wrong title</span><span id="n">Intended title</span><button aria-labelledby="n">Open</button>',
 control:'<img src="x"><img src="y" alt="A">'
};
const ids=['duplicate-id','duplicate-id-active','duplicate-id-aria','image-alt'];
(async()=>{const browser=await chromium.launch();
 try{for(const [version,file] of [['4.7.2',process.env.AXE_OLD_JS],['4.8.0',process.env.AXE_NEW_JS]])for(const [input,html] of Object.entries(inputs)){
  const page=await browser.newPage();
  await page.setContent('<!doctype html><html lang="en"><head><title>AF235</title></head><body>'+html+'</body></html>');
  await page.addScriptTag({path:file});
  const actual=await page.evaluate(()=>axe.version); if(actual!==version)throw Error('version mismatch '+actual);
  for(const [mode,options] of [['default',{}],['wcag2a',{runOnly:{type:'tag',values:['wcag2a']}}],['explicit',{runOnly:{type:'rule',values:ids},rules:Object.fromEntries(ids.map(x=>[x,{enabled:true}]))}]]){
   const result=await page.evaluate(opts=>axe.run(document,opts),options);
   const relevant=Object.fromEntries(['violations','incomplete','passes','inapplicable'].map(k=>[k,result[k].filter(r=>ids.includes(r.id)).map(r=>({id:r.id,tags:r.tags,nodes:r.nodes.map(n=>n.target)}))]));
   console.log(JSON.stringify({version,actual,browser:browser.version(),input,mode,relevant}));
  }
  if(input==='aria')console.log(JSON.stringify({version,input,ariaSnapshot:typeof page.getByRole('button').ariaSnapshot==='function'?await page.getByRole('button').ariaSnapshot():'unavailable'}));
  await page.close();
 }}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1});
JS
```
예상 v4.7.2 generic/active/aria 각각 해당 fixture에서 violation, v4.8.0 generic/active default·wcag2a에서 제외(명시 enabled 실행 시 시험 기대는 유지), aria review/incomplete 및 wcag412. image-alt mapping wcag111 유지, 이미지 목적의 실제 동등성은 별도. 실행 결과가 다르면 consumer.csv runtime 및 예상 수정; 관계/name 정상이라면 4.1.2 failure로 단정하지 말 것. 브라우저 버전, 실제 고정 빌드 및 input 옵션 포함한 JSONL 보존. 테스트 실행과 역사적 사용자의 실관측 별개.
**3순위** 실제 audit 필요 시 날짜판·도구 버전·옵션·raw artifact가 있는 공개 사례 하나 확보; 제공되지 않은 사용자의 과거 감사로 오인 금지. 독립 reviewer는 result SHA의 Q별 근거/반례/표를 검토. 
저장소 자체 범위 재검사(필요한 경우 실행 담당): git fetch origin; git diff --name-only 610bcdf35a3dc04bc7f55ce1ecf0a339d9d881e6...9d698c3e01b67fee6f189d0452efa4ccb3e2b572; 소유 경로 확인. 이번 세션은 API compare로만 점검.

## 색인 반영 제안
AF-RES-222(동일 entity/name 유지)와 조합: Citation/Edition/ClaimRevision/ChangeEvent/ConsumerRule 상태 분리, historical intent와 current instruction을 연결. 상태 PARTIAL, 경계 미확인 명시. 중앙 상태 파일/색인은 통합 담당이 검토 후 갱신하며 이 작업에서는 손대지 않음.
