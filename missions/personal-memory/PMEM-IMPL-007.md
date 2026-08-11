# PMEM-IMPL-007 — Actor Identity + Authentication Contract

Depends on: `001..006`

`LABEL != IDENTITY` and `AUTHENTICATED != AUTHORIZED`.

Canonical actors have immutable `actor_id`, actor type (`USER|MODEL|SYSTEM|TOOL|SERVICE`), display label, bindings, and status. Display-label changes are append-first metadata events.

Identity bindings are independent objects with `binding_id`, `actor_id`, method (`ACCOUNT|KEY|DEVICE|CREDENTIAL|USER_ASSERTION`), evidence reference, validity, and verification state.

Authentication flow: `binding presented -> binding verified -> actor resolved -> receipt`. Ambiguous resolution fails closed as `ACTOR=UNKNOWN`, `AUTHENTICATED=FALSE`.

Display names, email text, signature blocks, self-description, and model-generated claims cannot alone establish verified identity; they may produce USER_ASSERTED evidence only.

Binding revocation blocks future authentication through that binding while preserving historical receipts. Credential rotation does not automatically create a new actor.

Model/tool identity should include provider, identifier, version, and execution/session identifier where available.

All BIND/VERIFY/AUTHENTICATE/REJECT/REVOKE/RESOLVE operations produce receipts.

Core: **SIGNATURE != IDENTITY WITHOUT BINDING; AUTHENTICATION != AUTHORIZATION**.

`AUTHORITY_CREATED = FALSE`
