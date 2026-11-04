#!/usr/bin/env bash
# Fraud Finder 9000 local, read-only discovery and preservation.
# Git Bash / WSL / Linux. Never pushes, merges, deploys, signs or charges.
set -euo pipefail

ROOT="$(pwd)"
SELF="$ROOT/COMPUTERWISDOM-vortex-review"
if [[ ! -d "$SELF/.git" && -d "$ROOT/.git" ]]; then
  SELF="$ROOT"
  ROOT="$(dirname "$ROOT")"
fi
if [[ ! -d "$SELF/.git" ]]; then
  echo "ERROR: Run from your GitHub directory or COMPUTERWISDOM-vortex-review checkout." >&2
  exit 2
fi
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$ROOT/_cav_recovery_receipts/$STAMP"
mkdir -p "$OUT"
LOG="$OUT/session.txt"
exec > >(tee "$LOG") 2>&1

echo "CAV_RECOVERY_V1 | UTC $STAMP"
echo "workspace=$ROOT"
echo "baseline=$SELF"
echo "No GitHub/Cloudflare/Stripe writes. No automatic upload. No code from candidates executed."
echo
echo "== Baseline (review checkout) =="
git -C "$SELF" status --short || true
git -C "$SELF" rev-parse --abbrev-ref HEAD || true
git -C "$SELF" rev-parse HEAD || true
echo
echo "== Docker runtime =="
if command -v docker >/dev/null 2>&1; then
  docker inspect citizen-audit-vortex --format 'container={{.State.Status}} health={{if .State.Health}}{{.State.Health.Status}}{{else}}unknown{{end}}' 2>/dev/null || echo "Container unavailable"
else
  echo "Docker CLI unavailable"
fi
if command -v curl >/dev/null 2>&1; then
  curl --silent --show-error --output /dev/null --write-out 'local_http=%{http_code}\n' --max-time 6 http://127.0.0.1:8787/ || true
fi
echo
echo "== Source discovery (local only) =="
CANDIDATES="$OUT/candidates.txt"
: > "$CANDIDATES"
# Search only user GitHub workspace, never Docker volumes or private home folders.
while IFS= read -r -d '' manifest; do
  dir="$(dirname "$manifest")"
  case "$dir/" in
    "$SELF/"*|*"/node_modules/"*|*"/.git/"*|*"/_cav_recovery_receipts/"*) continue ;;
  esac
  if grep -Eiq 'fraud[ -]?finder|gopher[ -]?math|evidence[ -]?registry|fraudfinder9000' "$manifest" 2>/dev/null ||
     [[ "$(basename "$dir" | tr '[:upper:]' '[:lower:]')" =~ (fraud|gopher|evidence-registry) ]]; then
    printf '%s\n' "$dir" >> "$CANDIDATES"
  fi
done < <(find "$ROOT" -maxdepth 6 -type f -iname package.json -print0 2>/dev/null)
# Include directories matching the project name, including non-Node source projects.
while IFS= read -r -d '' dir; do
  case "$dir/" in
    "$SELF/"*|*"/node_modules/"*|*"/.git/"*|*"/_cav_recovery_receipts/"*) continue ;;
  esac
  printf '%s\n' "$dir" >> "$CANDIDATES"
done < <(find "$ROOT" -maxdepth 4 -type d \( -iname '*fraud*finder*' -o -iname '*gopher*math*' \) -print0 2>/dev/null)
sort -u "$CANDIDATES" -o "$CANDIDATES"
echo "Candidate directories:"
cat "$CANDIDATES"
COUNT="$(wc -l < "$CANDIDATES" | tr -d ' ')"
echo "candidate_count=$COUNT"

echo
echo "== Local preservation =="
if [[ "$COUNT" == 1 ]]; then
  SOURCE="$(head -n 1 "$CANDIDATES")"
  ARCHIVE="$OUT/fraudfinder-source-snapshot.tar.gz"
  # Local-only archive. Excludes common secret, cache, and build paths.
  tar --exclude='.git' --exclude='node_modules' --exclude='dist' --exclude='build' --exclude='coverage' --exclude='.next' --exclude='.env' --exclude='.env.*' --exclude='*.pem' --exclude='*.key' --exclude='*credentials*' --exclude='*secret*' --exclude='*.sqlite' --exclude='*.db' --exclude='*.log' --exclude='*.csv' --exclude='*.pdf' --exclude='*.zip' -czf "$ARCHIVE" -C "$(dirname "$SOURCE")" "$(basename "$SOURCE")"
  echo "snapshot=$ARCHIVE"
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$ARCHIVE" | tee "$OUT/archive.sha256"
  else
    echo "hash_status=NOT_TESTED (sha256sum unavailable)"
  fi
  echo "SOURCE_PRESERVED_LOCALLY=true"
  echo "SOURCE_VERIFIED_INDEPENDENTLY=false"
elif [[ "$COUNT" == 0 ]]; then
  echo "SOURCE_NOT_FOUND_IN_LOCAL_GITHUB_WORKSPACE"
  echo "The preview may live in a cloud workspace. Search miss is NOT proof of absence."
else
  echo "MULTIPLE_CANDIDATES_HOLD — preserving candidate paths only; no arbitrary source selected."
fi

echo
echo "== Reconciliation checkpoint =="
echo "baseline=$(git -C "$SELF" rev-parse HEAD 2>/dev/null || echo UNKNOWN)"
echo "root_role_merge=HOLD"
echo "docker_preview_same_source=NOT_ESTABLISHED"
echo "official_fixtures=NOT_RUN"
echo "verified_citizen_case_gates=0/5"
echo "CANON=false"
echo "AUTHORITY_CREATED=false"
echo "REPORT=$LOG"
