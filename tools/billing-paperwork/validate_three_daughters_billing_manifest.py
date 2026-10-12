#!/usr/bin/env python3
"""Fail-closed validator for the public Three Daughters billing manifest."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "THREE_DAUGHTERS_BILLING_PAPERWORK_V0_1"
STATUSES = {"PASS", "HOLD", "REJECT", "CONFLICT"}
PRECEDENCE = {"PASS": 0, "HOLD": 1, "CONFLICT": 2, "REJECT": 3}
DOCUMENT_CLASSES = {
    "UNKNOWN",
    "QUOTE",
    "INVOICE",
    "PURCHASE_ORDER",
    "CONTRACT_NOTICE",
    "REIMBURSEMENT_REQUEST",
    "PAYMENT_APPROVAL",
    "PAYMENT_WITNESS",
    "RECEIPT",
    "TAX_RECORD",
    "BANK_RECORD",
    "OTHER",
}
ALLOWED_CHOICES = {"RECEIPT_READER", "QUESTION_KEEPER", "REPLAY_WITNESS", "NONE"}
BANNED_PRIVATE_KEYS = {
    "name",
    "full_name",
    "daughter_name",
    "email",
    "email_address",
    "phone",
    "phone_number",
    "street_address",
    "home_address",
    "account_number",
    "routing_number",
    "tax_id",
    "ssn",
    "date_of_birth",
    "credential",
    "credentials",
    "private_key",
    "seed_phrase",
}


def _walk_keys(value: Any, path: str = "$"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield path, str(key)
            yield from _walk_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_keys(child, f"{path}[{index}]")


def _require_bool(container: dict[str, Any], key: str, expected: bool, errors: list[str], prefix: str) -> None:
    if container.get(key) is not expected:
        errors.append(f"{prefix}.{key} must be {str(expected).lower()}")


def validate(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["root must be a JSON object"]

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must equal {SCHEMA_VERSION}")
    if data.get("status") != "DRAFT_OBSERVER_ORGANIZER":
        errors.append("status must remain DRAFT_OBSERVER_ORGANIZER")
    if data.get("authority") is not False:
        errors.append("authority must be false")
    if data.get("default_disposition") != "HOLD":
        errors.append("default_disposition must be HOLD")
    if data.get("document_class") not in DOCUMENT_CLASSES:
        errors.append("document_class is not allowed")

    for object_path, key in _walk_keys(data):
        if key.lower() in BANNED_PRIVATE_KEYS:
            errors.append(f"private key name is prohibited at {object_path}.{key}")

    source = data.get("source_pointer")
    if not isinstance(source, dict):
        errors.append("source_pointer must be an object")
    else:
        if source.get("provider") not in {"NONE", "GOOGLE_DRIVE_PRIVATE", "GITHUB_PUBLIC_SCHEMA", "OTHER_PRIVATE"}:
            errors.append("source_pointer.provider is not allowed")
        if source.get("opaque_id") != "UNSET":
            errors.append("public template source_pointer.opaque_id must remain UNSET")
        digest = source.get("content_sha256")
        if digest != "UNSET" and not (isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest)):
            errors.append("content_sha256 must be UNSET or lowercase SHA-256")

    public = data.get("public_boundary")
    if not isinstance(public, dict):
        errors.append("public_boundary must be an object")
    else:
        _require_bool(public, "private_content_committed", False, errors, "public_boundary")
        _require_bool(public, "public_metadata_only", True, errors, "public_boundary")
        _require_bool(public, "connector_accounts_assumed_unified", False, errors, "public_boundary")

    family = data.get("family_superposition")
    if not isinstance(family, dict):
        errors.append("family_superposition must be an object")
    else:
        if family.get("mode") != "SUPERPOSITION":
            errors.append("family_superposition.mode must be SUPERPOSITION")
        _require_bool(family, "participants_named", False, errors, "family_superposition")
        _require_bool(family, "public_assignment_collapse_allowed", False, errors, "family_superposition")
        _require_bool(family, "session_local_choice_required", True, errors, "family_superposition")
        _require_bool(family, "authorized_adult_supervision_required", True, errors, "family_superposition")
        _require_bool(family, "silence_is_consent", False, errors, "family_superposition")
        _require_bool(family, "refusal_penalty", False, errors, "family_superposition")
        mirrors = family.get("mirrors")
        if not isinstance(mirrors, list) or len(mirrors) != 3:
            errors.append("family_superposition.mirrors must contain exactly three mirrors")
        else:
            ids: list[str] = []
            for index, mirror in enumerate(mirrors):
                prefix = f"family_superposition.mirrors[{index}]"
                if not isinstance(mirror, dict):
                    errors.append(f"{prefix} must be an object")
                    continue
                ids.append(str(mirror.get("mirror_id")))
                if mirror.get("state") != "UNASSIGNED":
                    errors.append(f"{prefix}.state must remain UNASSIGNED in public artifacts")
                choices = mirror.get("allowed_choices")
                if not isinstance(choices, list) or set(choices) != ALLOWED_CHOICES or len(choices) != 4:
                    errors.append(f"{prefix}.allowed_choices must contain the four exact choices")
            if set(ids) != {"A", "B", "C"} or len(ids) != len(set(ids)):
                errors.append("mirror_id values must be exactly A, B, and C")

    financial = data.get("financial_state")
    if not isinstance(financial, dict):
        errors.append("financial_state must be an object")
    else:
        for key in (
            "document_approved",
            "payment_authorized",
            "payment_executed",
            "transaction_witness_present",
            "settlement_claimed",
        ):
            _require_bool(financial, key, False, errors, "financial_state")

    connectors = data.get("connector_boundaries")
    if not isinstance(connectors, dict):
        errors.append("connector_boundaries must be an object")
    else:
        _require_bool(connectors, "github_public_schema_only", True, errors, "connector_boundaries")
        _require_bool(connectors, "google_drive_mutation_authorized", False, errors, "connector_boundaries")
        if connectors.get("google_drive_target_folder_id") != "UNSET":
            errors.append("google_drive_target_folder_id must remain UNSET")
        _require_bool(connectors, "openai_advisory_only", True, errors, "connector_boundaries")
        _require_bool(connectors, "openai_private_content_allowed", False, errors, "connector_boundaries")

    multi = data.get("leeloo_multi_pass")
    lane_keys = (
        "record_reality",
        "authority_law",
        "execution_resources_money",
        "oversight_correction",
        "time_gap_version",
        "cross_edges",
    )
    if not isinstance(multi, dict):
        errors.append("leeloo_multi_pass must be an object")
    else:
        lane_values: list[str] = []
        for key in lane_keys:
            value = multi.get(key)
            if value not in STATUSES:
                errors.append(f"leeloo_multi_pass.{key} must be PASS, HOLD, REJECT, or CONFLICT")
            else:
                lane_values.append(value)
        overall = multi.get("overall")
        if overall not in STATUSES:
            errors.append("leeloo_multi_pass.overall must be PASS, HOLD, REJECT, or CONFLICT")
        if len(lane_values) == len(lane_keys) and overall in STATUSES:
            expected = max(lane_values, key=lambda value: PRECEDENCE[value])
            if overall != expected:
                errors.append(f"leeloo_multi_pass.overall must be {expected} from fail-closed precedence")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {Path(argv[0]).name} MANIFEST.json", file=sys.stderr)
        return 2
    manifest_path = Path(argv[1])
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"REJECT: cannot read valid JSON: {exc}", file=sys.stderr)
        return 1
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"REJECT: {error}", file=sys.stderr)
        return 1
    print("PASS: public billing paperwork manifest is fail-closed and authority=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))


