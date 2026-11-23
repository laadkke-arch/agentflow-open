'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const base=__dirname,which=process.argv[2];
if(!['runtime','runtime-v270'].includes(which)) throw new Error('Allowed replay runtime required');
const mod=path.join(base,'scratch',which,'node_modules');
const vl=require(path.join(mod,'vega-lite')),vg=require(path.join(mod,'vega'));
const found=new Map();
for(const file of Object.keys(require.cache)) {
  if(!file.startsWith(mod+path.sep))continue;let d=path.dirname(file);
  while(d.startsWith(mod)) {
    const p=path.join(d,'package.json');
    if(fs.existsSync(p)) {const j=JSON.parse(fs.readFileSync(p));found.set(d,{name:j.name,version:j.version,path:path.relative(mod,d)});break;}
    d=path.dirname(d);
  }
}
const result={UTC:new Date().toISOString(),node:process.version,compiler:vl.version,runtime:vg.version,
              imported_packages:[...found.values()].sort((a,b)=>a.path.localeCompare(b.path)),
              note:'Imports only, no compilation or input changes.'};
fs.writeFileSync(path.join(base,'imported-versions-'+which+'.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result));
