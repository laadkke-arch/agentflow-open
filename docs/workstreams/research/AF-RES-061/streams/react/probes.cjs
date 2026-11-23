/* AF-RES-061 researcher auxiliary probes. Not upstream tests or historical user output. */
'use strict';
process.env.NODE_ENV = 'development';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {createRequire} = require('node:module');
const req = createRequire(path.join(__dirname, '.workbench/runtime/package.json'));
const {SpringValue, Globals} = req('@react-spring/core');
const {frameLoop} = req('@react-spring/shared');
const {raf} = req('@react-spring/rafz');
const baseConfig = {mass:1,tension:100,friction:10,velocity:0};
const sourceCommit = 'b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a';
Globals.assign({frameLoop:'demand',skipAnimation:false});
const state = s => ({value:s.get(),velocity_pt_per_ms:s.velocity,idle:s.idle,isAnimating:s.isAnimating,
  elapsed_ms:s.animation.values[0]?.elapsedTime,lastPosition:s.animation.values[0]?.lastPosition,
  lastVelocity:s.animation.values[0]?.lastVelocity,goal:s.goal,config:{...s.animation.config}});
const make = (extra={},from=0,to=1) => {
  Globals.assign({skipAnimation:false});frameLoop.clear();
  const s=new SpringValue(from);
  s.start({to,config:{...baseConfig,...extra}});
  return s;
};
const stop = s => {s.stop();frameLoop.clear();};
const results=[];
const add=(run_id,input,output,classification='researcher_auxiliary')=>results.push({run_id,input,output,classification});
for (const clamp of [false,true]) {
  const case_id=clamp?'RS-B':'RS-N';
  for (const dt of [16,250]) {
    const s=make({clamp});s.advance(dt);
    add(`${case_id}-direct-${dt}`,{case_id,from:0,to:1,config:{...baseConfig,clamp},calls:[dt]},state(s));stop(s);
  }
  for (const dt of [1,16,1000/60]) {
    const s=make({clamp});let time=0,firstAbove=null,firstIdle=null,max=-Infinity;
    const trace=[];
    while (time<3000 && !s.idle) {
      s.advance(dt);time+=dt;
      const o=state(s);max=Math.max(max,o.value);
      const r={time_ms:time,value:o.value,velocity_pt_per_ms:o.velocity_pt_per_ms,idle:o.idle};
      trace.push(r);
      if(firstAbove===null&&o.value>1)firstAbove=r;
      if(o.idle&&firstIdle===null)firstIdle=r;
    }
    add(`${case_id}-frames-${dt}`,{case_id,from:0,to:1,config:{...baseConfig,clamp},constant_dt_ms:dt,max_wall_ms:3000},
      {first_emitted_above_goal:firstAbove,first_idle:firstIdle,max_emitted_value:max,final:state(s),trace});stop(s);
  }
}
for (const dt of [16.1,16.9,1000]) {
  const s=make();s.advance(dt);add(`RS-X-fractional-or-large-${dt}`,{config:baseConfig,calls:[dt]},state(s));stop(s);
}
for(const friction of [1000,3000]){
  const s=make({friction});s.advance(16);add(`RS-X-strong-damping-${friction}`,{config:{...baseConfig,friction},calls:[16]},state(s));stop(s);
}
for (const precision of [undefined,0.01,0.001,0.0001]) {
  const c=precision===undefined?{}:{precision};const s=make(c);let t=0,lastMoving=null;
  while(!s.idle&&t<10000){lastMoving=state(s);s.advance(1);t++;}
  add(`RS-X-precision-${precision??'default'}`,{config:{...baseConfig,...c},dt_ms:1,max_wall_ms:10000},
    {first_idle_ms:s.idle?t:null,previous:lastMoving,final:state(s)});stop(s);
}
for(const cancel of [false,true]){
  const s=make();let event=null;s.start({onRest:r=>{event=r;}});s.advance(16);const before=state(s);s.stop(cancel);
  add(`RS-X-stop-${cancel}`,{config:baseConfig,advance_ms:16,stop_cancel:cancel},{before,after:state(s),onRest:event});stop(s);
}
{
  const s=make();s.advance(100);const before=state(s);s.start({to:-1});const afterRetarget=state(s);s.advance(1);
  add('RS-X-retarget',{initial_goal:1,new_goal:-1,advance_before_ms:100,advance_after_ms:1},{before,afterRetarget,afterAdvance:state(s)});stop(s);
}
{
  const s=make();s.advance(16);const before=state(s);Globals.assign({skipAnimation:true});frameLoop.advance(16);
  add('RS-X-skip-active',{advance_before_ms:16,assign_skipAnimation:true,next_frame_ms:16},{before,after:state(s)});stop(s);
  Globals.assign({skipAnimation:true});const n=new SpringValue(0);n.start({to:1,config:baseConfig});
  add('RS-X-skip-new',{from:0,to:1,skipAnimation_before_start:true},state(n));stop(n);Globals.assign({skipAnimation:false});
}
{
  frameLoop.clear();let clock=1000;raf.now=()=>clock;raf.frameLoop='demand';const s=make();
  raf.advance();const first=state(s);clock+=250;raf.advance();
  add('RS-X-raf-large-gap',{clock_ms:[1000,1250],normal_raf_first_delta_ms:16.667,observed_gap_ms:250},
    {first,second:state(s),source_policy:'rafz update caps subsequent elapsed delta at64ms; SpringValue then uses ceil(dt) 1ms substeps'});stop(s);
}
const modules=['@react-spring/core','@react-spring/animated','@react-spring/shared','@react-spring/rafz','@react-spring/types','react'];
const packages=modules.map(name=>{const p=req(name+'/package.json');return {name:p.name,version:p.version};});
for(const p of packages)if(p.name.startsWith('@react-spring/')&&p.version!=='10.0.3')throw Error('Wrong component package '+p.name);
const artifact=req.resolve('@react-spring/core').replace(/index\.js$/,'react-spring_core.development.cjs');
const metadata={generated_utc:new Date().toISOString(),reader:'/root/react_release',source_commit:sourceCommit,
  node:process.version,platform:process.platform,arch:process.arch,packages,
  execution:'published npm CommonJS development component; no browser rendering; manual advance and one isolated raf clock probe',
  loaded_file:path.relative(__dirname,artifact),loaded_file_sha256:crypto.createHash('sha256').update(fs.readFileSync(artifact)).digest('hex'),
  input_origin:'researcher preselected RS-N/RS-B plus explicitly postseal auxiliary counterexamples',
  independent_original_output:false,full_upstream_suite:'미실시',probe_count:results.length};
fs.writeFileSync(path.join(__dirname,'raw-outputs.json'),JSON.stringify({metadata,results},null,2)+'\n');
console.log(JSON.stringify({metadata,summary:results.map(r=>({run_id:r.run_id,output:r.output.trace?{first_emitted_above_goal:r.output.first_emitted_above_goal,first_idle:r.output.first_idle,max_emitted_value:r.output.max_emitted_value,trace_length:r.output.trace.length}:r.output}))},null,2));
