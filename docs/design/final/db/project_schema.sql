-- 확인 장부 구조 v1 프로젝트 장부 스키마. 프로젝트마다 따로 둔다(ATTACH 별칭 {p}).
-- 공용 장부 ID(obs_id 등)는 값으로만 든다. 외래 키로 묶지 않는다.

-- 요청판: 원문 그대로. 고치면 새 판이다.
CREATE TABLE IF NOT EXISTS {p}.request_rev (
  req_id        INTEGER PRIMARY KEY,
  request_key   TEXT NOT NULL,
  rev           INTEGER NOT NULL,
  received_at   TEXT NOT NULL,
  text          TEXT NOT NULL,
  selected_part TEXT NOT NULL,
  idem_key      TEXT NOT NULL UNIQUE,
  UNIQUE (request_key, rev)
);
-- 조건: 원문 범위와 출처 도장.
CREATE TABLE IF NOT EXISTS {p}.requirement (
  req_id     INTEGER NOT NULL REFERENCES request_rev(req_id),
  code       TEXT NOT NULL,
  kind       TEXT NOT NULL CHECK (kind IN ('must','must_not','prefer','out_of_scope')),
  text       TEXT NOT NULL,
  provenance TEXT NOT NULL CHECK (provenance IN ('explicit','studio','inferred','later')),
  stamped_at TEXT NOT NULL,
  PRIMARY KEY (req_id, code)
);
-- Studio가 채운 판·환경·상태.
CREATE TABLE IF NOT EXISTS {p}.context_fact (
  req_id     INTEGER NOT NULL REFERENCES request_rev(req_id),
  key        TEXT NOT NULL,
  value      TEXT NOT NULL,
  provenance TEXT NOT NULL CHECK (provenance IN ('explicit','studio','inferred','later')),
  source_ref TEXT,
  stamped_at TEXT NOT NULL,
  PRIMARY KEY (req_id, key)
);
-- 결과를 보이기 전에 봉인한 "이미 고려한 대안". 이 행이 있어야 노출(exposure 'shown')을 쓸 수 있다.
-- state: given(사용자가 적음) / declined(적기를 거절) / none(적을 것이 없음). 봉인이 없으면 결정 변화는 U로 고정된다.
CREATE TABLE IF NOT EXISTS {p}.prior_seal (
  req_id     INTEGER PRIMARY KEY REFERENCES request_rev(req_id),
  sealed_at  TEXT NOT NULL,
  state      TEXT NOT NULL DEFAULT 'given' CHECK (state IN ('given','declined','none')),
  items_json TEXT NOT NULL,
  sha256     TEXT NOT NULL
);
-- 서랍 검색용 필요 문장. 꼬리표와 같은 칸으로 나눈다. 사용자 필요에 대한 말이므로 비공개다.
CREATE TABLE IF NOT EXISTS {p}.need (
  req_id INTEGER NOT NULL REFERENCES request_rev(req_id),
  slot   TEXT NOT NULL CHECK (slot IN ('input','output','user_without','keeps','breaks_when','summary')),
  lang   TEXT NOT NULL,
  text   TEXT NOT NULL,
  PRIMARY KEY (req_id, slot, lang)
);
-- 해석 복창과 묻기 결정. 답 첫 줄에 쓴다.
CREATE TABLE IF NOT EXISTS {p}.interpretation (
  req_id     INTEGER NOT NULL REFERENCES request_rev(req_id),
  code       TEXT NOT NULL,     -- 갈리는 조건 코드
  chosen     TEXT NOT NULL,
  other      TEXT,
  decision   TEXT NOT NULL CHECK (decision IN ('proceed','reread','common','fetch','verify','ask_once','conditional')),
  question   TEXT,             -- ask_once일 때 보낸 질문
  answer     TEXT,
  decided_at TEXT NOT NULL,
  PRIMARY KEY (req_id, code)
);
-- 탐색 기록: 어느 길이 무엇을 찾았고 왜 접히거나 빠졌나.
CREATE TABLE IF NOT EXISTS {p}.search_run (
  search_id INTEGER PRIMARY KEY,
  req_id    INTEGER NOT NULL REFERENCES request_rev(req_id),
  path      TEXT NOT NULL CHECK (path IN ('drawer','fresh')),
  query     TEXT NOT NULL,
  ran_at    TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS {p}.search_hit (
  search_id        INTEGER NOT NULL REFERENCES search_run(search_id),
  rank             INTEGER NOT NULL,
  url              TEXT NOT NULL,
  obs_id           INTEGER,          -- 서랍 적중이면 공용 관측 ID
  matched_tokens   TEXT NOT NULL,
  lexical_accident INTEGER NOT NULL CHECK (lexical_accident IN (0,1)),
  eligible         INTEGER NOT NULL DEFAULT 1 CHECK (eligible IN (0,1)),  -- 서랍 후보 자격(두 칸·서로 다른 내용어 둘)
  PRIMARY KEY (search_id, rank)
);
-- 판정 쪽지: (요청판, 조건, 관측) 판정. 덧붙이기만 한다.
CREATE TABLE IF NOT EXISTS {p}.slip (
  slip_id    INTEGER PRIMARY KEY,
  req_id     INTEGER NOT NULL REFERENCES request_rev(req_id),
  code       TEXT NOT NULL,
  obs_id     INTEGER NOT NULL,
  verdict    TEXT NOT NULL CHECK (verdict IN ('Y','N','U','NA')),
  role       TEXT NOT NULL CHECK (role IN ('direct','transplant','principle','test','reference')),
  ladder     TEXT NOT NULL CHECK (ladder IN ('L0','L1','L2','L3','L4','L5')),
  reason     TEXT NOT NULL,
  premises   TEXT NOT NULL DEFAULT '{}',  -- 이 판정이 기대는 요건 사실(JSON). 다음 요청판에서 같으면 재사용
  written_at TEXT NOT NULL,
  cause      TEXT NOT NULL CHECK (cause IN ('initial','channel','audit','user','request')),
  supersedes INTEGER REFERENCES slip(slip_id)
);
-- 답 실행과 자리. 당시 문장 그대로 보존한다.
CREATE TABLE IF NOT EXISTS {p}.answer_run (
  run_id      INTEGER PRIMARY KEY,
  req_id      INTEGER NOT NULL REFERENCES request_rev(req_id),
  produced_at TEXT NOT NULL,
  -- 답이 없을 때의 네 상태는 서로 다르다: 검증된 후보 없음 / 예산 소진 / 원문 접근 실패 / 범위 안 후보 없음
  status      TEXT NOT NULL CHECK (status IN ('complete','partial','none_verified','budget_exhausted',
                                              'source_unreachable','none_in_scope')),
  budget_json TEXT NOT NULL,
  next_action TEXT,
  rule_version TEXT NOT NULL DEFAULT 'final-v1',  -- 자리 규칙·관문·문턱의 판. 규칙이 바뀐 뒤에도 재생이 어느 규칙의 답인지 안다
  idem_key    TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS {p}.answer_slot (
  run_id   INTEGER NOT NULL REFERENCES answer_run(run_id),
  slot_no  INTEGER NOT NULL,
  kind     TEXT NOT NULL CHECK (kind IN ('direct','transplant','principle','test','reference','check')),
  sentence TEXT NOT NULL,
  ladder   TEXT NOT NULL,
  hold     TEXT NOT NULL,     -- 보류·철회 조건
  PRIMARY KEY (run_id, slot_no)
);
-- 사용 쪽지: 답 자리가 어느 공용 관측을 인용했나. 철회 전파의 유일한 길이다.
-- part: first_link(첫 링크) support(뒷받침) flip(뒤집을 위치) contrast(관문 ③의 동종 기준선으로만 인용).
-- contrast로 인용한 관측이 바뀌어도 그 자리에는 철회 알림을 내지 않는다(EVAL-X1 T2-b).
CREATE TABLE IF NOT EXISTS {p}.usage (
  run_id  INTEGER NOT NULL,
  slot_no INTEGER NOT NULL,
  obs_id  INTEGER NOT NULL,
  part    TEXT NOT NULL CHECK (part IN ('first_link','support','flip','contrast')),
  PRIMARY KEY (run_id, slot_no, obs_id, part),
  FOREIGN KEY (run_id, slot_no) REFERENCES answer_slot(run_id, slot_no)
);
-- 접힌 근접 대안과 갈린 조건.
CREATE TABLE IF NOT EXISTS {p}.folded (
  run_id    INTEGER NOT NULL REFERENCES answer_run(run_id),
  url       TEXT NOT NULL,
  obs_id    INTEGER,
  condition TEXT NOT NULL,
  reason    TEXT NOT NULL,
  PRIMARY KEY (run_id, url, condition)   -- 같은 주소의 다른 위치·다른 갈린 조건을 따로 접을 수 있게
);
-- 알림: 공용 관측의 대체가 이 프로젝트 답 자리에 닿았을 때.
CREATE TABLE IF NOT EXISTS {p}.notice (
  notice_id  INTEGER PRIMARY KEY,
  run_id     INTEGER NOT NULL,
  slot_no    INTEGER NOT NULL,
  old_obs    INTEGER NOT NULL,
  new_obs    INTEGER NOT NULL,
  effect     TEXT NOT NULL,
  created_at TEXT NOT NULL,
  text       TEXT NOT NULL,
  UNIQUE (run_id, slot_no, old_obs, new_obs)
);
-- 노출과 이후 행동(평가용).
CREATE TABLE IF NOT EXISTS {p}.exposure (
  run_id  INTEGER NOT NULL,
  slot_no INTEGER NOT NULL,
  event   TEXT NOT NULL CHECK (event IN ('shown','opened','expanded','adopted','rejected')),
  at      TEXT NOT NULL,
  note    TEXT,
  PRIMARY KEY (run_id, slot_no, event, at)
);

CREATE TRIGGER IF NOT EXISTS {p}.request_rev_no_update BEFORE UPDATE ON request_rev
BEGIN SELECT RAISE(ABORT, 'request_rev is immutable'); END;
-- 봉인은 노출보다 먼저이고 노출 뒤에 바꿀 수 없어야 '새로 알았나'를 셀 수 있다.
CREATE TRIGGER IF NOT EXISTS {p}.prior_seal_no_update BEFORE UPDATE ON prior_seal
BEGIN SELECT RAISE(ABORT, 'prior_seal is immutable'); END;
CREATE TRIGGER IF NOT EXISTS {p}.prior_seal_no_delete BEFORE DELETE ON prior_seal
BEGIN SELECT RAISE(ABORT, 'prior_seal is immutable'); END;
CREATE TRIGGER IF NOT EXISTS {p}.slip_no_update BEFORE UPDATE ON slip
BEGIN SELECT RAISE(ABORT, 'slip is append-only'); END;
CREATE TRIGGER IF NOT EXISTS {p}.slip_no_delete BEFORE DELETE ON slip
BEGIN SELECT RAISE(ABORT, 'slip is append-only'); END;
CREATE TRIGGER IF NOT EXISTS {p}.answer_slot_no_update BEFORE UPDATE ON answer_slot
BEGIN SELECT RAISE(ABORT, 'answer_slot is immutable'); END;
CREATE TRIGGER IF NOT EXISTS {p}.usage_no_delete BEFORE DELETE ON usage
BEGIN SELECT RAISE(ABORT, 'usage is append-only'); END;
