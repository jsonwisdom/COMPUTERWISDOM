-- Private D1 database. Never expose via GitHub Pages.
-- Build 012: fresh-install schema. Existing databases apply migrations/0002_build012_dual_key.sql instead.
CREATE TABLE IF NOT EXISTS credentials (
 id TEXT PRIMARY KEY,
 public_key BLOB NOT NULL,
 counter INTEGER NOT NULL DEFAULT 0,
 transports TEXT NOT NULL DEFAULT '[]',
 created_at INTEGER NOT NULL,
 label TEXT NOT NULL DEFAULT 'primary' CHECK(label IN ('primary','recovery')),
 aaguid TEXT,
 last_used_at INTEGER,
 enrolled_by TEXT
);
CREATE TABLE IF NOT EXISTS challenges (
 id TEXT PRIMARY KEY,
 challenge TEXT NOT NULL,
 purpose TEXT NOT NULL CHECK(purpose IN ('register','login','enroll_auth','register_secondary','remove_auth')),
 expires_at INTEGER NOT NULL,
 session_hash TEXT,
 authorized_by TEXT
);
CREATE TABLE IF NOT EXISTS sessions (
 token_hash TEXT PRIMARY KEY,
 expires_at INTEGER NOT NULL,
 credential_id TEXT
);
CREATE TABLE IF NOT EXISTS credential_events (
 seq INTEGER PRIMARY KEY AUTOINCREMENT,
 at INTEGER NOT NULL,
 event TEXT NOT NULL CHECK(event IN ('enrolled','removed')),
 credential_id TEXT NOT NULL,
 actor TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS challenges_expiry ON challenges(expires_at);
CREATE INDEX IF NOT EXISTS sessions_expiry ON sessions(expires_at);
