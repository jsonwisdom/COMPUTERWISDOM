# Jason's Congressional Accountability Membrane — v0.1

## Purpose

Classify Congress-facing records without silently promoting publication, legislative activity, oversight, or enforcement into law, factual truth, guilt, or government authority.

## Twelve independent lanes

1. Statutory authority
2. Bill status
3. Authorization
4. Appropriation
5. Committee jurisdiction
6. Required congressional notice
7. Hearing or testimony
8. Committee report
9. Inspector General or audit
10. Transparency or public reporting
11. DOJ/FBI referral or response
12. Judicial, FISA, or constitutional review

## Constitutional membranes

```text
INTRODUCED_BILL != LAW
PASSED_HOUSE != LAW
PASSED_SENATE != LAW
COMMITTEE_REPORT != LAW
PUBLIC_LAW = ENACTED_LAW only when enactment fields are source-bound

AUTHORIZATION != APPROPRIATION
APPROPRIATION != EXECUTION
HEARING_TESTIMONY != FACT_PROVEN
REFERRAL_TO_FBI != FBI_FINDING
INVESTIGATION != GUILT
CLASSIFIED != UNACCOUNTABLE

ONCHAIN_ANCHOR != LEGAL_IDENTITY_PROOF
ENS_CONTROL != GOVERNMENT_AUTHORITY
TIMESTAMPED_HASH != UNDERLYING_CLAIM_TRUE
```

`OBSERVER_RESULT=PROVEN` has exactly one meaning: the specified congressional evidence-classification gates resolved to `PROVEN`. It never means the underlying allegation is proven.

## Agent/tool boundary

The OpenAI agent surface may extract candidate fields and call the deterministic verifier. It must return the verifier's structured receipt unchanged. It may not widen `PROVEN`, invent missing sources, execute real-world actions, contact Congress, submit referrals, or create legal conclusions. External publication and government-facing submission require separate human authorization.

The implementation deliberately keeps the deterministic verifier independent of model execution. Synthetic tests exercise semantic boundaries; they do not test live Congress.gov records or create authority.

## John Jay Sentinel: Constitution Reverse Replay

The constitutional corpus must not be collapsed into one document. The sentinel asks backward from a present claim through the government action, actor, claimed power, exact constitutional provision, later amendments, ratification evidence, Federalist and Anti-Federalist advocacy, enacted statutes, judicial precedent, oversight records, rights, limits, and remedies.

John Jay is historically relevant as a Federalist essay author and the first Chief Justice. That makes him a useful educational question surface, not a simulated judge and not an authority over present disputes.

```text
FEDERALIST_ESSAY != CONSTITUTIONAL_TEXT
FOUNDER_OPINION != CONTROLLING_PRECEDENT
CONSTITUTION_ANNOTATED != SUPREME_COURT_JUDGMENT
SENTINEL != COURT
QUESTION != ACCUSATION
```

Primary public reference surfaces include the National Archives Constitution and amendment transcripts, Library of Congress Federalist collections, Congress's Constitution Annotated, enacted Public Laws, and official court opinions. Each source keeps its own document class and evidentiary role.
