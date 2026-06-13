# GitHub Direct Fix V0.1

## Purpose

Preserve the fix for the recurring GitHub Direct failure where valid local work cannot be pushed because the wrong credential wins the authentication race.

## Fault Signature

```text
Invalid username or token.
Password authentication is not supported for Git operations.
fatal: Authentication failed
```

## Root Cause

A stale or invalid `GITHUB_TOKEN` / `GH_TOKEN` environment variable can override a valid GitHub CLI login.

This creates a false failure pattern:

```text
artifact good
commit good
branch good
repo good
push blocked
```

The failure is not the work. The failure is credential precedence.

## Correct Identity

Use the GitHub CLI authenticated identity:

```text
jsonwisdom via gh auth
```

## Fix

```bash
unset GITHUB_TOKEN
unset GH_TOKEN
gh auth status
gh auth setup-git
git push
```

## Permanent Cloud Shell Guard

Add this to `~/.bashrc`:

```bash
unset GITHUB_TOKEN
unset GH_TOKEN
```

Then reload:

```bash
source ~/.bashrc
```

## Verification

A successful fix shows:

```text
[new branch] <branch> -> <branch>
branch '<branch>' set up to track 'origin/<branch>'.
```

## Rule

Never treat credential-layer failure as artifact failure.

```text
Bad badge blocked good work.
Remove bad badge.
Use gh identity.
Push again.
```

Authority: false.  
No Fake Green: true.
