"""Replay the separate, constructed alpha/ICC independence check.

This does not reproduce any natural case or claim historical runtime behavior.
The checked-in tiny fixture's embedded ICC is reused so input bytes are stable.
"""
from pathlib import Path
from PIL import Image
import json, hashlib, subprocess
import numpy as np
from capture import BASE, now

def run():
    directory=BASE/'supplementary-constructed'
    source=directory/'rgba-with-icc.png'
    image=Image.open(source); image.load()
    alpha=np.asarray(image.convert('RGBA'))[...,3]
    profile=image.info.get('icc_profile')
    assert profile is not None and alpha.flatten().tolist()==[0,85,170,255]
    version=subprocess.run(['magick','-version'],capture_output=True,text=True,check=True).stdout
    assert version.startswith('Version: ImageMagick 7.1.1-43 '), 'This constructed receipt was made with 7.1.1-43; do not relabel another runtime.'
    result=[]
    for label,options in [('alpha_preserved_profile_removed',['-strip']),('profile_preserved_alpha_removed',['-alpha','off'])]:
        path=directory/(label+'.png');cmd=['magick',str(source),*options,str(path)]
        start=now(); r=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=20)
        output=Image.open(path); output.load()
        result.append({'label':label,'command':cmd,'started_utc':start,'finished_utc':now(),'exit_code':r.returncode,'runtime_version':version,'alpha_samples_equal':bool(np.array_equal(alpha,np.asarray(output.convert('RGBA'))[...,3])),'icc_bytes_equal':profile==output.info.get('icc_profile'),'output_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'natural_case':False})
    assert [(r['alpha_samples_equal'],r['icc_bytes_equal']) for r in result]==[(True,False),(False,True)]
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
