-- common
CREATE TABLE links (
    url TEXT PRIMARY KEY,
    title TEXT
);
-- A
CREATE TABLE last_observation (
    url TEXT PRIMARY KEY REFERENCES links(url),
    value TEXT,
    status TEXT NOT NULL
);
-- B
CREATE TABLE observations (
    id TEXT PRIMARY KEY,
    url TEXT NOT NULL REFERENCES links(url),
    edition TEXT,
    target_key TEXT NOT NULL,
    location TEXT,                  -- JSON: caller's scope and resolved original location
    observed_at INTEGER,
    kind TEXT,
    value TEXT,                     -- JSON scalar projection, never source body
    provider_delivery_id TEXT NOT NULL UNIQUE
);
CREATE INDEX observation_scope ON observations(url, target_key, edition, observed_at);
-- C
CREATE TABLE decisions (
    id TEXT PRIMARY KEY,
    url TEXT NOT NULL REFERENCES links(url),
    project TEXT NOT NULL,
    target_key TEXT NOT NULL,
    requested_edition TEXT,
    request_selector TEXT NOT NULL,
    input_key TEXT,
    input TEXT,
    preservation TEXT,
    delivered_at INTEGER NOT NULL,
    observation_id TEXT REFERENCES observations(id),
    outcome TEXT NOT NULL,
    delivered_value TEXT,
    reason TEXT NOT NULL,
    predecessor_id TEXT REFERENCES decisions(id)
);
CREATE INDEX decision_scope ON decisions(url, project, target_key, requested_edition, input_key);
