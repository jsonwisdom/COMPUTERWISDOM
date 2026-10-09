#!/usr/bin/env bash
set -euo pipefail
BASE="https://jsonwisdom.github.io/COMPUTERWISDOM/tesla-vault/"
for file in "" "health.json" "evidence-manifest.json" "government-sidecar.json"; do
  url="$BASE$file"
  code="$(curl -sSL --max-time 25 -o /dev/null -w "%{http_code}" "$url")"
  echo "HTTP $code $url"
  test "$code" = "200" || exit 1
done
echo "PASS: all public endpoints returned HTTP 200"
