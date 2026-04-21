#!/bin/bash
set -e

echo "📡 Fetching ZTWS attestation verifier..."
REPO_RAW="https://raw.githubusercontent.com/jsonwisdom/COMPUTERWISDOM/main/attestation"
curl -sL "$REPO_RAW/verify.py" -o /tmp/verify.py
curl -sL "$REPO_RAW/measurements.json" -o /tmp/measurements.json

python3 /tmp/verify.py "$@"
