"""Run a frozen AF-RES-107 slot in an isolated directory and retain its evidence."""

import argparse
from datetime import datetime, timezone
from importlib import metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import traceback

import measure

ROOT = Path(__file__).resolve().parent
INPUTS = json.loads((ROOT/'inputs.json').read_bytes())
PROTOCOL = json.loads((ROOT/'protocol.json').read_bytes())


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def command(argv, name, cwd, logdir, receipt, env):
    start = now()
    stdout=logdir/(name+'.stdout')
    stderr=logdir/(name+'.stderr')
    with stdout.open('wb') as out, stderr.open('wb') as err:
        try:
            status=subprocess.run(argv,cwd=cwd,env=env,stdout=out,stderr=err,timeout=65,check=False).returncode
        except (OSError,subprocess.TimeoutExpired) as exc:
            err.write(f'{type(exc).__name__}: {exc}\n'.encode())
            status=124 if isinstance(exc,subprocess.TimeoutExpired) else 127
    receipt['steps'].append({'stage':name,'argv':list(map(str,argv)),'cwd':str(cwd),'started_utc':start,
                             'finished_utc':now(),'exit':status,'stdout':stdout.name,'stderr':stderr.name})
    if status:
        raise RuntimeError(f'{name} exited {status}')


def verify_support(path, case):
    if path is None:
        raise FileNotFoundError('provide --wpt-support with the three sealed resource files')
    for name,item in case['support'].items():
        if measure.digest(path/name)!=item['sha256']:
            raise ValueError(f'WPT support SHA mismatch: {name}')


def run_case(slot, settings):
    case_id=slot['case']
    original=INPUTS['cases'][case_id]
    case=slot.get('observation_case',original)
    output=settings.output/slot['id']
    output.mkdir(parents=True,exist_ok=False)
    recorded={k:v for k,v in slot.items() if k!='observation_case'}
    receipt={**recorded,'started_utc':now(),'steps':[],'first_failure':None,'exit':0,
             'result':None,'patch_sha256':None,'original_sha256':None,'edited_input_sha256':None}
    current='prepare'
    try:
        if case_id=='S' and not slot.get('synthetic_use'):
            verify_support(settings.wpt_support,case)
        source=ROOT/slot.get('source',original['path'])
        receipt['source']=str(source.relative_to(ROOT))
        receipt['original_sha256']=measure.digest(source)
        if 'source' not in slot and receipt['original_sha256']!=original['sha256']:
            raise ValueError('sealed original SHA mismatch')
        patch=ROOT/slot['patch'] if slot.get('patch') else None
        receipt['patch_sha256']=measure.digest(patch) if patch else None
        with tempfile.TemporaryDirectory(prefix='afres107-'+slot['id']+'-') as tmp:
            cwd=Path(tmp)
            env={**os.environ,'LC_ALL':'C.UTF-8','TZ':'UTC','TEXMFVAR':str(cwd/'texmf-var'),
                 'TEXMFCONFIG':str(cwd/'texmf-config')}
            infile=cwd/('input'+source.suffix)
            shutil.copyfile(source,infile)
            if patch:
                current='patch'
                command(['git','apply','--whitespace=nowarn',patch],'patch',cwd,output,receipt,env)
                if slot.get('reverse_patch'):
                    current='reverse'
                    command(['git','apply','--reverse','--whitespace=nowarn',patch],'reverse',cwd,output,receipt,env)
            receipt['edited_input_sha256']=measure.digest(infile)
            shutil.copyfile(infile,output/infile.name)
            if case_id=='T':
                current='pdfLaTeX'
                try:
                    command([settings.pdflatex,'-no-shell-escape','-halt-on-error','-interaction=nonstopmode',
                             '-file-line-error',infile.name],current,cwd,output,receipt,env)
                finally:
                    for name in ('input.pdf','input.log'):
                        if (cwd/name).is_file():
                            shutil.copyfile(cwd/name,output/name)
                current='PDF vector and raster'
                observation=measure.pdf(output/'input.pdf',output,case)
                receipt['result']='input.pdf'
            elif case_id=='S':
                current='Chromium SVG DOM and raster'
                if slot.get('synthetic_use'):
                    from controls import observe_use
                    observation=observe_use(infile,output,settings.chromium)
                else:
                    observation=measure.marker(infile,output,case,settings.wpt_support,settings.chromium)
                receipt['result']='rendered.svg'
            else:
                current='dot'
                try:
                    command([settings.dot,'-v','-Tsvg','-ooutput.svg','-Tjson','-ooutput.dot.json',infile.name],
                            current,cwd,output,receipt,env)
                finally:
                    for name in ('output.svg','output.dot.json'):
                        if (cwd/name).is_file():
                            shutil.copyfile(cwd/name,output/name)
                current='SVG XML and Chromium raster'
                observation=measure.svg_graph(output/'output.svg',output,case,settings.chromium)
                receipt['result']='output.svg'
            measured_at=now()
            receipt['steps'].append({'stage':current,'engine':('PyMuPDF' if case_id=='T' else 'Chromium'),
                                     'finished_utc':measured_at,'exit':0})
            write_json(output/'observed.json',observation)
    except Exception as exc:
        receipt['first_failure']=current
        previous=receipt['steps'][-1] if receipt['steps'] else {}
        receipt['exit']=previous.get('exit',1) if previous.get('stage')==current and previous.get('exit') else 1
        receipt['error']=f'{type(exc).__name__}: {exc}'
        (output/'failure.txt').write_text(traceback.format_exc(),encoding='utf-8')
    receipt['finished_utc']=now()
    receipt['files']={p.name:{'sha256':measure.digest(p),'bytes':p.stat().st_size} for p in sorted(output.iterdir())}
    write_json(output/'receipt.json',receipt)
    print(slot['id'],receipt['exit'],receipt['first_failure'],flush=True)
    return receipt


def read_command(argv):
    value=subprocess.run(argv,capture_output=True,text=True,check=False)
    return {'argv':argv,'exit':value.returncode,'stdout':value.stdout,'stderr':value.stderr}


def environment(settings):
    package_commands=[['kpsewhich','-engine=pdftex','-format=fmt','pdflatex.fmt'],['kpsewhich','pgfplots.sty'],
                      ['kpsewhich','pgfplots.revision.tex'],['kpsewhich','pgfplots.code.tex'],['kpsewhich','pgf.revision.tex'],
                      ['kpsewhich','cmr10.pfb'],['kpsewhich','cmbx12.pfb'],['kpsewhich','cmr7.pfb'],
                      ['fc-match','-f','%{family}\t%{file}\n','Arial'],['fc-match','-f','%{family}\t%{file}\n','serif']]
    checks=[read_command(args) for args in package_commands]
    files={}
    for info in checks:
        output=info['stdout'].strip().split('\t')[-1]
        if output and Path(output).is_file():
            files[output]={'sha256':measure.digest(output),'bytes':Path(output).stat().st_size}
            if output.endswith('revision.tex'):
                files[output]['content']=Path(output).read_text(errors='replace')
    tools={}
    for name,flag in ((settings.pdflatex,'-version'),(settings.dot,'-V'),(settings.chromium,'--version')):
        path=Path(shutil.which(name)).resolve()
        tools[name]={'path':str(path),'sha256':measure.digest(path),'version':read_command([name,flag])}
    distro=Path('/etc/os-release').read_text() if Path('/etc/os-release').is_file() else None
    value={'captured_utc':now(),'os_release':distro,'python':sys.version,'tools':tools,
           'libraries':{name:metadata.version(name) for name in ('PyMuPDF','numpy','Pillow','playwright')},
           'package_and_font_lookup':checks,'packages_and_fonts':files,'shell_escape':'disabled',
           'chromium':'headless, sRGB, DPR 1, temporary process, offline HTTP route, no service workers',
           'tex_clock':'UTC, host timestamps, no forced SOURCE_DATE_EPOCH',
           'dot_layout':'dot engine, built-in SVG and JSON written in one invocation',
           'wpt_support_expected':INPUTS['cases']['S']['support']}
    settings.output.parent.mkdir(parents=True,exist_ok=True)
    write_json(settings.output,value)


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('mode',choices=('environment','baseline','matrix','controls'))
    cli.add_argument('--output',type=Path,required=True)
    cli.add_argument('--wpt-support',type=Path)
    cli.add_argument('--pdflatex',default='pdflatex')
    cli.add_argument('--dot',default='dot')
    cli.add_argument('--chromium',default='/usr/bin/chromium')
    cli.add_argument('--slot',help='run just one frozen slot ID')
    args=cli.parse_args()
    args.output=args.output.resolve()
    if args.wpt_support:
        args.wpt_support=args.wpt_support.resolve()
    if args.mode=='environment':
        environment(args)
        return 0
    if args.mode=='controls':
        from controls import slots
        cases=slots()
    else:
        cases=PROTOCOL['baseline_slots' if args.mode=='baseline' else 'main_slots']
    if args.slot:
        cases=[case for case in cases if case['id']==args.slot]
        if not cases:
            cli.error(f'unknown slot ID {args.slot}')
    results=[run_case(case,args) for case in cases]
    return int(any(r['exit'] for r in results))


if __name__=='__main__':
    raise SystemExit(main())
