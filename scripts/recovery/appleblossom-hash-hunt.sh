#!/usr/bin/env bash
# Apple Blossom v2 — read-only history + worktree + digest hunt.
# Run with Git Bash from the parent GitHub directory.
# Optional DEEP_HASH=1 hashes ALL reachable Git blobs (slow, potentially hours).
set -euo pipefail
ROOT="${1:-$PWD}"
ROOT="$(cd "$ROOT" && pwd)"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$ROOT/_cav_recovery_receipts/appleblossom_$STAMP"
mkdir -p "$OUT"
INDEX="$OUT/matches.tsv"
LOG="$OUT/run.log"
printf 'source\trepository\tlocator\tsha256\tbytes\ttarget\n' > "$INDEX"
exec > >(tee "$LOG") 2>&1
OLD_STATE="0aa3d075ba6d4e200211474c9b280258aacc66058684db71cff57c5206cc6427"
LIVE_STATE="d2a77b7decc7c7ef5a9fc23968a1c1fe203948f998a25949cdedf4bcd611ba24"
# Validator target is a partial prefix: never assert equality from prefix alone.
OLD_VALIDATOR_PREFIX="e0a623d0"
LIVE_VALIDATOR_PREFIX="d771785d"
sha() { sha256sum | awk '{print tolower($1)}'; }
classify() {
  case "$1" in
    "$OLD_STATE") echo "MATCH_ORIGINAL_STATE" ;;
    "$LIVE_STATE") echo "MATCH_LIVE_STATE" ;;
    "$OLD_VALIDATOR_PREFIX"*) echo "POSSIBLE_ORIGINAL_VALIDATOR_PREFIX_ONLY" ;;
    "$LIVE_VALIDATOR_PREFIX"*) echo "POSSIBLE_LIVE_VALIDATOR_PREFIX_ONLY" ;;
    *) echo "RELATED_CANDIDATE_NOT_TARGET" ;;
  esac
}
record_file() {
  local f="$1" repo="$2" digest count mark
  digest="$(sha256sum "$f" | awk '{print tolower($1)}')"
  count="$(wc -c < "$f" | tr -d ' ')"
  mark="$(classify "$digest")"
  printf 'worktree\t%s\t%s\t%s\t%s\t%s\n' "$repo" "$f" "$digest" "$count" "$mark" >> "$INDEX"
  echo "WORKTREE $mark $f ($count bytes)"
}
record_blob() {
  local repo="$1" oid="$2" label="$3" digest count mark
  digest="$(git -C "$repo" cat-file blob "$oid" | sha)"
  count="$(git -C "$repo" cat-file -s "$oid")"
  mark="$(classify "$digest")"
  printf 'reachable_blob\t%s\t%s :: %s\t%s\t%s\t%s\n' "$repo" "$oid" "$label" "$digest" "$count" "$mark" >> "$INDEX"
  if [[ "$mark" != "RELATED_CANDIDATE_NOT_TARGET" ]]; then echo "HIT $mark $repo $oid $label"; fi
}
echo "APPLEBLOSSOM_READ_ONLY_V2 UTC=$STAMP"
echo "ROOT=$ROOT DEEP_HASH=${DEEP_HASH:-0}"
echo "No checkout/reset/fetch/push/validator run. Existing receipts untouched."
repc=0; filec=0; blobc=0
for repo in "$ROOT"/*; do
  [[ -d "$repo" ]] || continue
  [[ -e "$repo/.git" ]] || continue
  repc=$((repc+1))
  echo "REPO $(basename "$repo")"
  # Filename discovery in working trees, including untracked/ignored matches.
  while IFS= read -r -d '' f; do
    [[ -f "$f" ]] || continue
    case "$f" in */.git/*|*/node_modules/*|*/.next/*|*/dist/*|*/build/*|*/_cav_recovery_receipts/*) continue;; esac
    filec=$((filec+1))
    record_file "$f" "$repo"
  done < <(find "$repo" -maxdepth 12 -type f \( -iname '*appleblossom*' -o -iname '*validator_replay*' -o -path '*/surfaces/appleblossom/state.json' -o -iname 'RECEIPT_INDEX.txt' \) -print0 2>/dev/null)
  # Enumerate reachable Git objects irrespective of original relative path.
  # Map named candidates; blob names from rev-list are historical hints, not unique identities.
  mapfile -t objs < <(git -C "$repo" rev-list --objects --all 2>/dev/null | grep -Ei 'apple.?blossom|VALIDATOR_REPLAY|RECEIPT_INDEX' || true)
  for item in "${objs[@]}"; do
    oid="${item%% *}"
    label="${item#* }"
    [[ "$label" == "$item" ]] && continue
    [[ "$(git -C "$repo" cat-file -t "$oid" 2>/dev/null || true)" == "blob" ]] || continue
    blobc=$((blobc+1))
    record_blob "$repo" "$oid" "$label"
  done
  if [[ "${DEEP_HASH:-0}" == "1" ]]; then
    echo "DEEP_HASH: scanning all reachable blobs in $(basename "$repo"); can be slow"
    while read -r oid; do
      [[ "$(git -C "$repo" cat-file -t "$oid" 2>/dev/null || true)" == "blob" ]] || continue
      size="$(git -C "$repo" cat-file -s "$oid")"
      # indexed state is 3486 bytes; validator receipt size unknown.
      # deep mode checks <=1 MB to avoid huge media objects.
      [[ "$size" -le 1048576 ]] || continue
      digest="$(git -C "$repo" cat-file blob "$oid" | sha)"
      if [[ "$digest" == "$OLD_STATE" || "$digest" == "$LIVE_STATE" || "$digest" == "$OLD_VALIDATOR_PREFIX"* || "$digest" == "$LIVE_VALIDATOR_PREFIX"* ]]; then
        mark="$(classify "$digest")"
        printf 'deep_blob\t%s\t%s\t%s\t%s\t%s\n' "$repo" "$oid" "$digest" "$size" "$mark" >> "$INDEX"
        echo "DEEP HIT $mark $(basename "$repo") $oid"
      fi
    done < <(git -C "$repo" rev-list --objects --all 2>/dev/null | awk '{print $1}' | sort -u)
  fi
done
echo "repos_scanned=$repc worktree_candidates=$filec path_agnostic_named_blobs=$blobc"
echo "independent_recovery=NOT_ESTABLISHED_UNLESS_EXACT_DIGEST_MATCH"
echo "original_validator_digest=PREFIX_ONLY_NEEDS_FULL_HASH_FROM_RECEIPT"
echo "CANON=false AUTHORITY_CREATED=false"
echo "INDEX=$INDEX"
echo "LOG=$LOG"
