#!/usr/bin/env python3
"""Materialize a public-question case directory from a bounded intake object.

Deterministic filesystem operation only. This tool does not decide truth,
authority, guilt, jurisdiction, or legal deadlines.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

QUESTION_ID_RE = re.compile(r"^Q-[0-9]{8}-[A-Z0-9_-]+$")
SUBDIRS = (
    "authority/claimed_authority",
    "authority/jurisdiction_receipts",
    "records/public",
    "records/court",
    "records/agency",
    "records/source_bytes",
    "money/appropriations",
    "money/contracts",
    "money/travel_lodging",
    "responses/official",
    "responses/congressional",
    "responses/oig",
    "clocks",
    "contradictions",
    "receipts",
    "replay",
)


def parse_timestamp(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("submitted_at must include a timezone offset")
    return dt.astimezone(timezone.utc)


def materialize(intake: dict, root: Path) -> Path:
    question_id = intake.get("question_id", "")
    if not QUESTION_ID_RE.fullmatch(question_id):
        raise ValueError("invalid question_id")

    submitted_at = parse_timestamp(intake["submitted_at"])
    due_at = submitted_at + timedelta(hours=24)

    case_dir = root / question_id
    if case_dir.exists():
        raise FileExistsError(f"case already exists: {case_dir}")

    for subdir in SUBDIRS:
        (case_dir / subdir).mkdir(parents=True, exist_ok=False)

    normalized = dict(intake)
    normalized["portal_sla_hours"] = 24
    normalized["portal_status_due_at"] = due_at.isoformat().replace("+00:00", "Z")
    normalized.setdefault("portal_status", "DIRECTORY_MATERIALIZED")
    normalized.setdefault("replay_state", "HOLD")
    normalized["authority_created"] = False

    (case_dir / "intake.json").write_text(
        json.dumps(normalized, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    question_text = normalized["question_text"].strip()
    (case_dir / "QUESTION.md").write_text(
        "# Public Question\n\n"
        f"Question ID: `{question_id}`\n\n"
        f"> {question_text}\n\n"
        "Status: `HOLD` until required record and authority edges are bound.\n\n"
        "`PUBLIC_QUESTION != PROVEN_CLAIM`\n",
        encoding="utf-8",
    )

    candidates = normalized.get("authority_candidates", [])
    (case_dir / "authority" / "candidates.json").write_text(
        json.dumps(candidates, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    portal_clock = {
        "clock_type": "PORTAL_TRANSPARENCY_SLA",
        "submitted_at": submitted_at.isoformat().replace("+00:00", "Z"),
        "status_due_at": due_at.isoformat().replace("+00:00", "Z"),
        "sla_hours": 24,
        "legal_deadline_created": False,
        "status": "RUNNING",
        "allowed_terminal_statuses": [
            "ANSWER_RECEIVED",
            "RECORDS_RECEIVED",
            "ACKNOWLEDGMENT_RECEIVED",
            "ROUTED_TO_STATUTORY_PROCESS",
            "NO_RESPONSE_OBSERVED",
            "JURISDICTION_UNRESOLVED",
        ],
    }
    (case_dir / "clocks" / "portal_24h.json").write_text(
        json.dumps(portal_clock, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    legal_clock = {
        "status": "UNBOUND",
        "note": "Populate only from a statute, rule, court order, regulation, or other source-bound deadline.",
        "portal_24h_is_legal_deadline": False,
    }
    (case_dir / "clocks" / "legal_deadlines.json").write_text(
        json.dumps(legal_clock, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    for subdir in SUBDIRS:
        target = case_dir / subdir
        if any(target.iterdir()):
            continue
        (target / "README.md").write_text(
            "# Pending evidence lane\n\nNo receipt has been admitted to this lane yet.\n",
            encoding="utf-8",
        )

    return case_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("intake", type=Path, help="JSON intake file")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("public-question-router/questions"),
        help="case directory root",
    )
    args = parser.parse_args()

    intake = json.loads(args.intake.read_text(encoding="utf-8"))
    case_dir = materialize(intake, args.root)
    print(case_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
