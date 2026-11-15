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



def check_lineage(packet, source_root):
    """Proof that typed G1 inputs occur in a specific page of hashed source bytes.

    A hand-typed fixture by itself can only prove arithmetic, not source correctness.
    Exact text-excerpt matching remains a mechanical check, NOT government authentication.
    """
    r = packet.get("reconciliation", {})
    digest = r.get("source_sha256")
    references = r.get("line_receipts", {})
    expected = r.get("reported", {})
    keys = ("revenues", "expenses", "balance_before_transfers",
            "net_transfers", "change_in_net_position")
    if not digest or not isinstance(references, dict) or source_root is None:
        return "UNKNOWN", {"reason": "source-bound line receipts absent"}
    if not HEX64.fullmatch(digest):
        return "FAIL", {"reason": "invalid source SHA-256"}
    sources = {a.get("source_id"): a for a in packet.get("sources", [])}
    source_id = r.get("source_id")
    source = sources.get(source_id)
    if not source or source.get("sha256") != digest:
        return "FAIL", {"reason": "fixture digest differs from source receipt"}
    file = (source_root / "sha256" / digest).resolve()
    if not file.is_relative_to(source_root.resolve()):
        return "FAIL", {"reason": "unsafe source path"}
    if not file.is_file():
        return "UNKNOWN", {"reason": "original bytes unavailable"}
    if sha(file) != digest:
        return "FAIL", {"reason": "source bytes fail SHA-256"}
    if any(k not in references for k in keys):
        return "UNKNOWN", {"reason": "some ACFR line receipts unavailable"}
    try:
        import fitz
        with fitz.open(str(file)) as doc:
            if not doc.is_pdf:
                return "FAIL", {"reason": "the evidence source is not a PDF"}
            for key in keys:
                e = references[key]
                page_index = e.get("page_index")
                excerpt = e.get("excerpt", "")
                if not isinstance(page_index, int) or not (0 <= page_index < doc.page_count):
                    return "FAIL", {"reason": f"bad page index for {key}"}
                if not isinstance(excerpt, str) or len(excerpt.strip()) < 10:
                    return "FAIL", {"reason": f"missing exact source text for {key}"}
                raw = " ".join(doc[page_index].get_text(sort=True).split())
                needle = " ".join(excerpt.split())
                numeric = str(expected[key])
                number_forms = {numeric, f"{int(numeric):,}"} if numeric.lstrip("-").isdigit() else {numeric}
                if needle not in raw or not any(x in needle for x in number_forms):
                    return "FAIL", {"reason": f"no matching labeled value on source page for {key}"}
    except ImportError:
        return "UNKNOWN", {"reason": "PyMuPDF not available to bind source text"}
    except (ValueError, OSError, RuntimeError, KeyError, TypeError) as e:
        return "UNKNOWN", {"reason": f"source parse/readback incomplete: {type(e).__name__}"}
    return "PASS", {"source_sha256": digest, "line_receipts_matched": len(keys),
                    "scope_note": "verified bytes + text excerpts; document authenticity still UNKNOWN"}

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



def safe_margin_test(pdf, margin_mm):
    """Check all rendered paint bboxes, not merely the A4 MediaBox.

    Conservative by design: full-bleed decorative content fails too, unless
    separately redesigned. A clipping loss outside the page still needs visual
    inspection and a human reviewed capture, so this is not a complete proof of fit.
    """
    if margin_mm is None:
        return "UNKNOWN", {"reason": "safe_margin_mm has not been declared"}
    try:
        margin = dec(margin_mm) * Decimal(72) / Decimal("25.4")
        if margin < 0 or margin > Decimal(50):
            return "FAIL", {"reason": "safe margin outside supported range (0..50 pt)"}
        import fitz
        with fitz.open(str(pdf)) as doc:
            if doc.page_count < 1:
                return "FAIL", {"reason": "empty PDF"}
            checked = 0
            for i, pg in enumerate(doc, 1):
                r = pg.mediabox
                allowed = (float(margin), float(margin), r.width - float(margin), r.height - float(margin))
                ops = pg.get_bboxlog()
                if not ops:
                    return "UNKNOWN", {"reason": f"page {i} contains no inspectable rendered marks"}
                for typ, box in ops:
                    if typ not in {"fill-text", "stroke-text", "fill-path", "stroke-path", "fill-image", "fill-shade"}:
                        continue
                    checked += 1
                    if (box[0] < allowed[0] - .05 or box[1] < allowed[1] - .05 or
                        box[2] > allowed[2] + .05 or box[3] > allowed[3] + .05):
                        return "FAIL", {"page": i, "type": typ, "bounding_box_pt": [round(v,2) for v in box],
                                        "safe_box_pt": [round(v,2) for v in allowed]}
            if checked == 0:
                return "UNKNOWN", {"reason": "no visible paint operations inspected"}
            return "PASS", {"pages": doc.page_count, "paint_operations_checked": checked,
                            "safe_margin_mm": float(dec(margin_mm)),
                            "limitation": "bboxlog cannot rule out content clipped outside the MediaBox"}
    except ImportError:
        return "UNKNOWN", {"reason": "PyMuPDF unavailable"}
    except (ValueError, OSError, RuntimeError, InvalidOperation) as e:
        return "UNKNOWN", {"reason": f"margin inspection unavailable: {type(e).__name__}"}

def check_pdf(packet, pdf):
    """G3: PDF/A and PDF/UA checks + safe margins + independent 2nd reader."""
    if not pdf or not pdf.is_file():
        return "UNKNOWN", {"geometry": "UNKNOWN", "pdfa": "UNKNOWN", "pdfua": "UNKNOWN"}
    archive = packet.get("archive", {})
    geom, geonote = geometry_test(pdf)
    margin, margindetail = safe_margin_test(pdf, packet.get("page_geometry", {}).get("safe_margin_mm"))
    target = archive.get("target_pdfa")
    if target not in {"2u", "2b"}:
        return "FAIL", {"geometry": geom, "reason": "unsupported packet PDF/A target"}
    a, anote = vera_test(pdf, target)
    u, unote = vera_test(pdf, "ua1")
    # A second, independent PDF/UA reader such as PAC (plus human checkpoints)
    # must be separately evidenced; veraPDF invoked twice is not two tools.
    independent_reader = "UNKNOWN"
    components = [geom, margin, a, u, independent_reader]
    status = "FAIL" if "FAIL" in components else "UNKNOWN" if "UNKNOWN" in components else "PASS"
    return status, {"geometry": geom, "geometry_note": geonote,
                    "safe_margin": margin, "safe_margin_report": margindetail,
                    "pdfa": a, "pdfa_report": anote,
                    "pdfua": u, "pdfua_report": unote,
                    "secondary_pdfua_reader": independent_reader,
                    "human_accessibility_review": "UNKNOWN"}


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
    calc, math = check_fiscal(packet)
    source_match, source_match_detail = check_lineage(packet, source_root)
    g1 = "FAIL" if "FAIL" in (calc, source_match) else "PASS" if calc == source_match == g0 == "PASS" else "UNKNOWN"
    math["arithmetic_only_status"] = calc
    math["source_bound_status"] = source_match
    math["source_bound_detail"] = source_match_detail
    g2, labels = check_labels(packet)
    g3, pdf_detail = check_pdf(packet, pdf)
    g4, coverage = check_linkage(packet, g0)
    g5, readback = check_readback(packet, pdf, manifest, root_digest, readback_pdf, readback_manifest)
    gates = {"G0": g0, "G1": g1, "G2": g2, "G3": g3, "G4": g4, "G5": g5}
    # User has not approved a coverage threshold or independently trusted root receipt.
    # A complete test suite must never silently authorize a release.
    releasable = False
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
