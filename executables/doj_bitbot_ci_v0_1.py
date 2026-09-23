#!/usr/bin/env python3
"""DOJ BitBot v0.1 deterministic CI substrate.

Reads existing immutable observation and replay records, revalidates their
linkage, and emits a zero-authority verdict certificate.

This module performs no fetches, no replays, and no source-verification
promotion.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import doj_bitbot_fetch_v0_1 as fetch_stage
import doj_bitbot_replay_v0_1 as replay_stage

SPECIMEN_ROOT = Path("internal-rules-schism") / "poc"


class EvidenceIntegrityError(RuntimeError):
    pass


class EvidenceAmbiguityError(RuntimeError):
    pass


@dataclass(frozen=True)
class CiCertificate:
    ci_id: str
    target: str
    rule_specimen_id: Optional[str]
    latest_observation_id: Optional[str]
    latest_observation_state: Optional[str]
    latest_replay_id: Optional[str]
    latest_replay_content_result: Optional[str]
    latest_replay_availability: Optional[str]
    verdict: str
    verdict_reason: str
    primary_source_verified: bool = False
    authority_created: bool = False
    schema: str = "doj.bitbot.ci.v0.1"

    def __post_init__(self) -> None:
        if self.authority_created:
            raise AssertionError("DOJ BitBot CI may never create authority")
        if self.primary_source_verified:
            raise AssertionError(
                "DOJ BitBot CI v0.1 may never promote primary-source verification"
            )
        if self.schema != "doj.bitbot.ci.v0.1":
            raise AssertionError("Unexpected DOJ BitBot CI schema")


def _canonical_json_bytes(value: dict) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")


def _finalize_certificate(cert: CiCertificate) -> CiCertificate:
    payload = asdict(cert)
    payload["ci_id"] = ""
    digest = hashlib.sha256(_canonical_json_bytes(payload)).hexdigest()
    return replace(cert, ci_id=f"DOJ-CI-{digest[:12].upper()}")


def _certificate(
    *,
    target: str,
    rule_specimen_id: Optional[str],
    verdict: str,
    verdict_reason: str,
    observation=None,
    replay=None,
) -> CiCertificate:
    cert = CiCertificate(
        ci_id="PENDING",
        target=target,
        rule_specimen_id=rule_specimen_id,
        latest_observation_id=(
            observation.observation_id if observation is not None else None
        ),
        latest_observation_state=(
            observation.state if observation is not None else None
        ),
        latest_replay_id=(replay.replay_id if replay is not None else None),
        latest_replay_content_result=(
            replay.content_result if replay is not None else None
        ),
        latest_replay_availability=(
            replay.availability_transition if replay is not None else None
        ),
        verdict=verdict,
        verdict_reason=verdict_reason,
        primary_source_verified=False,
        authority_created=False,
    )
    return _finalize_certificate(cert)


def _validate_target_url(target: str) -> str:
    parsed = urlparse(target)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("target URL must be absolute http(s)")
    return target


def _load_observations_for_target(target_url: str):
    observations = []
    if not fetch_stage.OBSERVATIONS_DIR.exists():
        return observations

    for path in sorted(fetch_stage.OBSERVATIONS_DIR.glob("DOJ-OBS-*.json")):
        try:
            obs, _, _ = replay_stage._load_stored_observation(path.stem)
        except Exception as exc:
            raise EvidenceIntegrityError(
                f"Invalid observation record {path.name}: {exc}"
            ) from exc

        if obs.observed_at.tzinfo is None:
            raise EvidenceIntegrityError(
                f"Observation {obs.observation_id} has naive timestamp"
            )

        if obs.state == "OBSERVED_BYTES" and not replay_stage._verify_observed_object(obs):
            raise EvidenceIntegrityError(
                f"Observation object integrity failed: {obs.observation_id}"
            )

        if obs.requested_url == target_url:
            observations.append(obs)

    return observations


def _parse_replay_record(path: Path):
    file_bytes = path.read_bytes()
    try:
        data = json.loads(file_bytes.decode("utf-8"))
        receipt = replay_stage.ReplayReceipt(
            replay_id=data["replay_id"],
            first_observation_id=data["first_observation_id"],
            first_observation_sha256=data["first_observation_sha256"],
            second_observation_id=data["second_observation_id"],
            second_observation_sha256=data["second_observation_sha256"],
            requested_url=data["requested_url"],
            first_state=data["first_state"],
            second_state=data["second_state"],
            first_source_sha256=data["first_source_sha256"],
            second_source_sha256=data["second_source_sha256"],
            content_result=data["content_result"],
            availability_transition=data["availability_transition"],
            resolved_url_comparable=data["resolved_url_comparable"],
            resolved_url_changed=data["resolved_url_changed"],
            redirect_chain_comparable=data["redirect_chain_comparable"],
            redirect_chain_changed=data["redirect_chain_changed"],
            authority_created=data["authority_created"],
            schema=data["schema"],
        )
    except Exception as exc:
        raise EvidenceIntegrityError(
            f"Invalid replay receipt {path.name}: {exc}"
        ) from exc

    if path.stem != receipt.replay_id:
        raise EvidenceIntegrityError(
            f"Replay identity mismatch: filename {path.stem}, stored {receipt.replay_id}"
        )

    try:
        first, first_hash, _ = replay_stage._load_stored_observation(
            receipt.first_observation_id
        )
        second, second_hash, _ = replay_stage._load_stored_observation(
            receipt.second_observation_id
        )
    except Exception as exc:
        raise EvidenceIntegrityError(
            f"Replay {receipt.replay_id} references invalid observation: {exc}"
        ) from exc

    if first_hash != receipt.first_observation_sha256:
        raise EvidenceIntegrityError(
            f"Replay {receipt.replay_id} first observation hash mismatch"
        )
    if second_hash != receipt.second_observation_sha256:
        raise EvidenceIntegrityError(
            f"Replay {receipt.replay_id} second observation hash mismatch"
        )

    if not (
        receipt.requested_url
        == first.requested_url
        == second.requested_url
    ):
        raise EvidenceIntegrityError(
            f"Replay {receipt.replay_id} target linkage mismatch"
        )

    if second.observed_at < first.observed_at:
        raise EvidenceIntegrityError(
            f"Replay {receipt.replay_id} observation chronology inverted"
        )

    if first.state == "OBSERVED_BYTES" and not replay_stage._verify_observed_object(first):
        raise EvidenceIntegrityError(
            f"Replay {receipt.replay_id} first object integrity failed"
        )
    if second.state == "OBSERVED_BYTES" and not replay_stage._verify_observed_object(second):
        raise EvidenceIntegrityError(
            f"Replay {receipt.replay_id} second object integrity failed"
        )

    first_verified = replay_stage._verify_observed_object(first)
    second_verified = replay_stage._verify_observed_object(second)
    expected_content = replay_stage._content_result(
        first, second, first_verified, second_verified
    )
    expected_availability = replay_stage._availability_transition(first, second)
    expected_resolved_comp, expected_resolved_changed = (
        replay_stage._resolution_comparison(first, second)
    )
    expected_redirect_comp, expected_redirect_changed = (
        replay_stage._redirect_comparison(first, second)
    )

    expected_fields = {
        "first_state": first.state,
        "second_state": second.state,
        "first_source_sha256": first.sha256,
        "second_source_sha256": second.sha256,
        "content_result": expected_content,
        "availability_transition": expected_availability,
        "resolved_url_comparable": expected_resolved_comp,
        "resolved_url_changed": expected_resolved_changed,
        "redirect_chain_comparable": expected_redirect_comp,
        "redirect_chain_changed": expected_redirect_changed,
    }
    for field, expected in expected_fields.items():
        if getattr(receipt, field) != expected:
            raise EvidenceIntegrityError(
                f"Replay {receipt.replay_id} field {field} does not re-derive"
            )

    return receipt


def _replays_ending_at(observation_id: str, target_url: str):
    if not replay_stage.REPLAYS_DIR.exists():
        return []

    matches = []
    for path in sorted(replay_stage.REPLAYS_DIR.glob("DOJ-REPLAY-*.json")):
        receipt = _parse_replay_record(path)
        if (
            receipt.second_observation_id == observation_id
            and receipt.requested_url == target_url
        ):
            matches.append(receipt)

    if len(matches) > 1:
        raise EvidenceAmbiguityError(
            f"Multiple replay receipts terminate at observation {observation_id}"
        )
    return matches


def _map_replay_verdict(receipt):
    content = receipt.content_result
    availability = receipt.availability_transition

    if content == "EXACT" and availability == "AVAILABLE_TO_AVAILABLE":
        return (
            "STABLE_AVAILABLE",
            "Latest replay revalidates exact source bytes and availability.",
        )
    if content == "CHANGED" and availability == "AVAILABLE_TO_AVAILABLE":
        return (
            "SOURCE_CHANGED",
            "Latest replay observed different verified source bytes.",
        )
    if availability == "AVAILABLE_TO_MISSING":
        return (
            "SOURCE_DISAPPEARED",
            "Latest replay transitioned from observed bytes to HTTP 404.",
        )
    if availability == "MISSING_TO_AVAILABLE":
        return (
            "SOURCE_APPEARED",
            "Latest replay transitioned from HTTP 404 to observed bytes.",
        )
    if availability == "AVAILABLE_TO_BLOCKED":
        return (
            "SOURCE_BLOCKED",
            "Latest replay transitioned from observed bytes to HTTP access failure.",
        )
    if availability == "BLOCKED_TO_AVAILABLE":
        return (
            "SOURCE_BECAME_AVAILABLE",
            "Latest replay transitioned from HTTP access failure to observed bytes.",
        )
    if availability == "NETWORK_FAILURE":
        return (
            "FETCH_FAILURE",
            "Latest replay could not observe the target because of a network/transport failure.",
        )
    return (
        "OBSERVATION_ANOMALY",
        "Latest replay is valid but does not map to a promoted v0.1 verdict.",
    )


def _evaluate_url(target_url: str, rule_specimen_id: Optional[str] = None):
    target_url = _validate_target_url(target_url)
    observations = _load_observations_for_target(target_url)

    if not observations:
        return _certificate(
            target=target_url,
            rule_specimen_id=rule_specimen_id,
            verdict="PENDING_FIRST_FETCH",
            verdict_reason="No stored observation exists for this target.",
        )

    observations.sort(key=lambda obs: (obs.observed_at, obs.observation_id))
    latest = observations[-1]

    replays = _replays_ending_at(latest.observation_id, target_url)
    if replays:
        replay = replays[0]
        verdict, reason = _map_replay_verdict(replay)
        return _certificate(
            target=target_url,
            rule_specimen_id=rule_specimen_id,
            observation=latest,
            replay=replay,
            verdict=verdict,
            verdict_reason=reason,
        )

    if latest.state == "OBSERVED_BYTES":
        return _certificate(
            target=target_url,
            rule_specimen_id=rule_specimen_id,
            observation=latest,
            verdict="REPLAY_REQUIRED",
            verdict_reason="Latest source bytes were observed but have not been replayed.",
        )

    return _certificate(
        target=target_url,
        rule_specimen_id=rule_specimen_id,
        observation=latest,
        verdict="FETCH_FAILURE",
        verdict_reason=f"Latest observation is fail-closed in state {latest.state}.",
    )


def _resolve_rule_specimen(specimen_id: str):
    matches = []
    if SPECIMEN_ROOT.exists():
        for path in sorted(SPECIMEN_ROOT.glob("**/rule.json")):
            try:
                data = json.loads(path.read_bytes().decode("utf-8"))
            except Exception as exc:
                raise EvidenceIntegrityError(
                    f"Invalid rule specimen {path}: {exc}"
                ) from exc
            if data.get("poc_id") == specimen_id:
                matches.append((path, data))

    if len(matches) > 1:
        raise EvidenceAmbiguityError(
            f"Multiple rule specimens match {specimen_id}"
        )
    return matches[0] if matches else None


def _evaluate_specimen(specimen_id: str):
    resolved = _resolve_rule_specimen(specimen_id)
    if resolved is None:
        return _certificate(
            target=specimen_id,
            rule_specimen_id=specimen_id,
            verdict="RULE_SPECIMEN_NOT_FOUND",
            verdict_reason="No stored rule specimen matches this identifier.",
        )

    _, specimen = resolved
    attestation = specimen.get("source_attestation")
    if not isinstance(attestation, dict):
        raise EvidenceIntegrityError(
            f"Rule specimen {specimen_id} has no valid source_attestation object"
        )

    canonical_url = attestation.get("canonical_url")
    if canonical_url is None:
        return _certificate(
            target=specimen_id,
            rule_specimen_id=specimen_id,
            verdict="HOLD_PRIMARY_BYTES",
            verdict_reason=(
                "Rule specimen declares primary source pending. "
                "No fetch target is available."
            ),
        )
    if not isinstance(canonical_url, str):
        raise EvidenceIntegrityError(
            f"Rule specimen {specimen_id} canonical_url has invalid type"
        )

    return _evaluate_url(canonical_url, rule_specimen_id=specimen_id)


def ci_evaluate(target: str) -> CiCertificate:
    """Evaluate existing BitBot evidence without network or replay execution."""
    if not isinstance(target, str) or not target.strip():
        raise ValueError("target must be a non-empty URL or rule specimen ID")

    try:
        if target.startswith(("http://", "https://")):
            return _evaluate_url(target)
        return _evaluate_specimen(target)
    except EvidenceAmbiguityError as exc:
        return _certificate(
            target=target,
            rule_specimen_id=(None if target.startswith(("http://", "https://")) else target),
            verdict="EVIDENCE_AMBIGUITY_HOLD",
            verdict_reason=str(exc),
        )
    except EvidenceIntegrityError as exc:
        return _certificate(
            target=target,
            rule_specimen_id=(None if target.startswith(("http://", "https://")) else target),
            verdict="EVIDENCE_INTEGRITY_HOLD",
            verdict_reason=str(exc),
        )


def main() -> int:
    import sys

    if len(sys.argv) != 2:
        print("Usage: doj_bitbot_ci_v0_1.py <URL|RULE_SPECIMEN_ID>")
        return 1

    try:
        certificate = ci_evaluate(sys.argv[1])
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    print(json.dumps(asdict(certificate), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
