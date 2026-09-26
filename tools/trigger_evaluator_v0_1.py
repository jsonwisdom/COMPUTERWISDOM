"""
tools/trigger_evaluator_v0_1.py
Receipt-gated trigger evaluator for watch_trigger_engine_v0_1.

Statuses are exactly MAINTAIN, OBSERVE, and TRANSITION_READY.
There is no HOLD status and no fourth outcome.

evaluate() enforces the evaluation contract itself. It does not assume an
upstream caller ran the JSON schemas. Contract violations raise
TriggerEvaluationRejected (a ValueError). They are not coerced into MAINTAIN
or OBSERVE, and authority:true is not rewritten to false.

The contract is the canonical trigger and watch-receipt schemas
(schemas/trigger_v0_1.schema.json, schemas/watch_receipt_v0_1.schema.json):
every present field must satisfy its property schema, unknown fields are
rejected, and decision fields are always required. Archival receipt fields
that the original three state vectors omit (watch_id, collected_at,
source_url, hash, authority) stay optional unless the caller supplied a
schema that requires them. Any value that is present is still checked, so
authority other than false, a bad hash, or a bad identifier is rejected.

hostname, date-time, and uri are checked explicitly. The jsonschema build
used by the watch-trigger CI job does not register those format checkers.
Transitions must be strict upgrades (to_level > from_level). The trigger
schema allows same-level and downgrade integers; evaluate() does not.

Returned authority is always false.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple
from urllib.parse import urlparse

import jsonschema
from jsonschema import Draft202012Validator


class TriggerEvaluationRejected(ValueError):
    """Raised when a trigger or receipt is not safe to evaluate.

    This is the rejection signal for evaluate(). It is not an evaluation
    status. MAINTAIN still means two contract-valid inputs whose domains
    differ.
    """


_SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"
_TRIGGER_SCHEMA_PATH = _SCHEMA_DIR / "trigger_v0_1.schema.json"
_RECEIPT_SCHEMA_PATH = _SCHEMA_DIR / "watch_receipt_v0_1.schema.json"

# Decision fields the original unit vectors always carry. Full-schema
# archival requirements are applied when the caller passes that schema.
_TRIGGER_DECISION_REQUIRED = (
    "trigger_id",
    "source_domain",
    "artifact_type",
    "state_transition",
)
_RECEIPT_DECISION_REQUIRED = (
    "source_domain",
    "artifact_type",
    "verified",
)

_CONSTRAINT_KEYS = frozenset(
    {
        "$ref",
        "allOf",
        "anyOf",
        "const",
        "enum",
        "format",
        "not",
        "oneOf",
        "pattern",
        "properties",
        "required",
        "type",
    }
)

_HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$"
)
_DATE_TIME_RE = re.compile(
    r"^(?P<dt>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})"
    r"(?P<frac>\.\d+)?"
    r"(?P<tz>Z|[+-]\d{2}:\d{2})$"
)


def _load_schema(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _decision_schema(schema: Mapping[str, Any], required: Tuple[str, ...]) -> Dict[str, Any]:
    narrowed = dict(schema)
    narrowed["required"] = list(required)
    return narrowed


def _is_hostname(value: str) -> bool:
    return _HOSTNAME_RE.fullmatch(value) is not None


def _is_date_time(value: str) -> bool:
    match = _DATE_TIME_RE.fullmatch(value)
    if match is None:
        return False
    tz = match.group("tz")
    if tz == "Z":
        tz = "+00:00"
    frac = match.group("frac") or ""
    try:
        datetime.fromisoformat(f"{match.group('dt')}{frac}{tz}")
    except ValueError:
        return False
    return True


def _is_uri(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme) and bool(parsed.netloc or parsed.path)


_FORMAT_CHECKS = {
    "hostname": _is_hostname,
    "date-time": _is_date_time,
    "uri": _is_uri,
}


def _schema_constrains(schema: Any) -> bool:
    return isinstance(schema, dict) and bool(_CONSTRAINT_KEYS.intersection(schema))


def _validate_instance(validator: Any, instance: Dict[str, Any], label: str) -> None:
    try:
        validator.validate(instance)
    except jsonschema.ValidationError as exc:
        path = ".".join(str(part) for part in exc.absolute_path)
        where = f"{label}.{path}" if path else label
        raise TriggerEvaluationRejected(f"{where} rejected: {exc.message}") from exc


def _enforce_format(label: str, key: str, fmt: str, value: str) -> None:
    check = _FORMAT_CHECKS.get(fmt)
    if check is None:
        raise TriggerEvaluationRejected(f"{label}.{key} rejected: unsupported format {fmt}")
    if not check(value):
        raise TriggerEvaluationRejected(f"{label}.{key} rejected: invalid {fmt}")


def _enforce_formats(instance: Mapping[str, Any], schema: Mapping[str, Any], label: str) -> None:
    properties = schema["properties"]
    for key, value in instance.items():
        fmt = properties[key].get("format")
        if isinstance(fmt, str) and isinstance(value, str):
            _enforce_format(label, key, fmt, value)


def _require_object(value: Any, label: str) -> None:
    if isinstance(value, dict):
        return
    raise TriggerEvaluationRejected(f"{label} must be an object")


def _require_upgrade(state_transition: Mapping[str, Any]) -> Tuple[int, int]:
    from_level = state_transition["from_level"]
    to_level = state_transition["to_level"]
    if type(from_level) is not int or type(to_level) is not int:
        raise TriggerEvaluationRejected(
            "state_transition from_level and to_level must be integers"
        )
    if to_level == from_level:
        raise TriggerEvaluationRejected(
            "state_transition same-level rejected: to_level must be greater than from_level"
        )
    if to_level < from_level:
        raise TriggerEvaluationRejected(
            "state_transition downgrade rejected: to_level must be greater than from_level"
        )
    return from_level, to_level


def _enforce_caller_schema(instance: Dict[str, Any], schema: Any, label: str) -> None:
    if not _schema_constrains(schema):
        return
    validator_cls = jsonschema.validators.validator_for(schema)
    _validate_instance(validator_cls(schema), instance, label)


_TRIGGER_CANONICAL = _load_schema(_TRIGGER_SCHEMA_PATH)
_RECEIPT_CANONICAL = _load_schema(_RECEIPT_SCHEMA_PATH)
_TRIGGER_DECISION_SCHEMA = _decision_schema(_TRIGGER_CANONICAL, _TRIGGER_DECISION_REQUIRED)
_RECEIPT_DECISION_SCHEMA = _decision_schema(_RECEIPT_CANONICAL, _RECEIPT_DECISION_REQUIRED)
Draft202012Validator.check_schema(_TRIGGER_DECISION_SCHEMA)
Draft202012Validator.check_schema(_RECEIPT_DECISION_SCHEMA)
_TRIGGER_DECISION_VALIDATOR = Draft202012Validator(_TRIGGER_DECISION_SCHEMA)
_RECEIPT_DECISION_VALIDATOR = Draft202012Validator(_RECEIPT_DECISION_SCHEMA)


class TriggerEvaluator:
    def __init__(self, trigger_schema: Dict[str, Any], receipt_schema: Dict[str, Any]):
        self.trigger_schema = trigger_schema
        self.receipt_schema = receipt_schema
        self.authority = False

    def evaluate(self, trigger: Any, receipt: Any) -> Dict[str, Any]:
        """
        Evaluate trigger against receipt per the three-state table.

        States, only after the contract checks pass:
        - MAINTAIN: domains differ
        - OBSERVE: domains match, but artifact types differ or verified is false
        - TRANSITION_READY: domains and artifact types match and verified is true

        state_transition is true only in TRANSITION_READY.
        authority on the result is false.
        """
        _require_object(trigger, "trigger")
        _require_object(receipt, "receipt")
        _validate_instance(_TRIGGER_DECISION_VALIDATOR, trigger, "trigger")
        _validate_instance(_RECEIPT_DECISION_VALIDATOR, receipt, "receipt")
        _enforce_formats(trigger, _TRIGGER_CANONICAL, "trigger")
        _enforce_formats(receipt, _RECEIPT_CANONICAL, "receipt")
        from_level, to_level = _require_upgrade(trigger["state_transition"])
        _enforce_caller_schema(trigger, self.trigger_schema, "trigger")
        _enforce_caller_schema(receipt, self.receipt_schema, "receipt")

        result: Dict[str, Any] = {
            "status": "MAINTAIN",
            "state_transition": False,
            "from_level": None,
            "to_level": None,
            "authority": False,
        }

        if trigger["source_domain"] != receipt["source_domain"]:
            return result

        if trigger["artifact_type"] != receipt["artifact_type"] or receipt["verified"] is not True:
            result["status"] = "OBSERVE"
            return result

        result["status"] = "TRANSITION_READY"
        result["state_transition"] = True
        result["from_level"] = from_level
        result["to_level"] = to_level
        return result
