#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: $0 --case-id ID --transport ok|network_failure --redirect-count N --output-root DIR [--status CODE] [--body FILE]" >&2
  exit 64
}

case_id=""
transport=""
redirect_count=""
status=""
body=""
output_root=""

while (($#)); do
  case "$1" in
    --case-id) case_id=${2-}; shift 2 ;;
    --transport) transport=${2-}; shift 2 ;;
    --redirect-count) redirect_count=${2-}; shift 2 ;;
    --status) status=${2-}; shift 2 ;;
    --body) body=${2-}; shift 2 ;;
    --output-root) output_root=${2-}; shift 2 ;;
    *) usage ;;
  esac
done

[[ $case_id =~ ^[A-Za-z0-9._-]+$ ]] || usage
[[ $transport == "ok" || $transport == "network_failure" ]] || usage
[[ $redirect_count =~ ^[0-9]+$ ]] || usage
[[ -n $output_root ]] || usage

write_receipt() {
  local path=$1 decision=$2 route_path=$3
  mkdir -p "$(dirname "$path")"
  printf '{\n  "case_id": "%s",\n  "synthetic": true,\n  "decision": "%s",\n  "route_path": "%s",\n  "corpus_created": false,\n  "manifest_created": false,\n  "live_fetch_executed": false,\n  "authority_created": false\n}\n' \
    "$case_id" "$decision" "$route_path" > "$path"
}

if [[ $transport == "network_failure" ]]; then
  receipt="receipts/failures/network/${case_id}.json"
  write_receipt "$output_root/$receipt" "NETWORK_FAILURE" "$receipt"
  echo "ROUTE_DECISION=NETWORK_FAILURE"
  echo "ROUTE_PATH=$receipt"
  exit 0
fi

[[ $status =~ ^[0-9]{3}$ ]] || usage
[[ -n $body && -f $body ]] || usage

body_sha=$(sha256sum "$body" | awk '{print $1}')

if ((redirect_count > 0)) || [[ $status =~ ^3 ]]; then
  failure_body="receipts/failures/body/${body_sha}"
  hold_receipt="receipts/holds/redirect/${case_id}.json"
  mkdir -p "$output_root/receipts/failures/body"
  cp "$body" "$output_root/$failure_body"
  write_receipt "$output_root/$hold_receipt" "HOLD_REDIRECT_AMBIGUITY" "$failure_body"
  echo "ROUTE_DECISION=HOLD_REDIRECT_AMBIGUITY"
  echo "ROUTE_PATH=$hold_receipt"
  exit 0
fi

if [[ $status == "200" ]]; then
  corpus_path="corpus/raw/${body_sha}"
  receipt="receipts/router/${case_id}.json"
  mkdir -p "$output_root/corpus/raw"
  cp "$body" "$output_root/$corpus_path"
  write_receipt "$output_root/$receipt" "ADMIT_CORPUS" "$corpus_path"
  echo "ROUTE_DECISION=ADMIT_CORPUS"
  echo "ROUTE_PATH=$corpus_path"
  exit 0
fi

failure_body="receipts/failures/body/${body_sha}"
receipt="receipts/failures/http/${case_id}.json"
mkdir -p "$output_root/receipts/failures/body"
cp "$body" "$output_root/$failure_body"
write_receipt "$output_root/$receipt" "HTTP_FAILURE" "$failure_body"
echo "ROUTE_DECISION=HTTP_FAILURE"
echo "ROUTE_PATH=$failure_body"
