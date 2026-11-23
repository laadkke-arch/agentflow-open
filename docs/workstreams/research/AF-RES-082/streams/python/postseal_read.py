import json,pathlib,concurrent.futures
from http_read import fetch,D
jobs=[('bandersnatch','.readthedocs.yml'),('bandersnatch','docs/conf.py'),('bandersnatch','requirements_docs.txt'),('bandersnatch','tox.ini'),('bandersnatch','.github/workflows/doc_build.yml'),('build','.readthedocs.yml'),('build','docs/conf.py'),('build','tox.ini'),('build','.github/workflows/reusable-docs.yml'),('cibuildwheel','.readthedocs.yml'),('cibuildwheel','mkdocs.yml'),('cibuildwheel','noxfile.py')]
def one(j):
 n,p=j;sha=json.load(open(D/f'{n}-tag-metadata.json'))['commit_sha'];text,rec=fetch(f'https://raw.githubusercontent.com/pypa/{n}/{sha}/{p}',n+'-post-'+p)
 if text is not None:
  (D/(n+'-post-'+p.replace('/','_')+'-analysis.txt')).write_text(text)
 return n,p,text
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
  for n,p,text in ex.map(one,jobs):print('\nFILE',n,p,'\n',text,flush=True)
