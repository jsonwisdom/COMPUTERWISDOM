# THE ART OF LEARING — Classes with Glasses / Parent–Child v0.1
Status: DRAFT | READ_ONLY | AUTHORITY_FALSE

## Goal
LEARN -> VERIFY -> SIMULATE VOTE -> REPLAY -> IMPROVE.
Teach citizens the legal facts and quadratic arithmetic before simulated decisions. Education may never be a requirement for real voting or constitutional rights.

## First command
    python3 tools/leer/leer.py get children
This returns synthetic curriculum descendants, NOT human children. Follow with:
    python3 tools/leer/leer.py get child MN-13
    python3 tools/leer/leer.py learn MN-13
    python3 tools/leer/leer.py vote 3
    python3 tools/leer/leer.py replay

## Roles
Parent/guardian: consent and participation decisions for real minors.
Student: voluntary exploration and questioning.
Computer Wisdom: read public lessons, compute arithmetic, produce local replay digest.
Human reviewer: authenticates sources, laws, versions, real-world facts, and publication.
No repository or AI claims custody, legal or judicial authority, or power to determine voting eligibility.

## Classroom knobs
State = Minnesota or Alabama (never apply one state's laws as the other's).
Source date and law version = explicit; missing originals remain UNKNOWN.
Audit gates = 13; coverage means completeness, NOT truth.
Quadratic classroom vote = v^2 credits, budget 100; never an election.
Replay = deterministic SHA-256 of synthetic local payload; not source authenticity.

## Quad Onion
1. AUDIT: source and authority.
2. REPLAY: independent calculations.
3. HUMAN VALIDATION: review against official sources, preserve uncertainty.
4. PRODUCTION CANDIDATE: only with separate governance, child privacy review, and real evidence for each state.

## Privacy and authority
The public GitHub project contains zero real child identities, photos, family relationships, geolocation, contact data, biometrics, or political preferences. No automatic account discovery, recording, external writes, wallet signing, state-court action, or actual ballots.
Existing CHARTER.md and ROOT_BINDING.md require a dedicated authority-elevation event; this proposal itself grants no authority.
No official law PDFs are fetched, modified, or treated as verified by these fixtures.

## Related
docs/CONSTITUTION.md
docs/AUTHORITY_DECLARATION_SCHEMA_V1.md
agentic-game/DESIGN.md
projects/ziggy/README.md
Official Minnesota Constitution: https://www.revisor.mn.gov/constitution/
Official Alabama legislature: https://alison.legislature.state.al.us/

## Acceptance
Test command: python3 -m unittest discover -s tests -p 'test_leer_parent_child_v0_1.py'
All lessons synthetic; missing IDs fail closed; vote arithmetic exact; zero network side effects; deterministic replay; authority always false.
