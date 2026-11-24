from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops
import subprocess, hashlib, json, xml.etree.ElementTree as ET, time, platform, os
root=Path(__file__).resolve().parent; os.chdir(root)
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; font=ImageFont.truetype(font_path,48)
lines=[(120,150,'Offline notes stay local.'),(180,420,'Rom\u00e2nia p\u0103streaz\u0103 fi\u0219iere.')]
im=Image.new('RGB',(1600,1000),'white'); draw=ImageDraw.Draw(im); expected=[]
for x,y,line in lines:
    draw.text((x,y),line,font=font,fill='black')
    for word in line.split():
        prefix=line[:line.index(word)]; xx=x+draw.textlength(prefix,font=font)
        expected.append({'word':word,'bbox_px':list(draw.textbbox((xx,y),word,font=font))})
im.save('input.png',dpi=(200,200)); im.save('input.pdf',resolution=200)
receipt={'platform':platform.platform(),'font':font_path,'font_sha256':hashlib.sha256(Path(font_path).read_bytes()).hexdigest(),'input_dpi':200,'expected':expected,'commands':[]}
def run(*cmd):
    t=time.monotonic(); p=subprocess.run(cmd,capture_output=True,text=True,timeout=30); receipt['commands'].append({'argv':list(cmd),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'elapsed_s':round(time.monotonic()-t,3)});return p.returncode
run('tesseract','--version');run('tesseract','input.png','out','-l','eng+ron','--psm','6');run('tesseract','input.png','searchable','-l','eng+ron','--psm','6','pdf');run('tesseract','input.pdf','direct','-l','eng+ron','--psm','6','pdf');run('pdftotext','-bbox','searchable.pdf','bbox.html');run('pdftoppm','-r','200','-png','-singlefile','input.pdf','input-render');run('pdftoppm','-r','200','-png','-singlefile','searchable.pdf','output-render');run('pdfinfo','searchable.pdf');
if Path('out.txt').exists():receipt['txt']=Path('out.txt').read_text()
if Path('bbox.html').exists():
    words=[{'word':e.text,'bbox_pt':[float(e.attrib[k]) for k in ['xMin','yMin','xMax','yMax']]} for e in ET.parse('bbox.html').getroot().iter() if e.tag.endswith('}word')]; receipt['words']=words
    matches=[]
    for ex in expected:
        same=[w for w in words if w['word']==ex['word']]
        if len(same)==1:
            actual=[v*200/72 for v in same[0]['bbox_pt']]; target=ex['bbox_px']; center=lambda box:((box[0]+box[2])/2,(box[1]+box[3])/2); c1=center(actual);c2=center(target); dx,dy=abs(c1[0]-c2[0]),abs(c1[1]-c2[1]);matches.append({'word':ex['word'],'dx_px':round(dx,2),'dy_px':round(dy,2),'within_25px':max(dx,dy)<=25})
        else:matches.append({'word':ex['word'],'unknown':'not uniquely matched'})
    receipt['alignment']=matches;receipt['exact_word_matches']=sum('dx_px' in m for m in matches);receipt['within_25px']=sum(m.get('within_25px',False) for m in matches)
if Path('input-render.png').exists() and Path('output-render.png').exists():
    a=Image.open('input-render.png').convert('RGB');b=Image.open('output-render.png').convert('RGB');receipt['render_sizes']=[a.size,b.size];receipt['render_pixel_difference_nonzero']=sum(1 for p in ImageChops.difference(a,b).getdata() if p!=(0,0,0)) if a.size==b.size else None
receipt['sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir() if p.is_file() and p.name not in ('receipt.json',)}
Path('receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');print(json.dumps(receipt,ensure_ascii=False,indent=2))
