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
  first_seen_via TEXT NOT NULL CHECK (first_seen_via IN ('request','collection','channel','operator'))
);

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

-- 실행 영수증: 정확한 런타임, 프로그램 지문, 입력, 출력.
CREATE TABLE IF NOT EXISTS receipt (
  receipt_id     INTEGER PRIMARY KEY,
  runtime        TEXT NOT NULL,
  program_sha256 TEXT NOT NULL,
  input_json     TEXT NOT NULL,
  output_json    TEXT NOT NULL,
  ran_at         TEXT NOT NULL,
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
  quote         TEXT,              -- 원문 언어의 짧은 인용
  quote_lang    TEXT,
  quote_fp      TEXT,              -- 공백을 접은 인용의 sha256. 판이 달라도 같은 문장인지 본다
  statement     TEXT NOT NULL,     -- 원문 쪽에서 쓴 한 줄. 요청 문장을 쓰지 않는다
  evidence_ref  TEXT,              -- 인용이 원문 그대로가 아니면 판독문의 출처(연구 원장 행 등)
  flip_position TEXT,              -- 이 결론이 기대는 문장·줄·플래그
  receipt_id    INTEGER REFERENCES receipt(receipt_id),
  idem_key      TEXT NOT NULL UNIQUE,
  CHECK (outcome <> 'content' OR quote IS NOT NULL OR receipt_id IS NOT NULL OR method = 'intro_only'),
  CHECK (method <> 'executed' OR receipt_id IS NOT NULL)
);
CREATE INDEX IF NOT EXISTS observation_by_edition ON observation(edition_id, position);

-- 다시 본 기록. 바뀌지 않은 재열람은 여기에만 쌓인다(152의 안정 대조 재방문, 028의 감사 표본).
CREATE TABLE IF NOT EXISTS sighting (
  obs_id  INTEGER NOT NULL REFERENCES observation(obs_id),
  seen_at TEXT NOT NULL,
  via     TEXT NOT NULL CHECK (via IN ('request','collection','channel','audit')),
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

-- 대비: 같은 조건에서 두 관측이 어떻게 갈리는가. 원문에 대한 사실이라 공용이다.
CREATE TABLE IF NOT EXISTS contrast (
  contrast_id INTEGER PRIMARY KEY,
  left_obs    INTEGER NOT NULL REFERENCES observation(obs_id),
  right_obs   INTEGER NOT NULL REFERENCES observation(obs_id),
  condition   TEXT NOT NULL,
  left_value  TEXT NOT NULL,
  right_value TEXT NOT NULL,
  receipt_id  INTEGER REFERENCES receipt(receipt_id),
  UNIQUE (left_obs, right_obs, condition)
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

-- 변경 채널과 항목. 항목은 외부 ID 집합의 차분으로만 들어온다(표시일 창을 쓰지 않는다).
CREATE TABLE IF NOT EXISTS channel (
  channel_id     INTEGER PRIMARY KEY,
  supplier       TEXT NOT NULL,
  url            TEXT NOT NULL UNIQUE,
  kind           TEXT NOT NULL CHECK (kind IN ('release_notes','changelog','errata','yank_flag','revision_history','status','feed')),
  period_h       INTEGER NOT NULL DEFAULT 72,   -- 배경 시계 주기. 커서가 2배보다 늙으면 재사용 게이트가 닫힌다
  last_polled_at TEXT,
  last_item_count INTEGER NOT NULL DEFAULT 0
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
  UNIQUE (obs_id, cause, cause_ref)
);

-- 덧붙이기 전용 강제
CREATE TRIGGER IF NOT EXISTS observation_no_update BEFORE UPDATE ON observation
BEGIN SELECT RAISE(ABORT, 'observation is append-only'); END;
CREATE TRIGGER IF NOT EXISTS observation_no_delete BEFORE DELETE ON observation
BEGIN SELECT RAISE(ABORT, 'observation is append-only'); END;
CREATE TRIGGER IF NOT EXISTS edition_no_update BEFORE UPDATE ON edition
BEGIN SELECT RAISE(ABORT, 'edition is append-only'); END;
CREATE TRIGGER IF NOT EXISTS receipt_no_update BEFORE UPDATE ON receipt
BEGIN SELECT RAISE(ABORT, 'receipt is append-only'); END;
CREATE TRIGGER IF NOT EXISTS supersession_no_update BEFORE UPDATE ON supersession
BEGIN SELECT RAISE(ABORT, 'supersession is append-only'); END;
CREATE TRIGGER IF NOT EXISTS tag_ai AFTER INSERT ON tag BEGIN
  INSERT INTO tag_fts(rowid, text) VALUES (new.tag_id, new.text);
END;
CREATE TRIGGER IF NOT EXISTS tag_no_update BEFORE UPDATE ON tag
BEGIN SELECT RAISE(ABORT, 'tag is append-only; add a new tag'); END;
