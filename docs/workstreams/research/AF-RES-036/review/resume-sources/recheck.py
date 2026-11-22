"""Targeted post-seal source audit; does not regenerate experimental cards."""
import hashlib
import importlib.util
import io
import json
import re
import tarfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

BASE = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('fetchlib', BASE / 'scripts/fetchlib.py')
fetchlib = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetchlib)

TARGETS = [
 ('RS-01', ['R01'], 'http://www.bioconductor.org/help/workflows/rnaseqGene/', ['Page Not Found'], None),
 ('RS-02', ['R01'], 'https://bioconductor.org/packages/3.11/workflows/vignettes/rnaseqGene/inst/doc/rnaseqGene.html', ['preparing-quantification-input-to-deseq2', 'FASTQ', 'summarizeToGene'], None),
 ('RS-03', ['G01','G03'], 'https://pubs.opengroup.org/onlinepubs/9699919799/mindex.html', ['2018', 'newer'], None),
 ('RS-04', ['G01','G03'], 'https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html', ['tag_18', 'The shell is a command language interpreter'], None),
 ('RS-05', ['G03'], 'https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html', ['tag_18', 'tag_19', 'The shell is a command language interpreter'], None),
 ('RS-06', ['R03'], 'https://bioconductor.org/packages/S4Vectors', ['0.50.3', 'S4Vectors_'], None),
 ('RS-07', ['R03'], 'https://bioconductor.org/packages/3.23/bioc/src/contrib/S4Vectors_0.50.3.tar.gz', ['setValidity2 <- function', 'disableValidity()'], 'S4Vectors/R/S4-utils.R'),
 ('RS-08', ['G05'], 'https://gcc.gnu.org/onlinedocs/gcc/Preprocessor-Options.html', ['id="index-MM"', 'Like <samp class="option">-M', 'system header directories'], None),
 ('RS-09', ['G05'], 'https://gcc.gnu.org/onlinedocs/gcc-10.1.0/gcc/Preprocessor-Options.html', ['id="index-MM"', 'system header directories'], None),
]

def one(t):
 sid,cases,url,terms,member=t
 data,receipt=fetchlib.fetch(url,OUT,sid,'post_seal_targeted_source_recheck',cases,save_name=None)
 raw=data
 err=None
 if member and receipt.get('status')==200:
  try:
   with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as tf: raw=tf.extractfile(member).read()
  except Exception as e: err=repr(e); raw=b''
 snippets=[]
 for term in terms:
  b=term.encode(); at=raw.find(b)
  start=max(0,at-180) if at>=0 else None
  end=min(len(raw),at+len(b)+900) if at>=0 else None
  excerpt=raw[start:end] if at>=0 else b''
  snippets.append({'term':term,'found':at>=0,'exact_term_byte_offset':at if at>=0 else None,'excerpt_byte_start':start,'excerpt_byte_end':end,'excerpt':excerpt.decode('utf-8',errors='replace'),'excerpt_sha256':hashlib.sha256(excerpt).hexdigest()})
 record={'source_id':sid,'case_ids':cases,'url':url,'checked_utc':receipt['finished_utc'],'status':receipt['status'],'final_url':receipt.get('final_url'),'response_sha256':receipt['sha256'],'member':member,'member_error':err,'examined_source_sha256':hashlib.sha256(raw).hexdigest(),'snippets':snippets,'id_tag_18_present':bool(re.search(rb'(?:id|name)=[\"\x27]tag_18[\"\x27]',raw)),'id_tag_19_present':bool(re.search(rb'(?:id|name)=[\"\x27]tag_19[\"\x27]',raw)),'count_as_new_unique':False,'reason':'Repeated already-counted primary source for independent post-seal audit; not an added experimental observation.'}
 (OUT/(sid+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
 return {k:record[k] for k in ['source_id','status','final_url','member_error','id_tag_18_present','id_tag_19_present']} | {'terms':[(s['term'],s['found']) for s in snippets]}

if __name__=='__main__':
 OUT.mkdir(exist_ok=True,parents=True)
 with ThreadPoolExecutor(max_workers=4) as pool:
  for result in pool.map(one,TARGETS):print(json.dumps(result,ensure_ascii=False))
