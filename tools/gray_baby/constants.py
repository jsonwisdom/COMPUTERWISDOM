"""Shared vocabulary for the Gray Baby batch replay orchestrator.

Names follow the replay kernel (authority false, boundary NONE),
REPLAY_RECEIPT_SPEC_V1, and the Gray Baby gap-observer docs.
"""

from __future__ import annotations

PRODUCT = "GRAY_BABY_BULK_REPLAY_V1"
FACTORY = "GRAY_BABY_REPLAY_FACTORY_V1"
ROLE = "BATCH_REPLAY_ORCHESTRATOR"
SPEC = "REPLAY_RECEIPT_SPEC_V1"
SCHEMA_VERSION_BATCH = "GRAY_BABY_BATCH_RECEIPT_V1"
SCHEMA_VERSION_OBJECT = "GRAY_BABY_OBJECT_STATE_V1"
SCHEMA_VERSION_OPERATOR = "GRAY_BABY_OPERATOR_RESULT_V1"
SCHEMA_VERSION_ALIEN = "GRAY_BABY_ALIEN_CASE_V1"
SCHEMA_VERSION_SCOREBOARD = "GRAY_BABY_SCOREBOARD_V1"

AUTHORITY_CREATED = False
DEFAULT_ACCESS = "READ_ONLY"
REPLAY_MODE = "evidence_reexamination"
NETWORK = "NONE"

# Lower index is a stronger receipt. A stronger receipt may be recorded as a
# new receipt. A weaker receipt cannot erase or override a stronger one.
SOURCE_ORDER = (
    "RAW_CHAIN",
    "REPO_RECEIPTS",
    "DRIVE_HISTORY",
    "PUBLIC_INDEXES",
    "PAGE_LABELS",
)
SOURCE_RANK = {name: index for index, name in enumerate(SOURCE_ORDER)}

GAME_STATES = (
    "CLEAN",
    "UPGRADED",
    "CORRECTED",
    "DEMOTED",
    "HOLD",
    "CONFLICT",
    "INDEXER_DRIFT",
    "TEMPORAL_DRIFT",
    "ROLE_COLLAPSE",
    "MISSING_RECEIPT",
    "ALIEN",
)

# CLEAN / correction family -> receipt. HOLD family -> queue.
# Contradiction family -> specialist. ALIEN -> deep replay.
ROUTES = {
    "CLEAN": "RECEIPT",
    "UPGRADED": "RECEIPT",
    "CORRECTED": "RECEIPT",
    "DEMOTED": "RECEIPT",
    "HOLD": "QUEUE",
    "MISSING_RECEIPT": "QUEUE",
    "CONFLICT": "SPECIALIST",
    "INDEXER_DRIFT": "SPECIALIST",
    "TEMPORAL_DRIFT": "SPECIALIST",
    "ROLE_COLLAPSE": "SPECIALIST",
    "ALIEN": "DEEP_REPLAY",
}

CHEAP_LANE = (
    "OBJECT_SELECTOR",
    "TEMPORAL_GUARD",
    "CHAIN_BINDER",
    "RECEIPT_COMPARATOR",
    "DELTA_CLASSIFIER",
)

OPERATORS = (
    "OBJECT_SELECTOR",
    "TEMPORAL_GUARD",
    "SOURCE_RANKER",
    "CHAIN_BINDER",
    "TX_ORIGIN_FINDER",
    "ERC4337_DECODER",
    "CREATE2_DECODER",
    "INITIALIZER_DECODER",
    "EVENT_TOPIC_DECODER",
    "METADATA_BINDER",
    "INDEXER_DRIFT_DETECTOR",
    "EXPORT_VERSION_GUARD",
    "ROLE_COLLAPSE_SENTINEL",
    "IDENTITY_MEMBRANE",
    "RECEIPT_COMPARATOR",
    "DELTA_CLASSIFIER",
    "ALIEN_ROUTER",
    "REPLAY_RECEIPT_WRITER",
    "BATCH_SCOREKEEPER",
    "REGRESSION_SENTINEL",
)

SPECIALISTS = (
    "CHAIN",
    "ZORA",
    "ERC4337",
    "UNISWAP_V4",
    "IPFS",
    "GITHUB_RECEIPT",
    "DRIVE_HISTORY",
    "TEMPORAL",
    "PROVENANCE",
    "CONTRADICTION",
    "SCHEMA",
    "TEST",
    "ADVERSARIAL",
    "GRAY_BABY",
    "ALIEN",
    "HUMAN_REVIEW_GATE",
)

RULES = (
    "SEARCH_MISS_CANNOT_DELETE",
    "WEAKER_SOURCE_CANNOT_OVERRIDE",
    "WALLET_CANNOT_PROMOTE_TO_HUMAN",
    "OLD_SNAPSHOT_CANNOT_FALSIFY_LATER",
    "MISSING_DATA_CANNOT_BE_FABRICATED",
)

DESIGN_BATCH_SIZE = 32
DESIGN_INVENTORY_SIZE = 1024
HUMAN_SUMMARY_REF = "docs/gray-baby/REPLAY_FACTORY_V1.md"
CANONICALIZATION = "UTF-8 canonical_json sort_keys separators=(',', ':')"
CLOCK = "INPUT_TIMESTAMPS_ONLY"
SCOREKEEPER_NOTE = (
    "BATCH_SCOREKEEPER runs after this receipt is sealed and records itself "
    "on the scoreboard. This receipt does not claim the scorekeeper already ran."
)
FIXTURE_NOTE = (
    "No 1024-object inventory is stored in this repo. The default input is a "
    "small synthetic fixture labeled SYNTHETIC_TEST_ONLY. Chain fields in that "
    "fixture are not real chain data and must not be treated as receipts."
)

_UNROUTED = [state for state in GAME_STATES if state not in ROUTES]
if _UNROUTED:
    raise RuntimeError(f"unhandled game states: {_UNROUTED}")
