-- Build 012 migration for a database created from the Build 011 schema.sql.
-- Preserves every enrolled credential and session. Drops only pending one-time challenges
-- (180-second lifetime), because SQLite cannot alter the purpose CHECK constraint in place.
ALTER TABLE credentials ADD COLUMN label TEXT NOT NULL DEFAULT 'primary' CHECK(label IN ('primary','recovery'));
ALTER TABLE credentials ADD COLUMN aaguid TEXT;
ALTER TABLE credentials ADD COLUMN last_used_at INTEGER;
ALTER TABLE credentials ADD COLUMN enrolled_by TEXT;
ALTER TABLE sessions ADD COLUMN credential_id TEXT;
DROP TABLE IF EXISTS challenges;
CREATE TABLE challenges (
 id TEXT PRIMARY KEY,
 challenge TEXT NOT NULL,
 purpose TEXT NOT NULL CHECK(purpose IN ('register','login','enroll_auth','register_secondary','remove_auth')),
 expires_at INTEGER NOT NULL,
 session_hash TEXT,
 authorized_by TEXT
);
CREATE INDEX IF NOT EXISTS challenges_expiry ON challenges(expires_at);
CREATE TABLE IF NOT EXISTS credential_events (
 seq INTEGER PRIMARY KEY AUTOINCREMENT,
 at INTEGER NOT NULL,
 event TEXT NOT NULL CHECK(event IN ('enrolled','removed')),
 credential_id TEXT NOT NULL,
 actor TEXT NOT NULL
);
