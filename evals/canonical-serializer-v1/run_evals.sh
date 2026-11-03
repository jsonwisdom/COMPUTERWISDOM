#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/../.."
python3 evals/canonical-serializer-v1/compare.py
