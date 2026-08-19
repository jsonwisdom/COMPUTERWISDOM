"""Replay-safe normalizer for Microsoft Learn → Gray Baby → ResumeReplay v0.1.

This module normalizes representation only. It MUST NOT:
- assign or upgrade evidence_state
- create authority/employment claims
- infer production operation
- invent missing credential facts

Unknown top-level fields are rejected rather than silently dropped.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


SOURCE_TYPES = {
    "TRAINING_MODULE",
    "LEARNING_PATH",
    "TRANSCRIPT",
    "APPLIED_SKILL",
    "CERTIFICATION",
    "ONLINE_VERIFIABLE_CREDENTIAL",
    "EXECUTION_RECEIPT",
}

TOP_LEVEL_KEYS = {
    "schema_version",
    "provider",
    "identity",
    "source_type",
    "credential",
    "training",
    "scope",
    "limitations",
    "evidence_state",
    "external_witness",
    "execution_receipts",
    "allowed_resume_language",
    "forbidden_promotions",
    "gray_baby",
}


class NormalizationError(ValueError):
    """Raised when input cannot be normalized without inference or data loss."""


def _clean_string(value: Any, *, field: str, allow_none: bool = True) -> str | None:
    if value is None and allow_none:
        return None
    if not isinstance(value, str):
        raise NormalizationError(f"{field}: expected string")
    value = " ".join(value.split())
    if not value:
        if allow_none:
            return None
        raise NormalizationError(f"{field}: empty string not allowed")
    return value


def _clean_string_list(value: Any, *, field: str) -> list[str]:
    if not isinstance(value, list):
        raise NormalizationError(f"{field}: expected list")
    out: list[str] = []
    for idx, item in enumerate(value):
        cleaned = _clean_string(item, field=f"{field}[{idx}]", allow_none=False)
        if cleaned not in out:
            out.append(cleaned)
    return out


def _normalize_mapping(
    value: Any,
    *,
    field: str,
    allowed_keys: set[str],
    string_fields: set[str] = frozenset(),
) -> dict[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise NormalizationError(f"{field}: expected object")
    unknown = set(value) - allowed_keys
    if unknown:
        raise NormalizationError(f"{field}: unknown fields {sorted(unknown)}")
    out: dict[str, Any] = {}
    for key in allowed_keys:
        if key not in value:
            continue
        item = value[key]
        if key in string_fields:
            out[key] = _clean_string(item, field=f"{field}.{key}")
        else:
            out[key] = deepcopy(item)
    return out


def normalize_learn_object(raw_input: dict[str, Any]) -> dict[str, Any]:
    """Normalize one canonical ingestion candidate without assigning proof.

    Safe transformations:
    - deep-copy input
    - normalize whitespace in textual fields
    - de-duplicate scope/limitation/forbidden-promotion lists while preserving order
    - canonicalize source_type casing
    - reject unknown fields instead of silently dropping them

    Explicit non-behavior:
    - evidence_state is copied exactly if present
    - proof, authority, employment, and production states are never inferred
    """
    if not isinstance(raw_input, dict):
        raise NormalizationError("raw_input: expected object")

    unknown = set(raw_input) - TOP_LEVEL_KEYS
    if unknown:
        raise NormalizationError(f"raw_input: unknown fields {sorted(unknown)}")

    source_type_raw = _clean_string(
        raw_input.get("source_type"),
        field="source_type",
        allow_none=False,
    )
    source_type = source_type_raw.upper()
    if source_type not in SOURCE_TYPES:
        raise NormalizationError(f"source_type: unsupported value {source_type!r}")

    out: dict[str, Any] = {}

    # Rail metadata may be normalized, but never proof state.
    out["schema_version"] = _clean_string(
        raw_input.get("schema_version", "0.1"),
        field="schema_version",
        allow_none=False,
    )
    out["provider"] = _clean_string(
        raw_input.get("provider", "Microsoft Learn"),
        field="provider",
        allow_none=False,
    )
    out["source_type"] = source_type

    if "identity" in raw_input:
        out["identity"] = _normalize_mapping(
            raw_input["identity"],
            field="identity",
            allowed_keys={"profile_url", "transcript_url", "display_name"},
            string_fields={"profile_url", "transcript_url", "display_name"},
        )

    if "credential" in raw_input:
        out["credential"] = _normalize_mapping(
            raw_input["credential"],
            field="credential",
            allowed_keys={
                "name",
                "credential_id",
                "verified_url",
                "issue_date",
                "expiration_date",
                "status",
            },
            string_fields={
                "name",
                "credential_id",
                "verified_url",
                "issue_date",
                "expiration_date",
                "status",
            },
        )

    if "training" in raw_input:
        out["training"] = _normalize_mapping(
            raw_input["training"],
            field="training",
            allowed_keys={"title", "topic", "completion_date", "module_url"},
            string_fields={"title", "topic", "completion_date", "module_url"},
        )

    if "scope" in raw_input:
        out["scope"] = _clean_string_list(raw_input["scope"], field="scope")

    if "limitations" in raw_input:
        out["limitations"] = _clean_string_list(
            raw_input["limitations"], field="limitations"
        )

    if "evidence_state" in raw_input:
        # Critical membrane: copy only. Never derive or upgrade here.
        out["evidence_state"] = _clean_string(
            raw_input["evidence_state"],
            field="evidence_state",
            allow_none=False,
        )

    if "external_witness" in raw_input:
        out["external_witness"] = _normalize_mapping(
            raw_input["external_witness"],
            field="external_witness",
            allowed_keys={"witness_type", "url", "observed_at", "sha256"},
            string_fields={"witness_type", "url", "observed_at", "sha256"},
        )

    if "execution_receipts" in raw_input:
        receipts = raw_input["execution_receipts"]
        if not isinstance(receipts, list):
            raise NormalizationError("execution_receipts: expected list")
        out["execution_receipts"] = []
        for idx, receipt in enumerate(receipts):
            normalized = _normalize_mapping(
                receipt,
                field=f"execution_receipts[{idx}]",
                allowed_keys={
                    "system",
                    "repo",
                    "path",
                    "commit",
                    "deployment_receipt",
                    "telemetry_receipt",
                    "state",
                },
                string_fields={
                    "system",
                    "repo",
                    "path",
                    "commit",
                    "deployment_receipt",
                    "telemetry_receipt",
                    "state",
                },
            )
            out["execution_receipts"].append(normalized)

    if "allowed_resume_language" in raw_input:
        out["allowed_resume_language"] = _clean_string(
            raw_input["allowed_resume_language"],
            field="allowed_resume_language",
            allow_none=False,
        )

    if "forbidden_promotions" in raw_input:
        out["forbidden_promotions"] = _clean_string_list(
            raw_input["forbidden_promotions"],
            field="forbidden_promotions",
        )

    if "gray_baby" in raw_input:
        gray_baby = raw_input["gray_baby"]
        if not isinstance(gray_baby, dict):
            raise NormalizationError("gray_baby: expected object")
        allowed = {
            "observer_result",
            "authority_created",
            "employment_created",
            "production_proof_created",
        }
        unknown_gb = set(gray_baby) - allowed
        if unknown_gb:
            raise NormalizationError(
                f"gray_baby: unknown fields {sorted(unknown_gb)}"
            )
        out["gray_baby"] = deepcopy(gray_baby)
        if "observer_result" in out["gray_baby"]:
            out["gray_baby"]["observer_result"] = _clean_string(
                out["gray_baby"]["observer_result"],
                field="gray_baby.observer_result",
                allow_none=False,
            )

    return out
