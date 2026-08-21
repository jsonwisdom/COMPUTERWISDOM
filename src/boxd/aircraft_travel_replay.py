#!/usr/bin/env python3
"""BoxD AIRCRAFT_TRAVEL_REPLAY extractor.

Internal alias: FUCK_PLANE
Public purpose: normalize source-bound aircraft rows into audit JSON + GeoJSON.

This tool does not infer misconduct, motive, sexual purpose, or guilt.
It fails closed when row-level date/route/aircraft fields are missing.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Optional

PUBLIC_NAMES = {
    "donald trump": "donald_trump",
    "ghislaine maxwell": "ghislaine_maxwell",
    "jeffrey epstein": "jeffrey_epstein",
}

DATE_RE = re.compile(r"\b(19\d{2}|20\d{2})[-/](\d{1,2})[-/](\d{1,2})\b")
TAIL_RE = re.compile(r"\bN\d{2,5}[A-Z]{0,2}\b", re.I)


@dataclass
class Endpoint:
    code: str = "UNKNOWN"
    city: Optional[str] = None
    country: Optional[str] = None


@dataclass
class FlightRow:
    flight_id: str
    date: str
    tail_number: str
    origin: Endpoint
    destination: Endpoint
    public_passengers: dict
    other_passenger_count: int
    source_uri: str
    source_sha256: str
    source_page_or_line: str
    raw_row_sha256: str
    edge_state: str
    misconduct_inferred: bool = False


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_name(name: str) -> str:
    return " ".join(name.lower().strip().split())


def passenger_flags(names: Iterable[str]) -> tuple[dict, int]:
    flags = {v: False for v in PUBLIC_NAMES.values()}
    other = 0
    for name in names:
        key = normalize_name(name)
        if key in PUBLIC_NAMES:
            flags[PUBLIC_NAMES[key]] = True
        elif key:
            other += 1
    return flags, other


def parse_csv(path: Path, source_uri: str) -> list[FlightRow]:
    raw = path.read_bytes()
    source_hash = sha256_bytes(raw)
    rows: list[FlightRow] = []

    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for idx, row in enumerate(reader, start=2):
            # Expected tolerant columns: date, tail_number, origin_code, origin_city,
            # destination_code, destination_city, passengers, source_page_or_line.
            raw_row = json.dumps(row, sort_keys=True, ensure_ascii=False)
            names = [x.strip() for x in (row.get("passengers") or "").split(";") if x.strip()]
            flags, other = passenger_flags(names)

            date = (row.get("date") or "").strip() or "UNKNOWN"
            tail = (row.get("tail_number") or "").strip().upper() or "UNKNOWN"
            ocode = (row.get("origin_code") or "").strip().upper() or "UNKNOWN"
            dcode = (row.get("destination_code") or "").strip().upper() or "UNKNOWN"

            edge_state = "PROVEN"
            if "UNKNOWN" in {date, tail, ocode, dcode}:
                edge_state = "HOLD"

            rows.append(
                FlightRow(
                    flight_id=(row.get("flight_id") or f"ROW_{idx}").strip(),
                    date=date,
                    tail_number=tail,
                    origin=Endpoint(ocode, (row.get("origin_city") or None), (row.get("origin_country") or None)),
                    destination=Endpoint(dcode, (row.get("destination_city") or None), (row.get("destination_country") or None)),
                    public_passengers=flags,
                    other_passenger_count=other,
                    source_uri=source_uri,
                    source_sha256=source_hash,
                    source_page_or_line=(row.get("source_page_or_line") or f"csv-line:{idx}").strip(),
                    raw_row_sha256=sha256_text(raw_row),
                    edge_state=edge_state,
                )
            )
    return rows


def parse_text(path: Path, source_uri: str) -> list[dict]:
    """Produce candidate audit rows from plain text without inventing structure.

    Because legacy flight logs may be handwritten/scanned, this function deliberately
    does not promote regex hits to flight rows. It emits candidate line receipts that
    require human or table-parser confirmation.
    """
    raw = path.read_bytes()
    source_hash = sha256_bytes(raw)
    text = raw.decode("utf-8", errors="replace")
    out = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        low = line.lower()
        if not any(name in low for name in PUBLIC_NAMES):
            continue
        dates = ["-".join(m.groups()) for m in DATE_RE.finditer(line)]
        tails = [m.group(0).upper() for m in TAIL_RE.finditer(line)]
        out.append(
            {
                "candidate_id": f"LINE_{lineno}",
                "source_uri": source_uri,
                "source_sha256": source_hash,
                "source_page_or_line": f"text-line:{lineno}",
                "raw_row_sha256": sha256_text(line),
                "public_name_hits": [PUBLIC_NAMES[n] for n in PUBLIC_NAMES if n in low],
                "date_candidates": dates,
                "tail_candidates": tails,
                "edge_state": "HOLD",
                "reason": "TEXT_HIT_REQUIRES_ROW_CONFIRMATION",
                "misconduct_inferred": False,
            }
        )
    return out


def load_airport_lookup(path: Optional[Path]) -> dict:
    if not path:
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    # {"TEB": {"lon": -74.0608, "lat": 40.8501, "precision": "AIRPORT"}}
    return {k.upper(): v for k, v in data.items()}


def rows_to_geojson(rows: list[FlightRow], airport_lookup: dict) -> dict:
    features = []
    audit_only = []
    for row in rows:
        o = airport_lookup.get(row.origin.code)
        d = airport_lookup.get(row.destination.code)
        if row.edge_state != "PROVEN" or not o or not d:
            audit_only.append({**asdict(row), "geo_state": "HOLD"})
            continue

        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[o["lon"], o["lat"]], [d["lon"], d["lat"]]],
                },
                "properties": {
                    **asdict(row),
                    "origin_precision": o.get("precision", "AIRPORT"),
                    "destination_precision": d.get("precision", "AIRPORT"),
                    "geo_match_causation": False,
                },
            }
        )

    return {
        "type": "FeatureCollection",
        "features": features,
        "audit_only": audit_only,
        "authority_created": False,
        "proof_inferred": False,
        "standing_rules": [
            "PASSENGER != PARTICIPANT_IN_MISCONDUCT",
            "AIRCRAFT_WITH_BED != SEXUAL_PURPOSE",
            "FLIGHT_TO_USVI != PROOF_OF_CRIME",
            "GEO_MATCH != CAUSATION",
            "SEARCH_FAILURE != RECORD_ABSENCE",
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="BoxD aircraft-travel replay extractor")
    ap.add_argument("input", type=Path)
    ap.add_argument("--source-uri", required=True)
    ap.add_argument("--format", choices=["csv", "text"], required=True)
    ap.add_argument("--airport-lookup", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    if args.format == "csv":
        rows = parse_csv(args.input, args.source_uri)
        geo = rows_to_geojson(rows, load_airport_lookup(args.airport_lookup))
        args.out.write_text(json.dumps(geo, indent=2, sort_keys=True), encoding="utf-8")
    else:
        rows = parse_text(args.input, args.source_uri)
        args.out.write_text(
            json.dumps(
                {
                    "candidate_rows": rows,
                    "authority_created": False,
                    "proof_inferred": False,
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
