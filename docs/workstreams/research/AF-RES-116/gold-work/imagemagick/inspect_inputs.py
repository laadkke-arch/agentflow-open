"""Nonhistorical raw metadata/pixel inspection; never an ImageMagick regression run."""
import json, hashlib, pathlib, struct, subprocess
import numpy as np
from PIL import Image, __version__ as pillow_version
from capture import BASE, now, record_read

def hashed(v): return {'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()}
def simple(v):
    if isinstance(v,bytes): return hashed(v)
    if isinstance(v,(list,tuple)):return [simple(x) for x in v]
    if isinstance(v,(str,int,float)) or v is None:return v
    return str(v)
def inspect_tiff(name):
    path=BASE/'attachments'/'extracted'/name; raw=path.read_bytes(); im=Image.open(path)
    tags=dict(im.tag_v2); out={'file':str(path.relative_to(BASE)),'file_hash':hashed(raw),'inspected_utc':now(),'library':'Pillow '+pillow_version,'mode_reported_by_Pillow':im.mode,'tags':{str(k):simple(v) for k,v in sorted(tags.items())},'historical_runtime':False}
    assert tags[259]==1 and tags.get(284,1)==1 and set(tags[258])=={8}
    offsets=tags[273];counts=tags[279]
    if isinstance(offsets,int):offsets=(offsets,)
    if isinstance(counts,int):counts=(counts,)
    pixels=b''.join(raw[o:o+n] for o,n in zip(offsets,counts))
    expected=tags[256]*tags[257]*tags[277]; assert len(pixels)>=expected
    arr=np.frombuffer(pixels[:expected],dtype=np.uint8).reshape(tags[257],tags[256],tags[277])
    out['raw_decoder']='Direct uncompressed TIFF chunky 8-bit StripOffsets/StripByteCounts; no alpha application, color conversion or ImageMagick runtime.'
    out['shape']=list(arr.shape);out['channel_statistics']=[{'channel_index_zero_based':i,'min':int(arr[...,i].min()),'max':int(arr[...,i].max()),'unique_values':int(np.unique(arr[...,i]).size),'mean':float(arr[...,i].mean()),'sha256':hashlib.sha256(arr[...,i].tobytes()).hexdigest()} for i in range(arr.shape[2])]
    record_read(name,['raw TIFF IFD tags and all uncompressed strip samples; derived statistics are inspection, not a historical ImageMagick run'],utc=out['inspected_utc'])
    return out,arr

def main():
    results={'inspected_utc':now(),'historical_runtime_executed':False,'files':[]}
    arrays={}
    for name in ['meta.tif','demo.tif']:
        out,arr=inspect_tiff(name);results['files'].append(out);arrays[name]=arr
    for name in ['lena.png','mandril3.jpg']:
        path=BASE/'attachments'/name;im=Image.open(path);im.load();utc=now()
        results['files'].append({'file':str(path.relative_to(BASE)),'inspected_utc':utc,'file_hash':hashed(path.read_bytes()),'mode':im.mode,'size':list(im.size),'info':{k:simple(v) for k,v in im.info.items()},'library':'Pillow '+pillow_version,'historical_runtime':False})
        record_read(name,['Pillow image metadata and decoded pixel array'],utc=utc)
        if name=='lena.png':
            a=np.asarray(im.convert('RGB'));b=arrays['meta.tif'][...,:3]
            results['meta_rgb_vs_original_lena']={'equal_shapes':list(a.shape)==list(b.shape),'all_samples_equal':bool(np.array_equal(a,b)),'maximum_absolute_difference':int(np.max(np.abs(a.astype(int)-b.astype(int)))),'limitation':'Raw RGB sample equality does not establish ICC preservation or rendering equivalence across viewers.'}
    for command in [['magick','-version']]:
        r=subprocess.run(command,capture_output=True,text=True,timeout=10);results['available_runtime']={'command':command,'stdout':r.stdout,'stderr':r.stderr,'exit_code':r.returncode,'utc':now(),'qualification':'Inventory only. This runtime is not the requested historical version.'}
    (BASE/'input-inspection.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n');print(json.dumps(results,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
