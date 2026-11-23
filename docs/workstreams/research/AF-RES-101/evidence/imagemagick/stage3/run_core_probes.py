"""Bounded researcher controls, separate from requester execution evidence."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess

BASE=Path(__file__).resolve().parents[3]
OUT=BASE/'evidence/imagemagick/stage3/probes'
WORK=BASE/'.cache/imagemagick/stage3/probes'
OFFICIAL=BASE/'.cache/imagemagick/stage3/official'
OUT.mkdir(parents=True,exist_ok=True);WORK.mkdir(parents=True,exist_ok=True)
MAGICK=shutil.which('magick')
records=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def run(name,argv,cwd=WORK,save_text=True):
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    r=subprocess.run(argv,cwd=cwd,capture_output=True,timeout=45)
    row={'id':name,'utc':started,'argv':[str(x) for x in argv],'exit_code':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr)}
    if save_text:
        (OUT/f'{name}.stdout.txt').write_bytes(r.stdout);(OUT/f'{name}.stderr.txt').write_bytes(r.stderr)
        row['stdout_file']=f'probes/{name}.stdout.txt';row['stderr_file']=f'probes/{name}.stderr.txt'
    else:
        (WORK/f'{name}.stdout.bin').write_bytes(r.stdout)
        (OUT/f'{name}.stderr.txt').write_bytes(r.stderr)
    records.append(row);return r
version=run('version',[MAGICK,'-version']).stdout.decode()

# Execute the upstream shell file unchanged with only generated build variables.
up=WORK/'upstream';(up/'tests').mkdir(parents=True,exist_ok=True)
(up/'common.shi').write_text(f"MAGICK='{MAGICK}'\nsrcdir='{OFFICIAL}'\n")
script=OFFICIAL/'tests/cli-colorspace.tap'
r=run('upstream-cli-colorspace',['sh',str(script)],cwd=up)
tap=r.stdout.decode();upstream={'source_sha256':sha(script.read_bytes()),'source_commit':'eeb41d70c9baf418a3aa75c424fb305362a1b280','script_modified':False,'generated_environment_sha256':sha((up/'common.shi').read_bytes()),'ok_lines':sum(s=='ok' for s in tap.splitlines()),'not_ok_lines':sum(s=='not ok' for s in tap.splitlines()),'declared_plan':[s for s in tap.splitlines() if s.startswith('1..')],'execution_version':version.splitlines()[0]}

gradient=b'P5\n2000 1\n65535\n'+b''.join(struct.pack('>H',round(i*65535/1999)) for i in range(2000))
inp=WORK/'gradient.pgm';inp.write_bytes(gradient)
variants={'normalize':['-normalize'],'doc-alias':['-contrast-stretch','2%x1%'],'source-alias':['-contrast-stretch','0.15%x0.05%'],'contrast':['-brightness-contrast','0,90']}
pixels={}
for name,ops in variants.items():
    result=run(name,[MAGICK,str(inp),*ops,'-depth','16','-endian','MSB','gray:-'],save_text=False)
    if result.returncode==0:pixels[name]=list(struct.unpack('>'+'H'*(len(result.stdout)//2),result.stdout))
def cmp(a,b):
    x=pixels[a];y=pixels[b];d=[i for i,(u,v) in enumerate(zip(x,y)) if u!=v]
    return {'a':a,'b':b,'equal':x==y,'different_pixels':len(d),'first_difference':{'x':d[0],'a':x[d[0]],'b':y[d[0]]} if d else None,'lengths':[len(x),len(y)]}
normalization={'input_sha256':sha(gradient),'input_recipe':'P5 2000x1 maxval65535, big-endian samples round(i*65535/1999), i=0..1999','comparisons':[cmp('normalize','doc-alias'),cmp('normalize','source-alias'),cmp('normalize','contrast')],'samples':{name:{str(i):v[i] for i in [0,1,2,3,4,20,40,1000,1979,1998,1999]} for name,v in pixels.items()},'limit':'researcher synthetic gradient; not the QR source image and not requester execution'}

checker=b'P6\n80 60\n255\n'+bytes(c for y in range(60) for x in range(80) for c in ([255]*3 if (x//10+y//10)%2 else [0]*3))
pinp=WORK/'checker.ppm';pinp.write_bytes(checker)
coords='0,0 10,10 79,0 89,10 79,59 89,69 0,59 10,69'
perspective={'input_sha256':sha(checker),'input_recipe':'80x60 P6 black/white checker, 10x10 cells','coordinates':coords,'geometries':{},'explicit_viewport':{}}
rgba={}
for sign,label in [('-','minus'),('+','plus')]:
    args=[MAGICK,str(pinp),sign+'distort','Perspective',coords]
    result=run(f'distort-{label}-geometry',args+['-format','%wx%h %X %Y','info:'])
    perspective['geometries'][label]=result.stdout.decode()
    result=run(f'distort-{label}-viewport',[MAGICK,str(pinp),'-define','distort:viewport=80x60+0+0',sign+'distort','Perspective',coords,'-depth','8','RGBA:-'],save_text=False)
    rgba[label]=result.stdout
perspective['explicit_viewport']={'value':'80x60+0+0','rgba_identical':rgba['minus']==rgba['plus'],'minus_sha256':sha(rgba['minus']),'plus_sha256':sha(rgba['plus'])}
perspective['limit']='researcher supplied synthetic corners; does not demonstrate automatic detection, wrinkle removal or original request rectification'
result={'research_version':version,'upstream_script_execution':upstream,'normalize_doc_vs_source':normalization,'perspective_flags':perspective,'commands':records,'scope':'bounded researcher calibration, not original ImageMagick 7.0.10-61 execution and not historical requester evidence','upstream_validate_suite':'read fixed convert_options and return-status oracle; whole C validate suite not built or executed'}
(OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({'upstream':upstream,'normalization':normalization['comparisons'],'perspective':perspective,'all_exit_codes':[r['exit_code'] for r in records]},ensure_ascii=False,indent=2))
