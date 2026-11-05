#!/usr/bin/env bash
# DOJ Corporate Whistleblower Awards Pilot Program: rule-source check (v2).
#
# Phases (fail-closed, no partial baseline updates):
#   fetch    fetch + validate + hash every target into a temp STAGE dir
#   receipt  build the receipt with jq and validate it
#   write    write latest receipt, a per-pass history copy, and the log line
#   promote  per target: archive old baseline, install new one, write
#            provenance naming the receipt that authorized it
#   verify   re-hash installed baselines against what was staged
# A failed target never touches its last good baseline.
#
# Budget: a global deadline (default 600s). Each fetch is hard-capped at
# min(90s, time remaining) with timeout(1), so fetching ends at the deadline,
# not after it. Targets skipped or cut off are recorded as failures (HOLD),
# not dropped. Validation and promotion add a few seconds on top.
#
# Crash path: an EXIT trap writes a fallback receipt (printf only, no jq) to
# $BASE/crash/<pass>.json naming the phase and which targets were already
# promoted. The workflow commits only that file on failure.
#
# Env: BASE_DIR, TARGETS_FILE (lines: name|pdf-or-html|url|expected phrase),
#      DEADLINE_SECONDS. Test-only hooks: TEST_CRASH_AT=<phase>,
#      TEST_CRASH_AFTER_PROMOTING=<name>, TEST_CORRUPT_PROMOTED=<name>.
set -euo pipefail

BASE="${BASE_DIR:-receipts/doj-cwa}"
CUR="$BASE/current"
ARC="$BASE/archive"
HIST="$BASE/history"
CRASH="$BASE/crash"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UA="Mozilla/5.0 (compatible; receipt-check/1.0)"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
TSF="$(date -u +%Y%m%dT%H%M%SZ)"
SUFFIX="${GITHUB_RUN_ID:-$$}"
PASS_ID="M001-${TSF}-${SUFFIX}"
ARC_TAG="${TSF}-${SUFFIX}"
START_EPOCH="$(date +%s)"
DEADLINE="${DEADLINE_SECONDS:-600}"
PHASE="init"
LAST_TARGET=""
DONE=0
STAGE="$(mktemp -d)"
: > "$STAGE/promoted.txt"

on_exit() {
  local rc=$?
  if [ "$DONE" != 1 ]; then
    local incons=false
    if [ "$PHASE" = "promote" ] || [ "$PHASE" = "verify" ]; then incons=true; fi
    mkdir -p "$CRASH" 2>/dev/null || true
    {
      printf '{\n'
      printf '  "pass_id": "%s",\n' "$PASS_ID"
      printf '  "captured_at": "%s",\n' "$TS"
      printf '  "overall": "SCRIPT_CRASHED",\n'
      printf '  "crashed_in_phase": "%s",\n' "$PHASE"
      printf '  "last_target": "%s",\n' "$LAST_TARGET"
      if [ "$incons" = true ]; then
        printf '  "in_progress_target_when_crashed": "%s",\n' "$LAST_TARGET"
      else
        printf '  "in_progress_target_when_crashed": "",\n'
      fi
      printf '  "exit_code": %s,\n' "$rc"
      printf '  "fully_promoted_before_crash": "%s",\n' "$(tr '\n' ' ' < "$STAGE/promoted.txt" 2>/dev/null | sed 's/ *$//' || true)"
      printf '  "baselines_may_be_inconsistent": %s,\n' "$incons"
      printf '  "workflow_run_id": "%s",\n' "${GITHUB_RUN_ID:-local}"
      printf '  "rule_text_compared_to_prior": false,\n'
      printf '  "reward_eligibility": "NOT_ESTABLISHED",\n'
      printf '  "submission": "NONE",\n'
      printf '  "authority_created": false,\n'
      printf '  "note": "Script did not complete. No receipt from this pass authorizes any baseline."\n'
      printf '}\n'
    } > "$CRASH/${PASS_ID}.json" 2>/dev/null || true
    echo "CRASH: fallback receipt written to $CRASH/${PASS_ID}.json (phase=$PHASE rc=$rc)" >&2
  fi
  rm -rf "$STAGE"
}
trap on_exit EXIT

phase() {
  PHASE="$1"
  if [ "${TEST_CRASH_AT:-}" = "$1" ]; then echo "TEST HOOK: crashing at phase $1" >&2; exit 98; fi
}

mkdir -p "$CUR" "$ARC" "$HIST" "$CRASH"

default_targets() {
  cat <<'EOT'
guidance_pdf|pdf|https://www.justice.gov/criminal/media/1454776/dl?inline|Corporate Whistleblower Awards Pilot Program
faq_pdf|pdf|https://www.justice.gov/criminal/media/1454771/dl?inline|Whistleblower
landing_page|html|https://www.justice.gov/criminal/criminal-division-corporate-whistleblower-awards-pilot-program|Whistleblower
faq_page|html|https://www.justice.gov/criminal/whistleblower/frequently-asked-questions|Frequently Asked Questions
submitting_info_page|html|https://www.justice.gov/criminal/whistleblower/submitting-information-doj|Whistleblower
submission_award_process_page|html|https://www.justice.gov/criminal/whistleblower/whistleblower-submission-and-award-process|Whistleblower
additional_resources_page|html|https://www.justice.gov/criminal/whistleblower/additional-resources|Whistleblower
EOT
}

if [ -n "${TARGETS_FILE:-}" ]; then
  cp "$TARGETS_FILE" "$STAGE/targets.txt"
else
  default_targets > "$STAGE/targets.txt"
fi

sha() { sha256sum "$1" | awk '{print $1}'; }
read_prev() { if [ -f "$1" ]; then cat "$1"; fi; }

# Sets VERR (empty = valid) and PAGES. Fails closed if tools are missing.
validate_pdf() {
  local f="$1"
  VERR=""; PAGES=0
  if [ "$(head -c 5 "$f")" != "%PDF-" ]; then VERR="served bytes are not a PDF (no %PDF- header)"; return 0; fi
  if ! tail -c 2048 "$f" | grep -aq '%%EOF'; then VERR="PDF looks truncated (no %%EOF in last 2KB)"; return 0; fi
  if ! command -v pdftotext >/dev/null 2>&1 || ! command -v pdfinfo >/dev/null 2>&1; then
    VERR="poppler tools unavailable; cannot validate PDF"; return 0
  fi
  if ! pdfinfo "$f" > "$STAGE/$NAME.pdfinfo" 2> "$STAGE/$NAME.pdfinfo.err"; then VERR="pdfinfo failed"; return 0; fi
  PAGES="$(awk '/^Pages:/{print $2}' "$STAGE/$NAME.pdfinfo")"
  if ! [[ "$PAGES" =~ ^[0-9]+$ ]] || [ "$PAGES" -lt 1 ]; then VERR="pdfinfo reported no pages"; PAGES=0; return 0; fi
  if ! pdftotext -layout "$f" "$STAGE/$NAME.main.txt" 2> "$STAGE/$NAME.pdftotext.err"; then VERR="pdftotext failed"; return 0; fi
  if grep -qi 'error' "$STAGE/$NAME.pdftotext.err"; then
    VERR="pdftotext reported errors: $(head -c 160 "$STAGE/$NAME.pdftotext.err" | tr '\n' ' ')"; return 0
  fi
  local ff chars
  ff="$(tr -cd '\f' < "$STAGE/$NAME.main.txt" | wc -c | tr -d ' ')"
  if [ "$ff" -ne "$PAGES" ]; then VERR="text extraction covered $ff of $PAGES pages"; return 0; fi
  chars="$(wc -c < "$STAGE/$NAME.main.txt" | tr -d ' ')"
  if [ "$chars" -lt 200 ]; then VERR="too little extracted PDF text ($chars bytes)"; return 0; fi
  if [ -n "$EXPECT" ] && ! grep -qiF -- "$EXPECT" "$STAGE/$NAME.main.txt"; then
    VERR="expected phrase not found in PDF text: $EXPECT"; return 0
  fi
  return 0
}

: > "$STAGE/results.jsonl"
: > "$STAGE/promote.txt"

# ---------- fetch ----------
phase fetch
while IFS='|' read -r NAME KIND URL EXPECT; do
  [ -z "${NAME:-}" ] && continue
  LAST_TARGET="$NAME"
  EXPECT="${EXPECT:-}"
  RAW="$STAGE/$NAME.raw"
  STATUS=""; ERR=""; WHOLE=""; MAIN=""; REV=""; CHARS=0; PAGES=0
  PAGEDIFF=false; PM=""; PW=""; ACTION="none"; HTTP="000"; rc=0; VERR=""

  ELAPSED=$(( $(date +%s) - START_EPOCH ))
  if [ "$ELAPSED" -ge "$DEADLINE" ]; then
    STATUS="fetch_failed"; ERR="skipped: ${DEADLINE}s time budget reached before this target"
  else
    # Hard cap for this target = min(90s, time left in the global budget).
    # timeout(1) kills curl and its retries together, so the run cannot
    # overshoot the deadline by an in-flight request.
    CAP=90
    LEFT=$(( DEADLINE - ELAPSED ))
    if [ "$LEFT" -lt "$CAP" ]; then CAP="$LEFT"; fi
    HTTP="$(timeout "$CAP" curl -fsSL --connect-timeout 10 --max-time 30 --retry 2 --retry-delay 3 \
              --retry-max-time 60 --retry-all-errors -A "$UA" -o "$RAW" -w '%{http_code}' \
              "$URL" 2>"$STAGE/$NAME.err")" || rc=$?
    HTTP="${HTTP:-000}"
    FETCH_OK=true
    if [ "$rc" -ne 0 ] || [ ! -s "$RAW" ]; then
      FETCH_OK=false
    elif [ "$HTTP" != "200" ] && [[ "$URL" != file://* ]]; then
      FETCH_OK=false
    fi

    if [ "$FETCH_OK" != true ]; then
      STATUS="fetch_failed"; ERR="curl rc=$rc http=$HTTP"
      if [ "$rc" -eq 124 ]; then ERR="timed out at the ${CAP}s per-target cap (remaining budget)"; fi
    else
      WHOLE="$(sha "$RAW")"
      if [ "$KIND" = "pdf" ]; then
        validate_pdf "$RAW"
        if [ -n "$VERR" ]; then
          STATUS="validation_failed"; ERR="$VERR"
        else
          MAIN="$WHOLE"
          REV="$(pdftotext -f 1 -l 1 "$RAW" - 2>/dev/null \
                  | grep -E 'Issued:|Revised:' | tr '\n' ' ' | sed 's/[[:space:]]*$//' || true)"
          if [ -z "$REV" ]; then REV="NOT_FOUND"; fi
        fi
      else
        EX="$(python3 "$HERE/doj_cwa_extract.py" "$RAW" "$STAGE/$NAME.main.txt" "$EXPECT" || true)"
        if [ -n "$EX" ] && [ "$(jq -r '.ok' <<<"$EX" 2>/dev/null || echo false)" = "true" ]; then
          MAIN="$(jq -r '.sha256' <<<"$EX")"
          CHARS="$(jq -r '.chars' <<<"$EX")"
        else
          STATUS="extract_failed"
          ERR="extractor produced no output"
          if [ -n "$EX" ]; then
            ERR="$(jq -r '.error // "unknown extractor error"' <<<"$EX" 2>/dev/null || echo "unparseable extractor output")"
          fi
        fi
      fi
    fi
  fi

  if [ -z "$STATUS" ]; then
    PM="$(read_prev "$CUR/$NAME.main.sha256")"
    PW="$(read_prev "$CUR/$NAME.sha256")"
    if [ -z "$PM" ]; then
      STATUS="first_observation"; ACTION="first"
    elif [ "$MAIN" = "$PM" ]; then
      STATUS="unchanged"
    else
      STATUS="bytes_changed"; ACTION="replaced"
    fi
    if [ -n "$PW" ] && [ "$WHOLE" != "$PW" ]; then
      PAGEDIFF=true
      if [ "$ACTION" = "none" ]; then ACTION="refreshed"; fi
    fi
    printf '%s\n' "$WHOLE" > "$STAGE/$NAME.whole"
    printf '%s\n' "$MAIN"  > "$STAGE/$NAME.main"
    if [ "$ACTION" != "none" ]; then printf '%s|%s|%s\n' "$NAME" "$KIND" "$ACTION" >> "$STAGE/promote.txt"; fi
  fi

  jq -nc --arg name "$NAME" --arg kind "$KIND" --arg url "$URL" --arg http "$HTTP" \
        --arg status "$STATUS" --arg err "$ERR" --arg whole "$WHOLE" --arg main "$MAIN" \
        --arg prev "$PM" --arg rev "$REV" --arg action "$ACTION" --arg expect "$EXPECT" \
        --argjson chars "$CHARS" --argjson pages "$PAGES" --argjson pagediff "$PAGEDIFF" '
    {name:$name, kind:$kind, url:$url, http_code:$http, status:$status,
     error:(if $err=="" then null else $err end),
     expected_phrase:(if $expect=="" then null else $expect end),
     whole_sha256:(if $whole=="" then null else $whole end),
     main_sha256:(if $main=="" then null else $main end),
     previous_main_sha256:(if $prev=="" then null else $prev end),
     page_bytes_differ:$pagediff,
     promotion_planned:$action,
     revision_line:(if $rev=="" then null else $rev end),
     pdf_pages:(if $pages==0 then null else $pages end),
     extracted_chars:(if $chars==0 then null else $chars end)}' >> "$STAGE/results.jsonl"
done < "$STAGE/targets.txt"

# ---------- receipt ----------
phase receipt
OVERALL="$(jq -rs '
  if any(.[]; .status|IN("fetch_failed","validation_failed","extract_failed")) then "INCOMPLETE_HOLD"
  elif any(.[]; .status=="bytes_changed") then "bytes_changed"
  elif any(.[]; .status=="first_observation") then "first_observation"
  else "unchanged" end' "$STAGE/results.jsonl")"

jq -s --arg pass "$PASS_ID" --arg ts "$TS" --arg overall "$OVERALL" \
      --arg run "${GITHUB_RUN_ID:-local}" --arg commit "${GITHUB_SHA:-local}" '{
  pass_id: $pass,
  captured_at: $ts,
  overall: $overall,
  workflow_run_id: $run,
  workflow_commit: $commit,
  changed_targets: [.[] | select(.status=="bytes_changed") | .name],
  failed_targets:  [.[] | select(.status|IN("fetch_failed","validation_failed","extract_failed")) | .name],
  targets: .,
  rule_text_compared_to_prior: false,
  reward_eligibility: "NOT_ESTABLISHED",
  submission: "NONE",
  authority_created: false,
  note: "A hash shows which bytes were retrieved. It does not show the rules are correct or that anyone is eligible."
}' "$STAGE/results.jsonl" > "$STAGE/receipt.json"
jq -e . "$STAGE/receipt.json" >/dev/null

# ---------- write ----------
phase write
cp "$STAGE/receipt.json" "$BASE/latest_receipt.json"
cp "$STAGE/receipt.json" "$HIST/$PASS_ID.json"
RECEIPT_SHA="$(sha "$HIST/$PASS_ID.json")"
LINE="$(jq -r '[.targets[] | "\(.name)=\(.status)"] | join(" ")' "$STAGE/receipt.json")"
printf '%s %s %s %s\n' "$TS" "$PASS_ID" "$OVERALL" "$LINE" >> "$BASE/check_log.txt"

# ---------- promote ----------
phase promote
while IFS='|' read -r NAME KIND ACTION; do
  [ -z "${NAME:-}" ] && continue
  LAST_TARGET="$NAME"
  EXT="html"; if [ "$KIND" = "pdf" ]; then EXT="pdf"; fi
  CUR_RAW="$CUR/$NAME.$EXT"
  ARCHIVED_AS=""
  if [ -f "$CUR_RAW" ]; then
    ARCHIVED_AS="$NAME.$ARC_TAG.$EXT"
    if [ -e "$ARC/$ARCHIVED_AS" ]; then echo "archive name collision: $ARCHIVED_AS" >&2; exit 1; fi
    cp "$CUR_RAW" "$ARC/$ARCHIVED_AS"
    for SUF in sha256 main.sha256 main.txt provenance.json; do
      if [ -f "$CUR/$NAME.$SUF" ]; then cp "$CUR/$NAME.$SUF" "$ARC/$NAME.$ARC_TAG.$SUF"; fi
    done
  fi
  cp "$STAGE/$NAME.raw"   "$CUR_RAW"
  cp "$STAGE/$NAME.whole" "$CUR/$NAME.sha256"
  cp "$STAGE/$NAME.main"  "$CUR/$NAME.main.sha256"
  if [ -f "$STAGE/$NAME.main.txt" ]; then cp "$STAGE/$NAME.main.txt" "$CUR/$NAME.main.txt"; fi

  jq -n --arg name "$NAME" --arg pass "$PASS_ID" --arg rsha "$RECEIPT_SHA" \
        --arg rfile "history/$PASS_ID.json" --arg ts "$TS" --arg action "$ACTION" \
        --arg whole "$(cat "$STAGE/$NAME.whole")" --arg main "$(cat "$STAGE/$NAME.main")" \
        --arg arch "$ARCHIVED_AS" '{
    target:$name, authorized_by_pass:$pass, authorizing_receipt_file:$rfile,
    authorizing_receipt_sha256:$rsha, promoted_at:$ts, action:$action,
    whole_sha256:$whole, main_sha256:$main,
    previous_baseline_archived_as:(if $arch=="" then null else $arch end)}' > "$CUR/$NAME.provenance.json"
  jq -c . "$CUR/$NAME.provenance.json" >> "$BASE/promotion_log.jsonl"

  if [ "${TEST_CORRUPT_PROMOTED:-}" = "$NAME" ]; then echo "x" >> "$CUR_RAW"; fi
  if [ "${TEST_CRASH_AFTER_PROMOTING:-}" = "$NAME" ]; then echo "TEST HOOK: crash after promoting $NAME" >&2; exit 97; fi
  echo "$NAME" >> "$STAGE/promoted.txt"
done < "$STAGE/promote.txt"

# ---------- verify ----------
phase verify
while IFS='|' read -r NAME KIND ACTION; do
  [ -z "${NAME:-}" ] && continue
  LAST_TARGET="$NAME"
  EXT="html"; if [ "$KIND" = "pdf" ]; then EXT="pdf"; fi
  if [ "$(sha "$CUR/$NAME.$EXT")" != "$(cat "$STAGE/$NAME.whole")" ] \
     || [ "$(cat "$CUR/$NAME.main.sha256")" != "$(cat "$STAGE/$NAME.main")" ]; then
    echo "VERIFY FAILED: installed baseline for $NAME does not match staged hashes" >&2
    exit 1
  fi
done < "$STAGE/promote.txt"

DONE=1
echo "Receipt $PASS_ID written. Overall: $OVERALL"
if [ -n "${GITHUB_OUTPUT:-}" ]; then echo "overall=$OVERALL" >> "$GITHUB_OUTPUT"; fi
if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then
  { echo "### DOJ CWA rule check: $OVERALL"; echo; echo "$LINE" | tr ' ' '\n' | sed 's/^/- /'; } >> "$GITHUB_STEP_SUMMARY"
fi
