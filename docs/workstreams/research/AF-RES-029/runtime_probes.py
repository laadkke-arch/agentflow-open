"""Post-seal falsification observations in the installed environment only.

These probes cannot augment a sealed return, prove historical availability or
substitute for building a cross-version extension. No network or package install.
"""
import argparse, json, os, platform, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone

P=Path(__file__).resolve().parent

def observe():
 out={'checked_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'stage':'post-route-seal supplementary falsification','observations':[],'limits':['Only installed versions are executed.','No original return, candidate rank, citation or success count may be changed by these probes.','No extension is compiled against a second NumPy runtime; ABI compatibility remains a separate unexecuted test.']}
 if not (P/'evidence/route-seal.json').exists():raise RuntimeError('All route returns must be sealed before probes run')
 try:
  import numpy as np
  out['numpy_version']=np.__version__
  vals={str(n):str(np.result_type(np.array([1],dtype=np.uint16),n)) for n in [1,255,65536]}
  strong={name:str(np.result_type(v,np.array([1],dtype=np.int8))) for name,v in [('scalar',np.int64(1)),('zero_dim',np.array(1,dtype=np.int64)),('one_dim',np.array([1],dtype=np.int64))]}
  out['observations'].append({'id':'Q09-PROBE','input':'uint16 ndarray with Python ints1,255,65536; int64 scalar/0D/1D with int8 array','code':'np.result_type(array, value)','result':{'changing_values':vals,'typed_strength':strong},'meaning':'Records actual dtype resolution; does not test every arithmetic conversion or cast rule.'})
  x=np.arange(4,dtype=np.int32);y=np.from_dlpack(x);x[0]=99
  out['observations'].append({'id':'Q10-PROBE','input':'NumPy int32 CPU ndarray exported then consumed through DLPack','code':'y=np.from_dlpack(x); x[0]=99','result':{'is_ndarray':isinstance(y,np.ndarray),'shares_memory':bool(np.shares_memory(x,y)),'visible_mutation':int(y[0]),'device':x.__dlpack_device__(),'has_export':hasattr(x,'__dlpack__')},'meaning':'Intra-NumPy producer/consumer path only; no interlibrary or GPU claim.'})
  try:
   from numpy.dtypes import StringDType
   arr=np.array([['a','é'],['a much longer string','z']],dtype=StringDType(coerce=False))
   rejected=None
   try:np.array(['ok',42],dtype=StringDType(coerce=False));rejected={'rejected':False}
   except Exception as exc:rejected={'rejected':True,'exception_type':type(exc).__name__,'message':str(exc)}
   out['observations'].append({'id':'Q11-PROBE','input':'2x2 unequal UTF8 strings and [ok,42] with coerce=False','code':'np.array(data,dtype=StringDType(coerce=False))','result':{'shape':arr.shape,'dtype':str(arr.dtype),'values':arr.tolist(),'scalar_type':type(arr[0,1]).__name__,'strict_nonstring':rejected},'meaning':'Construction, shape/scalar and strict rejection only; serialization, arena/thread safety and all missing sentinels are not tested.'})
  except Exception as exc:out['observations'].append({'id':'Q11-PROBE','unexecuted_or_error':type(exc).__name__+': '+str(exc)})
 except Exception as exc:out['observations'].append({'id':'NUMPY-PROBES','unexecuted_or_error':type(exc).__name__+': '+str(exc)})
 code="import json,locale,sys;print(json.dumps({'utf8_mode':sys.flags.utf8_mode,'getpreferredencoding_false':locale.getpreferredencoding(False),'getencoding':locale.getencoding() if hasattr(locale,'getencoding') else None}))"
 for mode in [0,1]:
  env=dict(os.environ,LC_ALL='C',LANG='C',PYTHONCOERCECLOCALE='0',PYTHONDONTWRITEBYTECODE='1')
  cmd=[sys.executable,'-B','-X',f'utf8={mode}','-c',code]
  r=subprocess.run(cmd,env=env,text=True,capture_output=True,timeout=20)
  out['observations'].append({'id':f'Q06-LOCALE-{mode}','input':{'LC_ALL':'C','LANG':'C','PYTHONCOERCECLOCALE':'0','utf8':mode},'command':cmd,'exit_code':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip(),'meaning':'Distinguishes locale reporting from UTF8 mode in this installed Python; different from a claim about every supported interpreter version.'})
 return out

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',default='evidence/runtime-probes.json');args=p.parse_args();r=observe();dest=(P/args.output).resolve();assert dest.is_relative_to(P);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'output':str(dest),'observations':len(r['observations']),'numpy':r.get('numpy_version'),'stage':r['stage']}))
