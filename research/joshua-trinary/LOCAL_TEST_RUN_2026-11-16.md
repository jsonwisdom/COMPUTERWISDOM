# Local verification record — 2026-11-16

Project: CW-JOSHUA-TRINARY-001
Branch: research/cw-joshua-trinary-001
Method: GitHub connector fetched prototype.py and test_prototype.py at the named branch; contents transferred into an isolated local Python 3 environment for execution.

Command: python -m unittest -v test_prototype.py
Result: Ran 7 tests in 0.001s — OK
Tests:
- test_escalation_predicate — ok
- test_inquiry_not_automatically_transparent — ok
- test_manifest_not_signed — ok
- test_notify_evidence_gate — ok
- test_score_bounds_grid — ok
- test_silence_penalty — ok
- test_unknown_no_reward — ok

SHA-256 of locally executed source files:
prototype.py 2b3848778b3e46b418e4510cc61e7e83b66269350bab50c2d6b4775ac8314e64
test_prototype.py d65a31659f85f4c55b25523f251070a457e39c7b2616044ac42d635f7976ba87

SHA-256 of output log:
38dfe3aae0260035fc98e5e2205e6a367089cac335f7c7ceb28e8d1928f8f18f

Scope: syntax/execution of 7 supplied tests only. This does not validate full eight-scenario behavior, source provenance, unobserved real-world events, treaty claims, NVIDIA model evaluations, or human review.

Wolfram W1–W5: True at preceding checkpoint, limited tests (W4 finite sample grid, W5 example).
NVIDIA rag-eval: NOT RUN. Human H1–H5: PENDING.
CIRCUIT_STATUS: UNKNOWN.

This record is based on local execution; independent third-party CI reproduction remains pending.