"""Replay six separate upstream regressions for corroboration."""

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory

from PIL import Image
import numpy as np
from playwright.sync_api import sync_playwright

import measure
from run import ROOT, now, write_json


def process(argv,cwd,logs,tag):
    start=now()
    result=subprocess.run(argv,cwd=cwd,capture_output=True,check=False,timeout=65)
    (logs/(tag+'.stdout')).write_bytes(result.stdout)
    (logs/(tag+'.stderr')).write_bytes(result.stderr)
    return {'argv':argv,'exit':result.returncode,'started_utc':start,'finished_utc':now(),
            'stdout':tag+'.stdout','stderr':tag+'.stderr'}


def tex_case(original,output):
    with TemporaryDirectory(prefix='af107-upstream-tex-') as t:
        path=Path(t)
        shutil.copyfile(original,path/'test.tex')
        stage=process(['pdflatex','-no-shell-escape','-halt-on-error','-interaction=nonstopmode','test.tex'],path,output,'tex')
        for filename in ['test.log','test.pdf']:
            if (path/filename).is_file():
                shutil.copyfile(path/filename,output/filename)
    return {'steps':[stage],'lab_verdict':'assertions_returned_0' if stage['exit']==0 else 'failure',
            'local_pdf':(output/'test.pdf').is_file()}


def svg_case(original,expected,output,chromium):
    ext=original.name.rsplit('.',1)[-1]
    mime='image/svg+xml' if ext=='svg' else 'text/html; charset=utf-8'
    endpoint='/sample.'+ext
    rg=[]
    with sync_playwright() as playwright:
        with measure.browser_instance(playwright,chromium) as browser:
            for label,source in [('actual',original),('expected',expected)]:
                assets={endpoint:(mime,source)}
                ctx,page,requested,err=measure.open_page(browser,assets,endpoint,{'width':420,'height':220})
                if ext=='html':
                    page.wait_for_function("!document.documentElement.classList.contains('reftest-wait')")
                page.screenshot(path=output/(label+'.png'))
                rg.append({'label':label,'errors':err,'requested':requested})
                ctx.close()
    actual,expected_img=(np.asarray(Image.open(output/(name+'.png')).convert('RGB')) for name in ('actual','expected'))
    same=np.array_equal(actual,expected_img)
    return {'browser':rg,'same_full_pixels':bool(same),'screen_size':list(actual.shape[:2][::-1]),
            'green_pixels':int(measure.palette(actual,'#008000').sum()),
            'lab_verdict':'match' if same and all(not r['errors'] for r in rg) else 'different'}


def graph_case(original,expected,kind,output):
    argv=['dot','-Tjson',str(original),'-o',str(output/'actual.json')]
    stage=process(argv,output,output,'dot')
    if stage['exit']:
        return {'steps':[stage],'lab_verdict':'failure'}
    actual=json.loads((output/'actual.json').read_bytes())
    names={p['_gvid']:p['name'] for p in actual['objects']}
    edges={(names[e['tail']],names[e['head']]):e for e in actual['edges']}
    text=expected.read_text()
    comparisons={}
    if kind=='petersen':
        for a,b,color in [('0','1','blue'),('0','5','red'),('5','7','black')]:
            line=re.search(rf'^\s*{a}\s*--\s*{b}\s*\[(.*?)\];',text,re.M|re.S)
            declared=re.search(r'color=(\w+)',line.group(1))
            color_at_expected=declared[1] if declared else re.search(r'edge\s*\[color=(\w+)',text)[1]
            comparisons[f'{a}--{b}']={'reference':color_at_expected,'actual':edges[(a,b)]['color'],
                                      'same':color_at_expected==color==edges[(a,b)]['color']}
    else:
        for a,b in [('a','Z'),('b','Z'),('Z','A'),('Z','B')]:
            line=re.search(rf'^\s*{a}\s*->\s*{b}\s*\[(.*?)\];',text,re.M|re.S)
            pos=re.search(r'pos="([^"]+)',line[1])[1]
            wanted=('tail' if pos.startswith('s,') else 'head' if pos.startswith('e,') else 'none')
            record=edges[(a,b)]
            placement='tail' if record.get('_tdraw_') else 'head' if record.get('_hdraw_') else 'none'
            comparisons[f'{a}->{b}']={'reference':wanted,'actual':placement,'same':wanted==placement}
    return {'steps':[stage],'objects':len(names),'edges':len(edges),'comparisons':comparisons,
            'lab_verdict':'match_probes' if all(r['same'] for r in comparisons.values()) else 'different'}


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--inputs',required=True,type=Path)
    cli.add_argument('--output',required=True,type=Path)
    cli.add_argument('--chromium',default='/usr/bin/chromium')
    args=cli.parse_args()
    args.output=args.output.resolve()
    args.inputs=args.inputs.resolve()
    specs=json.loads((ROOT/'evidence/upstream/support-inputs.json').read_bytes())
    for id,spec in specs.items():
        o=args.output/id
        o.mkdir(parents=True,exist_ok=False)
        for key in ('input','expected'):
            if key in spec:
                data=spec[key]
                assert measure.digest(args.inputs/data['file'])==data['sha256'], (id,key)
        original=args.inputs/spec['input']['file']
        started=now()
        if id.startswith('T'):
            result=tex_case(original,o)
        elif id.startswith('S'):
            result=svg_case(original,args.inputs/spec['expected']['file'],o,args.chromium)
        else:
            result=graph_case(original,args.inputs/spec['expected']['file'],spec['probe'],o)
        receipt={'id':id,'started_utc':started,'finished_utc':now(),'inputs':spec,**result,
                 'outputs':{f.name:measure.digest(f) for f in sorted(o.iterdir())}}
        write_json(o/'receipt.json',receipt)
        print(id,result['lab_verdict'],flush=True)


if __name__=='__main__':
    main()
