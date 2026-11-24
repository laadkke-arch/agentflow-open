package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"runtime"

	"github.com/piprate/json-gold/ld"
)

type fileRef struct {
	Path        string `json:"path"`
	DocumentIRI string `json:"document_iri"`
	SHA256      string `json:"sha256"`
}

type request struct {
	Nonce          string          `json:"nonce"`
	Algorithm      string          `json:"algorithm"`
	SuiteRoot      string          `json:"suite_root"`
	Base           string          `json:"base"`
	ProcessingMode string          `json:"processing_mode"`
	Input          fileRef         `json:"input"`
	Context        *fileRef        `json:"context"`
	Reexpand       bool            `json:"reexpand"`
	Expected       json.RawMessage `json:"expected"`
}

type load struct {
	URL       string `json:"document_iri"`
	Path      string `json:"path"`
	SHA256    string `json:"sha256"`
	Mechanism string `json:"mechanism"`
	Status    string `json:"status"`
}

type pinnedLoader struct {
	root  string
	input fileRef
	log   []load
}

func (loader *pinnedLoader) read(ref fileRef, mechanism string) (interface{}, error) {
	index := len(loader.log)
	loader.log = append(loader.log, load{URL: ref.DocumentIRI, Path: ref.Path, Mechanism: mechanism, Status: "failed"})
	raw, err := os.ReadFile(filepath.Join(loader.root, ref.Path))
	if err != nil {
		return nil, err
	}
	hash := fmt.Sprintf("%x", sha256.Sum256(raw))
	loader.log[index].SHA256 = hash
	if hash != ref.SHA256 {
		return nil, fmt.Errorf("unexpected SHA-256 for %s", ref.Path)
	}
	document, err := ld.DocumentFromReader(bytes.NewReader(raw))
	if err != nil {
		return nil, err
	}
	loader.log[index].Status = "read"
	return document, nil
}

func (loader *pinnedLoader) LoadDocument(iri string) (*ld.RemoteDocument, error) {
	if iri != loader.input.DocumentIRI {
		loader.log = append(loader.log, load{URL: iri, Mechanism: "processor_loader", Status: "unmapped"})
		return nil, fmt.Errorf("unmapped document IRI: %s", iri)
	}
	document, err := loader.read(loader.input, "processor_loader")
	if err != nil {
		return nil, err
	}
	return &ld.RemoteDocument{DocumentURL: iri, Document: document}, nil
}

func observation(value interface{}, err error) map[string]interface{} {
	if err == nil {
		return map[string]interface{}{"kind": "json", "value": value}
	}
	fmt.Fprintf(os.Stderr, "%T: %s\n", err, err)
	if ldErr, ok := err.(*ld.JsonLdError); ok {
		return map[string]interface{}{
			"kind": "jsonld_error", "code": string(ldErr.Code),
			"name": "*ld.JsonLdError", "message": ldErr.Error(),
		}
	}
	return map[string]interface{}{
		"kind": "infrastructure_error", "name": fmt.Sprintf("%T", err), "message": err.Error(),
	}
}

func execute(req request, loader *pinnedLoader) (map[string]interface{}, map[string]interface{}) {
	opts := ld.NewJsonLdOptions(req.Base)
	opts.ProcessingMode = req.ProcessingMode
	opts.DocumentLoader = loader
	proc := ld.NewJsonLdProcessor()

	switch req.Algorithm {
	case "expand":
		return observation(proc.Expand(req.Input.DocumentIRI, opts)), nil
	case "compact":
		context, err := loader.read(*req.Context, "local_context_argument")
		if err != nil {
			return observation(nil, fmt.Errorf("compaction context: %v", err)), nil
		}
		actual, err := proc.Compact(req.Input.DocumentIRI, context, opts)
		result := observation(actual, err)
		if err != nil || !req.Reexpand {
			return result, nil
		}
		var expected interface{}
		if err := json.Unmarshal(req.Expected, &expected); err != nil {
			return result, map[string]interface{}{"expected": observation(nil, err)}
		}
		return result, map[string]interface{}{
			"actual":   observation(proc.Expand(actual, opts)),
			"expected": observation(proc.Expand(expected, opts)),
		}
	default:
		return observation(nil, fmt.Errorf("unknown algorithm: %s", req.Algorithm)), nil
	}
}

func main() {
	var req request
	if err := json.NewDecoder(os.Stdin).Decode(&req); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
	loader := &pinnedLoader{root: req.SuiteRoot, input: req.Input, log: []load{}}
	result, post := execute(req, loader)
	envelope := map[string]interface{}{
		"protocol": 1, "nonce": req.Nonce, "pid": os.Getpid(), "runtime": runtime.Version(),
		"actual": result, "loads": loader.log, "post_expansion": post,
	}
	if err := json.NewEncoder(os.Stdout).Encode(envelope); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
}
