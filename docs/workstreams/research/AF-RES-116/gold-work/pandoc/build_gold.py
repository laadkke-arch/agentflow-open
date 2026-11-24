"""Rebuild independent reference records from already captured/read first-party sources."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, re, shutil
from audit import ROOT, BASE, corpus

DOCS=corpus()
NOW=datetime.now(timezone.utc).isoformat()
READS=[json.loads(x) for x in (ROOT/'read-log.jsonl').read_text().splitlines()]
SPANS=[]

def span(sid,did,start,end,conditions,role,claim,required=False,minpos=10000):
    d=DOCS[did]; text=d['text']
    a=text.index(start,minpos);b=text.index(end,a+len(start))
    while b>a and text[b-1]=='\n':b-=1
    anchors=[(k,v) for k,v in d['anchors'].items() if v<=a and not k.startswith('toc-') and k not in ['TOC','title-block-header']]
    anchor=max(anchors,key=lambda x:x[1])[0]
    small=text[a:b].split('\n')[0]
    row={'interval_id':sid,'doc_id':did,'start':a,'end':b,'indexing':'Unicode code points; half-open [start,end)',
         'anchor':anchor,'url':d['url']+'#'+anchor,'version':d['version'],'upstream_commit':d['upstream_commit'],
         'quote':small[:100],'text':text[a:b],'condition_ids':conditions,'evidence_role':role,'supports':claim,
         'required_for_complete_case':required,'source_sha':d['source_sha']}
    SPANS.append(row);return sid

span('P1-O-selfcontained','p2192','--self-contained\n','--embed-resources\n',['O1','E1'],'operation + exception','2.19.2 self-contained는 embed-resources와 standalone의 동의어다.',True)
span('P1-O-toc','p2192','--toc, --table-of-contents\n','Note that if you are producing a PDF via ms',['O1','E1'],'operation + exception','TOC 생성과 standalone 요구를 설명한다. fenced div 내부 heading 포함은 증명하지 않는다.',True)
span('P1-E-depth','p2192','--toc-depth=NUMBER\n','--strip-comments\n',['E2'],'exception','기본 깊이 3이므로 원문의 level-2 B1/B2 누락은 단순 깊이 부족으로 설명되지 않는다.',True)
span('P1-P-fenced-shape','p2192','Extension: fenced_divs\n','Extension: bracketed_spans\n',['P1'],'input structure only','fenced Div 문법·그룹·중첩만 정의한다. 해당 그룹 heading의 TOC 포함을 증명하지 않는다.')
span('P1-E-unlisted','p2192','If the unlisted class is present in addition to unnumbered','Extension: implicit_header_references\n',['E4'],'exception','unnumbered+unlisted는 HTML 등에서 TOC 제외 조건이다. 원 입력에는 없음.')
span('P1-E-section-divs','p2192','--section-divs\n','--email-obfuscation=',['E5'],'counter-option','section-divs는 출력 section 포장과 ID 위치 옵션이며 임의 fenced group의 heading 수집 보장은 아니다.')
span('P1-E-native-divs','p2192','Extension: native_divs\n','Extension: native_spans\n',['E6'],'workaround exception','일반 HTML div 태그는 native Div로 읽힐 수 있다. 단순 태그 치환을 raw block과 동일시하지 않는다.')
span('P1-O-raw-attribute','p2192','Generic raw attribute\n','LaTeX macros\n',['O2','E6'],'conditional workaround building block','명시된 형식의 raw block 문법과 출력 형식 의존성을 증명한다. 원 입력 수정/필터의 실행 성공은 증명하지 않는다.')
span('P2-O-file-contract','p383','--abbreviations=FILE\n','--trace[=true|false]\n',['O1','P1','E1','E2'],'input contract + justified hold','한 행 한 약어, 공백 불가, Markdown reader 용도와 기본 파일 대체 규칙. 첫 공백/탭 이후를 버리는 구현은 이 문단에 없다.',True)
span('P2-E-smart','p383','Extension: smart\n','Note: If you are writing Markdown',['E3'],'exception','smart는 약어 뒤 NBSP를 넣으며 markdown 입력에서 기본 활성화다.')
span('P2-E-different-abbreviations','p383','Extension: abbreviations\n','Extension: alerts\n',['E4'],'similar-label counterexample','PHP Markdown Extra 약어 정의 키는 건너뛴다. --abbreviations 파일에 YAML/comment parsing을 추가하는 기능이 아니다.',True)
span('P3-O-pdf-path','p21403','Creating a PDF\n','When using LaTeX, the following packages',['O1','E1'],'conditional operation','PDF 생성, 기본 LaTeX와 대체 중간형식, 생성 TeX를 확인하는 디버깅 방법. 원 body가 PDF라고 말한 증거는 아니다.',True,minpos=7000)
span('P3-E-pdf-engine','p21403','--pdf-engine=PROGRAM\n','--pdf-engine-opt=STRING\n',['E1'],'engine exception','출력형식별 기본 PDF 엔진이 다르다. --to와 --pdf-engine 미제공을 pdflatex 확정으로 바꾸지 않는다.',True)
span('P3-O-figure','p21403','Extension: implicit_figures\n','Extension: link_attributes\n',['O1','P1','E2'],'figure precondition + limitation','단독 이미지+비어있지 않은 alt의 figure/caption 변환, 출력형식별 차이. 다음 페이지 float와 여백 보존은 보장하지 않는다.',True)
span('P3-O-pipe-table','p21403','Extension: pipe_tables\n','Since the pipes indicate column boundaries',['O1'],'operation syntax','첨부의 pipe table 형식과 header/alignment 조건. 페이지 flow는 증명하지 않는다.')
span('P3-E-latex-scope','p21403','Variables for LaTeX\n','Layout\n',['E1'],'format scope','다음 LaTeX 변수는 LaTeX 엔진 PDF에 적용된다.')
span('P3-P-geometry','p21403','geometry\noption for geometry package','hyperrefoptions\n',['P1','E3'],'layout parameter, not preservation proof','geometry 여백 설정 문법. float+longtable spill 부재를 보장하지 않는다.')
span('P3-E-margin-override','p21403','margin-left, margin-right, margin-top, margin-bottom\nsets margins if geometry','pagestyle\n',['E3'],'exception','geometry가 별도 margin 변수를 덮어쓴다.')
span('P3-E-wkhtmltopdf-scope','p21403','Variables for wkhtmltopdf\n','Variables for man pages\n',['E1','E4'],'similar-label counterexample','같은 margin 이름이라도 wkhtmltopdf 전용 문단은 LaTeX float/longtable 보존 근거가 아니다.')

CASES=[
{
 'case_id':'P1','specified_version':'2.19.2','fixed_commit':DOCS['p2192']['upstream_commit'],
 'O':{'id':'O1','definition':'원 게시글 Markdown을 2.19.2의 self-contained HTML+자동 TOC로 변환한다.'},
 'P':{'id':'P1','definition':'동급 B1/B2를 같은 Fenced3 그룹에 둔 구조를 유지하면서 두 항목을 모두 TOC에 남긴다. A1/A2로 쪼개는 것은 원 보존조건의 충족이 아니다.'},
 'expected_qualified_answer':{
  'disposition':'unmodified_native_div_input_does_not_preserve_requested_toc_membership',
  'answer':'기본 2.19.2 HTML writer에서 원 B1/B2 그룹은 이 목표를 충족하지 않는다. self-contained는 standalone을 포함하고 기본 TOC 깊이는 3이므로 --standalone 추가나 깊이 증가만으로 이 구조 문제가 해결된다고 할 수 없다. section builder는 Div가 heading으로 시작하고 뒤의 직접 Header들이 더 깊은 수준이며 특별 class/ID 제약을 통과할 때 section과 Div를 합친다. B1/B2는 같은 수준이라 이 경로에 들지 않고, TOC는 Header로 직접 시작하는 section-like Div만 방문하므로 그룹 안의 두 section을 보지 않는다. 본문에는 B1/B2가 남는 것과 TOC 포함은 별개다.',
  'conditional_alternative':'HTML 출력용 명시적 raw HTML opening/closing blocks 또는 이를 만드는 적절한 필터는 방출 HTML의 한 div 포장을 유지하면서 heading을 TOC 수집에 노출시키는 후보다. 이는 native Div AST 보존과 동일한 계약이 아니며, 2024 댓글 예시/2.19.2 raw 문법에 기반한 후보일 뿐 역사 바이너리 실행 성공으로 기록하지 않는다. 모든 attribute/ID, 필터 순서, 다른 출력 형식을 별도 검증해야 한다.',
  'evidence_level':'D2 fixed source implementation + D1 original report and maintainer explanation; D3 not performed'
 },
 'necessary_exceptions_counterinputs':[
  {'id':'E1','essential':True,'text':'TOC에는 standalone이 필요하지만 이 버전 self-contained가 이미 standalone을 포함한다. HTML 목표와 다른 writer의 규칙을 섞지 않는다.','corpus_intervals':['P1-O-selfcontained','P1-O-toc']},
  {'id':'E2','essential':True,'text':'기본 TOC depth 3은 원문의 level-2 B1/B2를 포함할 깊이다. 깊이만 늘리면 해결된다는 추측을 배제한다.','corpus_intervals':['P1-E-depth']},
  {'id':'E3','essential':True,'text':'정확한 구조 조건: 첫 block Header, 뒤의 직접 Header들은 더 깊은 level; column/columns/fragment class 제외; outer/inner ID가 둘 다 비고/같지 않으면 병합되지 않음. 복수 heading 전부 불가라는 일반화는 틀리다. 공식 toc.md는 #E/##e 같은 계층형 복수 heading이 포함되는 반례다.','corpus_intervals':[],'outside_sources':['PD-TOC-SHARED:574-592','PD-TOC-WRITERSHARED:429-456','PD-TEST-TOC']},
  {'id':'E4','essential':False,'text':'unnumbered+unlisted, 또는 요청 깊이 밖 heading은 또 다른 제외 조건이다. 원 입력에는 적용되지 않음.','corpus_intervals':['P1-E-unlisted']},
  {'id':'E5','essential':False,'text':'--section-divs의 출력 포장 설명을 임의 Div 내부 heading 포함 보장으로 읽지 않는다.','corpus_intervals':['P1-E-section-divs']},
  {'id':'E6','essential_if_raw_workaround_recommended':True,'text':'plain HTML div는 native_divs로 재구성될 수 있으므로 raw_attribute block과 구별한다. raw HTML 방식은 HTML output 및 source/AST 변경 허용 조건이 붙는다.','corpus_intervals':['P1-E-native-divs','P1-O-raw-attribute']}
 ],
 'minimum_supporting_intervals':[x for x in SPANS if x['interval_id'].startswith('P1-')],
 'outside_corpus_minimum_evidence':[{'source_id':'PD-TOC-SHARED','locator':'lines 574-592','conditions':['P1','E3']},{'source_id':'PD-TOC-WRITERSHARED','locator':'lines 429-456','conditions':['P1','E3']},{'source_id':'PD-TOC-WRITER','locator':'lines 283-291 and 510-524','conditions':['O1','P1']}],
 'justified_hold':'TOC 옵션/깊이와 fenced_divs 문법까지만 읽었다면 grouped headings 보존은 아직 증명되지 않았다고 보류한다. 원 보고를 반복하는 것은 동작 메커니즘의 문서 근거가 아니다.',
 'corpus_support_gap':'허용 매뉴얼의 가까운 절들은 O와 문법을 뒷받침하지만 E3의 section 수집 구현은 제공하지 않는다. 필수 구조 근거를 매뉴얼 라벨/예제만으로 대체하지 않는다.',
 'source_exhaustiveness':{'sufficient_for_unmodified_fixed_version_disposition':True,'sufficient_for_all_possible_workarounds':False,'historical_runtime_executed':False,'three_open_reachability':'not assessed by this reader; parent enumerator decides using exact intervals and gaps'},
 'known_gaps':['2.19.2 바이너리 실행 없음.','원 conditional Lua filter는 제공되지 않음.','원 native group 보존과 출력 HTML group 보존 중 변경 허용 범위는 추가 합의가 필요할 수 있음.']
},
{
 'case_id':'P2','specified_version':None,'fixed_version':'3.8.3','fixed_commit':DOCS['p383']['upstream_commit'],
 'O':{'id':'O1','definition':'설명·주석이 섞인 단일 원본을 --abbreviations 입력으로 직접 읽는다. 별도 산출 약어 파일 생성 단계를 제거하는 것이 조작 목표다.'},
 'P':{'id':'P1','definition':'원본의 설명·주석을 계속 보유하고, 기존 생성기의 필요한 고유 약어 키 집합과 동등하게 인식한다. 설명을 출력 문서에 표시하라는 요구가 아니다.'},
 'expected_qualified_answer':{
  'disposition':'unsupported_by_stock_3_8_3_abbreviation_loader',
  'answer':'판 미지정이므로 규칙대로 고정한 3.8.3에서도 abbr. : expansion 또는 abbr. 뒤 탭+comment를 그대로 --abbreviations에 주어 bare abbr.를 얻는 기능은 없다. readAbbreviations는 UTF-8 text의 비어 있지 않은 각 행 전체를 Set으로 만들며 YAML key/value, #comment 또는 첫 공백/탭 분리를 하지 않는다. Markdown str parser가 공백을 포함하지 않는 token을 이 Set과 정확히 비교하므로 설명이 붙은 전체 행은 원래 약어 token과 일치하지 않는다. 중복된 동일 행 제거와 YAML key 집합 생성은 다른 연산이다.',
  'preservation_option':'설명·주석을 가진 원본은 유지하고, 검증된 생성/전처리 단계가 bare key 목록을 매 실행 시 공급하게 하면 동기화 파일 관리 부담을 줄일 수 있다. 이것은 요청한 stock Pandoc의 직접 YAML 읽기와 다르다. 완전한 실제 약어 목록이 없으므로 단순 첫 공백 분리만으로 임의 YAML의 정확한 키 집합을 보장하지 않는다.',
  'evidence_level':'D2 fixed App/Markdown source + D1 manual/regression discussion; D3 not performed'
 },
 'necessary_exceptions_counterinputs':[
  {'id':'E1','essential':True,'text':'공식 계약은 한 행 한 약어, 공백 없음이다. 실제 구현은 space와 tab을 포함한 행 전체를 보관하며, 첫 공백/탭 이후를 comment로 버리지 않는다.','corpus_intervals':['P2-O-file-contract'],'outside_sources':['PD-ABBR-APP:368-376','PD-ABBR-READER:1765-1787']},
  {'id':'E2','essential':True,'text':'custom 파일을 선택하면 기본파일을 읽는 분기 대신 그 파일을 읽는다. defaults와 자동 union하지 않는다. 같은 행 dedup과 서로 다른 expansion을 가진 같은 key dedup을 혼동하지 않는다.','corpus_intervals':['P2-O-file-contract'],'outside_sources':['PD-ABBR-APP:371-376']},
  {'id':'E3','essential_for_claim_of_usable_abbreviation_effect':True,'text':'약어 효과는 Markdown reader의 smart가 활성화된 문맥에서 나타난다. plain matching token 다음 whitespace를 NBSP로 바꾸는 것이며, citation/note 및 구조적 whitespace의 예외가 있다. period 없는 약어는 2021 변경 이후 가능하므로 마침표 필수라고 일반화하면 틀린다.','corpus_intervals':['P2-E-smart'],'outside_sources':['PD-ABBR-READER:1765-1787','PD-R7124-C']},
  {'id':'E4','essential_if_abbreviations_extension_cited':True,'text':'Extension: abbreviations는 PHP Markdown Extra *[HTML]: ... 키를 건너뛰는 기능이다. YAML source reader나 comment-aware --abbreviations loader로 사용할 수 없다.','corpus_intervals':['P2-E-different-abbreviations']}
 ],
 'minimum_supporting_intervals':[x for x in SPANS if x['interval_id'].startswith('P2-')],
 'outside_corpus_minimum_evidence':[{'source_id':'PD-ABBR-APP','locator':'lines 368-376','conditions':['O1','P1','E1','E2']},{'source_id':'PD-ABBR-READER','locator':'lines 1765-1787','conditions':['P1','E3']}],
 'justified_hold':'--abbreviations 문단을 읽으면 enriched line이 문서화된 입력 계약을 벗어나며 direct YAML 지원을 확인하지 못했다고 결론내릴 수 있다. 그러나 매뉴얼의 spaces만으로 실제 tab stripping/no-stripping 구현이나 YAML 파싱 동작까지 확인했다고 말하지 않는다. 비슷한 이름의 Extension: abbreviations만 읽은 경우에는 약어 입력 파일 처리에 대한 근거가 없다고 보류한다.',
 'corpus_support_gap':'매뉴얼은 입력 계약의 한계와 유사 표지 반례를 주지만, 첫 공백/탭 이후를 버리지 않는 readAbbreviations 구현과 Set 의미는 corpus 밖이다. 계약에 근거한 제한된 부정과 구현을 확인한 완전한 부정을 구별한다.',
 'source_exhaustiveness':{'sufficient_for_stock_fixed_version_direct_loading_disposition':True,'sufficient_for_exact_user_key_set_equivalence':False,'reason':'실제 YAML/약어 전체집합 미제공; code path는 확정했으나 모든 custom parser/전처리의 정확성은 평가하지 않음.','historical_runtime_executed':False,'three_open_reachability':'not assessed by this reader'},
 'known_gaps':['원 작성자가 사용한 Pandoc 판은 불명; 3.8.3은 연구 규칙상 고정판이다.','실제 YAML, 중복 key 정책, multiline/quoted key, 전체 약어 집합은 미제공.','3.8.3 실행 없음; source-level inference를 실행 관찰로 승격하지 않음.']
},
{
 'case_id':'P3','specified_version':'2.14.0.3','fixed_commit':DOCS['p21403']['upstream_commit'],
 'O':{'id':'O1','definition':'원문이 제시한 표·그림·복수 문단의 페이지 출력을 렌더링한다. 최초 body에는 output format, command, engine이 명시되지 않았다.'},
 'P':{'id':'P1','definition':'표와 그림을 유지하고 그림이 다음 페이지로 실제 떠도 뒤따르는 텍스트/표가 하단 여백을 침범하지 않아야 한다. 표 제거/그림 대체/그림이 같은 페이지에 남는 대조를 성공 사례로 대체하지 않는다.'},
 'evidence_layers':[
  {'layer':'sealed_body','fact':'2.14.0.3, float+table의 overflow 보고와 table 제거/다른 figure로 대체하는 대조; command/output engine 미제공','source_id':'PD-N8526'},
  {'layer':'original_attachment_read_after_seal','fact':'layoutissue.md는 PDF 렌더 지시, Quarto 언급, html/pdf/docx format YAML 및 pipe table을 포함한다. 이것으로 PDF 의도가 추가 확인되지만 정확 Quarto/TeX 엔진·package 판은 정해지지 않는다.','source_id':'PD-N8526-MD'},
  {'layer':'later_comments_and_attachment','fact':'유지관리자 2023-01-05 확인 보고 및 longtable 의심; 작성자의 2023-01-07 첨부는 graphicx+longtable를 쓰는 TeX 재현 입력이다. 같은 자연 이슈 계보이며 새 독립 회귀로 세지 않는다.','source_ids':['PD-N8526-C','PD-N8526-TEX']}
 ],
 'expected_qualified_answer':{
  'disposition':'hold_runtime_preservation_guarantee; investigate_LaTeX_longtable_path_conditionally',
  'answer':'2.14.0.3이라는 Pandoc 판만으로 하단 여백 보존이나 특정 수정의 성공을 보장할 수 없다. 추가 원 첨부는 PDF/Quarto, 후속 첨부는 LaTeX longtable 경로를 가리킨다. 고정 LaTeX writer는 table을 longtable로, 단독 captioned image를 figure로 내보내고 default template은 htbp를 설정한다. 이 경로에서 longtable의 page/output routine과 실제 TeX/package 판을 확인해야 한다. 원 보고를 재현할 command·engine·template·package 환경이 없고 역사 실행도 하지 않았으므로 exact P3 해결 여부는 unknown이다.',
  'minimum_next_check':'실제 렌더 명령, Quarto/engine/TeX 배포판 및 longtable 버전, 생성된 standalone .tex와 log를 확보한다. 원 첨부에서 그대로 float가 다음 페이지에 놓이는 경우, 추가 문단 제거로 그림이 같은 페이지인 경우, 표 제거, 표를 그림으로 바꾼 경우를 같은 환경에서 비교한다. table 유지+실제 float+여백 보존을 동시에 확인해야 성공이다.',
  'evidence_level':'D1 original/maintainer reports and upstream independent counterinputs; D2 fixed writer/template and longtable source; D3 not performed'
 },
 'necessary_exceptions_counterinputs':[
  {'id':'E1','essential':True,'text':'원 body의 엔진 미상을 보존하고, 첨부/후속 확인을 새 층으로 기록한다. PDF는 LaTeX 외 경로도 있으므로 margin/figure 문단을 output-agnostic 보장으로 쓰지 않는다.','corpus_intervals':['P3-O-pdf-path','P3-E-pdf-engine','P3-E-latex-scope']},
  {'id':'E2','essential':True,'text':'implicit_figures는 alt+단독 paragraph의 figure 변환이고 output format에 따라 달라진다. float의 위치와 table 이후 page flow의 안전을 증명하지 않는다. 그림을 inline으로 바꾸거나 h 위치에 붙잡는 성공은 요청한 떠도 보존 조건을 시험한 것이 아니다.','corpus_intervals':['P3-O-figure'],'outside_sources':['PD-LATEX-WRITER:386-403','PD-LATEX-TEMPLATE:327-340','LT-R158-C']},
  {'id':'E3','essential':True,'text':'geometry 설정과 margin 변수 우선순위는 구성 조건이다. 값을 바꾸어 float/page 조합을 피하는 것과 overflow 결함의 해결을 구별한다.','corpus_intervals':['P3-P-geometry','P3-E-margin-override'],'outside_sources':['LT-R158','LT-DTX-416:1308-1347,1413-1437,2041-2113']},
  {'id':'E4','essential':True,'text':'표를 regular table/tabular로 바꾸면 다중 페이지 table 요구를 잃을 수 있다. longtable는 row 내부 page break와 다중 column의 한계도 있다. 이들은 해결 대안의 제약이며 현재 자연 입력에 모두 존재한다는 뜻은 아니다.','corpus_intervals':[],'outside_sources':['PD-N8526-C','LT-DTX-416:174-184,270-274,582-583,1025-1038']},
  {'id':'E5','essential':True,'text':'longtable v4.14 변경 또는 #137의 TeX Live 2024 성공은 모든 float 조합/P3 성공을 보장하지 않는다. #158은 수정 이후에도 같은 test가 실패했다고 maintainer가 기록했다. 현재 열린/닫힌 상태만으로 역사 판의 재현을 확정하지 않는다.','corpus_intervals':[],'outside_sources':['LT-R158-C','LT-R137-C']}
 ],
 'minimum_supporting_intervals':[x for x in SPANS if x['interval_id'].startswith('P3-')],
 'outside_corpus_minimum_evidence':[{'source_id':'PD-LATEX-TABLE','locator':'lines 45-77','conditions':['O1']},{'source_id':'PD-LATEX-WRITER','locator':'lines 386-403','conditions':['O1','E2']},{'source_id':'LT-R158','locator':'complete minimal example in body','conditions':['P1','E3','E5']},{'source_id':'LT-R158-C','locator':'2019-09-04 and 2021-09-01 maintainer comments','conditions':['E2','E5']}],
 'justified_hold':'페이지 output/engine이 빠진 원 요청에서 일반 figure/table 구문이나 geometry 문단만 읽었다면 보존 여부를 확정하지 않는다. LaTeX 분기를 가정해 조건부 조사 방향을 제시할 수 있으나, actual float+table+margin의 성공을 본 것처럼 말하지 않는다.',
 'corpus_support_gap':'허용 2.14.0.3 manual은 renderer 분기·figure/table 구문·여백 변수를 설명하지만 float+longtable output-routine 반례나 P3 해결 증거를 제공하지 않는다. P의 실현을 보장하는 corpus span은 식별되지 않았다.',
 'source_exhaustiveness':{'sufficient_for_engine_independent_preservation_decision':False,'sufficient_to_reject_unqualified_guarantee':True,'sufficient_to_identify_conditional_LaTeX_investigation':True,'historical_runtime_executed':False,'three_open_reachability':'not assessed by this reader'},
 'known_gaps':['원 실행 명령, 실제 PDF engine 및 engine version, Quarto version, 템플릿, TeX distribution/longtable package version unknown.','원 Markdown YAML의 format 중 무엇이 실제 사용되었는지는 body에 없음.','독립 historical rendering을 하지 않았으므로 reported overflow와 suggested remedy의 실행결과 미검증.','2021 longtable 4.16 source는 비교용 고정 구현이지 원 작성자의 설치 버전으로 확인된 것이 아님.']
}]

GOLD={'schema':1,'task':'AF-RES-116','reader':'gold_pandoc','compiled_utc':NOW,
 'scope':'independent reference reading; no authoring/hints/packets/experimental recipient results read',
 'exposure_note':'cases.json을 처음 표시할 때 전체 cases 객체가 표시되어 I1/I2/I3 요청문도 잠깐 보였음. 어떤 authoring, packets, hints, inputs, readers, trails/answers 또는 다른 gold 내용도 읽지 않았음.',
 'fixed_source_rule':'manual versions/anchors counted as one work; issue comments and attachments share their issue lineage; linked code/tests grouped conservatively',
 'runtime_statement':'No Pandoc/TeX conversion or regression suite was executed by this reader. Fetch, extraction, hashing, interval construction, and JSON checks are research tooling, not product runtime evidence.',
 'read_timestamps':'read-log.jsonl; large initial search/anchor display suffered tool truncation; every decisive excerpt was displayed again in bounded ranges before use',
 'corpus_sha256':hashlib.sha256((BASE/'corpus.json.gz').read_bytes()).hexdigest(),
 'source_counts':{'definition_unique':4,'regression_unique':3,'natural_request_lineages_already_counted_elsewhere':3,'new_allocated_unique':7,
 'definition_lineages':['pandoc-manual-all-versions','pandoc-section-toc-implementation','pandoc-abbreviation-input-implementation','pandoc-latex-generation-implementation'],
 'regression_lineages':['pandoc-8741-div-header-ids','pandoc-7124-abbreviation-limits','latex-longtable-float-tools3512-137-158'],
 'conservative_allocation_note':'longtable 4.16 implementation and independent extra issues 782/1023/8520/PR4392 were read but not added to the seven allocated works; natural-issue followups and tests likewise do not inflate counts.'},
 'cases':CASES}
(ROOT/'gold.json').write_text(json.dumps(GOLD,ensure_ascii=False,indent=2)+'\n')
(ROOT/'corpus-minimum-intervals.json').write_text(json.dumps(SPANS,ensure_ascii=False,indent=2)+'\n')

def rd(source):
    return [r for r in READS if r['source']==source]

SOURCES=[]
def source(sid,name,work,author,version,cases,confirmed,allocation='additional/same-work',count=False,limits=None,original_url=None):
    rp=ROOT/'snapshots'/(name+'.receipt.json')
    receipt=json.loads(rp.read_text()) if rp.exists() else {}
    reads=rd(name)
    row={'source_id':sid,'original_url':original_url or receipt.get('original_url'),'arrived_url':receipt.get('arrived_url'),
     'work_id':work,'lineage':work,'author':author,'version_or_published_date':version,
     'checked_utc':receipt.get('finished_utc'),'read_utc':[r['display_utc'] for r in reads],
     'read_sections':[r['sections'] for r in reads],'confirmed':confirmed,
     'limits':limits or '문서/소스 판독이며 제품 runtime 실행 증거가 아니다. public issue 현재 body는 최초 게시 당시 편집 전 body의 복원이 아니다.',
     'counter_observation_or_unknown':'case gold의 necessary_exceptions_counterinputs와 known_gaps 참조.',
     'questions':{'Q2':'조작/보존/예외의 실제 근거 위치와 corpus 외 격차','Q5':'유사 절/라벨과 충분한 판정의 차이','Q6':'구체적 반대 입력과 한계','Q7':'완전 근거의 가능성과 잘못된 확신을 구분하며 시간절약/채택을 추정하지 않음'},
     'linked_case_rows':cases,'allocation':allocation,'unique_counted':count,'primary':True,
     'status':'actually_read' if reads else 'captured_not_directly_read','evidence_level':'D2' if name.endswith(('.hs','.latex','.dtx')) else 'D1',
     'snapshot':str((ROOT/'snapshots'/name).relative_to(BASE)) if (ROOT/'snapshots'/name).exists() else None,
     'receipt':str(rp.relative_to(BASE)) if rp.exists() else None,'sha256':receipt.get('sha256')}
    SOURCES.append(row)

for did,sid,alloc,count in [('p2192','PD-MANUAL-2192','definition',True),('p383','PD-MANUAL-383','additional/same-work',False),('p21403','PD-MANUAL-21403','additional/same-work',False)]:
 d=DOCS[did];r=json.loads((BASE/d['capture_receipt']).read_text());reads=rd(did)
 SOURCES.append({'source_id':sid,'original_url':d['upstream_source_url'],'arrived_url':d['observed_source_arrival_url'],'work_id':'pandoc-manual-all-versions','lineage':'pandoc-manual-all-versions','author':'John MacFarlane and Pandoc contributors','version_or_published_date':d['version'],'upstream_commit':d['upstream_commit'],'checked_utc':r['finished_utc'],'read_utc':[q['display_utc'] for q in reads],'read_sections':[q['sections'] for q in reads],'confirmed':'위 corpus-minimum-intervals에 O/P/E 역할을 구분한 정확한 본문 구간 참조.','limits':'historical MANUAL.txt를 installed Pandoc 3.1.11.1로 렌더링한 corpus다. historical public HTML, native browser, 해당 historical binary 실행이 아니다. 최초 대형 anchor/search 표시 일부가 tool truncation되었으므로 결정적 내용은 재표시한 구간만 사용.','counter_observation_or_unknown':'문법/옵션 설명이 preservation 구현 또는 runtime guarantee가 되지 않음.','questions':['Q2','Q5','Q6','Q7'],'linked_case_rows':[{'p2192':'P1','p383':'P2','p21403':'P3'}[did]],'allocation':alloc,'unique_counted':count,'primary':True,'status':'actually_read','evidence_level':'D1','snapshot':d['source_file'],'receipt':d['capture_receipt'],'sha256':d['source_sha']})

cfg=[
 ('PD-TOC-SHARED','2.19.2-src_Text_Pandoc_Shared.hs','pandoc-section-toc-implementation','John MacFarlane / Pandoc contributors','2.19.2 53325aa2',['P1'],'makeSections의 첫 Header/직접 후속 Header level, class, ID 병합 제약을 실제 읽음.','definition',True),
 ('PD-TOC-WRITER','2.19.2-src_Text_Pandoc_Writers_HTML.hs','pandoc-section-toc-implementation','Pandoc contributors','2.19.2 53325aa2',['P1'],'HTML writer가 makeSections 후 shared TOC 생성기를 사용함.'),
 ('PD-TOC-WRITERSHARED','2.19.2-src_Text_Pandoc_Writers_Shared.hs','pandoc-section-toc-implementation','Pandoc contributors','2.19.2 53325aa2',['P1'],'sectionToListItem은 Header로 시작하는 Div만 재귀 처리; 임의 Div는 빈 목록.'),
 ('PD-ABBR-APP','3.8.3-src_Text_Pandoc_App.hs','pandoc-abbreviation-input-implementation','John MacFarlane / Pandoc contributors','3.8.3 568dab14',['P2'],'비어 있지 않은 전체 lines를 Set.fromList. YAML/comment/첫 whitespace 분리 없음.','definition',True),
 ('PD-ABBR-READER','3.8.3-src_Text_Pandoc_Readers_Markdown.hs','pandoc-abbreviation-input-implementation','Pandoc contributors','3.8.3 568dab14',['P2'],'smart guard, token 정확 매칭, 후속 whitespace/NBSP, citation/note 예외 및 PHP abbreviation key skip.'),
 ('PD-LATEX-TABLE','2.14.0.3-src_Text_Pandoc_Writers_LaTeX_Table.hs','pandoc-latex-generation-implementation','Pandoc contributors','2.14.0.3 227f675c',['P3'],'tableToLaTeX가 longtable을 내보내는 경로.','definition',True),
 ('PD-LATEX-WRITER','2.14.0.3-src_Text_Pandoc_Writers_LaTeX.hs','pandoc-latex-generation-implementation','Pandoc contributors','2.14.0.3 227f675c',['P3'],'captioned single image의 figure 출력 및 minipage/note 예외.'),
 ('PD-LATEX-TEMPLATE','2.14.0.3-data_templates_default.latex','pandoc-latex-generation-implementation','Pandoc template contributors','2.14.0.3 227f675c',['P3'],'longtable package, image bounds, default figure htbp 및 geometry 처리.'),
 ('PD-R8741','issue-8741.json','pandoc-8741-div-header-ids','BBBalls','2023-04-01 body; reported Pandoc 3.1.2',['P1'],'file-scope on/off의 EPUB split/TOC 대조. P1 historical HTML 실행과는 구별.','regression',True),
 ('PD-R8741-C','issue-8741-comments.json','pandoc-8741-div-header-ids','jgm; BBBalls; aaron-meyers','2023-04-02 through 2024-04-20',['P1'],'서로 다른 Div/Header ID가 section 처리에 간섭한다는 maintainer 설명. anchor 보존 때문에 단순 폐기가 문제.'),
 ('PD-R7124','issue-7124.json','pandoc-7124-abbreviation-limits','gwern','2021-03-04 body',['P2'],'et al, periodless, multiword 입력을 제시한 확장 요구. body의 period 필수 주장은 후속 변경으로 갱신됨.','regression',True),
 ('PD-R7124-C','issue-7124-comments.json','pandoc-7124-abbreviation-limits','jgm; gwern','2021-03-04 through 2021-03-10',['P2'],'period 필요조건은 완화했으나 spaces는 허용하지 않았다는 maintainer 변경 기록. 근거 없는 현재 period 제한을 반박.'),
 ('LT-R158','latex-issue-158.json','latex-longtable-float-tools3512-137-158','annProg','2019-07-16 body',['P3'],'float 두 개와 longtable의 짧은 독립 TeX MWE; 일부 수정을 거친 뒤에도 overflow 반례.','regression',True),
 ('LT-R158-C','latex-issue-158-comments.json','latex-longtable-float-tools3512-137-158','Frank Mittelbach; David Carlisle; contributors','2019-09-04 through 2023-10-24',['P3'],'htbp 대조가 h 배치로 진짜 float를 피한 것이라는 설명; v4.14 이후에도 이 test가 실패했다는 기록.'),
 ('LT-R137','latex-issue-137.json','latex-longtable-float-tools3512-137-158','timsifive','2019-03-25 body',['P3'],'관련 spill 보고와 tools/3512 계보. body 앞 9000자만 읽었으며 긴 MWE 후반부는 읽지 않음.'),
 ('LT-R137-C','latex-issue-137-comments.json','latex-longtable-float-tools3512-137-158','David Carlisle; Ulrike Fischer; stale bot','2019-11-28 through 2024-10-31',['P3'],'2024-10-31 maintainer가 original MWE의 TeX Live 2024 성공을 보고. P3 또는 모든 변형의 성공 증거 아님.'),
 ('LT-DTX-416','latex-longtable-2021.dtx','latex-longtable-float-tools3512-137-158','David Carlisle; David Kastrup; LaTeX team','longtable 4.16 2021-05-07; commit 7fe2b014',['P3'],'multipage tabular, row boundary page breaks, multiple-column incompatibility, v4.14 output routine 변경을 직접 읽음.'),
 ('PD-TEST-TOC','2.19.2-test-command-toc.md','pandoc-section-toc-implementation','Pandoc test contributors','2.19.2 53325aa2',['P1'],'공식 counterinput: #C/#D peer headings in one Div are absent, #E/##e hierarchy appears. Markdown output test이며 HTML은 shared implementation으로 연결.'),
 ('PD-TEST-SECTION','2.19.2-test-command-section-divs.md','pandoc-section-toc-implementation','Pandoc test contributors','2.19.2 53325aa2',['P1'],'same section ID nested example. 추가 독립 저작으로 세지 않음.'),
 ('PD-TEST-COLUMNS','2.19.2-test-command-make-section-column-divs.md','pandoc-section-toc-implementation','Pandoc test contributors','2.19.2 53325aa2',['P1'],'column/columns div를 일반 section으로 합치지 않는 official rendering expectation.'),
 ('PD-TEST-ABBR','3.8.3-test-command-md-abbrevs.md','pandoc-abbreviation-input-implementation','Pandoc test contributors','3.8.3 568dab14',['P2'],'Mr. Bob NBSP와 escaped period의 counterinput. 저장된 expected output이며 실행 안 함.'),
 ('PD-TEST-ABBR-DATA','3.8.3-test-command-abbrevs','pandoc-abbreviation-input-implementation','Pandoc test contributors','3.8.3 568dab14',['P2'],'Foo. 및 h.k.의 simple line fixture. enriched YAML fixture는 아님.'),
 ('PD-ADDITIONAL-8520','issue-8520.json','pandoc-8520-abbreviation-directory','bpj','2023-01-04',['P2'],'user data dir의 abbreviation path/language lookup 요청. 본 요청의 syntax 지원을 증명하지 않아 allocation 제외.'),
 ('PD-ADDITIONAL-782','issue-782.json','pandoc-782-short-table-breaks','reubano','2013-03-13 body; current metadata updated 2026',['P3'],'짧은 표 page break 제어와 float 대안의 tradeoff. 현재 open 상태를 cutoff 역사 상태로 사용하지 않음.'),
 ('PD-ADDITIONAL-1023','issue-1023.json','pandoc-1023-two-column-longtable','nrnrnr','2013-10-14 body; current metadata updated 2026',['P3'],'two-column longtable 오류 반례. 2026 closed 상태/새 floating table 기능을 2.14에 소급하지 않음.'),
 ('PD-ADDITIONAL-4392','issue-4392.json','pandoc-pr4392-proposed-table-environment','pajowu','2018-02-22 PR body; current metadata updated 2026',['P3'],'table environment switch 제안 PR. 제안/미병합 여부와 2.14 지원을 혼동하지 않음.')
]
for args in cfg:source(*args)
for n,cid,author in [(8518,'P1','ulrichb'),(8522,'P2','bpj'),(8526,'P3','chromevanadium')]:
 x=json.loads((BASE/f'recruitment/pandoc/issue-{n}.json').read_text());reads=rd(f'original-issue-{n}')
  # Original transport receipt is kept by the recruiter; no new fetch is implied.
 rpath=BASE/f'recruitment/pandoc/issue-{n}.json.receipt.json'
 r=json.loads(rpath.read_text())
 SOURCES.append({'source_id':f'PD-N{n}','original_url':x['html_url'],'capture_original_url':r.get('original_url'),'arrived_url':r.get('arrived_url'),'work_id':f'natural-pandoc-{n}','lineage':f'natural-pandoc-{n}','author':author,'version_or_published_date':x['created_at'],'checked_utc':r.get('finished_utc'),'read_utc':[r['display_utc'] for r in reads],'read_sections':['original body, metadata, body hash'],'confirmed':'봉인 natural request의 직접 body를 읽었고 해시 일치.','limits':'현재 body snapshot이며 최초 원문 복원 주장 없음; natural allocation은 parent가 이미 셈.','counter_observation_or_unknown':'body에 남은 uncertainty를 gold case에 보존.','questions':['Q2','Q5','Q6','Q7'],'linked_case_rows':[cid],'allocation':'additional/same-work','unique_counted':False,'primary':True,'status':'actually_read','evidence_level':'D1','snapshot':f'recruitment/pandoc/issue-{n}.json','receipt':str(rpath.relative_to(BASE))})
 source(f'PD-N{n}-C',f'issue-{n}-comments.json',f'natural-pandoc-{n}','issue participants', 'comments captured after packet seal',[cid],'원 사건 후속 설명; 동일 natural lineage로만 사용.')
source('PD-N8518-IMAGE','8518-reported-output.png','natural-pandoc-8518','ulrichb','2023-01-03 linked attachment',['P1'],'reported screenshot에 A1/A2 TOC 존재, B1/B2 TOC 부재 및 body 존재. 실제 binary 실행 아님.')
source('PD-N8526-MD','8526-layoutissue.md','natural-pandoc-8526','chromevanadium','original attachment 2023-01-05',['P3'],'PDF/Quarto 명시 및 format YAML, standalone figure, pipe table; body-only uncertainty와 구별.')
source('PD-N8526-TEX','8526-layoutissue.txt','natural-pandoc-8526','chromevanadium','followup attachment 2023-01-07',['P3'],'article/graphicx/longtable, figure 뒤 longtable과 반복 paragraph. 독립 저작/실행으로 세지 않음.')
for nm,sid in [('8526-testgraphic-original.png','PD-N8526-IMAGE'),('8526-testgraphic-followup.png','PD-N8526-IMAGE2')]:source(sid,nm,'natural-pandoc-8526','chromevanadium','2023 original/followup image',['P3'],'실제 pixel 표시를 읽음; 두 그림 바이트의 SHA-256가 같음. 레이아웃 runtime 증거 아님.')
for v in ['2.19.2','3.8.3','2.14.0.3']:source('PD-TREE-'+v,f'tree-{v}.json','discovery-index-pandoc','jgm/pandoc','fixed '+v,['P1','P2','P3'],'필터한 source/test 경로 inventory만 읽음. 구현이나 회귀의 추가 저작으로 세지 않음.')
source('LT-COMMIT-INDEX','latex-longtable-2021-commit.json','discovery-index-latex','latex3/latex2e','2021-05-08 commit metadata',['P3'],'2021-06-23 이전 longtable path 마지막 commit을 API로 고정. 원 사용자의 설치판이라는 뜻 아님.')
source('PD-N8520-C','issue-8520-comments.json','pandoc-8520-abbreviation-directory','GitHub API','capture time',['P2'],'댓글 배열이 비어 있음을 직접 확인; 의미적 별도 저작 아님.')

(ROOT/'sources-pandoc.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in SOURCES))
(ROOT/'source-allocation.json').write_text(json.dumps({'compiled_utc':NOW,'counted':[{'source_id':s['source_id'],'work_id':s['work_id'],'allocation':s['allocation']} for s in SOURCES if s['unique_counted']],'definition':sum(s['unique_counted'] and s['allocation']=='definition' for s in SOURCES),'regression':sum(s['unique_counted'] and s['allocation']=='regression' for s in SOURCES)},ensure_ascii=False,indent=2)+'\n')

# Original case-specific excerpts, not new natural requests.
ip=ROOT/'reproduction-inputs';ip.mkdir(exist_ok=True)
orig=json.loads((BASE/'recruitment/pandoc/issue-8518.json').read_text())['body']
p1=re.search(r'```md\r?\n(.*?)\r?\n```',orig,re.S).group(1).replace('\r\n','\n')+'\n'
(ip/'P1-original.md').write_text(p1)
shutil.copyfile(ROOT/'snapshots/8526-layoutissue.md',ip/'P3-original-layoutissue.md')
shutil.copyfile(ROOT/'snapshots/8526-layoutissue.txt',ip/'P3-followup-layoutissue.tex')
shutil.copyfile(ROOT/'snapshots/8526-testgraphic-original.png',ip/'testgraphic.png')

assert len({s['work_id'] for s in SOURCES if s['unique_counted']})==7
assert all(s['status']=='actually_read' for s in SOURCES if s['unique_counted'])
assert all(DOCS[s['doc_id']]['text'][s['start']:s['end']]==s['text'] for s in SPANS)
print(json.dumps({'case_ids':[c['case_id'] for c in CASES],'interval_count':len(SPANS),'source_rows':len(SOURCES),'definition_count':4,'regression_count':3,'output':'gold.json + sources-pandoc.jsonl + corpus-minimum-intervals.json'},ensure_ascii=False))
