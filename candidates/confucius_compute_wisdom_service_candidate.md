# Confucius Compute Wisdom Service

Status: Candidate only, not live.
Operator: jaywisdom.base.eth
Surface: /candidates/
Public website intent: yes, after approval.
Portal mutation: forbidden until explicit promotion.
Badge or credential grant: none.

## Purpose

Confucius Compute Wisdom is a public-facing builder guide service.

Builders bring code, specs, prompts, receipts, or broken workflows.
The service returns structured wisdom:

1. What the code appears to do
2. What claims it makes
3. What risks or missing receipts exist
4. What should be tested next
5. What proof object could be generated
6. Whether the artifact is HELD, PENDING, PUBLIC, REJECTED, or PROMOTED

## Service Loop

Input: Builder submits code or artifact.

Analysis: DeepSeek or another model assists with review, explanation, contradiction detection, and improvement suggestions.

Compute Wisdom Filter: Jay's rules convert the model output into claim tags, proof requirements, and next actions.

Output: Builder receives a Wisdom Report with clear status and recommended repair path.

Receipt: If the report is saved, it gets a receipt ID and hash.

## Public Website Role

The public website may eventually expose this as:

- Paste code here
- Upload artifact here
- Request Wisdom Report
- Get claim tags
- Get verification checklist
- Generate candidate receipt

No code execution is promised in this candidate.
No security audit is promised in this candidate.
No legal, financial, or compliance certification is granted.

## DeepSeek Role

DeepSeek may be used as an analysis engine or skill-building assistant.

DeepSeek does not grant truth by itself.
Computer Wisdom decides what counts as reviewable evidence.
Jay's Wisdom decides what gets promoted.

## Example Output Schema

```json
{
  "service": "Confucius Compute Wisdom",
  "status": "CANDIDATE_ONLY",
  "input_type": "CODE | SPEC | PROMPT | RECEIPT | WORKFLOW",
  "builder_claim": "HELD",
  "analysis_summary": "PENDING",
  "risk_notes": [],
  "recommended_tests": [],
  "proof_required": true,
  "receipt_status": "PENDING",
  "public_badge_granted": false
}
```

## Guardrails

- No portal.html mutation
- No live claims until promotion
- No public badge by default
- No fake audit certification
- No promise that AI analysis is correct without verification
- No secrets, private keys, credentials, or sensitive personal data should be submitted

## Canon

Builders can slap in code and get Wisdom back.
But Wisdom is not vibes.
Wisdom is structured review plus receipts.
