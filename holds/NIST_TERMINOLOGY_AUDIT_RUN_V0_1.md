# AUDIT RUN — NIST TERMINOLOGY PASS

PROCEDURE = FULL_MATH_AUDIT_V1 fields, applied manually
EXECUTABLE_IMPLEMENTATION = NOT_BOUND
OPERATOR_AUTHORIZATION = THIS_MESSAGE
TARGET = NIST terminology pass in holds/NIST_TERMINOLOGY_CORRECTION_V0_1.md
SCOPE = site:nist.gov pages read in this thread
EXCLUSIONS = non-NIST sources; unrecovered GCR AGI claim; Drive de-identification PDF
AUDIT_OF_OTHER_NAMED_AUDITS = NOT_THIS_RUN

INPUTS = AI 100-1, AI 100-3, AI 600-1, AI 200-1, AI 200-2 IPD, agent page, Agent Standards Initiative, super-intelligence page, Human-Centered SI, foundation-model glossary, 2019 hosted ODNI comment, Playbook, Roadmap
FAILED_SEARCHES = NIST-authored AGI standard; ASI as NIST-defined standard; formal SI capability threshold
UNKNOWN = AI 100-3 standalone ML-system entry not extracted; AI 600-1 definition paragraph not extracted
CONTRADICTIONS = none adjudicated; SI rename does not rewrite historical documents
TRANSITION_AUTHORITY = none created
CLOCKS = 2023-01-26 RMF; 2026-02-17 agent initiative; 2026-09-29 EO 14434 communications note

DISPOSITION = HOLD
REASON = procedure defined, executable not bound; several source paragraphs not extracted
NEXT_RECEIPT = AI 100-3 ML entry and AI 600-1 definition paragraph

FACTS_PROMOTED = 0
AUTHORITY_CREATED = false
V0_3_EDITED = false
V0_4_OPENED = false
