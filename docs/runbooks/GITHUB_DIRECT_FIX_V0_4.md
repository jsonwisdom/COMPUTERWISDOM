# GitHub Direct Fix V0.4

Fault code: GITHUB_DIRECT_AUTH_FAILURE

Symptom: push fails while local commits and branch are valid.

Lesson: do not treat a door problem as a document problem.

Fix route used:

- clear stale shell identity variables
- confirm GitHub CLI login
- route Git through GitHub CLI
- push branch again

Proof signal:

- branch accepted by remote
- branch tracks origin
- connector commits added to same branch

Authority: false.
No Fake Green: true.
Replay required: true.
