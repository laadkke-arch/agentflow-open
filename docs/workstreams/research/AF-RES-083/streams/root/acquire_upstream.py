"""Read bounded public primary sources; cache is excluded from committed evidence."""
import concurrent.futures, datetime, hashlib, json, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
CACHE = ROOT / '.workbench' / 'cache'
SOURCES = [
 ('UP-G38', 'https://raw.githubusercontent.com/OSGeo/gdal/c46fe7e20e33925735ae4b785752795af72823bc/doc/source/drivers/vector/parquet.rst'),
 ('UP-G39', 'https://raw.githubusercontent.com/OSGeo/gdal/bb5ea618e23e498e79e8b8e6bd7215ad94bb2103/doc/source/drivers/vector/parquet.rst'),
 ('UP-G39NEWS', 'https://raw.githubusercontent.com/OSGeo/gdal/bb5ea618e23e498e79e8b8e6bd7215ad94bb2103/NEWS.md'),
 ('UP-S160REL', 'https://raw.githubusercontent.com/scipy/scipy/v1.6.0/doc/release/1.6.0-notes.rst'),
 ('UP-S160QUAD', 'https://raw.githubusercontent.com/scipy/scipy/v1.6.0/scipy/integrate/_quadrature.py'),
 ('UP-S154QUAD', 'https://raw.githubusercontent.com/scipy/scipy/v1.5.4/scipy/integrate/quadrature.py'),
 ('UP-S160TEST', 'https://raw.githubusercontent.com/scipy/scipy/v1.6.0/scipy/integrate/tests/test_quadrature.py'),
 ('UP-S111REL', 'https://raw.githubusercontent.com/scipy/scipy/v1.11.0/doc/source/release/1.11.0-notes.rst'),
 ('UP-S114REL', 'https://raw.githubusercontent.com/scipy/scipy/v1.14.0/doc/source/release/1.14.0-notes.rst'),
 ('UP-GP100', 'https://geoparquet.org/releases/v1.0.0/'),
 ('UP-GP110', 'https://geoparquet.org/releases/v1.1.0/'),
 ('UP-GAFORMAT', 'https://geoarrow.org/format.html'),
]

def acquire(row):
    sid,url=row
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result={'source_id':sid,'requested_url':url,'opened_utc':started}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AF-RES-083 public-source-research'}),timeout=30) as response:
            raw=response.read()
            result.update(status=response.status,arrived_url=response.url,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
        path=CACHE/(sid+'.txt')
        path.write_bytes(raw)
        result['cache_path']=str(path.relative_to(ROOT))
        result['acquired']=True
    except Exception as exc:
        result.update(acquired=False,error=str(exc))
    return result

if __name__=='__main__':
    CACHE.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        rows=list(pool.map(acquire,SOURCES))
    (ROOT/'acquisition.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    print(json.dumps(rows,ensure_ascii=False,indent=2))
