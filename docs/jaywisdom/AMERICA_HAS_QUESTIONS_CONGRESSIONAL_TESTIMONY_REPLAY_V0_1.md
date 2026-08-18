# America Has Questions — Congressional Testimony Replay v0.1

**Author label:** `jaywisdom.base.eth`  
**Classification:** citizen technical questions / public-record oversight research  
**Authority created:** `false`  
**Submission to Congress performed:** `false`

## Takeaway

The Jay Zora Portal governance incident is **Congressional-worthy as a technical case study and Questions-for-the-Record prompt**, not as proof that Congress, GitHub, DOJ, or any federal actor committed wrongdoing.

The congressional question is broader than one repository:

> When software automation is allowed to execute, validate, publish, or mutate records, what prevents execution permission from silently becoming promotion authority?

## Public case-study anchor

Observed in `jsonwisdom/jay-zora-portal` on 2026-08-18:

```text
PR #6 = OPEN / DRAFT / UNMERGED
PR event fires
workflow advertises PR event
workflow checks out canonical base
workflow has contents: write
generated inventory is committed by github-actions[bot]
bot pushes directly to live-zora-ingestion
canonical ref advances while PR remains unmerged
```

Bound distinctions:

```text
PR_TRIGGER != PR_VALIDATION
WORKFLOW_SUCCESS != PR_HEAD_VALIDATED
BOT_COMMIT != PR_MERGE
CI_PERMISSION != HUMAN_AUTHORITY
ARTIFACT != GIT_PROMOTION
MERGEABLE != MERGED
```

This case study is private-repository governance evidence. It is **not** evidence of a federal violation, GitHub deception, malicious intent, unauthorized intrusion, or criminal conduct.

## Congressional precedent lane

Congress has already held hearings addressing adjacent software-governance questions:

1. **Safeguarding the Federal Software Supply Chain** — House Oversight and Accountability, 118th Congress, November 29, 2023, Congress.gov House Event 116610.
2. **SolarWinds and Beyond: Improving the Cybersecurity of Software Supply Chains** — House Science, Space, and Technology, 117th Congress, May 25, 2021, Congress.gov House Event 112699.
3. **Too Critical to Fail: Getting Software Right in an Age of Rapid Innovation** — House Armed Services Subcommittee on Cyber, Information Technologies, and Innovation, March 13, 2024, H.A.S.C. No. 118-61.
4. **The Federal Government in the Age of Artificial Intelligence** — House Oversight and Government Reform, 119th Congress, June 5, 2025, Congress.gov House Event 118339.
5. **Shaping Tomorrow: The Future of Artificial Intelligence** — House Oversight Subcommittee on Cybersecurity, Information Technology, and Government Innovation, September 17, 2025, Congress.gov House Event 118621.

These records establish that federal software supply chains, automated deployment, software authorization, AI adoption, and federal technology governance are legitimate congressional oversight subjects.

`HEARING_EXISTS != THIS_CASE_ADOPTED_BY_CONGRESS`

## America Has Questions — 12 Questions for the Record

### Q01 — Exact-head validation
When a CI system reports SUCCESS, should federal software policy require the record to identify the exact commit SHA, source ref, workflow definition, and checked-out tree that were actually validated?

### Q02 — Execution vs promotion authority
Should federal CI/CD systems require distinct credentials and policy gates for executing tests versus mutating a canonical branch, production environment, official dataset, or public record?

### Q03 — Pull-request event integrity
Should a job triggered by a pull request be permitted to validate a different ref than the proposed change without an explicit, machine-visible disposition such as `BASE_ONLY_VALIDATION`?

### Q04 — Automation write authority
Under what circumstances should a service account, bot, GitHub Action, AI agent, or other automation be permitted to write directly to a protected federal software or evidence branch?

### Q05 — Least privilege
Should federal repository and pipeline policy default pull-request workflows to read-only permissions and require separately authorized write-capable workflows?

### Q06 — Provenance envelope
Should federal software provenance include not only SBOM/component identity but also workflow source, runner identity, token scope, triggering event, checked-out ref, produced artifact hash, and final promotion actor?

### Q07 — Artifact vs canonical record
What controls should distinguish a generated artifact from an official/canonical government record, and who or what may promote one state into the other?

### Q08 — Bot accountability
Should every automated canonical mutation record the human or policy authority that authorized the bot's write capability, in addition to the bot identity that technically performed the write?

### Q09 — AI-agent authority
As federal agencies adopt agentic AI and coding assistants, what actions may an agent execute autonomously, and which actions require a separate human or institutional promotion gate?

### Q10 — Audit replayability
Should GAO, Inspectors General, and agency security teams be able to reconstruct: `TRIGGER → PERMISSIONS → CHECKOUT → EXECUTION → ARTIFACT → WRITE → REF_DELTA → APPROVAL` from immutable logs?

### Q11 — Green-check semantics
Should federal CI dashboards distinguish `WORKFLOW_COMPLETED_SUCCESSFULLY` from `PROPOSED_CHANGE_VALIDATED`, so operators and auditors cannot silently infer one from the other?

### Q12 — Procurement and contractor controls
Should federal software contracts require contractors and hosted development platforms to document how execution authority, deployment authority, repository mutation authority, and human approval are separated and audited?

## Candidate witness categories

- NIST secure-software / software-supply-chain standards leadership
- CISA software-supply-chain and secure-by-design leadership
- GAO information-technology and cybersecurity auditors
- OMB / Federal CISO or federal digital-policy leadership
- Federal acquisition and procurement officials
- Software supply-chain provenance specialists
- CI/CD platform and repository-governance providers
- Federal agency software-factory / DevSecOps operators
- Independent security researchers and open-source maintainers

`WITNESS_CATEGORY != INVITATION`

## Testimony evidence packet

A congressional-quality packet should separate five layers:

```text
A — CLAIM
What exact governance proposition is being advanced?

B — PUBLIC CASE RECEIPT
Workflow YAML, exact commit SHAs, PR state, branch delta, Actions run, bot commit.

C — GENERALIZABLE CONTROL FAILURE
Execution permission became capable of canonical promotion without the PR merge path.

D — FEDERAL RELEVANCE
Existing congressional hearings, federal software-supply-chain policy, procurement, AI/automation adoption.

E — LIMITS
Private repository case; no federal actor involved in the incident; no malicious intent, platform deception, crime, or federal violation proven.
```

## Congressional membrane

```text
CITIZEN_QUESTION != CONGRESSIONAL_FINDING
CASE_STUDY != NATIONAL_PREVALENCE
PRIVATE_REPO_EVENT != FEDERAL_EVENT
SOFTWARE_BUG != CYBERATTACK
CONTROL_WEAKNESS != EXPLOITATION
HEARING_TESTIMONY != FACT_PROVEN
QUESTIONS_FOR_RECORD != LEGISLATION
LEGISLATION != LAW
OVERSIGHT != GUILT
```

## Suggested committee lanes

Primary relevance:

- House Oversight / cybersecurity, IT, government operations
- House Science / technology and cybersecurity research
- House Armed Services / cyber, software acquisition, digital modernization when defense systems are implicated
- Senate Homeland Security and Governmental Affairs / federal management and cybersecurity

Additional committee jurisdiction depends on the federal agency, program, acquisition, or legal question being examined.

## Replay terminal

```text
CONGRESSIONAL_RELEVANCE = PASS_AS_TECHNICAL_CASE_STUDY
FEDERAL_MISCONDUCT_PROVEN = FALSE
GITHUB_MISCONDUCT_PROVEN = FALSE
QUESTIONS_FOR_THE_RECORD = READY_DRAFT
CONGRESSIONAL_SUBMISSION = NOT_PERFORMED
AUTHORITY_CREATED = FALSE
```
