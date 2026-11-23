const fs=require('fs'),path=require('path');const {createRequire}=require('module');const R=createRequire(path.resolve(process.argv[2],'package.json'));
const {EditorState,TextSelection}=R('prosemirror-state');const {Schema}=R('prosemirror-model');const {schema:basic}=R('prosemirror-schema-basic');const {addListNodes}=R('prosemirror-schema-list');const {Step}=R('prosemirror-transform');const {collab,receiveTransaction}=R('prosemirror-collab');
const schema=new Schema({nodes:addListNodes(basic.spec.nodes,'paragraph block*','block'),marks:basic.spec.marks});
const doc=s=>schema.node('doc',null,[schema.node('paragraph',null,s?schema.text(s):null)]);const results=[];
for(const version of ['103','104']){
 const H=R('history'+version);
 const snap=s=>({text:s.doc.textContent,selection:{from:s.selection.from,to:s.selection.to},undoDepth:H.undoDepth(s),redoDepth:H.redoDepth(s)});
 // Author's exactpublished stepJSON+initial text; headless dispatch, only history/collab plugins.
 let state=EditorState.create({schema,doc:doc('123456789'),plugins:[H.history(),collab({clientID:4})]});const trace=[];const put=(label,tr)=>{state=state.apply(tr);trace.push({label,...snap(state)})};
 const receive=(steps,remote=true)=>put('receive '+(remote?'remote5':'own4'),receiveTransaction(state,steps.map(s=>Step.fromJSON(schema,s)),steps.map(()=>remote?5:4)));
 try{
  for(const [pos,ch] of [[10,'A'],[11,'B'],[12,'C']])receive([{stepType:'replace',from:pos,to:pos,slice:{content:[{type:'text',text:ch}]}}]);
  put('selection6..13',state.tr.setSelection(TextSelection.create(state.doc,6,13)));
  receive([{stepType:'replace',from:13,to:13,slice:{content:[{type:'text',text:'D'}]}}]);
  put('localdelete6..13',state.tr.step(Step.fromJSON(schema,{stepType:'replace',from:6,to:13})));
  receive([{stepType:'replace',from:13,to:13,slice:{content:[{type:'text',text:'E'}]}}]);receive([{stepType:'replace',from:6,to:13}],false);
  let returned=H.undo(state,tr=>put('undo',tr));results.push({variant:'author-repro-headless',history_version:version,scope:'OriginalJSONsteps andinitialHTMLtext; historicalcoreversions,modernNode; exampleSetup UIplugins replaced byhistory+collab; not authorbrowserrun',returned,trace,after:snap(state)});
 }catch(e){results.push({variant:'author-repro-headless',history_version:version,error:{name:e.name,message:e.message},trace})}
 // Maintainer's regression fixture separate from authortrace/frozen metadata variants.
 state=EditorState.create({schema,doc:doc('123456789ABCD'),plugins:[H.history()]});const regression=[];
 try{
  state=state.apply(state.tr.setSelection(TextSelection.create(state.doc,6,13)));state=state.apply(state.tr.delete(6,13));let tr=state.tr.insert(6,schema.text('6789ABC')).insert(14,schema.text('E')).delete(6,13).setMeta('rebased',1).setMeta('addToHistory',false);tr.mapping.setMirror(0,2);state=state.apply(tr);regression.push({label:'before undo',...snap(state)});let returned=H.undo(state,tr=>{state=state.apply(tr)});results.push({variant:'maintainer-regression-historical-core',history_version:version,returned,trace:regression,after:snap(state)});
 }catch(e){results.push({variant:'maintainer-regression-historical-core',history_version:version,error:{name:e.name,message:e.message},trace:regression})}
}
fs.writeFileSync(process.argv[3],JSON.stringify({runtime:process.version,created_UTC:new Date().toISOString(),scope:'Post-hoc sensitivity not frozenopA/B; historicalcore reducesdependency mismatch,UI/runtime still different',results},null,2)+'\n');for(const r of results)console.log(JSON.stringify({variant:r.variant,history_version:r.history_version,error:r.error,after:r.after}));
