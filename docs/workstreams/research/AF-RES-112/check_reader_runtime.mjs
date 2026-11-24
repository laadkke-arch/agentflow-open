// Verify study-critical exposure accounting and choice restrictions using synthetic sources.
import fs from 'node:fs';
import assert from 'node:assert/strict';
const values=new Map(), outputs=[], saved=[];
globalThis.store=(k,v)=>values.set(k,structuredClone(v));
globalThis.load=k=>structuredClone(values.get(k));
globalThis.text=x=>outputs.push(structuredClone(x));
let input={request:'synthetic',url:'https://example.org/fixture',hint:''};
globalThis.tools={
  exec_command:async()=>({output:JSON.stringify(input),exit_code:0}),
  apply_patch:async p=>{saved.push(p);return{};},
  mcp__codex_apps__search_service_web_run:async()=>({content:[{type:'text',text:'Fixture (https://example.org/fixture)\n【turnMockview0】 Total lines: 2\nL0: '+('가😀x'.repeat(2000))+'\nL1: end'}]}),
  mcp__codex_apps__github_fetch:async()=>({structuredContent:{content:JSON.stringify([{name:'first.gd',type:'file',html_url:'https://github.com/x/y/blob/main/first.gd'},{name:'second.gd',type:'file',html_url:'https://github.com/x/y/blob/main/second.gd'}])}}),
  mcp__codex_apps__github_fetch_file:async a=>({structuredContent:{content:'# '+a.path+'\npass\n',display_url:'https://github.com/x/y/blob/main/'+a.path}}),
};
(0,eval)(fs.readFileSync(new URL('./reader_runtime.js',import.meta.url),'utf8'));
const run=globalThis.readerOp;
await run({session:'r90',action:'start'});
await run({session:'r90',action:'open',reason:'synthetic first view'});
await assert.rejects(()=>run({session:'r90',action:'next',reason:'must reject before judgment'}),/judgment/);
await run({session:'r90',action:'judge',disposition:'보류',answer:'synthetic'});
await assert.rejects(()=>run({session:'r90',action:'click',id:999,reason:'unseen link'}),/not visible/);
await run({session:'r90',action:'next',reason:'synthetic scroll'});
await run({session:'r90',action:'judge',disposition:'보류',answer:'synthetic'});
await run({session:'r90',action:'next',reason:'synthetic scroll'});
await run({session:'r90',action:'judge',disposition:'보류',answer:'synthetic'});
await assert.rejects(()=>run({session:'r90',action:'next',reason:'fourth view'}),/budget exhausted/);
await run({session:'r90',action:'finish',disposition:'보류',answer:'synthetic',stop_reason:'budget'});
const exp=outputs.filter(x=>x.type==='exposure' && x.session==='r90');
const all=outputs.filter(x=>x.type==='exposure');
assert.equal(all.length,3);
assert.deepEqual(all.map(x=>x.exposed_codepoints),[1500,1500,1500]);
assert.deepEqual(all.map(x=>x.exposed_utf8_bytes),[4000,4000,4000]);
assert.equal(all[2].cumulative_codepoints,4500);
await assert.rejects(()=>run({session:'r90',action:'finish'}),/inactive/);
input={request:'synthetic',url:'https://github.com/x/y',hint:''};
await run({session:'r91',action:'start'});
await run({session:'r91',action:'open',reason:'directory'});
await run({session:'r91',action:'judge',disposition:'보류',answer:'list only'});
await run({session:'r91',action:'click',id:0,from_step:1,reason:'first file'});
await run({session:'r91',action:'judge',disposition:'보류',answer:'one file'});
await run({session:'r91',action:'click',id:1,from_step:1,reason:'remembered second file'});
await run({session:'r91',action:'judge',disposition:'조건부',answer:'two files'});
await run({session:'r91',action:'finish',disposition:'조건부',answer:'synthetic',stop_reason:'budget'});
assert.ok(outputs.some(x=>x.type==='exposure' && x.exposed_text.includes('second.gd')));
console.log(JSON.stringify({status:'passed',synthetic_sessions:2,real_sessions:0,checks:['Unicode codepoints','UTF8 byte accounting','4500 total and 1500 per-view cap','fourth opening rejected','judgment before movement','unseen-link rejection','remembered visible-link choice','single final answer'],at_utc:new Date().toISOString()}));
