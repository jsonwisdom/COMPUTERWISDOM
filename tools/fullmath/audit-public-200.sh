#!/usr/bin/env bash
set -u

BASE_URL="\${1:-https://jsonwisdom.github.io/COMPUTERWISDOM/public/fullmath/}"
REPORT_ROOT="\${2:-./_machine-sync/JASON_STORY_WORK_SYNC_20261005-210908}"
MAX_WAIT="\${MAX_WAIT_SECONDS:-600}"
POLL="\${POLL_SECONDS:-10}"

RUN="FULLMATH_PUBLIC_AUDIT_$(date -u +%Y%m%d-%H%M%S)"
OUT="$REPORT_ROOT/$RUN"
mkdir -p "$OUT"

targets=(
  "HOME|$BASE_URL"
  "MATRIX|\${BASE_URL}matrix.html"
  "PLAY|https://jsonwisdom.github.io/COMPUTERWISDOM/public-record-verification/game.html"
  "KERNEL|https://jsonwisdom.github.io/COMPUTERWISDOM/docs/replay_kernel_v0_1.md"
  "ZORA|https://jsonwisdom.github.io/COMPUTERWISDOM/public/zora/CWAAS-FLYWHEEL-001_ZORA_DROP_RECEIPT.md"
  "MACHINE|https://jsonwisdom.github.io/COMPUTERWISDOM/docs/layered-machine-speed-scale-blueprint-v0-1.md"
)

start=$(date +%s)
attempt=0
while true; do
  attempt=$((attempt+1))
  code=$(curl -L -sS -o /dev/null -w "%{http_code}" "$BASE_URL" || true)
  now=$(date +%s)
  elapsed=$((now-start))
  pct=$((elapsed*100/MAX_WAIT))
  [ "$pct" -gt 99 ] && pct=99
  bars=$((pct/2))
  printf "\rWaiting for public 200 [%-50s] %3d%% attempt=%d HTTP=%s" "$(printf '%*s' "$bars" '' | tr ' ' '#')" "$pct" "$attempt" "$code"
  [ "$code" = "200" ] && break
  [ "$elapsed" -ge "$MAX_WAIT" ] && break
  sleep "$POLL"
done
printf "\n"

printf 'id,url,status,pass\n' > "$OUT/links.csv"
json_rows=""
all=true
i=0
total=\${#targets[@]}

for item in "\${targets[@]}"; do
  i=$((i+1))
  id="\${item%%|*}"
  url="\${item#*|}"
  code=$(curl -L -sS -o /dev/null -w "%{http_code}" "$url" || true)
  pass=false
  if [ "$code" = "200" ]; then pass=true; else all=false; fi
  pct=$((i*100/total))
  bars=$((pct/2))
  printf "\rAuditing links [%-50s] %3d%% %s HTTP=%s" "$(printf '%*s' "$bars" '' | tr ' ' '#')" "$pct" "$id" "$code"
  printf '%s,"%s",%s,%s\n' "$id" "$url" "$code" "$pass" >> "$OUT/links.csv"
  [ -n "$json_rows" ] && json_rows="$json_rows,"
  json_rows="$json_rows{\"id\":\"$id\",\"url\":\"$url\",\"status\":$code,\"pass\":$pass}"
done
printf "\n"

now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
cat > "$OUT/audit.json" <<EOF
{"schema":"FULLMATH_PUBLIC_200_AUDIT_V0_1","run_at":"$now","base_url":"$BASE_URL","all_required_200":$all,"authority_created":false,"identity_join":false,"results":[$json_rows]}
EOF

cat > "$OUT/proof.html" <<EOF
<!doctype html><meta charset="utf-8"><title>FULLMATH Public Proof Audit</title>
<h1>FULLMATH Public 200 Audit</h1>
<p><b>Run:</b> $now</p>
<p><b>ALL_REQUIRED_200:</b> $all</p>
<p>See <a href="links.csv">links.csv</a> and <a href="audit.json">audit.json</a>.</p>
<p>NO SOURCE REPO WAS MODIFIED.</p>
EOF

echo "FULLMATH PUBLIC AUDIT COMPLETE"
echo "ALL_REQUIRED_200=$all"
echo "Report directory: $OUT"
echo "NO SOURCE REPO WAS MODIFIED."
