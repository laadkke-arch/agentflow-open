const fs = require('fs');
const path = require('path');
const {createRequire} = require('module');
const requireReplay = createRequire(path.resolve(process.argv[2], 'package.json'));
const {Schema} = requireReplay('prosemirror-model');
const {EditorState, TextSelection} = requireReplay('prosemirror-state');
const IR = requireReplay('prosemirror-inputrules');
const schema = new Schema({nodes:{doc:{content:'paragraph+'},paragraph:{content:'text*',group:'block'},text:{group:'inline'}}});
const textDoc = s => schema.node('doc',null,[schema.node('paragraph',null,s?schema.text(s):null)]);
const histories = Object.fromEntries(['103','104','130','150'].map(v=>[v,requireReplay('history'+v)]));
const results=[];
function snap(state,H) {return {text:state.doc.textContent,doc:state.doc.toJSON(),selection:{from:state.selection.from,to:state.selection.to},undoDepth:H.undoDepth(state),redoDepth:H.redoDepth(state)}}
function command(state,cmd,time){let dispatches=0; const ok=cmd(state,tr=>{state=state.apply(time==null?tr:tr.setTime(time));dispatches++});return {state,ok,dispatches}}
function record(case_id,variant,op,version,fn){try{results.push({case_id,variant,op,history_version:version,...fn(histories[version])})}catch(e){results.push({case_id,variant,op,history_version:version,error:{name:e.name,message:e.message,stack:e.stack}})}}
const initial='abcdefghijklmnopqrstuvwxyz0123456789';
for(const variant of ['normal','reversed'])for(const op of ['A','B'])record('PN1',variant,op,'103',H=>{
 let state=EditorState.create({schema,doc:textDoc(initial),plugins:[H.history()]});
 const local=t=>{state=state.apply(H.closeHistory(state.tr.delete(25,30).setTime(t)))};
 const remote=t=>{state=state.apply(H.closeHistory(state.tr.insertText('R',state.doc.content.size-1).setTime(t)).setMeta('addToHistory',op==='B'))};
 if(variant==='normal'){local(1000);remote(2000)}else{remote(1000);local(2000)}
 const before=snap(state,H);const u=command(state,H.undo,3000);state=u.state;const afterUndo=snap(state,H);const r=command(state,H.redo,4000);state=r.state;return {scope:'researcher synthetic history-only metadata variant; not original collab bug',before,undo:{returned:u.ok,dispatches:u.dispatches,...afterUndo},redo:{returned:r.ok,dispatches:r.dispatches,...snap(state,H)}};
});
for(const variant of ['normal','later-x'])for(const op of ['A','B'])record('PN2',variant,op,'130',H=>{
 const plugin=IR.inputRules({rules:[IR.ellipsis]});
 let now=1000;const view={state:EditorState.create({schema,doc:textDoc(''),plugins:[H.history({newGroupDelay:500}),plugin]}),composing:false,dispatch(tr){this.state=this.state.apply(tr.setTime(now));}};
 const input=(ch,time)=>{now=time;const pos=view.state.selection.from;const handled=plugin.props.handleTextInput(view,pos,pos,ch);if(!handled)view.dispatch(view.state.tr.insertText(ch));return {char:ch,time,handled,text:view.state.doc.textContent}};
 const inputTrace=[input('.',1000),input('.',1001),input('.',1002)];if(variant==='later-x')inputTrace.push(input('x',1003));
 const before=snap(view.state,H);now=variant==='normal'?1003:1004;const u=command(view.state,op==='A'?H.undo:IR.undoInputRule,now);view.state=u.state;const afterUndo=snap(view.state,H);now++;const r=command(view.state,H.redo,now);view.state=r.state;
 return {scope:'minimal researcher inputRules completion; no real browser IME/author environment',inputTrace,before,undo:{returned:u.ok,dispatches:u.dispatches,...afterUndo},redo:{returned:r.ok,dispatches:r.dispatches,...snap(view.state,H)}};
});
for(const variant of ['normal','remote-b'])for(const op of ['A','B'])record('PT1',variant,op,'150',H=>{
 let state=EditorState.create({schema,doc:textDoc(''),plugins:[H.history()]});state=state.apply(state.tr.insertText('a').setTime(1000));if(op==='B')state=state.apply(H.closeHistory(state.tr));
 let second=state.tr.insertText('b').setTime(1100);if(variant==='remote-b')second=second.setMeta('addToHistory',false);state=state.apply(second);
 const before=snap(state,H);const u=command(state,H.undo,1200);state=u.state;const afterUndo=snap(state,H);const r=command(state,H.redo,1300);state=r.state;
 return {scope:'researcher deterministic timing/schema completion; original default test assertions read separately; opB/remote/redo extensions',before,undo:{returned:u.ok,dispatches:u.dispatches,...afterUndo},redo:{returned:r.ok,dispatches:r.dispatches,...snap(state,H)}};
});
// Post-hoc public regression fixture from commit9bdb377. Frozen PN1 intervention is different.
for(const version of ['103','104'])record('PN1','posthoc-public-regression','fixed-test',version,H=>{
 let state=EditorState.create({schema,doc:textDoc('123456789ABCD'),plugins:[H.history()]});state=state.apply(state.tr.setSelection(TextSelection.create(state.doc,6,13)));state=state.apply(state.tr.delete(6,13));
 let rebase=state.tr.insert(6,schema.text('6789ABC')).insert(14,schema.text('E')).delete(6,13).setMeta('rebased',1).setMeta('addToHistory',false);rebase.mapping.setMirror(0,2);state=state.apply(rebase);const before=snap(state,H);const u=command(state,H.undo);state=u.state;return {scope:'post-hoc maintainer regression input; not frozen opA/B',before,undo:{returned:u.ok,dispatches:u.dispatches,...snap(state,H)}};
});
fs.writeFileSync(process.argv[3],JSON.stringify({runtime:process.version,created_UTC:new Date().toISOString(),cases:results},null,2)+'\n');
for(const r of results)console.log(JSON.stringify({case:r.case_id,variant:r.variant,op:r.op,v:r.history_version,before:r.before?.text,undo:r.undo,redo:r.redo,error:r.error&&{name:r.error.name,message:r.error.message}}));
