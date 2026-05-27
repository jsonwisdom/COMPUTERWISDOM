# GitHub Ruleset Operator Guide

Checkpoint: OBSERVER_REFUSAL_MEMBRANE_001  
Repository: jsonwisdom/COMPUTERWISDOM  
Target branch: master  
Required workflow check: Verify Federal AI Observers / verify  
Authority model: PROCESS_BOUND  
Government authority claim: false

## Critical warning

GitHub's new Rulesets form is stateful. If you leave the draft page on mobile, the form can reset to zero.

Do not leave the ruleset draft while configuring it.

Use one of these safer paths:

1. Open GitHub Actions in a second browser tab/window before starting the ruleset.
2. Use desktop GitHub instead of mobile for rulesets.
3. If using mobile, copy this guide first, then configure the ruleset in one continuous pass.

## Pre-check

Before creating the ruleset, verify the required workflow has already passed on master.

Known passing receipt:

```json
{
  "workflow": "Verify Federal AI Observers",
  "job": "verify",
  "latest_known_passing_commit": "36d5ad7",
  "state": "RUNTIME_PROVEN"
}
```

If the required status check does not appear in GitHub's Add checks picker, push an empty trigger commit from Cloud Shell:

```bash
cd ~/COMPUTERWISDOM
git fetch origin master
git reset --hard origin/master
git commit --allow-empty -m "Register required status check"
git push origin master
```

Wait for the new Actions run to finish green before creating the ruleset.

## Configure the ruleset without leaving the page

1. Go to repository Settings.
2. Open Rules or Branches, depending on the GitHub UI shown.
3. Create a new branch ruleset.
4. Ruleset name:

```text
OBSERVER_REFUSAL_MEMBRANE_001
```

5. Enforcement status:

```text
Active
```

6. Bypass list:

```text
Empty
```

Do not add a bypass unless there is a documented emergency procedure.

7. Target branches:

Use Add target and select either:

```text
Include default branch
```

or manually target:

```text
master
```

8. Rules to enable:

```text
Require a pull request before merging
Require status checks to pass
Require branches to be up to date before merging
Require conversation resolution before merging
Block force pushes
```

9. Required status check:

Tap Add checks and select the workflow job:

```text
Verify Federal AI Observers / verify
```

If GitHub displays only the job name, select:

```text
verify
```

Do not save while the required checks list is empty.

10. Save or create the ruleset.

## Expected final state

```json
{
  "ruleset": "OBSERVER_REFUSAL_MEMBRANE_001",
  "enforcement": "ACTIVE",
  "target_branch": "master",
  "required_check": "Verify Federal AI Observers / verify",
  "bypass_list": [],
  "status": "BRANCH_ENFORCED_REFUSAL_MEMBRANE"
}
```

## If the form resets

Do not keep filling partial rules from memory.

Restart from this document and configure it in one pass.

The important rule is simple:

Committed is not enough. Passing CI is not enough. The passing CI job must be required by the branch ruleset.

No crown. No cosplay. Process or bust.
