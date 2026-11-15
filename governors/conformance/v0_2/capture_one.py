#!/usr/bin/env python3
"""CI-FIRST state ACFR source capture, ONE STATE PER INVOCATION.

No network work on import. No automatic runs in GitHub Actions. This creates
self-attested observation receipts; it does NOT authenticate state provenance,
make a state regulator-approved, or satisfy the fiscal/payout release gates.
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_SEEDS = Path(__file__).with_name("official_pdf_candidates_v0_1.json")
MAX_BYTES = 50 * 1024 * 1024
CHUNK = 256 * 1024


def stamp():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def digest_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for data in iter(lambda: handle.read(CHUNK), b""):
            h.update(data)
    return h.hexdigest()


def assert_safe_url(url, hosts):
    p = urllib.parse.urlsplit(url)
    if p.scheme != "https" or p.username or p.password or p.port not in (None, 443):
        raise ValueError("URL must be HTTPS, without credentials or custom port")
    if p.hostname not in hosts:
        raise ValueError("URL hostname not in the publisher-specific allowlist")
    if not p.path.lower().endswith(".pdf"):
        raise ValueError("only explicit PDF URLs accepted")
    return url


class ExplicitPublisherRedirects(urllib.request.HTTPRedirectHandler):
    def __init__(self, allowed):
        self.allowed = allowed

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        assert_safe_url(newurl, self.allowed)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def record_bytes(src, root, state, link_url, source_url, publisher, observed, source_type):
    """Stream bytes to immutable CAS before creating receipt. Caller owns src."""
    root = Path(root)
    cas = root / "sha256"
    cas.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=str(cas), prefix=".partial-")
    tmp = Path(name)
    h = hashlib.sha256()
    count = 0
    try:
        with os.fdopen(fd, "wb") as out:
            while True:
                piece = src.read(CHUNK)
                if not piece:
                    break
                count += len(piece)
                if count > MAX_BYTES:
                    raise ValueError("PDF exceeds 50 MiB safety limit")
                h.update(piece)
                out.write(piece)
            out.flush()
            os.fsync(out.fileno())
        with open(tmp, "rb") as inp:
            if inp.read(5) != b"%PDF-":
                raise ValueError("payload is not a PDF (magic header mismatch)")
        hexdigest = h.hexdigest()
        final = cas / hexdigest
        if final.exists():
            if final.stat().st_size != count or digest_file(final) != hexdigest:
                raise ValueError("existing CAS name has different bytes")
            tmp.unlink()
        else:
            os.replace(tmp, final)
        if digest_file(final) != hexdigest:
            raise ValueError("CAS readback checksum mismatch")
        return {
            "schema":"ci-first.source-receipt.v0.1",
            "state":state,
            "publisher":publisher,
            "publisher_landing":link_url,
            "requested_pdf_url":source_url,
            "observed_at_utc":observed,
            "recorded_at_utc":stamp(),
            "source_type":source_type,
            "sha256":hexdigest,
            "byte_count":count,
            "cas_path":"sha256/" + hexdigest,
            "cas_readback":"PASS",
            "pdf_header_check":"PASS",
            "issuer_authenticity":"UNKNOWN",
            "publisher_hash_match":"UNKNOWN",
            "trusted_timestamp":"UNKNOWN",
            "reconciliation_source_binding":"UNKNOWN",
            "eo_payment_linkage":"UNKNOWN",
            "release":"CLOSED",
            "authority_created":False,
        }
    finally:
        if tmp.exists():
            tmp.unlink()


def capture(state, seeds, root):
    spec = seeds["states"].get(state)
    if not spec:
        raise ValueError("state has no publisher-reviewed PDF candidate")
    allowed = set(spec["allowed_hosts"])
    url = assert_safe_url(spec["pdf_url"], allowed)
    opener = urllib.request.build_opener(ExplicitPublisherRedirects(allowed))
    request = urllib.request.Request(url, headers={"User-Agent": "CI-FIRST-evidence-review/0.1 (manual read-only source acquisition)",
                                                  "Accept":"application/pdf"})
    observed = stamp()
    with opener.open(request, timeout=40) as response:
        final_url = assert_safe_url(response.geturl(), allowed)
        receipt = record_bytes(response, root, state, spec["landing"], final_url,
                               spec["publisher"], observed, "official_website_https_response")
    out = Path(root) / "receipts"
    out.mkdir(parents=True, exist_ok=True)
    # A receipt in the output tree remains self-attested until externally anchored.
    path = out / (state + "_" + receipt["sha256"] + ".json")
    if path.exists():
        raise ValueError("receipt already exists; never silently overwrite observations")
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status":"SOURCE_BYTE_CAPTURED_SELF_ATTESTED",
                      "state":state, "digest":receipt["sha256"], "bytes":receipt["byte_count"],
                      "receipt":str(path), "cas":receipt["cas_path"],
                      "G0":"PARTIAL_NOT_AUTHENTICATED", "G1":"UNKNOWN", "release":"CLOSED"}, indent=2))
    return 0


def verify_one(path, root):
    receipt = json.loads(Path(path).read_text(encoding="utf-8"))
    digest = receipt.get("sha256", "")
    if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise ValueError("invalid digest")
    if receipt.get("cas_path") != "sha256/" + digest:
        raise ValueError("receipt CAS name and digest disagree")
    source = (Path(root) / receipt["cas_path"]).resolve()
    if not source.is_relative_to(Path(root).resolve()):
        raise ValueError("unsafe CAS path")
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.stat().st_size != receipt["byte_count"] or digest_file(source) != digest:
        raise ValueError("source bytes do not match receipt")
    print(json.dumps({"byte_integrity":"PASS","source_sha256":digest,
                      "authenticity":"UNKNOWN","G1":"UNKNOWN","release":"CLOSED"}, indent=2))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seeds", type=Path, default=DEFAULT_SEEDS)
    ap.add_argument("--root", type=Path, required=True)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--state", help="state abbreviation of ONE publisher-reviewed candidate")
    group.add_argument("--verify-receipt", type=Path)
    ap.add_argument("--ack-remote-access", action="store_true",
                    help="explicitly permit one read-only HTTPS PDF fetch; never used in CI")
    args = ap.parse_args()
    try:
        if args.verify_receipt:
            return verify_one(args.verify_receipt, args.root)
        if not args.ack_remote_access:
            raise ValueError("--ack-remote-access required to fetch any original PDF")
        seeds = json.loads(args.seeds.read_text(encoding="utf-8"))
        return capture(args.state.upper(), seeds, args.root)
    except (ValueError, OSError, json.JSONDecodeError, urllib.error.URLError) as e:
        print(json.dumps({"state":args.state, "operation":"FAILED",
                          "error":str(e), "G0":"UNKNOWN","G1":"UNKNOWN","release":"CLOSED"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
