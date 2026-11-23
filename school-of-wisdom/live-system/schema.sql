-- Existing attempts table is retained unchanged; do not drop historical rows.
CREATE TABLE IF NOT EXISTS attempts(principal TEXT NOT NULL, idem_key TEXT NOT NULL, request TEXT NOT NULL, receipt_id TEXT NOT NULL UNIQUE, receipt TEXT NOT NULL, PRIMARY KEY(principal,idem_key));
CREATE TABLE IF NOT EXISTS catalog_events(id TEXT PRIMARY KEY, sku TEXT NOT NULL, event_json TEXT NOT NULL, event_sha256 TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS audit_runs(id TEXT PRIMARY KEY, finished_at TEXT NOT NULL, cadence TEXT NOT NULL, checks_json TEXT NOT NULL, delta TEXT NOT NULL, receipt_sha256 TEXT NOT NULL, trigger TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS audit_time ON audit_runs(finished_at);
