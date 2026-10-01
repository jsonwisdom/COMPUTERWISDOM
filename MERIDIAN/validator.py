# validator.py
# PROPOSED / NOT CAPTURED / NOT BINDING
#
# This validator performs structural and registry-reference checks only.
# It MUST NOT fetch, re-hash bytes, enrich, infer, or promote evidence.

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ValidationError(Exception):
    code: str
    message: str = ""

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


@dataclass
class VectorResult:
    result: str                 # pass | fail | skip
    reason: Optional[str] = None
    error_code: Optional[str] = None


FORBIDDEN_KEYS = {
    "model_output",
    "llm_output",
    "inferred_conflict",
    "inferred_misconduct",
}


def _walk_keys(obj: Any, path: str = "") -> List[str]:
    keys: List[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            full = f"{path}.{k}" if path else k
            keys.append(full)
            keys.extend(_walk_keys(v, full))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            full = f"{path}[{i}]"
            keys.extend(_walk_keys(v, full))
    return keys


def _index_by_id(items: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {
        item["id"]: item
        for item in items
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def check_forbidden_keys(event: Dict[str, Any]) -> None:
    keys = _walk_keys(event)
    bad = [k for k in keys if k.split(".")[-1] in FORBIDDEN_KEYS]
    if bad:
        raise ValidationError(
            code="FORBIDDEN_FIELD_PRESENT",
            message=f"Forbidden keys present: {bad}",
        )


def check_source_class(
    event: Dict[str, Any],
    raw_captures: Dict[str, Dict[str, Any]],
    *,
    write_path: bool = True,
) -> None:
    src = event.get("source", {})
    cls = src.get("source_class")

    if cls == "captured":
        capture_id = src.get("raw_capture_id")
        content_hash = src.get("content_hash")
        url = src.get("url")

        if not capture_id:
            raise ValidationError(
                code="RAW_CAPTURE_NOT_FOUND",
                message="captured source requires raw_capture_id",
            )
        if not content_hash:
            raise ValidationError(
                code="CAPTURE_HASH_MISMATCH",
                message="captured source requires content_hash",
            )
        if not url:
            raise ValidationError(
                code="CAPTURE_URL_MISSING",
                message="captured source requires url copied from capture",
            )
        if src.get("operator") is not None:
            raise ValidationError(
                code="CAPTURED_OPERATOR_FORBIDDEN",
                message="captured source must not carry operator",
            )

        capture = raw_captures.get(capture_id)
        if capture is None:
            raise ValidationError(
                code="RAW_CAPTURE_NOT_FOUND",
                message="raw_capture_id does not resolve in supplied registry",
            )

        if capture.get("content_hash") != content_hash:
            raise ValidationError(
                code="CAPTURE_HASH_MISMATCH",
                message="event content_hash does not match referenced RAW_CAPTURE_v0",
            )

        if capture.get("url") != url:
            raise ValidationError(
                code="CAPTURE_URL_MISMATCH",
                message="event source.url must equal referenced capture requested/source url",
            )

    elif cls == "operator_relayed":
        if src.get("content_hash") is not None:
            raise ValidationError(
                code="OPERATOR_RELAY_HASH_FORBIDDEN",
                message="operator_relayed must not carry content_hash",
            )
        if src.get("raw_capture_id") is not None:
            raise ValidationError(
                code="OPERATOR_RELAY_CAPTURE_ID_FORBIDDEN",
                message="operator_relayed must not carry raw_capture_id",
            )
        if not src.get("operator"):
            raise ValidationError(
                code="OPERATOR_MISSING",
                message="operator_relayed requires operator",
            )

        status = event.get("verification", {}).get("status")
        if status != "observed":
            raise ValidationError(
                code="OPERATOR_RELAY_VERIFICATION_PROMOTION_FORBIDDEN",
                message="operator_relayed verification.status must be observed",
            )

    elif cls == "migrated_legacy":
        if write_path:
            raise ValidationError(
                code="MIGRATED_LEGACY_WRITE_FORBIDDEN",
                message="migrated_legacy may be emitted only by the migrator",
            )
        if src.get("content_hash") is not None:
            raise ValidationError(
                code="MIGRATED_LEGACY_HASH_BACKFILL_FORBIDDEN",
                message="migration must not backfill content_hash",
            )
        if src.get("raw_capture_id") is not None:
            raise ValidationError(
                code="MIGRATED_LEGACY_CAPTURE_BACKFILL_FORBIDDEN",
                message="migration must not backfill raw_capture_id",
            )

    else:
        raise ValidationError(
            code="SOURCE_CLASS_INVALID",
            message=f"unsupported source_class: {cls!r}",
        )


def check_vector_provenance(vector: Dict[str, Any]) -> None:
    cls = vector.get("source_class")
    content_hash = vector.get("content_hash")

    if content_hash is not None and cls != "captured":
        raise ValidationError(
            code="VECTOR_HASH_WITHOUT_CAPTURE",
            message="non-captured vector must not carry content_hash",
        )

    if vector.get("binding") != "proposed":
        raise ValidationError(
            code="VECTOR_BINDING_NOT_PROPOSED",
            message="current validator vector lane is proposed-only",
        )


def _check_supersede_cycle(
    candidate_id: str,
    target_id: str,
    events: Dict[str, Dict[str, Any]],
) -> None:
    seen = set()
    current_id: Optional[str] = target_id

    while current_id:
        if current_id == candidate_id:
            raise ValidationError(
                code="SUPERSEDE_CYCLE",
                message="supersede cycle detected",
            )
        if current_id in seen:
            # Existing registry cycle is itself invalid; fail closed.
            raise ValidationError(
                code="SUPERSEDE_CYCLE",
                message="cycle already present in supersession chain",
            )
        seen.add(current_id)

        current = events.get(current_id)
        if current is None:
            return
        if current.get("record_operation") not in {"correct", "retract", "supersede"}:
            return
        next_id = current.get("supersedes")
        current_id = next_id if isinstance(next_id, str) else None


def check_supersede(
    event: Dict[str, Any],
    events: Dict[str, Dict[str, Any]],
    raw_captures: Dict[str, Dict[str, Any]],
) -> None:
    """V7 path: non-captured superseding record must fail on the capture rule."""

    if event.get("record_operation") != "supersede":
        return

    target_id = event.get("supersedes")
    if not isinstance(target_id, str) or not target_id:
        raise ValidationError(
            code="SUPERSEDE_TARGET_MISSING",
            message="supersede requires supersedes event_id",
        )

    event_id = event.get("id")
    if target_id == event_id:
        raise ValidationError(
            code="SUPERSEDE_SELF",
            message="supersede cannot target self",
        )

    target = events.get(target_id)
    if target is None:
        raise ValidationError(
            code="SUPERSEDE_TARGET_MISSING",
            message="supersede target not found in supplied registry",
        )

    # Ensure V7's target-side preconditions are valid first.
    check_source_class(target, raw_captures, write_path=False)

    if isinstance(event_id, str):
        _check_supersede_cycle(event_id, target_id, events)

    if event.get("source", {}).get("source_class") != "captured":
        raise ValidationError(
            code="SUPERSEDE_REQUIRES_CAPTURED_SOURCE",
            message="supersede requires captured source_class on the new record",
        )


def run_vector(
    vector: Dict[str, Any],
    event: Dict[str, Any],
    registry: Dict[str, List[Dict[str, Any]]],
) -> VectorResult:
    """
    Execute a single proposed vector against supplied in-memory fixture data.

    No network fetch.
    No byte hash recomputation.
    No enrichment.
    No evidence promotion.
    """

    vid = vector.get("id")
    expects = vector.get("expects")

    if vid == "V3":
        return VectorResult(
            result="skip",
            reason="MIGRATION_NOT_IMPLEMENTED",
        )

    if vid == "V13":
        return VectorResult(
            result="skip",
            reason="COLLIDER_INPUT_SOURCE_CLASSES_ABSENT",
        )

    try:
        check_vector_provenance(vector)

        raw_captures = _index_by_id(registry.get("raw_captures", []))
        events = _index_by_id(registry.get("events", []))

        check_forbidden_keys(event)
        check_source_class(event, raw_captures, write_path=True)

        if vid == "V7":
            check_supersede(event, events, raw_captures)

        outcome = "pass"
        error_code = None

    except ValidationError as exc:
        outcome = "fail"
        error_code = exc.code

        if vid == "V7" and exc.code != "SUPERSEDE_REQUIRES_CAPTURED_SOURCE":
            return VectorResult(
                result="fail",
                reason="V7_WRONG_FAILURE_CODE",
                error_code=exc.code,
            )

    if expects == "fail" and outcome != "fail":
        return VectorResult(
            result="fail",
            reason="EXPECTED_FAIL_BUT_DID_NOT_FAIL",
            error_code=error_code,
        )

    if expects == "pass" and outcome != "pass":
        return VectorResult(
            result="fail",
            reason="EXPECTED_PASS_BUT_FAILED",
            error_code=error_code,
        )

    if expects == "skip":
        return VectorResult(
            result="skip",
            reason="VECTOR_DECLARED_SKIP",
            error_code=error_code,
        )

    return VectorResult(
        result=outcome,
        error_code=error_code,
    )
