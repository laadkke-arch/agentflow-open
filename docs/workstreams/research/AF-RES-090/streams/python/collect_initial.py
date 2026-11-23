import sys, json, concurrent.futures
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2] / 'tools'))
from http_evidence import fetch
ROOT=Path(__file__).parent
E=ROOT/'evidence'
URLS={
 'PY-P3-README':'https://raw.githubusercontent.com/pypa/cibuildwheel/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/README.md',
 'PY-P3-START-A':'https://cibuildwheel.pypa.io/en/stable/options/#enable',
 'PY-P3-START-B':'https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable',
 'PY-P1-README':'https://raw.githubusercontent.com/pypa/bandersnatch/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/README.md',
 'PY-P1-TREE':'https://api.github.com/repos/pypa/bandersnatch/git/trees/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74?recursive=1',
 'PY-P1-START-A':'https://bandersnatch.readthedocs.io/en/latest/',
 'PY-P1-START-B':'https://bandersnatch.readthedocs.io/en/7.0.1/',
}
def get(item):
 sid,url=item
 receipt,body=fetch(url,sid,E)
 return {k:receipt[k] for k in ['source_id','requested_url','final_url','status','content_type','body_bytes','sha256','error']}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex:
  for r in ex.map(get,URLS.items()): print(json.dumps(r))
