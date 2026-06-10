#!/usr/bin/env bash
set -euo pipefail
find . -type f | grep -Ei 'meme|goblin|clown|court' | sort > court_artifacts.txt
while read -r f; do sha256sum "$f"; done < court_artifacts.txt > court_artifact_hashes.txt
cat court_artifact_hashes.txt
