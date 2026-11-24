#!/usr/bin/env python3
"""Restore committed, lossless research archives inside this task's owned path.

Existing differing bytes are an error. No network, symlinks or path traversal.
"""
from pathlib import Path
import hashlib,json,tarfile
OWN=Path(__file__).resolve().parent.parent

def restore():
    archives=[OWN/'evidence/document-cache.tar.gz', OWN/'reachability/raw-enumeration.tar.gz']
    archives+=sorted((OWN/'evidence/reference-cache').glob('*.tar.gz'))
    restored=0;matched=0;files=0
    for archive in archives:
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                target=(OWN/member.name).resolve()
                if not target.is_relative_to(OWN) or not member.isfile():
                    raise ValueError('unexpected archive member '+member.name)
                raw=tar.extractfile(member).read();files+=1
                if target.exists():
                    if target.read_bytes()!=raw:raise ValueError('existing bytes differ: '+member.name)
                    matched+=1
                else:
                    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);restored+=1
    print(json.dumps({'archives':len(archives),'files':files,'restored':restored,'already_equal':matched,'network_used':False}))

if __name__=='__main__':restore()
