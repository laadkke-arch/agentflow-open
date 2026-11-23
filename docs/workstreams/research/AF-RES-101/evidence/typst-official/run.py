#!/usr/bin/env python3
"""Researcher fixtures for frozen AF-RES-101 candidates; not OP executions."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import fitz
from PIL import Image

OUT = Path(__file__).resolve().parent
TASK = OUT.parents[1]
CACHE = TASK / '.cache' / 'typst-official'
BINARY = CACHE / 'typst-x86_64-unknown-linux-musl' / 'typst'
INPUT = OUT / 'inputs'
OUTPUT = OUT / 'outputs'
INPUT.mkdir(parents=True, exist_ok=True)
OUTPUT.mkdir(parents=True, exist_ok=True)
Image.new('RGB', (100, 60), (30, 130, 220)).save(INPUT / 'synthetic-image.png')

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

fixtures = []
def add(name, source, candidate, role, note, expected_exit=0):
    fixtures.append(dict(id=name, source=source, candidate_id=candidate, role=role,
                         transformation=note, expected_exit=expected_exit))

head_a1 = '''#set page(height: 16.5cm, width: 18cm, margin: 1cm)
#set text(14pt, fill: rgb("#444444"))
#let members = range(1, 5).map(i => [Author #i \\ Lab #i \\ #link("mailto:author" + str(i) + "@example.invalid")])
#let edges = (paint: silver, thickness: 1pt, dash: "dashed")
'''
add('a1-initial', head_a1 + '''#set align(center)
#set page(background: grid(columns: (1fr, 1fr), rows: (1fr, 1fr, 1fr, 1fr), row-gutter: 1cm, block(height: 100%, width: 100%, stroke: edges)))
#grid(columns: (1fr, 1fr), rows: (1fr, 1fr, 1fr, 1fr), row-gutter: 1cm, ..members)
''', 'TY-A1', 'initial-control', 'Synthetic four authors replace all source names/affiliations/emails. Same page, grid track/gutter, single background block and text settings; reduced wrapper only.')
for name, extras in [('a1-c2', ''), ('a1-c3-outset-2pt', ', outset: 2pt'), ('a1-c3-outset-2cm', ', outset: 2cm')]:
    add(name, head_a1 + '''#let framed(item) = {
  set align(center + horizon)
  box(width: 100%, height: 100%, stroke: edges''' + extras + ''', item)
}
#grid(columns: (1fr, 1fr), rows: (1fr, 1fr, 1fr, 1fr), row-gutter: 1cm, ..members.map(framed))
''', 'TY-A1-C2' if not extras else 'TY-A1-C3', 'candidate' if not extras else 'researcher-specified-variant',
        'Synthetic authors. Same per-cell wrapper operation; for C3 only, researcher supplies outset and retains width/height because original suggestion did not specify them.')

mathhead = '#set page(width: 300pt, height: 90pt, margin: 12pt)\n#let colMath(x, color) = text(fill: color)[$#x$]\n'
add('a2-initial-success', mathhead + '#colMath($s_2^-$, red)\n', 'TY-A2', 'initial-success-control', 'Exact known working helper/call, page dimensions added for inspection.')
add('a2-initial-fail', mathhead + '$a x^2 + b x + c colMath(s_2^-, red)$\n', 'TY-A2', 'initial-failure-control', 'Original reported failed no-hash caller instantiated with the stated expression.', 1)
add('a2-c1', mathhead + '#let red = red\n$a x^2 + b x + c colMath(s_2^-, red)$\n', 'TY-A2-C1', 'candidate', 'Same helper and argument; added outer binding exactly as candidate first revision.')
add('a2-c2-exact', mathhead + '$colMath(s_2, #red)$\n', 'TY-A2-C2', 'candidate-literal', 'Literal first-comment caller lacks the superscript minus; this alone cannot establish preservation of original expression.')
add('a2-c2-original-expression', mathhead + '$a x^2 + b x + c colMath(s_2^-, #red)$\n', 'TY-A2-C2', 'candidate-applied-to-original-input', 'Researcher retains original math expression while applying only the proposed #red argument escape.')
add('a2-c1-shadowed', mathhead + '#let red = blue\n$a x^2 + b x + c colMath(s_2^-, red)$\n', 'TY-A2-C1', 'counterexample-input-state', 'Researcher changes outer binding to blue; helper/caller identical to C1. Tests scope-value dependence, not a claimed user attempt.')

pagehead = '#set page(width: 300pt, height: 216pt, margin: 20pt)\n'
fig = 'figure(rect(width: 100pt, height: 60pt, fill: aqua), caption: [CAP])'
add('u1-c1-literal-pagebreak', pagehead + 'BEFORE\n#pagebreak\n#align(center + horizon, ' + fig + ')\n#pagebreak\nAFTER\n',
    'TY-U1-C1', 'literal-prose-token-control', 'Tests literal #pagebreak from prose, without adding missing call parentheses.')
add('u1-c1-called-pagebreak', pagehead + 'BEFORE\n#pagebreak()\n#align(center + horizon, ' + fig + ')\n#pagebreak()\nAFTER\n',
    'TY-U1-C1', 'candidate-with-explicit-call', 'Parentheses supplied to invoke pagebreak; align is the named centering step. Synthetic rectangle/caption and markers replace image and surrounding text.')
add('u1-c2-page', pagehead + 'BEFORE\n#page[\n#set align(center + horizon)\n#' + fig + '\n]\nAFTER\n',
    'TY-U1-C2', 'candidate', 'Synthetic rectangle and caption preserve captioned image-like content; fixed size supports geometric inspection. Page container and local alignment unchanged.')
helper = '''#let my-fig(..args, placement: none) = {
  if placement == "p" { page[ #set align(center + horizon); #figure(..args) ] }
  else { figure(..args, placement: placement) }
}
'''
add('u1-c3-helper', pagehead + helper + 'BEFORE\n#my-fig(rect(width: 100pt, height: 60pt, fill: aqua), caption: [CAP], placement: "p")\nAFTER\n',
    'TY-U1-C3', 'candidate', 'First string-selector helper operation; no later page-value variant substituted. Synthetic markers and rectangle as C2.')
add('u1-c2-image', pagehead + 'BEFORE\n#page[\n#set align(center + horizon)\n#figure(image("synthetic-image.png", width: 100pt, height: 60pt), caption: [CAP])\n]\nAFTER\n',
    'TY-U1-C2', 'candidate-image-input', 'A real synthetic PNG replaces the rectangle to check the original image-and-caption input type. Other page operation unchanged.')
add('u1-c3-image', pagehead + helper + 'BEFORE\n#my-fig(image("synthetic-image.png", width: 100pt, height: 60pt), caption: [CAP], placement: "p")\nAFTER\n',
    'TY-U1-C3', 'candidate-image-input', 'A real synthetic PNG replaces the rectangle. Helper and string p dispatch remain the first proposed variant.')
add('u1-direct-p-rejected', pagehead + '#figure(rect(width:100pt,height:60pt), caption:[CAP], placement: "p")\n',
    'TY-U1-C3', 'counterexample-without-helper', 'Researcher drops helper and passes string p directly to built-in figure; this is not the proposed helper and should be rejected.', 1)

def pdf_observation(path):
    doc = fitz.open(path)
    pages=[]
    for i,p in enumerate(doc):
        drawings=[]
        for d in p.get_drawings():
            drawings.append({k:(list(v) if k=='rect' else v) for k,v in d.items()
                             if k in ['rect','fill','color','width','dashes','type']})
        spans=[]
        for b in p.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                for s in line['spans']:
                    spans.append({k:s[k] for k in ['text','bbox','color','size','font']})
        pages.append(dict(page=i+1,size=list(p.rect),text=p.get_text(),drawings=drawings,spans=spans))
    return dict(page_count=len(doc),pages=pages)

started=utc()
version=subprocess.run([str(BINARY),'--version'],text=True,capture_output=True)
records=[]
for spec in fixtures:
    source=INPUT/(spec['id']+'.typ'); source.write_text(spec['source'])
    target=OUTPUT/(spec['id']+'.pdf')
    command=[str(BINARY),'compile',str(source),str(target)]
    t=utc(); p=subprocess.run(command,text=True,capture_output=True)
    row={k:v for k,v in spec.items() if k!='source'}
    row.update(command=['typst','compile',str(source.relative_to(OUT)),str(target.relative_to(OUT))],started_utc=t,ended_utc=utc(),exit_code=p.returncode,
               stdout=p.stdout,stderr=p.stderr,input_sha256=digest(source),input_file=str(source.relative_to(OUT)),output_file=str(target.relative_to(OUT)))
    if p.returncode==0:
        row['output_sha256']=digest(target)
        row['observed']=pdf_observation(target)
        doc=fitz.open(target)
        if len(doc)<=3:
            for i in range(len(doc)):
                doc[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(OUTPUT/(spec['id']+'-page'+str(i+1)+'.png'))
    records.append(row)

receipt=dict(started_utc=started,ended_utc=utc(),source_release='v0.10.0',source_commit='70ca0d257bb4ba927f63260e20443f244e0bb58c',
             binary_version=version.stdout.strip(),binary_sha256=digest(BINARY),script_sha256=digest(Path(__file__)),
             execution_owner='researcher',historical_OP_execution=False,original_question_version='unreported',
             inputs_are_synthetic=True,full_upstream_suite_executed=False,
             cases=records)
(OUT/'run-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'version':version.stdout.strip(),'cases':[{'id':r['id'],'exit':r['exit_code'],'pages':r.get('observed',{}).get('page_count'),'stderr':r['stderr']} for r in records]},ensure_ascii=False,indent=2))
