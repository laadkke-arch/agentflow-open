#!/usr/bin/env python3
"""Exploratory v2.7.0 V03 sensitivity, added after the frozen main plan."""
import argparse
import hashlib
import json
from pathlib import Path
import reproduce as main

BASE=Path(__file__).resolve().parent
RUNTIME=BASE/'scratch/runtime-v270'

def setup(label='install-v270'):
    RUNTIME.mkdir(parents=True,exist_ok=True)
    files={
      'package':('vega-lite-v2.7.0-package.json','https://raw.githubusercontent.com/vega/vega-lite/v2.7.0/package.json'),
      'lock':('vega-lite-v2.7.0-yarn.lock','https://raw.githubusercontent.com/vega/vega-lite/v2.7.0/yarn.lock'),
      'registry':('vega-lite-v2.7.0-registry.json','https://registry.npmjs.org/vega-lite/2.7.0')}
    data={}
    for key,(name,url) in files.items():
        p=BASE/'scratch'/name
        if not p.exists(): main.fetch(name,url)
        data[key]=p.read_bytes()
    expected={
      'package':'ae2ad69c72a406fab3cb9d223ed05d2f61c05547b0567c1fcca82fed800c7852',
      'lock':'6fb733d8832a7d6089fff7eacaee19f0e58d225d15650137b29dad70856d841d'}
    for key,digest in expected.items():
        assert main.sha(data[key])==digest, 'Historical source hash mismatch: '+key
    package=json.loads(data['package']); registry=json.loads(data['registry'])
    assert package['version']==registry['version']=='2.7.0'
    assert package['peerDependencies']['vega']=='^3.0.0 || ^4.0.0'
    assert registry['dist']['tarball']=='https://registry.npmjs.org/vega-lite/-/vega-lite-2.7.0.tgz'
    assert registry['dist']['integrity']=='sha512-SqUDFD+1bHP6UgaFnI418XLW1ffcVMlQMdzI4Xh0HGjPKDPdLTF71iNjcTUwtTYt9rRLXRcRKdmCbBzuLtkg8g=='
    original=data['lock'].decode()
    assert 'vega@^4.0.0:\n  version "4.4.0"' in original
    lock=original.replace('vega@^4.0.0:\n','vega@4.4.0, vega@^4.0.0:\n')
    entry=['\nvega-lite@2.7.0:','  version "2.7.0"',
           '  resolved '+json.dumps(registry['dist']['tarball']),
           '  integrity '+registry['dist']['integrity'],'  dependencies:']
    for name,version in sorted(registry['dependencies'].items()):
        entry.append('    '+json.dumps(name)+' '+json.dumps(version))
    lock+='\n'.join(entry)+'\n'
    (RUNTIME/'yarn.lock').write_text(lock)
    main.save_json(RUNTIME/'package.json',{'name':'af-res-053-v270-exploratory','private':True,'version':'1.0.0',
                                          'dependencies':{'vega-lite':'2.7.0','vega':'4.4.0'}})
    main.save_json(BASE/'sensitivity-dependency-pins.json',{
        'prepared_UTC':main.utc(),'classification':'post-seal exploratory version sensitivity',
        'compiler':'2.7.0','runtime':'4.4.0','package_manager':'yarn@1.22.10',
        'source_urls':{k:v[1] for k,v in files.items()},
        'source_hashes':{k:main.sha(v) for k,v in data.items()},
        'runtime_lock_sha256':main.sha(lock.encode()),
        'release_tarball_integrity':registry['dist']['integrity'],
        'selection_reason':'v2.7.0 release lock resolves vega@^4.0.0 to 4.4.0; compatible with peer ^3 || ^4.',
        'lock_edits':'Only exact vega@4.4.0 alias and own vega-lite@2.7.0 root release entry appended; transitive versions unchanged.',
        'changes_vs_primary':'Compiler 5.1.0 to 2.7.0 plus its compatible locked runtime/dependency bundle, not compiler-only isolation. Input bytes unchanged.',
        'author_runtime_unknown':True})
    main.run_record(label,['npm','exec','--yes','--package=yarn@1.22.10','--','yarn','install',
       '--frozen-lockfile','--ignore-scripts','--ignore-optional','--non-interactive',
       '--cache-folder',str(BASE/'scratch/yarn-cache')],RUNTIME)
    assert main.sha((RUNTIME/'yarn.lock').read_bytes())==main.sha(lock.encode())

parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['setup','render']);parser.add_argument('--retry-once',action='store_true');arg=parser.parse_args()
if arg.stage=='setup': setup('install-v270-retry-once' if arg.retry_once else 'install-v270')
else: main.run_record('render-v270',['node',str(BASE/'sensitivity.cjs')],BASE)
