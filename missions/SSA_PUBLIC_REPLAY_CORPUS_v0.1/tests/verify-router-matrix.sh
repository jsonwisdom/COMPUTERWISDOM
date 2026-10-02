#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
router="$script_dir/route-http-observation.sh"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

printf 'synthetic success bytes\n' > "$work/200.body"
printf 'synthetic forbidden bytes\n' > "$work/403.body"
printf 'synthetic missing bytes\n' > "$work/404.body"
printf 'synthetic redirect bytes\n' > "$work/302.body"
printf 'synthetic unlisted success bytes\n' > "$work/204.body"

run_case() {
  local id=$1
  shift
  mkdir -p "$work/$id"
  bash "$router" --case-id "$id" --output-root "$work/$id" "$@" > "$work/$id.output"
}

assert_no_corpus() {
  local root=$1
  [[ ! -d "$root/corpus/raw" ]] || ! find "$root/corpus/raw" -type f -print -quit | grep -q .
}

assert_no_manifest() {
  local root=$1
  [[ ! -e "$root/manifest.jsonl" && ! -e "$root/manifest/manifest.jsonl" ]]
}

run_case http_200 --transport ok --redirect-count 0 --status 200 --body "$work/200.body"
success_sha=$(sha256sum "$work/200.body" | awk '{print $1}')
cmp "$work/200.body" "$work/http_200/corpus/raw/$success_sha"
grep -Fxq 'ROUTE_DECISION=ADMIT_CORPUS' "$work/http_200.output"
assert_no_manifest "$work/http_200"

for status in 403 404; do
  id="http_$status"
  body="$work/$status.body"
  run_case "$id" --transport ok --redirect-count 0 --status "$status" --body "$body"
  body_sha=$(sha256sum "$body" | awk '{print $1}')
  cmp "$body" "$work/$id/receipts/failures/body/$body_sha"
  grep -Fxq 'ROUTE_DECISION=HTTP_FAILURE' "$work/$id.output"
  assert_no_corpus "$work/$id"
  assert_no_manifest "$work/$id"
done

run_case redirect_302 --transport ok --redirect-count 0 --status 302 --body "$work/302.body"
grep -Fxq 'ROUTE_DECISION=HOLD_REDIRECT_AMBIGUITY' "$work/redirect_302.output"
test -f "$work/redirect_302/receipts/holds/redirect/redirect_302.json"
assert_no_corpus "$work/redirect_302"
assert_no_manifest "$work/redirect_302"

run_case redirected_200 --transport ok --redirect-count 1 --status 200 --body "$work/200.body"
grep -Fxq 'ROUTE_DECISION=HOLD_REDIRECT_AMBIGUITY' "$work/redirected_200.output"
test -f "$work/redirected_200/receipts/holds/redirect/redirected_200.json"
assert_no_corpus "$work/redirected_200"
assert_no_manifest "$work/redirected_200"

run_case network_failure --transport network_failure --redirect-count 0
grep -Fxq 'ROUTE_DECISION=NETWORK_FAILURE' "$work/network_failure.output"
test -f "$work/network_failure/receipts/failures/network/network_failure.json"
assert_no_corpus "$work/network_failure"
assert_no_manifest "$work/network_failure"

run_case http_204 --transport ok --redirect-count 0 --status 204 --body "$work/204.body"
grep -Fxq 'ROUTE_DECISION=HTTP_FAILURE' "$work/http_204.output"
assert_no_corpus "$work/http_204"
assert_no_manifest "$work/http_204"

echo "SSA_SYNTHETIC_ROUTER_MATRIX=PASS"
echo "HTTP_200_TO_CORPUS_RAW=PASS"
echo "HTTP_403_TO_FAILURE_BODY=PASS"
echo "HTTP_404_TO_FAILURE_BODY=PASS"
echo "REDIRECT_AMBIGUITY_HOLD=PASS"
echo "NETWORK_FAILURE_RECEIPT=PASS"
echo "UNLISTED_STATUS_FAIL_CLOSED=PASS"
echo "LIVE_SSA_FETCH_EXECUTED=FALSE"
echo "MANIFEST_CREATED=FALSE"
echo "AUTHORITY_CREATED=FALSE"
