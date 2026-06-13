# Identity Precedence Fault V0.2

Identity routing failure can look like work failure.

Observed pattern:

1. Work exists.
2. Commit exists.
3. Branch exists.
4. Remote rejects access.
5. Operator may think the artifact failed.
6. Actual issue may be the wrong identity path.

Rule: inspect identity routing before rebuilding artifacts.

Child version: the computer had a good key and a bad key. It tried the bad key first. Use the good key.

Authority: false.
No Fake Green: true.
Replay required: true.
