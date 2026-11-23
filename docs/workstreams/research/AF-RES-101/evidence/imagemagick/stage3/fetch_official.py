"""Fetch fixed official ImageMagick files into the ignored cache with receipts."""
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

BASE=Path(__file__).resolve().parents[3]
OUT=BASE/'evidence/imagemagick/stage3'
CACHE=BASE/'.cache/imagemagick/stage3/official'
CACHE.mkdir(parents=True,exist_ok=True)
SHA='eeb41d70c9baf418a3aa75c424fb305362a1b280'
PATHS=['www/command-line-options.html','www/command-line-processing.html','MagickWand/operation.c','MagickCore/distort.c','MagickCore/enhance.c','tests/cli-colorspace.tap','tests/validate-convert.tap','tests/validate.h','tests/validate.c','tests/common.shi','tests/cli-pipe.tap']
def fetch(path):
    url=f'https://raw.githubusercontent.com/ImageMagick/ImageMagick/{SHA}/{path}'
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        response=urllib.request.urlopen(url,timeout=45);raw=response.read()
        dest=CACHE/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
        return {'path':path,'url':url,'pinned_url':f'https://github.com/ImageMagick/ImageMagick/blob/{SHA}/{path}','utc':utc,'status':response.status,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'git_blob_sha1':hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest(),'version':'7.0.10-61','commit':SHA}
    except Exception as error:return {'path':path,'url':url,'utc':utc,'error':str(error)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:receipts=list(pool.map(fetch,PATHS))
(OUT/'official-acquisition.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2))
print(json.dumps(receipts,ensure_ascii=False,indent=2))
