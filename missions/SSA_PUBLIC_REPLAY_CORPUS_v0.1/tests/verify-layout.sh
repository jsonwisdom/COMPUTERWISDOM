#!/usr/bin/env bash
set -euo pipefail

cd /replay

required=(
  "README.md"
  "Dockerfile"
  "contracts/directory-contract.json"
  "receipts/scaffold-declaration.json"
  "tests/route-http-observation.sh"
  "tests/verify-layout.sh"
  "tests/verify-router-matrix.sh"
  "tests/verify-reverse-audit.sh"
)

for path in "${required[@]}"; do
  if [[ ! -f "${path}" ]]; then
    echo "MISSING_REQUIRED_FILE=${path}" >&2
    exit 1
  fi
done

if find receipts -maxdepth 1 -type f ! -name "scaffold-declaration.json" -print -quit | grep -q .; then
  echo "RUNTIME_RECEIPT_INCLUDED_IN_IMAGE=PROHIBITED" >&2
  exit 1
fi

if [[ -e "manifest.jsonl" || -e "manifest/manifest.jsonl" ]]; then
  echo "PLACEHOLDER_MANIFEST=PROHIBITED" >&2
  exit 1
fi

if [[ -d "corpus/raw" ]] && find "corpus/raw" -type f -print -quit | grep -q .; then
  echo "UNADMITTED_RAW_BYTES=PRESENT" >&2
  exit 1
fi

grep -Fq '"authority_created": false' contracts/directory-contract.json
grep -Fq '"network_access_allowed": false' contracts/directory-contract.json
grep -Fq '"runtime_verified": false' receipts/scaffold-declaration.json
grep -Fq '"manifest_created": false' receipts/scaffold-declaration.json
grep -Fq '"live_fetch_executed": false' receipts/scaffold-declaration.json

echo "SSA_SCAFFOLD_LAYOUT=PASS"
echo "RUNTIME_RECEIPTS_IN_IMAGE=FALSE"
echo "CORPUS_CREATED=FALSE"
echo "MANIFEST_CREATED=FALSE"
echo "RUNTIME_FETCH_VERIFIED=FALSE"
echo "AUTHORITY_CREATED=FALSE"
echo "FILE_SHA256_BEGIN"
sha256sum "${required[@]}"
echo "FILE_SHA256_END"

tests/verify-router-matrix.sh
tests/verify-reverse-audit.sh
