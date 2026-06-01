# GOBLIN PRECEDENT INDEX V0.1

Artifact: `GOBLIN_PRECEDENT_INDEX_V0_1.md`  
Purpose: Classify recurring operator failures into reusable precedents.  
Mode: Observer Only  
Authority: false  
Trinity: PROTECT | WITNESS | APPEND_ONLY  
Date: 2026-06-01

---

## Court Schema

```text
Input → Classifier → Output
Operator observation → Symptom → Goblin ID → Receipt + Checklist + Recovery
Error output
Unexpected behavior
Deployment outcome
Runtime symptom
```

Core Rule: Classify assumptions before debugging symptoms.

---

## Implementation Status

```json
{
  "implementation_status": {
    "reference_engine": "DRAFTED",
    "self_test": "PASSED_OPERATOR_REPORTED",
    "assistant_independent_verification": false,
    "known_limitations": [
      "bash post-command capture requires wrapper",
      "zsh preferred for full fidelity",
      "GC-004 must avoid eager deploy warnings",
      "GC-006 requires .env.example comparison for missing keys"
    ]
  }
}
```

---

## Goblin Registry

| GC-ID | Goblin Name | Receipt | Checklist | Priority | Status |
|---|---|---|---|---|---|
| GC-001 | Nested Repository Goblin | FR-001 | CL-001 | HIGH | Anchored |
| GC-002 | Missing Dependency Goblin | FR-002 | CL-002 | HIGH | Anchored |
| GC-003 | Wrong Branch Goblin | FR-003 | CL-003 | HIGH | Anchored |
| GC-004 | Time Traveler Goblin | FR-004 | CL-004 | HIGH | Anchored |
| GC-005 | Wrong Network Goblin | FR-005 | CL-005 | HIGH | Anchored |
| GC-006 | Missing Environment Goblin | FR-006 | CL-006 | HIGH | Anchored |
| GC-007 | Schema Mismatch Goblin | FR-007 | CL-007 | HIGH | Anchored |
| GC-008 | Ghost Deployment Goblin | FR-008 | CL-008 | HIGH | Anchored |
| GC-009 | Permission Goblin | FR-009 | CL-009 | HIGH | Anchored |
| GC-010 | Assumption Cascade Goblin | FR-010 | CL-010 | CRITICAL | Anchored |

Progress: 10 of 10 anchored. Court is seated.

---

## Receipts

### FR-001 — GC-001: Nested Repository Goblin

Summary: The operator assumed their current working directory was the repository root, when in fact they were inside a subdirectory of a repository — or worse, inside a nested repository.

Violated Assumption: The operator trusted pwd appearance instead of explicit verification of repository root.

Symptoms:

- Git commands affect wrong repo
- Relative paths resolve incorrectly
- Build scripts find wrong config files
- `git status` shows unexpected files
- `git rev-parse --show-toplevel` returns unexpected path

CL-001 Checklist:

1. `git rev-parse --show-toplevel` — print repository root
2. Compare with `pwd` — are you in root or subdir?
3. `find . -name ".git" -type d` — detect nested repos
4. If nested: restructure or use `--git-dir`

Recovery:

1. Run `cd $(git rev-parse --show-toplevel)`
2. Re-run command from root
3. For nested repos: consolidate or use explicit `--git-dir`

Final Rule: Thou shalt verify thy repository root before any git operation.

---

### FR-002 — GC-002: Missing Dependency Goblin

Summary: The operator assumed a package, module, binary, or library was installed, available in PATH, or at the correct version without explicit verification.

Violated Assumption: The operator trusted "it worked before" / environment state instead of explicit availability and version verification.

Symptoms:

- `command not found` for tools that "should be installed"
- `ModuleNotFoundError` / `ImportError` despite prior install
- Version mismatch errors
- Build succeeds locally but fails in CI/container
- `which`/`where` returns nothing or wrong path
- Package manager says "already satisfied" but code fails

CL-002 Checklist:

1. `which <binary>` — verify in PATH
2. `npm list | grep <pkg>` / `pip show <pkg>` — verify installed
3. `<runtime> --version` — check runtime version
4. `cat package.json | grep <pkg>` — verify declared
5. Run clean install in isolation

Recovery:

1. Install/upgrade exact required version
2. Use lockfiles: `package-lock.json`, `Pipfile.lock`, `Cargo.lock`
3. Commit dependency changes
4. Rebuild from clean state

Final Rule: Thou shalt verify thy dependencies are explicitly installed and versioned before trusting them.

---

### FR-003 — GC-003: Wrong Branch Goblin

Summary: The operator assumed they were on the correct git branch, tag, or commit hash, when in fact they were detached, on an old/outdated branch, or had unmerged/unpulled changes.

Violated Assumption: The operator trusted "I'm probably on the right branch" instead of explicit verification of git context.

Symptoms:

- Changes don't appear after commit/push
- `git pull` brings unexpected code or conflicts
- CI fails with "expected commit not found"
- Local code doesn't match teammates
- `git status` shows detached HEAD

CL-003 Checklist:

1. `git branch --show-current` — print current branch
2. `git rev-parse --abbrev-ref HEAD` — confirm branch
3. `git log -1 --oneline` — verify latest commit
4. `git remote update && git status -uno` — check incoming

Recovery:

1. `git checkout main` or correct branch
2. `git pull` to synchronize
3. Rebase or merge as needed
4. Re-verify with `git status` and `git log`

Final Rule: Thou shalt verify thy current branch and commit before any git operation or deployment.

---

### FR-004 — GC-004: Time Traveler Goblin

Summary: The operator assumed the commit hash they were deploying matched the intended version, when in fact they were deploying an old commit, a different tag, or uncommitted changes.

Violated Assumption: The operator trusted "I just committed" instead of verifying the exact commit hash.

Symptoms:

- Deployment shows old behavior
- `git log` shows newer commits but deployed version is behind
- Tag points to wrong commit
- CI deploys unexpected version
- Hotfix doesn't fix the issue

CL-004 Checklist:

1. `git rev-parse HEAD` — get current commit hash
2. `git describe --tags` — get current tag
3. Compare with expected deployment hash/tag
4. `git diff --stat` — check for uncommitted changes
5. `git log --oneline -5` — review recent history

Recovery:

1. `git checkout <correct-commit-or-tag>`
2. Rebuild from clean state
3. Deploy again
4. Verify deployed hash matches source

Final Rule: Thou shalt verify thy commit hash matches deployment target before any release.

---

### FR-005 — GC-005: Wrong Network Goblin

Summary: The operator assumed they were connected to the correct network: mainnet, testnet, or local, when in fact they were on the wrong chain, wrong RPC endpoint, or wrong environment.

Violated Assumption: The operator trusted the RPC URL without verifying chain ID or network state.

Symptoms:

- Transaction succeeds but doesn't affect expected state
- Contract addresses don't match known deployments
- `cast chain-id` returns unexpected value
- Explorer shows different network
- Balance shows unexpected values
- Revert reasons mention wrong chain

CL-005 Checklist:

1. `cast chain-id --rpc-url $RPC_URL` — verify chain ID
2. `curl -X POST $RPC_URL --data '{"method":"net_version"}'` — confirm
3. Check `EXPECTED_CHAIN_ID` environment variable
4. Verify explorer URL matches network
5. Check wallet/keystore network configuration

Recovery:

1. Set correct `RPC_URL` and `CHAIN_ID`
2. Re-run command with explicit `--rpc-url` flag
3. Verify contract addresses on correct explorer
4. Re-execute transaction

Final Rule: Thou shalt verify thy network and chain ID before any transaction or contract call.

---

### FR-006 — GC-006: Missing Environment Goblin

Summary: The operator assumed environment variables, config files, or runtime flags were set correctly, when in fact they were missing, overridden, misspelled, or empty.

Violated Assumption: The operator trusted "it's probably set" instead of explicit verification.

Symptoms:

- Connection errors to services that "should be configured"
- Application uses default/fallback values
- Typos in variable names, such as `DATABASE_URL` vs `DATABASE_ULR`
- Different behavior between local and CI
- Secrets or keys undefined at runtime
- Config file present but not loaded

CL-006 Checklist:

1. `printenv | grep -E 'KEY|URL|PATH|SECRET'` — inspect variables
2. `cat .env` — verify config file
3. Compare `.env` with `.env.example` for missing keys
4. Check for empty values: `if [ -z "$VAR" ]; then echo "missing"; fi`
5. Verify config loading order: shell profile, docker env, CI

Recovery:

1. Export missing variables or fill `.env`
2. Use `export` or proper `.env` loading
3. Restart application in corrected environment
4. Add environment validation at startup

Final Rule: Thou shalt print and verify thy environment variables before trusting any runtime configuration.

---

### FR-007 — GC-007: Schema Mismatch Goblin

Summary: The operator assumed data structures, API responses, contract ABIs, database schemas, or config formats matched expectations, when in fact the shape had changed.

Violated Assumption: The operator trusted implicit contracts instead of verifying explicit schemas.

Symptoms:

- `undefined is not a function` / `cannot read property 'x' of undefined`
- JSON parse errors on valid-looking payloads
- Contract reverts with `function selector not recognized`
- SQL errors: `column does not exist`
- Type errors despite "correct" code
- API returns 200 but payload structure changed

CL-007 Checklist:

1. Log raw payload/response — inspect actual shape
2. Diff current ABI/schema against last known good version
3. Check API version headers
4. Verify database migration status
5. `cast interface <address>` or `forge inspect <contract> abi`
6. Add runtime validation: zod, ajv, ABI check

Recovery:

1. Capture actual received shape
2. Diff against expected schema/ABI
3. Identify breaking change: field renamed, removed, nested
4. Update consumer code or pin producer to compatible version
5. Add schema validation to prevent regression

Final Rule: Verify the shape before trusting the data.

---

### FR-008 — GC-008: Ghost Deployment Goblin

Summary: The operator assumed a deployment, transaction, or state change succeeded and was finalized, when in fact it was pending, reverted, queued, cached, or never executed.

Violated Assumption: The operator trusted success logs instead of verifying finality and observable effect.

Symptoms:

- Deployment script says "success" but contract not reachable
- Transaction hash exists but state unchanged
- CI shows green but application unchanged
- Frontend updates locally but not in production
- "Deployed to staging" but staging still runs old build
- Transaction confirmed but effect not visible

CL-008 Checklist:

1. Verify finality: block confirmation count
2. Query actual on-chain/application state post-deployment
3. Bypass CDN/cache: force refresh
4. Verify build artifact hash matches deployed hash
5. Test with read-only transaction that exercises new logic
6. Monitor logs for post-deployment errors

Recovery:

1. If pending: wait for finality or resubmit with higher gas
2. If reverted: inspect revert reason
3. If wrong environment: deploy to correct target
4. If stale cache: invalidate cache tags/CDN purge
5. Re-verify after each action

Final Rule: Thou shalt verify observable state after deployment, not trust success logs.

---

### FR-009 — GC-009: Permission Goblin

Summary: The operator assumed file, directory, or process permissions — read/write/execute, ownership, sudo access — were correct when in fact they were insufficient, misapplied, or masked.

Violated Assumption: The operator trusted "I have access" instead of explicit verification.

Symptoms:

- Permission denied on files/directories that "should be accessible"
- Script runs in one terminal but fails in another
- Docker/container operations fail with permission errors
- Sudo commands still fail or behave unexpectedly
- Files created with wrong ownership
- `ls -la` shows unexpected permissions

CL-009 Checklist:

1. `ls -la` — check actual permissions and ownership
2. `whoami && id` — confirm current user and group
3. `stat -c %a` — verify numeric permissions
4. `touch testfile && rm testfile` — test write permission
5. Check `umask`
6. Verify container/user mapping

Recovery:

1. `chmod` and `chown` to correct permissions
2. Run with appropriate user: `sudo -u`, `docker exec -u`
3. Fix `umask` or Dockerfile `USER` directive
4. Test operation again in corrected context

Final Rule: Thou shalt verify permissions and ownership before any read, write, or execute operation.

---

### FR-010 — GC-010: Assumption Cascade Goblin

Summary: The operator compounded multiple unverified assumptions, leading to cascading failures. This is a meta-goblin that triggers when three or more distinct goblins are detected in a single debugging session.

Violated Assumption: The operator assumed that adding more changes would fix the problem, rather than rebasing to known-good state.

Symptoms:

- Three or more different error types in rapid succession
- "Fix" introduces new errors
- Debugging session exceeds 30 minutes without resolution
- Same error persists after multiple attempted fixes
- Operator cannot explain the current system state

Trigger Condition: Three or more distinct goblin classes detected within the cascade window. Default: 15 minutes.

Required Action: STOP_AND_REBASE

CL-010 Checklist — Circuit Breaker Protocol:

1. STOP — Introduce no new changes
2. COUNT — Enumerate active goblins by ID
3. CLEANSE — `git clean -fdx && rm -rf node_modules` or equivalent
4. REBASE — Return to known-good state: `git fetch origin && git reset --hard origin/main`
5. VERIFY — Execute one operation in isolation
6. PROCEED — Resume only after successful verification

Recovery:

1. Halt all debugging activity
2. Run CL-010 steps in order
3. Document which assumption failed first
4. Rebuild from clean baseline
5. Re-apply changes one at a time with verification

Lesson: When the third goblin appears, you have lost situational authority. Rebase to foundation.

Final Rule: When symptoms multiply faster than understanding — STOP. Rebase to foundation. Then continue.

---

## Symptom Lookup Table

| Symptom | Likely Goblin(s) |
|---|---|
| command not found | GC-002 |
| ModuleNotFoundError / ImportError | GC-002 |
| Wrong code running after deploy | GC-003, GC-004, GC-008 |
| Deployment changed nothing | GC-004, GC-008 |
| Permission denied | GC-009 |
| Git commands affect wrong repo | GC-001 |
| Relative paths resolve incorrectly | GC-001 |
| Different behavior local vs CI | GC-002, GC-005, GC-006, GC-007 |
| RPC/connection errors | GC-005 |
| Wrong chain state | GC-005 |
| Environment variable missing | GC-006 |
| Works locally, fails elsewhere | GC-005, GC-006, GC-007 |
| Migration fails | GC-007 |
| Schema/ABI mismatch | GC-007 |
| Transaction hash exists but no effect | GC-005, GC-008 |
| Multiple unrelated failures | GC-010 |

---

## Intercept Priority Order

When multiple triggers fire simultaneously, evaluate in this order:

1. GC-010 — circuit breaker, override all
2. GC-001 — foundation, directory context
3. GC-009 — permission, access
4. GC-002 — dependency, availability
5. GC-006 — environment, config
6. GC-005 — network, connectivity
7. GC-003/GC-004 — branch/commit, version state
8. GC-007 — schema, structure
9. GC-008 — deployment, finality

---

## Observer-Only Enforcement

Authority: false means:

| Action | Permitted |
|---|---|
| Print receipt | Yes |
| Show checklist | Yes |
| Recommend recovery | Yes |
| Halt execution automatically | No |
| Modify state | No |
| Suppress operator choice | No |

The operator must choose to follow precedent. The Court witnesses; it does not compel.

---

## Constitutional Rule

When symptoms multiply faster than understanding:

STOP.  
Rebase to foundation.  
Then continue.

Authority: false.

---

## Version History

| Version | Date | Changes |
|---|---|---|
| V0.1 | 2026-06-01 | Initial consolidated blueprint. 10 goblins anchored. Circuit breaker defined. Observer-only mode locked. |

---

End of `GOBLIN_PRECEDENT_INDEX_V0_1.md`
