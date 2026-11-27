-- 확인 장부 공용 장부 스키마(제품 단위 1). 설계 예제 docs/design/final/db/schema.sql에서 옮겼다.
-- 바꾼 것: locator 정규화 열(R-1 n1), observation 앵커·대응 열(R-1 m1), receipt·contrast는 지문만(07 D6c).
-- 08-implementation.md I3·I4·I5 참조.
-- 확인 장부 구조 v1 저장 스키마 (SQLite 3.35 이상, FTS5 필요)
--
-- 두 저장소로 나눈다.
--   공용 장부(commons): 원문에 대해 말한 것. 프로젝트 사이에서 재사용한다.
--   프로젝트 장부(project): 사용자의 필요에 대해 말한 것. 그 프로젝트만 읽는다.
-- 공용 장부는 프로젝트 장부를 참조하지 않는다. 프로젝트 장부는 공용 장부의 ID를 값으로만 든다.
-- 확정 기록은 덧붙이기만 한다. 고침은 새 행(대체, 취소, 새 쪽지)으로 한다.

-- ===================== 공용 장부 =====================

-- 위치: 원 URL 문자열 그대로. 경로·쿼리·fragment를 지우지 않는다.
CREATE TABLE IF NOT EXISTS locator (
  locator_id     INTEGER PRIMARY KEY,
  url            TEXT NOT NULL UNIQUE,
  first_seen_at  TEXT NOT NULL,
  first_seen_via TEXT NOT NULL CHECK (first_seen_via IN ('request','collection','channel','operator')),
  -- 정규화 키(07 R-1 임시안). 원래 문자열(url)은 그대로 두고 키를 더한다. 재사용은 (page, 판, 위치)로 찾는다.
  -- target은 묶어 보여 주는 데만 쓴다(전역 병합 금지). norm_rules가 실패 이유를 담으면 page = url이다.
  url_norm       TEXT,
  page           TEXT,
  target         TEXT,
  norm_rules     TEXT
);
CREATE INDEX IF NOT EXISTS locator_by_page ON locator(page);

-- 주소 별칭: 리다이렉트, 이관, 거울, 보관본. 같은 대상이라는 뜻이 아니라 "이 주소로도 열린다"는 뜻이다.
CREATE TABLE IF NOT EXISTS locator_alias (
  alias_id     INTEGER PRIMARY KEY,
  from_id      INTEGER NOT NULL REFERENCES locator(locator_id),
  to_id        INTEGER NOT NULL REFERENCES locator(locator_id),
  kind         TEXT NOT NULL CHECK (kind IN ('redirect','moved','mirror','archive')),
  asserted_at  TEXT NOT NULL,
  evidence_obs INTEGER REFERENCES observation(obs_id),
  CHECK (from_id <> to_id)
);
-- 별칭 취소는 따로 적는다. 취소된 별칭은 읽을 때 건너뛴다.
CREATE TABLE IF NOT EXISTS locator_alias_cancel (
  alias_id     INTEGER PRIMARY KEY REFERENCES locator_alias(alias_id),
  cancelled_at TEXT NOT NULL,
  reason       TEXT NOT NULL
);

-- 인용 본문. 관측은 지문만 든다. 권리자가 요청하면 본문만 지우고 묘비(지운 시각·이유)를 남긴다(07 D7).
-- 같은 문장은 판이 달라도 한 행이다. 지운 뒤 같은 문장을 다시 읽어도 본문을 다시 쓰지 않는다.
CREATE TABLE IF NOT EXISTS quote_text (
  quote_fp     TEXT PRIMARY KEY,
  text         TEXT,
  stored_at    TEXT NOT NULL,
  erased_at    TEXT,
  erase_reason TEXT,
  CHECK ((text IS NULL) = (erased_at IS NOT NULL))
);

-- 원문 가져오기 기록(07 D1). 예산이 세는 단위다. 요청 시계의 가져오기는 프로젝트 장부에 둔다(누가 왜 읽었는지는 공용에 남기지 않는다).
CREATE TABLE IF NOT EXISTS fetch_log (
  fetch_id    INTEGER PRIMARY KEY,
  clock       TEXT NOT NULL CHECK (clock IN ('follow','background','deadline')),  -- deadline: 기한 읽기를 따로 셀 때(08 I22)
  url         TEXT NOT NULL,
  edition_key TEXT,
  at          TEXT NOT NULL,
  outcome     TEXT NOT NULL CHECK (outcome IN ('ok','not_modified','not_found','unreachable','truncated','unsupported')),
  bytes       INTEGER,
  job_id      INTEGER
);

-- 판: 번호·태그·커밋·DOI·문서 개정 ID. 없으면 kind='fetch'로 (가져온 시각, 지문)을 키로 쓴다.
CREATE TABLE IF NOT EXISTS edition (
  edition_id    INTEGER PRIMARY KEY,
  locator_id    INTEGER NOT NULL REFERENCES locator(locator_id),
  edition_key   TEXT NOT NULL,
  kind          TEXT NOT NULL CHECK (kind IN ('release','revision','commit','doi','fetch')),
  published_at  TEXT,          -- NULL이면 발행 시각 불명
  first_seen_at TEXT NOT NULL,
  UNIQUE (locator_id, edition_key)
);

-- 실행 영수증: 정확한 런타임, 프로그램 지문, 입력·출력의 지문(07 D6c).
-- 입력·출력 본문은 요청 수치를 담으므로 요청 프로젝트 장부({p}.receipt_body)에 둔다. 지문은 프로젝트 비밀 열쇠로 만든
-- HMAC이라, 작은 입력(예: maxsize 8)을 사전 대입으로 되찾을 수 없다. 대신 프로젝트 사이 영수증 재사용은 없다(08 I5).
-- ran_on은 날짜까지만 둔다(07 D6b와 같은 이유).
CREATE TABLE IF NOT EXISTS receipt (
  receipt_id     INTEGER PRIMARY KEY,
  runtime        TEXT NOT NULL,      -- 실제로 돈 판(예: CPython 3.12.3). 원한 판과 다르면 프로젝트 장부 exec_log에 둘 다 남는다
  program_sha256 TEXT NOT NULL,      -- 공개 프로그램의 sha256(요청 수치는 프로그램이 아니라 입력으로 받는다)
  input_fp       TEXT NOT NULL,
  output_fp      TEXT NOT NULL,
  ran_on         TEXT NOT NULL,
  idem_key       TEXT NOT NULL UNIQUE
);

-- 관측: (판, 위치)에서 무엇을 보았나. 같은 내용을 다시 보면 새 관측이 아니라 sighting을 더한다.
CREATE TABLE IF NOT EXISTS observation (
  obs_id        INTEGER PRIMARY KEY,
  edition_id    INTEGER NOT NULL REFERENCES edition(edition_id),
  position      TEXT NOT NULL,     -- 절·줄·논리 키
  observed_at   TEXT NOT NULL,     -- 처음 본 시각
  method        TEXT NOT NULL CHECK (method IN ('intro_only','read_line','executed')),
  outcome       TEXT NOT NULL CHECK (outcome IN ('content','not_found','unreachable','unsupported','truncated')),
  quote_lang    TEXT,              -- 인용 본문은 quote_text에 지문으로 둔다(07 D7: 권리자 요청 때 본문만 지운다)
  quote_fp      TEXT,              -- 공백을 접은 인용의 sha256. 판이 달라도 같은 문장인지 본다
  statement     TEXT NOT NULL,     -- 원문 쪽에서 쓴 한 줄. 요청 문장을 쓰지 않는다
  evidence_ref  TEXT,              -- 인용이 원문 그대로가 아니면 판독문의 출처(연구 원장 행 등)
  flip_position TEXT,              -- 이 결론이 기대는 문장·줄·플래그
  receipt_id    INTEGER REFERENCES receipt(receipt_id),
  reader        TEXT,              -- 판독한 주체: 모델 ID와 프롬프트 판, 또는 사람. 잘못된 판독기의 관측을 골라 다시 확인한다
  via_alias     INTEGER REFERENCES locator_alias(alias_id),  -- 이 별칭을 따라 열었다(07 D5). 별칭 취소 때 인용 자리에 알린다
  -- 앵커와 판 사이 대응(07 R-1 임시안 m1). 인용 앵커는 quote_fp다. 멱등 키에는 넣지 않는다.
  anchor_symbol TEXT,              -- ast 기호 경로(예: Queue, Queue.shutdown)
  anchor_in_doc INTEGER CHECK (anchor_in_doc IN (0,1)),   -- 위치가 그 기호의 docstring 안인가
  map_method    TEXT CHECK (map_method IN ('direct','exact_quote','symbol','unmapped')),  -- 이 위치를 어떻게 찾았나
  map_from      INTEGER REFERENCES observation(obs_id),   -- 대응의 출발 관측(앞 판)
  map_rules     TEXT,
  byte_span     TEXT,              -- 고정판 원문의 바이트 범위('683-897'). 관문 재열람 때 이 범위만 받는다
  idem_key      TEXT NOT NULL UNIQUE,
  CHECK (outcome <> 'content' OR quote_fp IS NOT NULL OR receipt_id IS NOT NULL OR method = 'intro_only'),
  CHECK (method <> 'executed' OR receipt_id IS NOT NULL)
);
CREATE INDEX IF NOT EXISTS observation_by_edition ON observation(edition_id, position);

-- 다시 본 기록. 바뀌지 않은 재열람은 여기에만 쌓인다(152의 안정 대조 재방문, 028의 감사 표본).
CREATE TABLE IF NOT EXISTS sighting (
  obs_id  INTEGER NOT NULL REFERENCES observation(obs_id),
  seen_at TEXT NOT NULL,
  via     TEXT NOT NULL CHECK (via IN ('request','collection','channel','audit')),
  reader  TEXT,
  PRIMARY KEY (obs_id, seen_at, via)
);

-- 꼬리표: 무엇이 들어가 무엇이 나오고 누가 어디서 쓰나. 칸 x 두 높이 x 원문 언어·영어(+묻는 언어).
-- 칸: input(받는 것) output(내는 것) user_without(쓰는 쪽과 그쪽에 없는 것) keeps(지키는 것)
--     breaks_when(깨지는 조건) summary(칸을 나누지 않은 한 줄, 카탈로그 설명 등)
CREATE TABLE IF NOT EXISTS tag (
  tag_id       INTEGER PRIMARY KEY,
  obs_id       INTEGER NOT NULL REFERENCES observation(obs_id),
  slot         TEXT NOT NULL CHECK (slot IN ('input','output','user_without','keeps','breaks_when','summary')),
  height       TEXT NOT NULL CHECK (height IN ('concrete','one_up')),
  lang         TEXT NOT NULL,
  text         TEXT NOT NULL,
  audience     TEXT,                -- 만든 사람이 밝힌 대상 사용자(원문 그대로)
  written_from TEXT NOT NULL CHECK (written_from IN ('source_quote','maker_statement','catalog_description')),
  UNIQUE (obs_id, slot, height, lang, text)
);
CREATE VIRTUAL TABLE IF NOT EXISTS tag_fts USING fts5(
  text, content='tag', content_rowid='tag_id', tokenize='porter unicode61'
);
-- 한국어 두 층 색인(07 R-5 결정, 규칙 판 t2, afledger/tokenize.py). rowid = tag_id.
-- words: 조사·어미를 하나 뗀 어절 줄기(기능 어절 포함, 감사 검색용), grams: 줄기의 음절 2-gram. 엔진이 꼬리표를 쓸 때 채운다.
CREATE VIRTUAL TABLE IF NOT EXISTS tag_fts_ko USING fts5(words, grams, tokenize='unicode61');

-- 대비: 같은 조건에서 두 관측이 어떻게 갈리는가. 조건과 값에 요청 수치가 들어가므로(07 M7c) 본문은
-- 프로젝트 장부({p}.contrast)에 두고 공용에는 두 관측과 본문 지문(HMAC)만 둔다(07 D6c).
CREATE TABLE IF NOT EXISTS contrast (
  contrast_id INTEGER PRIMARY KEY,
  left_obs    INTEGER NOT NULL REFERENCES observation(obs_id),
  right_obs   INTEGER NOT NULL REFERENCES observation(obs_id),
  body_fp     TEXT NOT NULL,
  receipt_id  INTEGER REFERENCES receipt(receipt_id),
  UNIQUE (left_obs, right_obs, body_fp)
);

-- 대체: 나중 관측이 앞 관측의 "지금" 결론을 바꾼다. 앞 관측 자체는 그대로 남는다.
CREATE TABLE IF NOT EXISTS supersession (
  old_obs        INTEGER NOT NULL REFERENCES observation(obs_id),
  new_obs        INTEGER NOT NULL REFERENCES observation(obs_id),
  effect         TEXT NOT NULL CHECK (effect IN ('invalidates','changes_value','confirms')),
  effective_from TEXT,              -- 세상에서 바뀐 시각(불명이면 NULL)
  known_from     TEXT NOT NULL,     -- 우리가 안 시각
  PRIMARY KEY (old_obs, new_obs),
  CHECK (old_obs <> new_obs)
);

-- 대체 취소: 잘못 쓴 대체(판독 오류)를 되돌린다. 대체 행은 고치지 않고 취소 행을 더한다.
-- 바른 판독은 원 관측과 내용이 같아 새 관측이 생기지 않으므로, "반대 방향의 새 관측"으로는 되돌릴 수 없다.
-- 취소된 대체의 new_obs는 철회된 판독으로 본다(재사용·인용·감시에서 뺀다).
CREATE TABLE IF NOT EXISTS supersession_cancel (
  old_obs      INTEGER NOT NULL,
  new_obs      INTEGER NOT NULL,
  cancelled_at TEXT NOT NULL,
  reason       TEXT NOT NULL,
  PRIMARY KEY (old_obs, new_obs),
  FOREIGN KEY (old_obs, new_obs) REFERENCES supersession(old_obs, new_obs)
);

-- 원문 접근 실패 연속(08 I38): 같은 실패가 SOURCE_FAIL_STREAK번 이어진 순간. 전파가 이 행으로 '원문 접근 실패'를 알린다.
CREATE TABLE IF NOT EXISTS source_failure (
  failure_id  INTEGER PRIMARY KEY,
  base_obs    INTEGER NOT NULL REFERENCES observation(obs_id),   -- 감시 계보의 기준 관측
  fail_obs    INTEGER NOT NULL REFERENCES observation(obs_id),   -- 마지막 실패 관측
  outcome     TEXT NOT NULL,
  at          TEXT NOT NULL,
  streak      INTEGER NOT NULL,
  UNIQUE (base_obs, fail_obs, at)
);
CREATE TRIGGER IF NOT EXISTS source_failure_no_update BEFORE UPDATE ON source_failure
BEGIN SELECT RAISE(ABORT, 'source_failure is append-only'); END;
CREATE TRIGGER IF NOT EXISTS source_failure_no_delete BEFORE DELETE ON source_failure
BEGIN SELECT RAISE(ABORT, 'source_failure is append-only'); END;

-- 변경 채널과 항목. 항목은 외부 ID 집합의 차분으로만 들어온다(표시일 창을 쓰지 않는다).
CREATE TABLE IF NOT EXISTS channel (
  channel_id     INTEGER PRIMARY KEY,
  supplier       TEXT NOT NULL,
  url            TEXT NOT NULL UNIQUE,
  kind           TEXT NOT NULL CHECK (kind IN ('release_notes','changelog','errata','yank_flag','revision_history','status','feed')),
  period_h       INTEGER NOT NULL DEFAULT 72,   -- 배경 시계 주기. 커서가 2배보다 늙으면 재사용 게이트가 닫힌다
  last_polled_at TEXT,                          -- 폴링을 시도한 시각(운영 지표). 커서가 아니다(08 I35)
  last_item_count INTEGER NOT NULL DEFAULT 0,
  windowed       INTEGER NOT NULL DEFAULT 0,    -- 목록이 최근 창만 주는 채널(피드 한 쪽). 결번 규칙이 적용된다
  confirmed_at   TEXT,                          -- 확인 커서: 마지막 ok 폴링 시각. 재사용 관문 조건 (1)이 본다
  cursor         TEXT,                          -- 확인 커서: 지금까지 본 외부 ID 집합의 지문(시각이 아니라 변화로 센다)
  needs_full_listing INTEGER NOT NULL DEFAULT 0 -- 겹침 구간 결번 뒤 전체 목록 1회가 필요하다(04 7절)
);
CREATE TABLE IF NOT EXISTS channel_item (
  item_id       INTEGER PRIMARY KEY,
  channel_id    INTEGER NOT NULL REFERENCES channel(channel_id),
  external_id   TEXT NOT NULL,
  first_seen_at TEXT NOT NULL,
  title         TEXT NOT NULL,
  summary       TEXT,
  locator_url   TEXT,               -- 항목이 가리키는 문서(있으면)
  edition_key   TEXT,               -- 항목이 가리키는 판(있으면)
  UNIQUE (channel_id, external_id)
);
-- 감시 키: 어떤 관측의 뒤집을 위치가 어느 채널에 닿는가. match_key가 ''이면 그 채널의 모든 항목.
-- 층은 둘이다. same_address(같은 주소의 판 이력) / supplier(공급자·제품 공지).
-- deadline은 원문이 공지한 기한이다. 기한 24시간 전과 기한에 직접 읽고, 기한이 지났다는 것만으로 무효로 하지 않는다.
CREATE TABLE IF NOT EXISTS watch (
  obs_id     INTEGER NOT NULL REFERENCES observation(obs_id),
  channel_id INTEGER NOT NULL REFERENCES channel(channel_id),
  match_key  TEXT NOT NULL DEFAULT '',
  layer      TEXT NOT NULL DEFAULT 'same_address' CHECK (layer IN ('same_address','supplier')),
  deadline   TEXT,
  PRIMARY KEY (obs_id, channel_id, match_key)
);
-- 재확인 작업. 같은 원인으로 두 번 들어와도 하나다. 같은 관측에 열린 작업이 있으면 새 원인은 그 작업에 합친다.
CREATE TABLE IF NOT EXISTS recheck_job (
  job_id      INTEGER PRIMARY KEY,
  obs_id      INTEGER NOT NULL REFERENCES observation(obs_id),
  cause       TEXT NOT NULL CHECK (cause IN ('channel','deadline','audit','request')),
  cause_ref   TEXT NOT NULL,
  enqueued_at TEXT NOT NULL,
  state       TEXT NOT NULL DEFAULT 'queued' CHECK (state IN ('queued','leased','done','failed')),
  lease_until TEXT,
  attempts    INTEGER NOT NULL DEFAULT 0,
  result_obs  INTEGER REFERENCES observation(obs_id),
  merged_causes TEXT NOT NULL DEFAULT '',   -- 열린 작업에 합쳐진 다른 원인(쉼표 구분)
  not_before  TEXT,                         -- 다시 하기(08 I41): 이 시각 전에는 작업자가 잡지 않는다
  UNIQUE (obs_id, cause, cause_ref)
);

-- 덧붙이기 전용 강제
CREATE TRIGGER IF NOT EXISTS observation_no_update BEFORE UPDATE ON observation
BEGIN SELECT RAISE(ABORT, 'observation is append-only'); END;
CREATE TRIGGER IF NOT EXISTS observation_no_delete BEFORE DELETE ON observation
BEGIN SELECT RAISE(ABORT, 'observation is append-only'); END;
-- 인용 본문은 지우기(본문 → NULL)만 허용한다. 다른 본문으로 바꾸거나 묘비를 지울 수 없다.
CREATE TRIGGER IF NOT EXISTS quote_text_erase_only BEFORE UPDATE ON quote_text
WHEN NEW.text IS NOT NULL OR OLD.text IS NULL OR NEW.quote_fp <> OLD.quote_fp
BEGIN SELECT RAISE(ABORT, 'quote_text can only be erased'); END;
CREATE TRIGGER IF NOT EXISTS quote_text_no_delete BEFORE DELETE ON quote_text
BEGIN SELECT RAISE(ABORT, 'quote_text keeps a tombstone'); END;
CREATE TRIGGER IF NOT EXISTS edition_no_update BEFORE UPDATE ON edition
BEGIN SELECT RAISE(ABORT, 'edition is append-only'); END;
CREATE TRIGGER IF NOT EXISTS receipt_no_update BEFORE UPDATE ON receipt
BEGIN SELECT RAISE(ABORT, 'receipt is append-only'); END;
CREATE TRIGGER IF NOT EXISTS supersession_no_update BEFORE UPDATE ON supersession
BEGIN SELECT RAISE(ABORT, 'supersession is append-only'); END;
CREATE TRIGGER IF NOT EXISTS supersession_no_delete BEFORE DELETE ON supersession
BEGIN SELECT RAISE(ABORT, 'supersession is append-only; add supersession_cancel'); END;
CREATE TRIGGER IF NOT EXISTS supersession_cancel_no_update BEFORE UPDATE ON supersession_cancel
BEGIN SELECT RAISE(ABORT, 'supersession_cancel is append-only'); END;
CREATE TRIGGER IF NOT EXISTS tag_ai AFTER INSERT ON tag BEGIN
  INSERT INTO tag_fts(rowid, text) VALUES (new.tag_id, new.text);
END;
CREATE TRIGGER IF NOT EXISTS tag_no_update BEFORE UPDATE ON tag
BEGIN SELECT RAISE(ABORT, 'tag is append-only; add a new tag'); END;
