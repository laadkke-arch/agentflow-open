import urllib.request,urllib.parse,json,pathlib,datetime,hashlib
P=pathlib.Path(__file__).parent
repo='pandoc/extra';tag='3.7.0.0-ubuntu'
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
receipts=[]
# Anonymous public pull-scoped registry token stays in memory; neither token nor authorization header is printed or persisted.
auth_url='https://auth.docker.io/token?'+urllib.parse.urlencode({'service':'registry.docker.io','scope':'repository:'+repo+':pull'})
try:
 r=urllib.request.urlopen(auth_url,timeout=45);auth=json.load(r);token=auth['token']
 receipts.append({'purpose':'anonymous public registry authentication','url':auth_url,'checked_utc':now(),'status':r.status,'token_stored':False})
except Exception as e:
 receipts.append({'purpose':'anonymous public registry authentication','url':auth_url,'checked_utc':now(),'error':repr(e)})
 P.joinpath('image-metadata-receipts.json').write_text(json.dumps(receipts,indent=2));print(json.dumps(receipts,indent=2));raise SystemExit(1)
accept=','.join(['application/vnd.oci.image.index.v1+json','application/vnd.docker.distribution.manifest.list.v2+json','application/vnd.oci.image.manifest.v1+json','application/vnd.docker.distribution.manifest.v2+json'])
def get(url,kind):
 req=urllib.request.Request(url,headers={'Authorization':'Bearer '+token,'Accept':accept})
 start=now()
 try:
  r=urllib.request.urlopen(req,timeout=45);raw=r.read();d=json.loads(raw)
  receipts.append({'url':url,'purpose':kind,'started_utc':start,'finished_utc':now(),'status':r.status,'content_type':r.headers.get('Content-Type'),'docker_content_digest':r.headers.get('Docker-Content-Digest'),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
  return d,receipts[-1]
 except Exception as e:
  receipts.append({'url':url,'purpose':kind,'started_utc':start,'finished_utc':now(),'error':repr(e)});raise
try:
 base='https://registry-1.docker.io/v2/'+repo
 index,ireceipt=get(base+'/manifests/'+tag,'fixed numeric tag manifest/index')
 output={'repository':repo,'tag':tag,'checked_utc':now(),'index_annotations':index.get('annotations'),'index_digest':ireceipt['docker_content_digest'],'platforms':[],'release_source_linkage':'unresolved'}
 if 'manifests' in index:
  output['platforms']=[{'digest':m.get('digest'),'platform':m.get('platform'),'annotations':m.get('annotations')} for m in index['manifests']]
  matches=[m for m in index['manifests'] if m.get('platform',{}).get('os')=='linux' and m.get('platform',{}).get('architecture')=='amd64']
  if not matches:raise ValueError('No Linux amd64 manifest')
  manifest,mreceipt=get(base+'/manifests/'+matches[0]['digest'],'Linux amd64 image manifest')
 else:manifest=index;mreceipt=ireceipt
 output['manifest_digest']=mreceipt['docker_content_digest'];output['manifest_annotations']=manifest.get('annotations')
 config_digest=manifest['config']['digest'];config,creceipt=get(base+'/blobs/'+config_digest,'image config metadata only; no filesystem layer')
 # Deliberately suppress Env, Entrypoint, Cmd, working directory, history, layers and build commands before model exposure.
 output['config_digest']=config_digest;output['config_digest_matches']='sha256:'+creceipt['sha256']==config_digest
 output['config']={k:config.get(k) for k in ['created','architecture','os']}
 output['labels']=config.get('config',{}).get('Labels',{})
 labels=output['labels'];output['revision']=labels.get('org.opencontainers.image.revision');output['source']=labels.get('org.opencontainers.image.source');output['version']=labels.get('org.opencontainers.image.version')
 if output['revision'] and output['source']:output['release_source_linkage']='candidate explicit OCI labels; confirm referenced commit metadata'
 output['no_image_execution']=True;output['filesystem_layers_downloaded']=0
 P.joinpath('image-release-metadata.json').write_text(json.dumps(output,indent=2));print(json.dumps(output,indent=2))
except Exception as e:print(json.dumps({'error':repr(e)},indent=2))
finally:P.joinpath('image-metadata-receipts.json').write_text(json.dumps(receipts,indent=2))
