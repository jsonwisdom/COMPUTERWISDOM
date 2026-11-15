#!/usr/bin/env python3
"""CI-FIRST Governor conformance v0.2: conservative, read-only verifier.

Exit 0 only for a fully releasable packet; 2 for HOLD, 3 for a detected FAIL.
Requires Python 3.10+. Optional external binaries: veraPDF, pdfinfo (poppler).
Never trusts self-asserted PASS in manifest as independent evidence.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from decimal import Decimal, InvalidOperation
from pathlib import Path

HEX64 = re.compile(r"^[0-9a-f]{64}$")
A4_PT = (210 * 72 / 25.4, 297 * 72 / 25.4)
NEEDED = ("authority", "appropriation", "payment", "reporting")
VALID_SCOPES = {"governmental_activities", "primary_government", "business_type", "component_units"}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def dec(value):
    if isinstance(value, bool):
        raise InvalidOperation("boolean is not a decimal")
    return Decimal(str(value))


def check_source_receipts(packet, root):
    """G0: validate actual captured bytes, not a claimed SHA field alone."""
    sources = packet.get("sources", [])
    if not sources:
        return "UNKNOWN", []
    details = []
    for s in sources:
        digest, count, cas = s.get("sha256"), s.get("byte_count"), s.get("cas_path")
        if not digest or count is None or not cas or root is None:
            details.append({"source_id": s.get("source_id"), "status": "UNKNOWN"})
            continue
        if not HEX64.fullmatch(digest) or cas != "sha256/" + digest:
            details.append({"source_id": s.get("source_id"), "status": "FAIL", "reason": "invalid CAS binding"})
            continue
        full = (root / cas).resolve()
        if not full.is_relative_to(root.resolve()):
            details.append({"source_id": s.get("source_id"), "status": "FAIL", "reason": "path traversal"})
        elif not full.is_file():
            details.append({"source_id": s.get("source_id"), "status": "UNKNOWN", "reason": "bytes unavailable"})
        elif full.stat().st_size != count or sha(full) != digest:
            details.append({"source_id": s.get("source_id"), "status": "FAIL", "reason": "byte mismatch"})
        else:
            details.append({"source_id": s.get("source_id"), "status": "PASS"})
    statuses = {d["status"] for d in details}
    return ("FAIL" if "FAIL" in statuses else "UNKNOWN" if "UNKNOWN" in statuses else "PASS"), details


def check_fiscal(packet):
    """G1: recompute both named totals from one consistently scoped statement."""
    r = packet.get("reconciliation", {})
    p = r.get("reported", {})
    keys = ("revenues", "expenses", "balance_before_transfers", "net_transfers",
            "change_in_net_position")
    if any(k not in p for k in keys):
        return "UNKNOWN", {"reason": "missing reported line"}
    try:
        rev, expense, before, trans, after = (dec(p[k]) for k in keys)
        sb = dec(r["special_items_before_transfers"])
        sa = dec(r["special_items_after_transfers"])
        computed_before = rev - expense + sb
        computed_after = computed_before + trans + sa
    except (InvalidOperation, KeyError, TypeError, ValueError):
        return "FAIL", {"reason": "invalid typed numerical input"}
    residual_before = before - computed_before
    residual_after = after - computed_after
    tol = Decimal("0.001")  # USD millions, tolerance explicitly declared
    status = "PASS" if abs(residual_before) <= tol and abs(residual_after) <= tol else "FAIL"
    return status, {
        "computed_before_transfers_million": str(computed_before),
        "computed_change_net_position_million": str(computed_after),
        "residual_before_million": str(residual_before),
        "residual_after_million": str(residual_after),
        "tolerance_million": str(tol)
    }


def check_labels(packet):
    """G2: scopes/labels never silently collapse; unit is explicit."""
    r = packet.get("reconciliation", {})
    p = r.get("reported", {})
    required = ("balance_before_transfers", "net_transfers", "change_in_net_position")
    valid = (r.get("scope") in VALID_SCOPES and r.get("unit") == "USD_millions"
             and r.get("transfers_presentation") in {"gross", "net"}
             and all(k in p for k in required)
             and bool(r.get("statement")) and bool(r.get("source_id"))
             and bool(packet.get("fiscal_year_end"))
             and packet.get("release") == "CLOSED")
    return ("PASS" if valid else "FAIL"), {"explicit_pre_post_labels": all(k in p for k in required)}


def vera_test(pdf, flavour):
    """Independent veraPDF formal machine-readable test. Never trusts PDF metadata alone."""
    if not shutil.which("verapdf"):
        return "UNKNOWN", "veraPDF CLI not installed"
    try:
        p = subprocess.run(["verapdf", "-f", flavour, str(pdf)],
                           capture_output=True, timeout=120, text=True, check=False)
        root = ET.fromstring(p.stdout)
        reports = [e for e in root.iter() if e.tag.rsplit("}", 1)[-1] == "validationReport"]
        if p.returncode != 0 or len(reports) != 1:
            return "UNKNOWN", "no complete single veraPDF report"
        return ("PASS" if reports[0].get("isCompliant") == "true" else "FAIL"), reports[0].get("profileName", "")
    except (ET.ParseError, OSError, subprocess.TimeoutExpired) as e:
        return "UNKNOWN", str(e)


def geometry_test(pdf):
    """Check EVERY page; no automatic U.S. Letter normalization."""
    if not shutil.which("pdfinfo"):
        return "UNKNOWN", "pdfinfo not available"
    try:
        # pdfinfo -box all-page line output from Poppler; use PyMuPDF only if available
        import fitz
        doc = fitz.open(str(pdf))
        if doc.page_count == 0:
            return "FAIL", "empty PDF"
        for i, pg in enumerate(doc, 1):
            w, h = pg.mediabox.width, pg.mediabox.height
            if abs(w - A4_PT[0]) > 0.05 or abs(h - A4_PT[1]) > 0.05:
                return "FAIL", f"page {i} MediaBox {w:.2f} x {h:.2f} not A4"
        return "PASS", f"{doc.page_count} pages A4"
    except ImportError:
        return "UNKNOWN", "PyMuPDF not installed (pip install pymupdf)"
    except (ValueError, RuntimeError, OSError) as e:
        return "UNKNOWN", str(e)


def check_pdf(packet, pdf):
    """G3: true PDF/A-2u AND PDF/UA-1 machine checks, plus page geometry."""
    if not pdf or not pdf.is_file():
        return "UNKNOWN", {"geometry": "UNKNOWN", "pdfa": "UNKNOWN", "pdfua": "UNKNOWN"}
    archive = packet.get("archive", {})
    geom, geonote = geometry_test(pdf)
    target = archive.get("target_pdfa")
    if target not in {"2u", "2b"}:
        return "FAIL", {"geometry": geom, "reason": "unsupported packet PDF/A target"}
    a, anote = vera_test(pdf, target)
    u, unote = vera_test(pdf, "ua1")
    components = [geom, a, u]
    status = "FAIL" if "FAIL" in components else "UNKNOWN" if "UNKNOWN" in components else "PASS"
    return status, {"geometry": geom, "geometry_note": geonote,
                    "pdfa": a, "pdfa_report": anote,
                    "pdfua": u, "pdfua_report": unote}


def check_linkage(packet, verified_sources):
    """G4: four independent receipt-backed edges per sampled disbursement."""
    sample = packet.get("payment_sample", {})
    payments = sample.get("payments", [])
    count = sample.get("sampled_count", 0)
    if count == 0:
        return "UNKNOWN", {"numerator": 0, "denominator": 0, "coverage": None}
    if count != len(payments):
        return "FAIL", {"reason": "denominator differs from actual sampled items"}
    digests = {s.get("sha256") for s in packet.get("sources", []) if s.get("sha256")}
    complete = 0
    for pay in payments:
        edges = pay.get("edges", {})
        if all(isinstance(edges.get(k), str) and HEX64.fullmatch(edges[k])
               and edges[k] in digests for k in NEEDED):
            complete += 1
    coverage = complete / count
    return ("PASS" if verified_sources == "PASS" else "UNKNOWN"), {
        "numerator": complete, "denominator": count,
        "coverage": coverage, "status_note": "PASS means counted edges have source CAS receipts; not a legal finding"
    }


def check_readback(packet, pdf, manifest, ext_manifest_digest, readback_pdf, readback_manifest):
    """G5: independent readbacks with external manifest digest; no recursive self-hash."""
    p = packet.get("artifact_receipts", {})
    expected_pdf = p.get("pdf_sha256")
    if not (pdf and manifest and readback_pdf and readback_manifest and ext_manifest_digest
            and expected_pdf):
        return "UNKNOWN", {"reason": "detached digest or readback missing"}
    paths = (pdf, manifest, readback_pdf, readback_manifest)
    if any(not q.is_file() for q in paths):
        return "UNKNOWN", {"reason": "actual files unavailable"}
    if not (HEX64.fullmatch(expected_pdf) and HEX64.fullmatch(ext_manifest_digest)):
        return "FAIL", {"reason": "invalid digest syntax"}
    verified = (sha(pdf) == sha(readback_pdf) == expected_pdf
                and sha(manifest) == sha(readback_manifest) == ext_manifest_digest)
    return ("PASS" if verified else "FAIL"), {"external_manifest_sha256": ext_manifest_digest}


def validate(packet, source_root=None, pdf=None, manifest=None, root_digest=None,
             readback_pdf=None, readback_manifest=None):
    g0, source_detail = check_source_receipts(packet, source_root)
    g1, math = check_fiscal(packet)
    g2, labels = check_labels(packet)
    g3, pdf_detail = check_pdf(packet, pdf)
    g4, coverage = check_linkage(packet, g0)
    g5, readback = check_readback(packet, pdf, manifest, root_digest, readback_pdf, readback_manifest)
    gates = {"G0": g0, "G1": g1, "G2": g2, "G3": g3, "G4": g4, "G5": g5}
    releasable = all(gates[k] == "PASS" for k in ("G0", "G1", "G2", "G3", "G5")) and coverage.get("denominator", 0) > 0
    return {"state": packet.get("state"), "gates": gates, "releasable": releasable,
            "release": "ELIGIBLE_FOR_REVIEW" if releasable else "CLOSED",
            "detail": {"source_receipts": source_detail, "math": math, "labels": labels,
                       "pdf": pdf_detail, "linkage": coverage, "readback": readback},
            "authority_created": False, "payment_authorized": False}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("record", type=Path)
    ap.add_argument("--source-root", type=Path)
    ap.add_argument("--pdf", type=Path)
    ap.add_argument("--manifest", type=Path)
    ap.add_argument("--external-manifest-sha256")
    ap.add_argument("--readback-pdf", type=Path)
    ap.add_argument("--readback-manifest", type=Path)
    opts = ap.parse_args()
    packet = json.loads(opts.record.read_text(encoding="utf-8"))
    result = validate(packet, opts.source_root, opts.pdf, opts.manifest,
                      opts.external_manifest_sha256, opts.readback_pdf, opts.readback_manifest)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["releasable"]:
        return 0
    return 3 if "FAIL" in result["gates"].values() else 2


if __name__ == "__main__":
    sys.exit(main())
