# COBALT_SELECTION_VECTOR_V0_1

Status: HOLD

Executable object only. No features. No producer binding.

PARENT: COBALT_RULESET_SELECTION_RECEIPT_V0_1
PARENT_STATE: HOLD
THIS_VECTOR_STATE: HOLD
LEG_A: DETERMINISTIC_SELECTION -> HOLD until output bytes match
LEG_B: HISTORICAL_EXECUTION_BINDING -> NOT_IN_SCOPE

## Pin

| Pin | Value | Role |
| --- | --- | --- |
| repository | https://github.com/base/base | source |
| schedule commit | 6a3a32ecbae0abc37bac888f0b9ab2197273dd1d | #5196 — Mainnet cobalt_timestamp lands |
| operator floor label | v1.4.2 | version label only |
| version-label commit | b55767d | chore(release): set version to 1.4.2; not a binary hash |
| config object | ChainConfig::mainnet() | compiled schedule |
| chain_id | 8453 | input |
| overrides | NONE (RuntimeUpgradeRegistry clear for 8453) | required |
| cobalt trigger | Some(1_790_791_200) | compiled |
| beryl trigger | Some(1_782_410_400) | compiled |
| denim trigger | None -> ForkCondition::Never | compiled |

SOURCE_CODE != RUNNING_BINARY
VERSION_LABEL != BINARY_HASH
BINARY_HASH != RUNTIME_CONFIG

v1.4.2 is not the pin. The pin is commit + config + overrides=NONE. A v1.4.2 binary is acceptable only after its tree contains 6a3a32e and its runtime config hash matches ChainConfig::mainnet() with empty overrides.

## APIs under test

Not a Cobalt boolean. The ladder.

```text
ChainUpgrades::mainnet()
  .is_beryl_active_at_timestamp(ts)   -> bool
  .is_cobalt_active_at_timestamp(ts)  -> bool
  .is_denim_active_at_timestamp(ts)   -> bool

BaseUpgrade::from_chain_and_timestamp(8453, ts) -> Option
```

`from_chain_and_timestamp` is the maximal-active selector.
`is_cobalt_active_at_timestamp == false` proves NOT_COBALT only. It does not emit Beryl.

## Vector

Two rows. Same pin. No other inputs.

```text
VECTOR_A
  ts = 1790791199
  expected:
    is_beryl_active_at_timestamp  = true
    is_cobalt_active_at_timestamp = false
    is_denim_active_at_timestamp  = false
    from_chain_and_timestamp      = Some(BaseUpgrade::Beryl)

VECTOR_B
  ts = 1790791201
  expected:
    is_beryl_active_at_timestamp  = true
    is_cobalt_active_at_timestamp = true
    is_denim_active_at_timestamp  = false
    from_chain_and_timestamp      = Some(BaseUpgrade::Cobalt)
```

## Canonical output bytes

UTF-8, LF, no trailing spaces.

```text
8453 1790791199 Beryl=1 Cobalt=0 Denim=0 selected=Beryl
8453 1790791201 Beryl=1 Cobalt=1 Denim=0 selected=Cobalt
```

Any other encoding is a different vector. Match is byte-for-byte on those two lines.

Why `selected=Beryl` is legal on A: Beryl timestamp 1_782_410_400 <= 1790791199, Cobalt 1_790_791_200 > 1790791199, Denim Never. Maximal execution upgrade on the ladder is therefore Beryl. That is ladder proof, not NOT_COBALT inference.

## What a matching run proves

```text
PINNED_CLIENT + PINNED_CONFIG + HEADER_TIMESTAMP
        ->
DETERMINISTIC_RULESET
```

That is LEG_A PASS only.

It does not prove:

```text
LIVE_PRODUCER_BINARY
LIVE_PRODUCER_CONFIG
LIVE_EXECUTION_PATH
```

Those stay LEG_B.

## What this vector must not absorb

```text
DETERMINISTIC_SELECTION != HISTORICAL_EXECUTION
NETWORK_ACCEPTANCE != PRODUCER_CONFIGURATION
FORK_ACTIVATION != FEATURE_EXERCISE
```

No B20 call. No validity tx. No TEE registrar. No registry poller.

52000927 remains first observed block after trigger, not proven first Cobalt-executed block.

## Result schema

```text
COBALT_SELECTION_VECTOR_V0_1
RUN_ID:
BINARY_HASH:
CONFIG_HASH:
OVERRIDES:              NONE
OUTPUT_BYTES:
LEG_A:                  HOLD
LEG_B:                  NOT_IN_SCOPE
OVERALL_SELECTION:      HOLD
```

Fill BINARY_HASH, CONFIG_HASH, and OUTPUT_BYTES from one process. If output bytes match the two canonical lines and overrides stayed empty, promote LEG_A only. Leave the parent selection receipt HOLD until LEG_B exists.
