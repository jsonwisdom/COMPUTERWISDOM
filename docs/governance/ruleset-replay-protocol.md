# Ruleset Replay Protocol - PR #322

## Status

- Repo: jsonwisdom/COMPUTERWISDOM
- Source PR: #322
- Title: Fix verify path-filter deadlock
- Final squash merge SHA: 9a8fb144e1ae2805b08b5b551c52df7bf0e797d4
- Merged at: 2026-06-12T23:06:58Z
- Authority: false
- No Fake Green: true

## Root Cause

PR #322 fixed a GitHub required-check deadlock. The verify check was required, but verify.yml could be skipped by path filtering. GitHub then waited forever for verify to report.

## Replay Commands

gh pr view <PR_NUMBER> --json statusCheckRollup,mergeStateStatus,headRefOid,mergeCommit
gh api repos/jsonwisdom/COMPUTERWISDOM/commits/<HEAD_SHA>/status
gh api repos/jsonwisdom/COMPUTERWISDOM/commits/<HEAD_SHA>/check-runs

## Safe Fix Pattern

1. Keep verify.yml able to run on PRs that must satisfy required checks.
2. Keep workflow and job naming aligned to verify.
3. Emit both a check run named verify and a classic status context named verify.
4. If GitHub still says Expected, inspect ruleset source binding.
5. Remove stale required-check bindings and re-add the live verify context.

## Forbidden Moves

- No force merge.
- No fake green.
- No ruleset bypass unless documented.
- No authority claim from a local-only artifact.

## Replay Posture

PR_322=MERGED_CONFIRMED
PATH_FILTER_DEADLOCK=DEFEATED
NORMAL_PR_FLOW=true
AUTHORITY=false
NO_FAKE_GREEN=true
