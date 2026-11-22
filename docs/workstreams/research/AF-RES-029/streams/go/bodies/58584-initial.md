## Background

At the moment, Go programs compiled as `GOOS=js GOARCH=wasm` cannot directly [export functions](https://docs.wasmer.io/integrations/examples/imports-and-exports) or other symbols directly as WASM exports. 

The only way to export a value is to wrap it and assign as a global JS namespace object (aka `window/globalThis`).

By default, each WASM module produced by Go compiler exports a few functions used internally by `wasm_exec.js` bridge and list of those symbols are hardcoded into a linker, like `wasm_export_resume`.

## Current State

Current FFI allows wrapping Go functions as callbacks and assign them to JS global namespace object. 
Go callback can only accept and return `js.Value` values.

This approach might be okay for simple tasks but might introduce some drawbacks for complex cases.

* We depend on `globalThis` to attach Go callbacks.
* Wrapping JS value references and calling Go's JS callback is an expensive process.
* Unable to pass low-level Go native values. Only `js.Value` references can be passed.

## Proposal

I propose to add some kind of mechanism to mark Go function to be exported in WASM module. It can be a compiler directive like `//go:wasmexport` or a special instruction similar to `CallImport` for exports.

Exported function should appear in exported WebAssembly instance symbols alongside built-in exports.

### Calling Exports

The export implementation can be low-level as existing import mechanism used internally by `wasm_exec.js`.

Values should be manually prepared and pushed into Go stack before calling an export.
Access to Go's memory allocator might be required for complex values like strings or slices.

**Abstract example:**

```go
package foo

//go:wasmexport
func Bar(id int) {
   fmt.Println("Foobar:", id)
}
```


```js
const callBar = (id) => {
  // Obtain exported function
  const foobarFunc = go._inst.exports["foo·Bar"];
  const { getsp, mem}  = go._inst.exports();

  // Put values on stack
  const view = new DataView(mem);
  const sp = getsp();
  view.setInt32(sp + 8, id, true);

  // Call exported Go function
  foobarFunc();
}
```
