# THE GIBSON — Architecture V0.1

A directories-first, replayable control plane for questions, artifacts, routes, mirrors, and receipts across Drive, GitHub, and OpenAI-backed tools.

## Primary question
How can one question become a traceable object that moves across systems without losing provenance, silently changing meaning, or creating authority?

## Core loop
QUESTION → OBJECT → ROUTE → REPLAY → RECEIPT → MIRROR

## Control planes
- Drive = artifact library + human-readable source/readback
- GitHub = versioned executable contracts + schemas + CI
- OpenAI = reasoning/agent layer operating over declared inputs and tool permissions

## Rules
1. No invisible hops.
2. No silent normalization.
3. A mirror is not the source.
4. Absence is not failure and not proof.
5. Every consequential write produces a receipt.
6. Same bounded inputs should replay to the same result.
7. Labels do not imply identity, ownership, or authority.
8. Public and restricted lanes may share schema but not silently share data.
9. OpenAI models may propose, classify, summarize, and compare; they do not become source authority.
10. Human remains consequential authority.

## Security boundary
The Gibson is for organizing, replaying, testing, and navigating authorized data. It is not a credential harvester, intrusion framework, persistence mechanism, or covert targeting system.

master_mutated=false
merge_performed=false
facts_promoted=0
authority_created=false
