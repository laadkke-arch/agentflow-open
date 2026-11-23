// Corrective auxiliary probe: attach callback to the initial start, not a later no-op update.
'use strict';
process.env.NODE_ENV='development';
const path=require('node:path');
const fs=require('node:fs');
const {createRequire}=require('node:module');
const req=createRequire(path.join(__dirname,'.workbench/runtime/package.json'));
const {SpringValue,Globals}=req('@react-spring/core');
const {frameLoop}=req('@react-spring/shared');
Globals.assign({frameLoop:'demand',skipAnimation:false});
const results=[];
for(const cancel of [false,true]){
  frameLoop.clear();let event=null;
  const s=new SpringValue(0);
  s.start({to:1,config:{mass:1,tension:100,friction:10,velocity:0},onRest:r=>{event=r;}});
  s.advance(16);const before={value:s.get(),velocity:s.velocity};s.stop(cancel);
  results.push({cancel,before,after:{value:s.get(),velocity:s.velocity,goal:s.goal,idle:s.idle},onRest:event});
}
const output={generated_utc:new Date().toISOString(),classification:'researcher auxiliary correction',
  correction:'In probes.cjs the listener was added through a subsequent no-op start and the recorded event was null. Do not interpret that setup as a failed cancellation callback. This probe attaches it to the actual initial start. Original raw output preserved.',
  node:process.version,component:'@react-spring/core10.0.3',results};
fs.writeFileSync(path.join(__dirname,'stop-correction.json'),JSON.stringify(output,null,2)+'\n');
console.log(JSON.stringify(output,null,2));
