"""Reference targets and explicitly unexecuted checks; does not run Pandoc/TeX."""
import json,re,hashlib
from datetime import datetime,timezone
from audit import ROOT,corpus

D=corpus(); now=datetime.now(timezone.utc).isoformat()
def target(did,start,end,role,conditions,minpos=7000):
    d=D[did];a=d['text'].index(start,minpos);b=d['text'].index(end,a)+len(end)
    anchors=[(k,v) for k,v in d['anchors'].items() if v<=a and not k.startswith('toc-') and k not in ['TOC','title-block-header']]
    return {'doc_id':did,'start':a,'end':b,'indexing':'Unicode code points, half-open [start,end)',
            'anchor':max(anchors,key=lambda x:x[1])[0],'text':d['text'][a:b],'role':role,'conditions':conditions,
            'arrival_rule':'누적 실제 노출이 이 전체 본문 구간을 포함해야 도달. 목차 label/링크 선택만으로는 미도달.'}

rows=[
 {'case_id':'P1','selected_by':'gold_pandoc; no C/hint exposure','exact_answer_target':'outside',
  'exact_answer_reason':'원 grouped B1/B2의 결정적 section 구성/TOC 순회 규칙은 고정 구현이며 corpus manual에 없다.',
  'primary_corpus_section_target':target('p2192','--toc, --table-of-contents\n','in the output document.','O의 정확한 기능 절; P/E3 답 절은 아님',['O1']),
  'nearby_structure_target':target('p2192','Extension: fenced_divs\n','plus some attributes.','P의 입력 구문 절; TOC inclusion의 결정적 근거로 세지 않음',['P1-shape']),
  'outside_decisive_sources':[{'source_id':'PD-TOC-SHARED','locator':'574-592'},{'source_id':'PD-TOC-WRITERSHARED','locator':'429-456'}],
  'similar_label_caution':'--section-divs, fenced_divs 문법, 혹은 제목 깊이만 읽고 동급 grouped heading 보존까지 도달했다고 세지 않는다.'},
 {'case_id':'P2','selected_by':'gold_pandoc; no C/hint exposure','exact_answer_target':'outside',
  'exact_answer_reason':'매뉴얼은 정확한 입력 계약을 주지만 space/tab 이후 실제 처리와 key-set 동등성의 결정적 판정은 stock loader+consumer source를 요구한다.',
  'primary_corpus_section_target':target('p383','--abbreviations=FILE\n','with abbreviations one to a line.','정확한 파일 기능 절; 계약상 제한/보류에 사용. 실제 탭 처리 구현과 구분',['O1','P1-contract']),
  'contract_decision_target':target('p383','--abbreviations=FILE\n','The strings may not contain spaces.','문서계약 범위의 제한된 부정을 위한 완전 문단. exact implementation answer와 구별',['O1','P1-contract','E1-contract']),
  'similar_label_counter_target':target('p383','Extension: abbreviations\n','abbreviation keys are simply skipped (as opposed to being parsed as paragraphs).','파일 loader와 다른 기능이라는 반례 절',['E4']),
  'outside_decisive_sources':[{'source_id':'PD-ABBR-APP','locator':'368-376'},{'source_id':'PD-ABBR-READER','locator':'1765-1787'}],
  'similar_label_caution':'Extension: abbreviations에 정확히 도달해도 --abbreviations 파일 입력에 도달한 것으로 세지 않는다.'},
 {'case_id':'P3','selected_by':'gold_pandoc; no C/hint exposure','exact_answer_target':'outside',
  'exact_answer_reason':'float+longtable 보존의 결정적 반례는 corpus 밖이며 exact 원 환경의 성공/실패는 runtime unknown. body의 엔진 미상을 자동 LaTeX 확정으로 바꾸지 않는다.',
  'primary_corpus_section_target':target('p21403','--pdf-engine=PROGRAM\n','Use the specified engine when producing PDF output.','PDF로 확인/가정한 경우 필요한 engine 분기 기능 절. 최초 body의 output 확정 증거는 아님',['O1-conditional','E1']),
  'nearby_figure_target':target('p21403','Extension: implicit_figures\n','will be rendered as a figure with a caption.','그림 구문의 정확한 절; 실제 float/여백 보존 결정 절이 아님',['O1','E2']),
  'nearby_latex_layout_target':target('p21403','Variables for LaTeX\n','creating a PDF with a LaTeX engine.','LaTeX layout 변수의 적용 범위 절; longtable 보존 증거 아님',['E1']),
  'outside_decisive_sources':[{'source_id':'LT-R158','locator':'minimal example body'},{'source_id':'LT-R158-C','locator':'2019-09-04 / 2021-09-01 maintainer comments'},{'source_id':'PD-N8526-MD','locator':'original PDF/Quarto attachment'},{'source_id':'PD-N8526-TEX','locator':'later figure+longtable input'}],
  'additional_runtime_evidence_required':True,
  'similar_label_caution':'figure, table, margin 관련 절을 읽은 성공과 table+실제 다음-page float+하단여백 보존을 확인한 성공을 합치지 않는다.'}
]
for row in rows:
    primary=dict(row['primary_corpus_section_target'])
    primary['interval_id']=row['case_id']+'-primary-related-feature-arrival'
    primary['reason']='reference가 요청된 조작에 직접 대응하는 기능 절로 선정; label을 넘어서 실제 첫 문장까지 읽은 도달만 계산한다.'
    row['related_operation_targets']=[primary]
    row['decisive_answer_target']={'inside_corpus':False,'source_ids':[r['source_id'] for r in row['outside_decisive_sources']],'reason':row['exact_answer_reason']}
    row['other_related_targets']=[dict(t,interval_id=row['case_id']+'-'+key,reason='관련/대조 구간이며 primary operation arrival 또는 decisive answer arrival과 별도 집계') for key,t in list(row.items()) if key not in ['primary_corpus_section_target'] and isinstance(t,dict) and 'doc_id' in t]
payload={'schema':1,'created_utc':now,'selector':'independent gold_pandoc','selection_exposure':'No authoring, packets, hints, inputs, readers, trails/answers, or other gold content read.','metric_separation':'primary_corpus_section_target measures arrival at the correct related feature definition only. exact_answer_target is separately outside for the decisive conditions described here; no budget reachability is inferred.','cases':rows}
(ROOT/'target-spans.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')

ip=ROOT/'reproduction-inputs';ip.mkdir(exist_ok=True)
p1=(ip/'P1-original.md').read_text()
(ip/'P1-hierarchy-counter.md').write_text(p1.replace('## B2\n','### B2\n'))
raw=p1.replace('::: Fenced3\n','```{=html}\n<div class="Fenced3">\n```\n')
last=raw.rfind(':::\n');raw=raw[:last]+'```{=html}\n</div>\n```\n'+raw[last+4:]
(ip/'P1-raw-wrapper-candidate.md').write_text(raw)
(ip/'P2-bare-keys.txt').write_text('Foo.\nHTML\n')
(ip/'P2-space-enriched.yaml').write_text('Foo. : An expansion # retained source comment\nHTML : Hypertext Markup Language\n')
(ip/'P2-tab-enriched.txt').write_text('Foo.\t: An expansion # retained source comment\nHTML\t: Hypertext Markup Language\n')
(ip/'P2-example.md').write_text('Foo. Bar\n\nHTML is an abbreviation.\n')
tex=(ip/'P3-followup-layoutissue.tex').read_text()
(ip/'P3-followup-with-listfiles.tex').write_text('\\listfiles\n'+tex)
up=json.loads((ROOT/'snapshots/latex-issue-158.json').read_text())['body']
uptex=re.search(r'```latex\s*\n(.*?)```',up,re.S).group(1).replace('\r\n','\n')
(ip/'P3-upstream-158.tex').write_text(uptex)

checks=[
 {'check_id':'P1-original','case_id':'P1','status':'not_run','input':'reproduction-inputs/P1-original.md','provenance':'exact original inline input, line endings normalized','argv':['<PANDOC_2.19.2_BINARY>','P1-original.md','--self-contained','--toc','--output=P1-original.html'],'necessary_observations':['binary --version must be 2.19.2','TOC A1/A2 present; B1/B2 absent according to source-derived expectation','body B1/B2 present; one Fenced3 wrapper retained'],'do_not_infer':'Stored screenshot and upstream expected test output are not this execution.'},
 {'check_id':'P1-hierarchy-counter','case_id':'P1','status':'not_run','input':'reproduction-inputs/P1-hierarchy-counter.md','provenance':'researcher-constructed counterinput; changes only B2 from level 2 to level 3; not a proposed solution preserving original heading hierarchy','argv':['<PANDOC_2.19.2_BINARY>','P1-hierarchy-counter.md','--self-contained','--toc','--output=P1-hierarchy-counter.html'],'necessary_observations':['B1/B2 expected to appear as hierarchical items','one output group retained'],'do_not_infer':'This changes the natural input and never replaces P1 in the natural sample.'},
 {'check_id':'P1-raw-candidate','case_id':'P1','status':'not_run','input':'reproduction-inputs/P1-raw-wrapper-candidate.md','provenance':'researcher adaptation of same-issue 2024 raw HTML proposal; native AST shape changed','argv':['<PANDOC_2.19.2_BINARY>','P1-raw-wrapper-candidate.md','--self-contained','--toc','--output=P1-raw-wrapper-candidate.html'],'necessary_observations':['both peer headings in TOC','single Fenced3 emitted HTML grouping and valid nesting','source attributes/IDs required by real filter preserved'],'do_not_infer':'No claim of historical-version success until actually executed; native Div AST is not preserved.'},
 {'check_id':'P2-space-tab-matrix','case_id':'P2','status':'not_run','input':['reproduction-inputs/P2-bare-keys.txt','reproduction-inputs/P2-space-enriched.yaml','reproduction-inputs/P2-tab-enriched.txt','reproduction-inputs/P2-example.md'],'provenance':'constructed small inputs based on original schematic; full original file/keys unavailable','argv_template':['<PANDOC_3.8.3_BINARY>','--from=markdown+smart','--to=native','--abbreviations=<KEYS_FILE>','P2-example.md'],'variants':['P2-bare-keys.txt','P2-space-enriched.yaml','P2-tab-enriched.txt'],'necessary_observations':['exact reader token/space output, not just successful exit','bare keys expected NBSP; enriched variants expected not to match bare tokens','source files must remain byte-identical before/after; compare hashes'],'do_not_infer':'Three schematic outputs cannot prove equivalence for the unknown full YAML key set.'},
 {'check_id':'P2-smart-exception','case_id':'P2','status':'not_run','input':['reproduction-inputs/P2-bare-keys.txt','reproduction-inputs/P2-example.md'],'provenance':'constructed exception check','argv':['<PANDOC_3.8.3_BINARY>','--from=markdown-smart','--to=native','--abbreviations=P2-bare-keys.txt','P2-example.md'],'necessary_observations':['no abbreviation NBSP effect when smart disabled'],'do_not_infer':'Does not test arbitrary punctuation or multiword keys.'},
 {'check_id':'P3-tex-component','case_id':'P3','status':'not_run','input':['reproduction-inputs/P3-followup-with-listfiles.tex','reproduction-inputs/testgraphic.png'],'provenance':'original followup TeX plus non-rendered \\listfiles instrumentation; engine identity is unresolved','argv':['<ACTUAL_LATEX_ENGINE_BINARY>','-interaction=nonstopmode','-halt-on-error','-recorder','P3-followup-with-listfiles.tex'],'necessary_observations':['record exact engine --version, full log package versions and template','actual next-page figure location','table retained; text/table lower bounds against body text area across pages','repeat TeX passes as necessary until longtable widths stabilize'],'do_not_infer':'A selected current pdflatex run is not the original unknown Quarto/TeX environment.'},
 {'check_id':'P3-controls','case_id':'P3','status':'not_run','input':'reproduction-inputs/P3-original-layoutissue.md + testgraphic.png','provenance':'original attachment; controls described by author; need original actual render command','argv':['<ORIGINAL_RENDER_COMMAND_AND_OPTIONS_UNKNOWN>'],'variants':['original with extra pre-figure paragraph and table','delete pre-figure paragraph so figure fits same page','remove table','replace table with another figure'],'necessary_observations':['same actual engine/template/package environment for all variants','record float and table coordinates, page text area, log diagnostics','a success without an actual next-page float is a diagnostic control only'],'do_not_infer':'Raw Pandoc invocation need not honor Quarto format YAML or match original pipeline.'},
 {'check_id':'P3-independent-upstream-counter','case_id':'P3','status':'not_run','input':'reproduction-inputs/P3-upstream-158.tex','provenance':'original independent LaTeX issue 158 MWE','argv':['<RECORDED_LATEX_ENGINE_BINARY>','-interaction=nonstopmode','-halt-on-error','P3-upstream-158.tex'],'variants':['original first figure no placement argument','first figure [htbp] diagnostic variant'],'necessary_observations':['verify whether h placement avoided genuine floating in the second variant','package/runtime version recorded'],'do_not_infer':'A passed independent MWE does not by itself decide exact P3.'}
]
cp={'schema':1,'created_utc':now,'all_product_runtime_status':'not_run','required_setup':'Use an already available exact historical binary/engine if authorized later; this task did not install or run it.','checks':checks,'input_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ip.iterdir()) if p.is_file()}}
(ROOT/'unexecuted-checks.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'targets':len(rows),'checks':len(checks),'all_runtime':'not_run','inputs':len(cp['input_hashes'])},ensure_ascii=False))
