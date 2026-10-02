#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
router="$script_dir/route-http-observation.sh"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

# Deliberately use identical bytes for two different HTTP statuses. If custody
# and receipts preserve the distinction, reverse inspection should recover it.
printf 'synthetic shared failure bytes\n' > "$work/shared.body"
root="$work/replay"
mkdir -p "$root"

bash "$router" --case-id alpha --output-root "$root" --transport ok --redirect-count 0 --status 403 --body "$work/shared.body" > "$work/403.out"
bash "$router" --case-id beta  --output-root "$root" --transport ok --redirect-count 0 --status 404 --body "$work/shared.body" > "$work/404.out"

body_sha=$(sha256sum "$work/shared.body" | awk '{print $1}')
body_path="$root/receipts/failures/body/$body_sha"
r403="$root/receipts/failures/http/alpha.json"
r404="$root/receipts/failures/http/beta.json"

test -f "$body_path"
cmp "$work/shared.body" "$body_path"
test -f "$r403"
test -f "$r404"

grep -Fq '"decision": "HTTP_FAILURE"' "$r403"
grep -Fq '"decision": "HTTP_FAILURE"' "$r404"
grep -Fq "\"route_path\": \"receipts/failures/body/$body_sha\"" "$r403"
grep -Fq "\"route_path\": \"receipts/failures/body/$body_sha\"" "$r404"

# The current receipt schema does not preserve the upstream status. Therefore
# reverse audit may recover the failure class, but not 403 versus 404. Case IDs
# are labels and must not be promoted into evidence of status identity.
if grep -Eq '"(http_)?status"[[:space:]]*:' "$r403" "$r404"; then
  echo "HTTP_STATUS_FIELD_UNEXPECTED=TRUE" >&2
  exit 1
fi

[[ ! -d "$root/corpus/raw" ]] || ! find "$root/corpus/raw" -type f -print -quit | grep -q .
[[ ! -e "$root/manifest.jsonl" && ! -e "$root/manifest/manifest.jsonl" ]]

echo "SSA_REVERSE_AUDIT=PASS"
echo "FAILURE_CLASS_RECOVERABLE=TRUE"
echo "HTTP_STATUS_403_VS_404_RECOVERABLE=FALSE"
echo "LABEL_NOT_EVIDENCE=TRUE"
echo "CRISSCROSS_APPLESAUCE=HOLD_EXACT_STATUS_IDENTITY"
echo "LIVE_SSA_FETCH_EXECUTED=FALSE"
echo "MACOS_OBSERVATION_CREATED=FALSE"
echo "MANIFEST_CREATED=FALSE"
echo "AUTHORITY_CREATED=FALSE"
