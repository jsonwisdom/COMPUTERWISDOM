# PMEM-IMPL-009 — Disclosure + Composition Safety Contract

Depends on: `001..008`

`AUTHORIZED TO REASON != AUTHORIZED TO DISCLOSE`.

Individually permitted fragments may compose into an unauthorized inference: `SAFE(m1) AND SAFE(m2)` does not imply `SAFE(m1 + m2)`.

Canonical disclosure requests bind actor, destination, purpose, requested fields, evidence ids, derived claims, and request time.

Disclosure gate: `USABLE AND EXPORT_AUTHORIZED AND PURPOSE_MATCH AND DESTINATION_AUTHORIZED AND COMPOSITION_SAFE AND MINIMIZED`; unknown => FALSE.

Any synthesis is a derived object, so its authority is independently evaluated and may only narrow from creator and dependencies.

Composition requires derived-claim analysis before disclosure. Data minimization permits `OMIT|REDACT|GENERALIZE|AGGREGATE|PSEUDONYMIZE`; narrowing transformations may not fabricate evidence.

Authorization is destination-bound. Forwarding is a new disclosure event.

Side channels count as disclosure: prompts, tool arguments, URLs, logs, telemetry, files, email, API calls, and model context sent externally.

Disclosure receipts bind sources, derived claims, requested/released/withheld fields, transformations, authority basis, result, and output hash.

Core: **AUTHORIZED PARTS != AUTHORIZED COMPOSITION; DISCLOSE ONLY THE MINIMUM AUTHORIZED RESULT**.

`AUTHORITY_CREATED = FALSE`
