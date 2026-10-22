# MAXWELL ATOMIC MAGNET AUDIT v0.1 — ACE Authority Chain

**Class:** `PUBLIC_RESEARCH_CROSSWALK / AUTHORITY_EDGE_REPLAY`  
**Date:** 2026-08-19  
**Authority created:** `FALSE`  
**Institutional endorsement claimed:** `FALSE`  
**Operational command claimed:** `FALSE`

## Term boundary

`Maxwell Atomic Magnet` is a project-created audit label. Exact-phrase searches in connected Drive, GitHub, and official Air University / Air Force public pages did not establish it as an official Air Force or Air University term.

```text
ATOMIC = reduce one broad institutional claim to one named concept and the smallest independently testable receipts.
MAGNET = pull only receipts sharing a real identity edge: same named concept, organization, authority instrument, date, exercise, implementation record, or execution event.
NARRATIVE SIMILARITY != EDGE
```

## Test claim

> “Air University develops advanced warfighting concepts that are subsequently executed as operational practice by the United States Air Force.”

### Atomic object

Named concept: **Agile Combat Employment (ACE)**.

## CrissCross / AppleSauce map

### 1. Maxwell place edge

Official Maxwell material identifies the 42d Air Base Wing as the host organization and Air University as headquartered at Maxwell / a major mission partner.

`STATE = PROVEN_PUBLIC_SOURCE`

```text
COLOCATION != COMMAND
```

### 2. Air University / LeMay doctrine edge

The Curtis E. LeMay Center for Doctrine Development and Education publicly describes itself as the principal organization for developing and assessing Air Force doctrine and the Air Force lead for lessons learned.

`STATE = PROVEN_PUBLIC_SOURCE`

`EDUCATION_ONLY` is too narrow for the LeMay Center because its doctrine-development role is explicit.

### 3. Doctrine authority edge

Official Air University reporting states that the LeMay Center developed the first Air Force doctrine publication on ACE and that the Chief of Staff of the Air Force signed AFDN 1-21 on 2021-12-09, codifying ACE as an operational scheme of maneuver.

`STATE = PROVEN_PUBLIC_SOURCE`

```text
LeMay doctrine development -> CSAF signature
LEMay DEVELOPMENT != CSAF AUTHORITY
```

A real authority bridge exists through the CSAF signature.

### 4. Service implementation edge

Official Department of the Air Force reporting on 2022-06-23 states that the Air Force operationalized ACE to codify and synchronize ACE tactics enterprise-wide, including organization, training, equipping, theater posture, and joint / partner integration.

`STATE = PROVEN_PUBLIC_SOURCE`

```text
SERVICE DOCTRINE / SENIOR AIR FORCE DIRECTION
-> ENTERPRISE IMPLEMENTATION
```

### 5. Maxwell execution / training edge

Official Air University / AETC reporting documents a 34th Special Operations Squadron culmination exercise at Maxwell in March-April 2022. Maxwell provided staging and logistics support; the unit described the event as an opportunity to plan and execute ACE concepts and validate tactics, techniques, procedures, and readiness.

`STATE = PROVEN_EXERCISE_EXECUTION`

```text
EXERCISE_EXECUTION != COMBAT_OPERATION
MAXWELL_SUPPORT != AIR_UNIVERSITY_COMMAND_OF_34SOS
```

### 6. 2026 retrospective edge

A 2026 Air University Press paper describes a multiyear Headquarters Air Force effort to develop, implement, and institutionalize ACE across major commands and subordinate units.

`STATE = PROVEN_PUBLIC_SOURCE_AS_PUBLISHED_DESCRIPTION`

```text
AU_PRESS_PUBLICATION != ORIGINAL_EXECUTION_ORDER
```

It is a strong retrospective source, not the authorizing order itself.

## Reverse replay

```text
OBSERVED ACE EXERCISE / OPERATIONALIZATION
↑
UNIT / SERVICE IMPLEMENTATION
↑
HEADQUARTERS AIR FORCE ENTERPRISE ACTION
↑
CSAF-SIGNED DOCTRINE
↑
LEMAY CENTER DOCTRINE DEVELOPMENT
↑
AIR UNIVERSITY / MAXWELL INSTITUTIONAL CONTEXT
```

## Result

- Air University / LeMay produces doctrine and concept material: `PROVEN`.
- CSAF adopted ACE doctrine through signed AFDN 1-21: `PROVEN`.
- Air Force enterprise operationalization of ACE: `PROVEN`.
- ACE was exercised at Maxwell by an operational squadron with Maxwell / AU support: `PROVEN_AS_EXERCISE`.
- Air University itself directly commanded the operational squadron: `REJECT` absent a receipt; public evidence shows support / doctrine roles and separate unit execution.
- A specific combat mission was caused by an Air University publication: `HOLD` pending mission-order / tasking / execution receipts.
- The broad claim `AU concept -> USAF execution` is therefore `BOUND`, not automatically `PROVEN` or `REJECTED`.

## Atomic Magnet finding

The invalid transition remains:

```text
EDUCATION -> [MAGIC] -> EXECUTION
```

But this replay found a legitimate intermediary chain:

```text
LEMAY DOCTRINE DEVELOPMENT
-> CSAF DOCTRINE SIGNATURE
-> HEADQUARTERS AIR FORCE OPERATIONALIZATION
-> MAJCOM / UNIT IMPLEMENTATION
-> EXERCISE / OPERATIONAL-PRACTICE RECEIPTS
```

The missing edge was not filled by inference. It was replaced with documented authority nodes.

## Gray Baby ruling

**SHOW ME THE EDGE succeeded.**

The edge exists for ACE at the doctrine / service-implementation level. The edge does **not** prove Air University directly commands operational units.

### PROVEN

- Maxwell / AU institutional context
- LeMay doctrine-development role
- CSAF ACE doctrine signature
- Air Force ACE operationalization
- 34th SOS ACE exercise at Maxwell

### BOUND

- ACE as an example of Air University-connected doctrine later implemented across the Air Force

### HOLD

- named combat operation caused by a specific AU paper, class, wargame, or publication
- specific funding line causally attributed to an AU-originated concept unless appropriations / program / order receipts bind it

### REJECT

- Air University education automatically transfers operational command authority
- physical presence at Maxwell creates command authority

```text
NO INFERENCE. ONLY RECEIPTS.
IDEAS MAY TRAVEL FREELY. AUTHORITY DOES NOT.
SHOW ME THE EDGE.
```

## Public source rail

- Air University — Curtis E. LeMay Center: https://www.airuniversity.af.edu/LeMay/
- Air University — CSAF signs Agile Combat Employment doctrine note (2021-12-14): https://www.airuniversity.af.edu/News/Display/Article/2873496/csaf-signs-agile-combat-employment-doctrine-note/
- U.S. Air Force — Air Force operationalizes ACE concept (2022-06-23): https://www.af.mil/News/Article-Display/Article/3072831/air-force-operationalizes-ace-concept-addresses-todays-changing-threat-environm/
- Air University — 34th Special Operations Squadron exercises agile combat employment at Maxwell (2022-04-04): https://www.airuniversity.af.edu/News/Display/Article/2987837/34th-special-operations-squadron-exercises-agile-combat-employment-at-maxwell/
- Air University Press — Implementing New Airpower Concepts: Insights from Agile Combat Employment (2026-03-30): https://www.airuniversity.af.edu/AUPress/Display/Article/4447332/implementing-new-airpower-concepts-insights-from-agile-combat-employment/

## OpenAI Platform boundary

Platform topology is tooling / access context only.

```text
MODEL OUTPUT != SOURCE
OPENAI PLATFORM != INSTITUTIONAL AUTHORITY
```

No API key is required or created by this audit.
