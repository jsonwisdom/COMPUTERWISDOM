# Wave 1 Master Launch Checklist

**Compute Wisdom v1.3 Constitutional Substrate**  
**Launch Gate — Public Review Path Only**

## Core Rule

No emails for routing government builds.

Wave 1 critique routes through the public repository, GitHub Issues, and the feedback ledger. Email or direct messages may only be used to point someone to the public review path; they are not canonical critique channels.

## Launch Boundary

Wave 1 is:

- constitutional infrastructure research
- critique-seeking
- non-authoritative
- non-runtime
- non-governance
- non-payment
- non-wallet

Wave 1 is not:

- a deployment proposal
- a government service
- signer logic
- a payment rail
- an authority surface
- an email-based review process

## Required Public Entry Points

- [ ] `site/index.html`
- [ ] `site/styles.css`
- [ ] `docs/WAVE1_REVIEWER_PACKET_v1_3.md`
- [ ] `docs/WAVE1_REVIEW_INSTRUCTIONS.md`
- [ ] `docs/ONE_PAGE_SUMMARY_v1_3.md`
- [ ] `docs/EXECUTIVE_BRIEF_v1_3.md`
- [ ] `docs/TECHNICAL_SPECIFICATION_APPENDIX_v1_3.md`
- [ ] `docs/REPLAY_RECEIPT_LAYER_v1_3.md`
- [ ] `docs/TWO_WAY_COMMUNICATIONS_PROTOCOL_v1_3.md`
- [ ] `docs/FAILURE_MODE_CATALOG_v1.md`
- [ ] `wave-1/feedback-ledger/README.md`
- [ ] `wave-1/feedback-ledger/2026-05_wave1_ledger.md`

## Required Issue Templates

- [ ] `.github/ISSUE_TEMPLATE/constitutional-critique.md`
- [ ] `.github/ISSUE_TEMPLATE/replay-receipt-critique.md`
- [ ] `.github/ISSUE_TEMPLATE/communications-protocol-critique.md`
- [ ] `.github/ISSUE_TEMPLATE/failure-mode-critique.md`
- [ ] `.github/ISSUE_TEMPLATE/accessibility-offline-redress.md`

## Public Review Flow

```text
site/
  ↓
docs/WAVE1_REVIEWER_PACKET_v1_3.md
  ↓
docs/WAVE1_REVIEW_INSTRUCTIONS.md
  ↓
docs/TECHNICAL_SPECIFICATION_APPENDIX_v1_3.md
  ↓
GitHub Issue Templates
  ↓
wave-1/feedback-ledger/
```

## External Pointer Rule

Any external post, message, or mention should point only to the public review path.

Allowed:

- repository root
- static site
- Wave 1 reviewer packet
- GitHub Issues

Not allowed as canonical routing:

- private email thread
- direct-message review queue
- private spreadsheet
- off-repo document comments
- hidden reviewer adjudication

## First Public Launch Copy

Use this posture if posting publicly:

```text
Compute Wisdom v1.3 is open for Wave 1 quiet review.

This is constitutional infrastructure research, not a runtime, product, wallet, payment rail, government service, or source of authority.

Critique routes through public GitHub Issues so review remains contextualized and replayable.

Start here: [site or reviewer packet link]
```

## Launch Check

Before posting:

- [ ] All links resolve
- [ ] Issue templates appear in GitHub issue creation UI
- [ ] Static site is readable on mobile
- [ ] Tipjar language remains research-only and non-investment
- [ ] No file implies runtime authority
- [ ] No file implies government deployment
- [ ] No private channel is described as canonical

## Core Boundary

A receipt is a pointer to replayable legitimacy, not legitimacy itself.

No constitutional communication may create hidden state, silent obligation, or unchallengeable authority.

Every failure mode must be detectable, replayable, and human-escalatable.
