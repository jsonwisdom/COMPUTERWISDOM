# REPO_FAMILY_MAP_V0_1

Parent: COMPUTERWISDOM  
Child: JOY  

## Routing Rule

COMPUTERWISDOM is the parent operator/workflow repo.

JOY lives under COMPUTERWISDOM as the daughter publishing/output lane.

AL is the ALMS verification engine and receipt substrate.

zero_trust_repos is local mirror/inventory only. It is not the canonical destination for new work.

## Current Boundary

- COMPUTERWISDOM/JOY contains JOY as daughter repo/worktree.
- COMPUTERWISDOM/alms contains operator tooling and workflows.
- AL contains ALMS validators, schemas, receipts, replay engines.
- No loose root receipts.
- No fake green.

authority: false  
verified: false  
no_fake_green: true
