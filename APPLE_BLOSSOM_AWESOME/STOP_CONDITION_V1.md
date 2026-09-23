# APPLE BLOSSOM AWESOME STOP CONDITION V1

## Core correction

Lifecycle labels are NOT stop conditions.

ACTIVE
ARCHIVE
KEEP
FREEZE
RETIRE

are operator disposition labels only.

They MUST NOT substitute for knowing what a repository is.

## Audit stop condition

A repository may leave DEEP_AUDIT only when all project-identity questions have end-to-end receipts:

1. REPO ROOT
   - default branch identified
   - current head commit identified

2. BYTE / TREE STATE
   - Git tree object identified
   - recursive path/blob inventory captured, or sharded subtree manifests captured for oversized repositories
   - no unexplained truncation

3. PURPOSE
   - project purpose reconstructed from source evidence
   - repo name alone is never evidence

4. FUNCTION
   - executable / operational surfaces identified where present
   - placeholder / namespace / empty repo distinguished from functioning project

5. LINEAGE
   - meaningful version or commit lineage connected
   - current project state distinguished from historical state

6. IDENTITY
   - operator / ENS / wallet / attestation claims classified by proof level
   - witness != controller signature

7. EXTERNAL DEPENDENCIES
   - material pointers to Drive, chain, other repos, services, or public surfaces resolved or explicitly held

8. CONFLICT
   - contradictory purpose/function claims reconciled or marked CONFLICT

9. OPEN GAPS
   - no unresolved gap that changes project identity

10. SNAPSHOT
   - project snapshot receipt written with head, tree, paths/blobs, purpose, function, lineage, identity, pointers, and gap state

ONLY THEN:

DEEP_AUDIT -> SNAPSHOT_COMPLETE -> DELTA_MODE

## Delta mode

After a complete snapshot:

same head/tree
= NO_CHANGE

new head/tree
= compare old...new
= inspect changed paths and new/removed tree edges
= re-open deep audit only when a material trigger fires

Material triggers:
- purpose file changed
- executable surface changed
- identity/anchor file changed
- external pointer changed
- history rewrite / force move
- tree truncation or corruption
- previously resolved contradiction reappears
- Jason explicitly requests full replay

## Non-collapse

LIFECYCLE_LABEL != PROJECT_IDENTITY
README != PROJECT
REPO_NAME != PURPOSE
HEAD_SHA != PURPOSE
TREE_SHA != PURPOSE
SNAPSHOT != TRUTH
DELTA != NONMATERIAL
NO_CHANGE != NO_RISK
