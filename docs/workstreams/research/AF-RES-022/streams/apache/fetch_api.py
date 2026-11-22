import urllib.request,json,datetime,hashlib,pathlib,sys
BASE=pathlib.Path(__file__).parent/'.read-cache'
BASE.mkdir(exist_ok=True)
def fetch(name, endpoint, params):
 url='https://lists.apache.org/api/'+endpoint+'.json'
 raw=urllib.request.urlopen(urllib.request.Request(url,data=json.dumps(params).encode(),headers={'Content-Type':'application/json','User-Agent':'Mozilla/5.0'}),timeout=90).read()
 data=json.loads(raw)
 result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'request':{'url':url,'body':params},'sha256':hashlib.sha256(raw).hexdigest(),'data':data}
 (BASE/(name+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2))
 return data
if __name__=='__main__':
 data=fetch(sys.argv[1],sys.argv[2],json.loads(sys.argv[3])); print(json.dumps(data,ensure_ascii=False))
