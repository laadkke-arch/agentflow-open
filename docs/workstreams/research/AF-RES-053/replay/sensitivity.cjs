'use strict';
// Post-seal exploratory version sensitivity. No primary input is modified.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const BASE=__dirname, MOD=path.join(BASE,'scratch/runtime-v270/node_modules');
const vl=require(path.join(MOD,'vega-lite')), vega=require(path.join(MOD,'vega'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const save=(rel,value)=>{
  const p=path.join(BASE,rel); fs.mkdirSync(path.dirname(p),{recursive:true});
  const data=typeof value==='string'?value:JSON.stringify(value,null,2)+'\n';fs.writeFileSync(p,data);
  return {path:rel,bytes:Buffer.byteLength(data),sha256:sha(data)};
};
function installed() {
  const rows=[];
  function scan(dir) {
    if(!fs.existsSync(dir)) return;
    for(const n of fs.readdirSync(dir)) {
      if(n.startsWith('.')) continue;
      const p=path.join(dir,n);
      if(n.startsWith('@')) {scan(p);continue;}
      const m=path.join(p,'package.json');if(!fs.existsSync(m)) continue;
      const j=JSON.parse(fs.readFileSync(m));rows.push({name:j.name,version:j.version,path:path.relative(MOD,p),manifest_sha256:sha(fs.readFileSync(m))});
      scan(path.join(p,'node_modules'));
    }
  }
  scan(MOD);return rows;
}
function scene(root) {
  const rows=[];
  function visit(mark,address) {
    for(const [i,item] of (mark.items||[]).entries()) {
      const p=address+'/items/'+i;
      const row={path:p,role:mark.role||null,marktype:mark.marktype||null,name:mark.name||null};
      for(const k of ['text','fill','stroke','opacity','x','y','width','height','font','fontSize','limit']) if(item[k]!==undefined) row[k]=item[k];
      if(item.datum!==undefined) row.datum=JSON.parse(JSON.stringify(item.datum));rows.push(row);
      for(const [j,child] of (item.items||[]).entries()) visit(child,p+'/items/'+j);
    }
  }
  visit(root,'/root');return rows;
}
async function main() {
  if(vl.version!=='2.7.0'||vega.version!=='4.4.0') throw new Error('Wrong sensitivity runtime');
  save('sensitivity-versions.json',{UTC:new Date().toISOString(),node:process.version,
    compiler:vl.version,runtime:vega.version,installed_packages:installed(),
    compiler_main_sha256:sha(fs.readFileSync(require.resolve(path.join(MOD,'vega-lite')))),
    runtime_main_sha256:sha(fs.readFileSync(require.resolve(path.join(MOD,'vega')))),
    canvas_present:fs.existsSync(path.join(MOD,'canvas/package.json'))});
  const receipts=[];
  for(const operation of ['A','B']) {
    const run_id='V03-v270-'+operation, input='inputs/V03-fixed-'+operation+'.json';
    const bytes=fs.readFileSync(path.join(BASE,input));const spec=JSON.parse(bytes);
    const warnings=[], logger=vega.logger(vega.Warn);
    for(const level of ['warn','error','info','debug']) logger[level]=(...args)=>{warnings.push({level,args:args.map(String)});return logger;};
    const row={run_id,operation,classification:'exploratory post-seal sensitivity; not preregistered prediction test',
      started_UTC:new Date().toISOString(),input:{path:input,sha256:sha(bytes)},input_changes:[],
      schema:spec.$schema,compiler:vl.version,runtime:vega.version,warnings};let view;
    try {
      const compiled=vl.compile(spec,{logger}).spec;
      row.compiled=save('outputs/'+run_id+'.vega.json',compiled);
      const loader={load:async url=>{throw new Error('External loads prohibited: '+url);},sanitize:async url=>{throw new Error('External images prohibited: '+url);}};
      view=new vega.View(vega.parse(compiled),{renderer:'none',logger,loader});
      await view.runAsync();
      row.svg=save('outputs/'+run_id+'.svg',await view.toSVG());
      row.scenegraph=save('outputs/'+run_id+'.scenegraph.json',scene(view.scenegraph().root));
      row.status='rendered';
    } catch(error) {
      row.status='failed';row.error={name:error.name,message:error.message,stack:error.stack};
    } finally {
      if(view) view.finalize();row.finished_UTC=new Date().toISOString();receipts.push(row);
      save('sensitivity-render-receipts.json',receipts);console.log(JSON.stringify(row));
    }
  }
  if(receipts.some(r=>r.status!=='rendered')) process.exitCode=1;
}
main().catch(error=>{console.error(error.stack);process.exitCode=1;});
