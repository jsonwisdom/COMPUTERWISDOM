# GitHub Direct Fix V0.3

Fault code: GITHUB_DIRECT_AUTH_FAILURE

Symptom: push fails even when local commits exist and the working tree is clean.

Lesson: access failure is not artifact failure.

Fix steps:

1. Clear stale shell identity variables.
2. Check GitHub CLI login.
3. Route Git through GitHub CLI.
4. Push again.

Verification: GitHub accepts the branch and the local branch tracks origin.

Authority: false.
No Fake Green: true.
Replay required: true.
