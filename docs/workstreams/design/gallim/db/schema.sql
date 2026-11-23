PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS request_revision (
  id TEXT PRIMARY KEY NOT NULL, request_id TEXT NOT NULL,
  previous_id TEXT CHECK(previous_id IS NULL OR previous_id<>id), original_text TEXT NOT NULL CHECK(length(original_text)>0),
  UNIQUE(request_id,id), UNIQUE(request_id,previous_id),
  FOREIGN KEY(request_id,previous_id) REFERENCES request_revision(request_id,id)
);
CREATE UNIQUE INDEX IF NOT EXISTS request_one_root ON request_revision(request_id) WHERE previous_id IS NULL;
CREATE TABLE IF NOT EXISTS requirement (
  request_revision_id TEXT NOT NULL REFERENCES request_revision(id),
  id TEXT NOT NULL, label TEXT NOT NULL CHECK(length(label)>0),
  required INTEGER NOT NULL CHECK(required IN (0,1)),
  start_char INTEGER NOT NULL CHECK(start_char>=0), end_char INTEGER NOT NULL CHECK(end_char>start_char),
  PRIMARY KEY(request_revision_id,id)
);
CREATE TABLE IF NOT EXISTS resource (
  id TEXT PRIMARY KEY NOT NULL, subject TEXT NOT NULL CHECK(length(subject)>0), kind TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS edition (
  id TEXT PRIMARY KEY NOT NULL, resource_id TEXT NOT NULL REFERENCES resource(id),
  version TEXT NOT NULL CHECK(length(version)>0), UNIQUE(resource_id,version)
);
CREATE TABLE IF NOT EXISTS candidate_context (
  id TEXT PRIMARY KEY NOT NULL, request_revision_id TEXT NOT NULL REFERENCES request_revision(id),
  edition_id TEXT NOT NULL REFERENCES edition(id), scope TEXT NOT NULL CHECK(length(scope)>0),
  configuration TEXT NOT NULL CHECK(length(configuration)>0),
  UNIQUE(id,request_revision_id), UNIQUE(request_revision_id,edition_id,scope,configuration)
);
CREATE TABLE IF NOT EXISTS source_document (
  id TEXT PRIMARY KEY NOT NULL, url TEXT NOT NULL, title TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS source_revision (
  document_id TEXT NOT NULL REFERENCES source_document(id), revision_key TEXT NOT NULL,
  previous_key TEXT CHECK(previous_key IS NULL OR previous_key<>revision_key), capture_scope TEXT NOT NULL CHECK(length(capture_scope)>0),
  content TEXT NOT NULL CHECK(length(content)>0), sha256 TEXT NOT NULL CHECK(length(sha256)=64),
  PRIMARY KEY(document_id,revision_key), UNIQUE(document_id,previous_key),
  FOREIGN KEY(document_id,previous_key) REFERENCES source_revision(document_id,revision_key)
);
CREATE UNIQUE INDEX IF NOT EXISTS source_one_root ON source_revision(document_id) WHERE previous_key IS NULL;
CREATE TABLE IF NOT EXISTS source_fragment (
  id TEXT PRIMARY KEY NOT NULL, document_id TEXT NOT NULL, revision_key TEXT NOT NULL,
  start_char INTEGER NOT NULL CHECK(start_char>=0), end_char INTEGER NOT NULL CHECK(end_char>start_char),
  sha256 TEXT NOT NULL CHECK(length(sha256)=64), locator TEXT NOT NULL CHECK(length(locator)>0),
  FOREIGN KEY(document_id,revision_key) REFERENCES source_revision(document_id,revision_key)
);
CREATE TABLE IF NOT EXISTS claim (
  id TEXT PRIMARY KEY NOT NULL, context_id TEXT NOT NULL, evidence_context_id TEXT NOT NULL,
  request_revision_id TEXT NOT NULL, requirement_id TEXT NOT NULL,
  kind TEXT NOT NULL CHECK(kind IN ('direct','proposal','analogy')),
  direction TEXT NOT NULL CHECK(direction IN ('support','refute')),
  fragment_id TEXT NOT NULL REFERENCES source_fragment(id), assertion TEXT NOT NULL CHECK(length(assertion)>0),
  FOREIGN KEY(context_id,request_revision_id) REFERENCES candidate_context(id,request_revision_id),
  FOREIGN KEY(evidence_context_id,request_revision_id) REFERENCES candidate_context(id,request_revision_id),
  FOREIGN KEY(request_revision_id,requirement_id) REFERENCES requirement(request_revision_id,id)
);
CREATE INDEX IF NOT EXISTS claim_target ON claim(context_id,requirement_id);
CREATE INDEX IF NOT EXISTS claim_source ON claim(fragment_id);
CREATE TABLE IF NOT EXISTS decision_run (
  id INTEGER PRIMARY KEY, operation_key TEXT NOT NULL UNIQUE, command_hash TEXT NOT NULL,
  context_id TEXT NOT NULL REFERENCES candidate_context(id), evaluator_version TEXT NOT NULL,
  input_json TEXT NOT NULL, output_json TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('verified','excluded','pending')),
  created_at TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS decision_item (
  run_id INTEGER NOT NULL REFERENCES decision_run(id), requirement_id TEXT NOT NULL,
  state TEXT NOT NULL CHECK(state IN ('supported','refuted','conflicting','unknown')),
  detail_json TEXT NOT NULL, PRIMARY KEY(run_id,requirement_id)
);
CREATE TABLE IF NOT EXISTS run_claim (
  run_id INTEGER NOT NULL REFERENCES decision_run(id), claim_id TEXT NOT NULL REFERENCES claim(id),
  eligibility TEXT NOT NULL CHECK(eligibility IN ('active','superseded')),
  PRIMARY KEY(run_id,claim_id)
);
CREATE INDEX IF NOT EXISTS run_claim_reverse ON run_claim(claim_id,run_id);
CREATE TABLE IF NOT EXISTS decision_parent (
  run_id INTEGER NOT NULL REFERENCES decision_run(id), parent_id INTEGER NOT NULL REFERENCES decision_run(id),
  PRIMARY KEY(run_id,parent_id), CHECK(parent_id<run_id)
);
CREATE INDEX IF NOT EXISTS decision_descendants ON decision_parent(parent_id,run_id);
CREATE TABLE IF NOT EXISTS recheck_job (
  id INTEGER PRIMARY KEY, run_id INTEGER NOT NULL REFERENCES decision_run(id),
  document_id TEXT NOT NULL, revision_key TEXT NOT NULL,
  UNIQUE(run_id,document_id,revision_key),
  FOREIGN KEY(document_id,revision_key) REFERENCES source_revision(document_id,revision_key)
);
CREATE TABLE IF NOT EXISTS recheck_resolution (
  job_id INTEGER PRIMARY KEY REFERENCES recheck_job(id), replacement_run_id INTEGER NOT NULL REFERENCES decision_run(id)
);
CREATE INDEX IF NOT EXISTS fragment_revision ON source_fragment(document_id,revision_key);
CREATE TRIGGER IF NOT EXISTS requirement_span BEFORE INSERT ON requirement WHEN
  NEW.end_char>(SELECT length(original_text) FROM request_revision WHERE id=NEW.request_revision_id)
BEGIN SELECT RAISE(ABORT,'requirement span outside request'); END;
CREATE TRIGGER IF NOT EXISTS source_span BEFORE INSERT ON source_fragment WHEN
  NEW.end_char>(SELECT length(content) FROM source_revision WHERE document_id=NEW.document_id AND revision_key=NEW.revision_key)
BEGIN SELECT RAISE(ABORT,'source span outside capture'); END;
CREATE TRIGGER IF NOT EXISTS request_revision_deny_update BEFORE UPDATE ON request_revision
BEGIN SELECT RAISE(ABORT,'immutable request_revision'); END;
CREATE TRIGGER IF NOT EXISTS request_revision_deny_delete BEFORE DELETE ON request_revision
BEGIN SELECT RAISE(ABORT,'immutable request_revision'); END;
CREATE TRIGGER IF NOT EXISTS requirement_deny_update BEFORE UPDATE ON requirement
BEGIN SELECT RAISE(ABORT,'immutable requirement'); END;
CREATE TRIGGER IF NOT EXISTS requirement_deny_delete BEFORE DELETE ON requirement
BEGIN SELECT RAISE(ABORT,'immutable requirement'); END;
CREATE TRIGGER IF NOT EXISTS resource_deny_update BEFORE UPDATE ON resource
BEGIN SELECT RAISE(ABORT,'immutable resource'); END;
CREATE TRIGGER IF NOT EXISTS resource_deny_delete BEFORE DELETE ON resource
BEGIN SELECT RAISE(ABORT,'immutable resource'); END;
CREATE TRIGGER IF NOT EXISTS edition_deny_update BEFORE UPDATE ON edition
BEGIN SELECT RAISE(ABORT,'immutable edition'); END;
CREATE TRIGGER IF NOT EXISTS edition_deny_delete BEFORE DELETE ON edition
BEGIN SELECT RAISE(ABORT,'immutable edition'); END;
CREATE TRIGGER IF NOT EXISTS candidate_context_deny_update BEFORE UPDATE ON candidate_context
BEGIN SELECT RAISE(ABORT,'immutable candidate_context'); END;
CREATE TRIGGER IF NOT EXISTS candidate_context_deny_delete BEFORE DELETE ON candidate_context
BEGIN SELECT RAISE(ABORT,'immutable candidate_context'); END;
CREATE TRIGGER IF NOT EXISTS source_document_deny_update BEFORE UPDATE ON source_document
BEGIN SELECT RAISE(ABORT,'immutable source_document'); END;
CREATE TRIGGER IF NOT EXISTS source_document_deny_delete BEFORE DELETE ON source_document
BEGIN SELECT RAISE(ABORT,'immutable source_document'); END;
CREATE TRIGGER IF NOT EXISTS source_revision_deny_update BEFORE UPDATE ON source_revision
BEGIN SELECT RAISE(ABORT,'immutable source_revision'); END;
CREATE TRIGGER IF NOT EXISTS source_revision_deny_delete BEFORE DELETE ON source_revision
BEGIN SELECT RAISE(ABORT,'immutable source_revision'); END;
CREATE TRIGGER IF NOT EXISTS source_fragment_deny_update BEFORE UPDATE ON source_fragment
BEGIN SELECT RAISE(ABORT,'immutable source_fragment'); END;
CREATE TRIGGER IF NOT EXISTS source_fragment_deny_delete BEFORE DELETE ON source_fragment
BEGIN SELECT RAISE(ABORT,'immutable source_fragment'); END;
CREATE TRIGGER IF NOT EXISTS claim_deny_update BEFORE UPDATE ON claim
BEGIN SELECT RAISE(ABORT,'immutable claim'); END;
CREATE TRIGGER IF NOT EXISTS claim_deny_delete BEFORE DELETE ON claim
BEGIN SELECT RAISE(ABORT,'immutable claim'); END;
CREATE TRIGGER IF NOT EXISTS decision_run_deny_update BEFORE UPDATE ON decision_run
BEGIN SELECT RAISE(ABORT,'immutable decision_run'); END;
CREATE TRIGGER IF NOT EXISTS decision_run_deny_delete BEFORE DELETE ON decision_run
BEGIN SELECT RAISE(ABORT,'immutable decision_run'); END;
CREATE TRIGGER IF NOT EXISTS decision_item_deny_update BEFORE UPDATE ON decision_item
BEGIN SELECT RAISE(ABORT,'immutable decision_item'); END;
CREATE TRIGGER IF NOT EXISTS decision_item_deny_delete BEFORE DELETE ON decision_item
BEGIN SELECT RAISE(ABORT,'immutable decision_item'); END;
CREATE TRIGGER IF NOT EXISTS run_claim_deny_update BEFORE UPDATE ON run_claim
BEGIN SELECT RAISE(ABORT,'immutable run_claim'); END;
CREATE TRIGGER IF NOT EXISTS run_claim_deny_delete BEFORE DELETE ON run_claim
BEGIN SELECT RAISE(ABORT,'immutable run_claim'); END;
CREATE TRIGGER IF NOT EXISTS decision_parent_deny_update BEFORE UPDATE ON decision_parent
BEGIN SELECT RAISE(ABORT,'immutable decision_parent'); END;
CREATE TRIGGER IF NOT EXISTS decision_parent_deny_delete BEFORE DELETE ON decision_parent
BEGIN SELECT RAISE(ABORT,'immutable decision_parent'); END;
CREATE TRIGGER IF NOT EXISTS recheck_job_deny_update BEFORE UPDATE ON recheck_job
BEGIN SELECT RAISE(ABORT,'immutable recheck_job'); END;
CREATE TRIGGER IF NOT EXISTS recheck_job_deny_delete BEFORE DELETE ON recheck_job
BEGIN SELECT RAISE(ABORT,'immutable recheck_job'); END;
CREATE TRIGGER IF NOT EXISTS recheck_resolution_deny_update BEFORE UPDATE ON recheck_resolution
BEGIN SELECT RAISE(ABORT,'immutable recheck_resolution'); END;
CREATE TRIGGER IF NOT EXISTS recheck_resolution_deny_delete BEFORE DELETE ON recheck_resolution
BEGIN SELECT RAISE(ABORT,'immutable recheck_resolution'); END;
