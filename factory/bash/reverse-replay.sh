#!/usr/bin/env bash
set -u

github_root="${1:-}"
if [[ -z "$github_root" || ! -d "$github_root" ]]; then
  printf '%s\n' 'REVERSE_REPLAY=HOLD_GITHUB_ROOT_MISSING'
  exit 2
fi

overall=0
for repo in COMPUTERWISDOM GPKMONSTER JOY; do
  repo_path="$github_root/$repo"
  if [[ ! -d "$repo_path/.git" ]]; then
    printf 'REPO=%s STATE=HOLD_CHECKOUT_MISSING\n' "$repo"
    overall=1
    continue
  fi
  branch="$(git -C "$repo_path" branch --show-current 2>/dev/null || true)"
  commit="$(git -C "$repo_path" rev-parse HEAD 2>/dev/null || true)"
  dirty="$(git -C "$repo_path" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
  printf 'REPO=%s BRANCH=%s COMMIT=%s DIRTY=%s STATE=OBSERVED\n' "$repo" "$branch" "$commit" "$dirty"
done

printf '%s\n' 'AUTHORITY_CREATED=false' 'EXTERNAL_WRITE=false' 'MERGE=false' 'PUBLICATION=false'
exit "$overall"
