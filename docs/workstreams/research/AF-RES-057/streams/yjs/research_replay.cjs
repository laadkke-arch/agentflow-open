/* Researcher-authored inputs frozen in cases.json. No expected-value assertions.
 * Usage: node research_replay.cjs /absolute/path/to/installed/yjs CASE_ID
 * It is not the upstream test suite or an author execution.
 */
const path = require('path')
const Y = require(path.resolve(process.argv[2]))
const which = process.argv[3]
const literal = 'this text can not be undone'
function originCase(includeSkip, variant) {
  const doc = new Y.Doc()
  const text = doc.get('text', Y.Text)
  const um = new Y.UndoManager(text, new Set(includeSkip ? [null, 'SKIP'] : [null]), {captureTimeout: 0})
  const ordinary = () => text.insert(text.length, 'mine ')
  const protectedEdit = () => doc.transact(() => text.applyDelta([{insert: literal}]), variant === 'single_author' ? null : 'SKIP')
  if (variant === 'reverse') { protectedEdit(); ordinary() }
  else if (variant === 'literal_only') protectedEdit()
  else { ordinary(); protectedEdit() }
  const before = text.toString()
  const undoDepth = um.undoStack.length
  um.undo()
  const afterUndo = text.toString()
  const afterUndoDepths = [um.undoStack.length, um.redoStack.length]
  um.redo()
  const afterRedo = text.toString()
  um.undo(); um.undo()
  return {variant, includeSkip, before, undoDepth, afterUndo, afterUndoDepths, afterRedo, afterTwoUndosFromRedo: text.toString()}
}
function copyCase(gc, insertionControl) {
  const doc = new Y.Doc({gc})
  const text = doc.getText('quill')
  let um
  if (insertionControl) um = new Y.UndoManager(text)
  text.insert(0, 'Hello World')
  if (!insertionControl) {um = new Y.UndoManager(text); text.delete(0, 5)}
  const newDoc = new Y.Doc({gc})
  Y.applyUpdate(newDoc, Y.encodeStateAsUpdate(doc))
  const newText = newDoc.getText('quill')
  newText.insert(0, '123')
  const newUm = new Y.UndoManager(newText)
  newUm.undoStack = um.undoStack
  const before = newText.toString()
  const undoDepth = newUm.undoStack.length
  let n = 0
  while (newUm.undoStack.length && n++ < 20) newUm.undo()
  if (newUm.undoStack.length) throw new Error('Researcher loop cap exceeded')
  const afterUndo = newText.toString()
  const afterUndoDepths = [newUm.undoStack.length, newUm.redoStack.length]
  n = 0
  while (newUm.redoStack.length && n++ < 20) newUm.redo()
  if (newUm.redoStack.length) throw new Error('Researcher redo loop cap exceeded')
  return {gc, insertionControl, before, undoDepth, afterUndo, afterUndoDepths, afterRedo: newText.toString(), clientIDs: [doc.clientID,newDoc.clientID]}
}
function arrayCase(boundary) {
  const doc = new Y.Doc()
  const array0 = doc.getArray('array')
  const um = new Y.UndoManager(array0, {captureTimeout: Number.MAX_VALUE})
  array0.push([1,2,3])
  if (boundary) um.stopCapturing()
  array0.push([4,5,6])
  const before = array0.toArray()
  const undoDepth = um.undoStack.length
  um.undo()
  const afterUndo = array0.toArray()
  const afterUndoDepths = [um.undoStack.length, um.redoStack.length]
  um.redo()
  const afterRedo = array0.toArray()
  um.undo()
  const repeatedFirstUndo = array0.toArray()
  um.undo()
  return {boundary, before, undoDepth, afterUndo, afterUndoDepths, afterRedo, repeatedFirstUndo, repeatedSecondUndo:array0.toArray()}
}
const out = []
function observe(label, fn) {
  try {out.push({label, status:'completed', observations:fn()})}
  catch (error) {out.push({label, status:'exception', message:String(error), stack:error.stack})}
}
if (which === 'YN1') for (const variant of ['normal','reverse','single_author','literal_only']) for(const option of [false,true]) observe(`${variant}-${option?'opB':'opA'}`,()=>originCase(option,variant))
else if (which === 'YN2') for(const control of [false,true]) for(const gc of [true,false]) observe(`${control?'insertion_control':'deletion'}-${gc?'opA':'opB'}`,()=>copyCase(gc,control))
else if (which === 'YT1') for(const boundary of [true,false]) observe(boundary?'opA':'opB',()=>arrayCase(boundary))
else throw new Error('CASE_ID must be YN1, YN2, or YT1')
console.log(JSON.stringify({case_id:which, runtime:process.version, at_UTC:new Date().toISOString(), evidence_kind:'researcher_replay', results:out},null,2))
