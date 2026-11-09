#!/usr/bin/env python3
"""Hash the main-content text of a justice.gov page.

usage: doj_cwa_extract.py <html_file> <out_text_file> [expected_phrase]

Prints exactly one JSON line and always exits 0; the caller decides from "ok".
  ok=true  -> {"ok":true,"sha256":...,"chars":N,"h1":...,"ended_at_updated":true}
  ok=false -> {"ok":false,"error":...}

Scope: everything from the page <h1> through the "Updated ..." line, inside
<main>. Header, menus and footer are excluded so chrome changes do not read
as rule changes.

Content validity (all required; any miss is a failure, never a baseline):
  - a <main> element and an <h1> inside it
  - an "Updated ..." line after the h1 (block/error pages do not have one)
  - at least MIN_CHARS of text
  - the expected phrase, case-insensitive, if one is given
"""
import hashlib
import json
import re
import sys

from bs4 import BeautifulSoup, Comment

MIN_CHARS = 200


def emit(obj):
    print(json.dumps(obj))
    sys.exit(0)


def main():
    if len(sys.argv) not in (3, 4):
        emit({"ok": False, "error": "usage: doj_cwa_extract.py <html> <out> [phrase]"})
    src, out = sys.argv[1], sys.argv[2]
    expect = sys.argv[3] if len(sys.argv) == 4 else ""
    try:
        with open(src, "rb") as fh:
            html = fh.read()
    except OSError as exc:
        emit({"ok": False, "error": f"read failed: {exc}"})

    soup = BeautifulSoup(html, "html.parser")
    root = soup.find("main") or soup.find(id="main-content")
    if root is None:
        emit({"ok": False, "error": "no <main> element"})
    h1 = root.find("h1")
    if h1 is None:
        emit({"ok": False, "error": "no <h1> inside main"})

    parts = []
    ended = False
    take_next = False
    for s in h1.find_all_next(string=True):
        if root not in s.parents:
            break
        if isinstance(s, Comment):
            continue
        if s.parent is not None and s.parent.name in ("script", "style", "noscript"):
            continue
        t = " ".join(s.split())
        if not t:
            continue
        parts.append(t)
        if take_next:  # date string that followed a bare "Updated"
            ended = True
            break
        if t.startswith("Updated"):
            if re.fullmatch(r"Updated:?", t):
                take_next = True
                continue
            ended = True
            break

    text = "\n".join(parts)
    if not ended:
        emit({"ok": False, "error": "no 'Updated' line after the page heading (layout changed or not a real content page)"})
    if len(text) < MIN_CHARS:
        emit({"ok": False, "error": f"too little main text ({len(text)} chars)"})
    if expect and expect.lower() not in text.lower():
        emit({"ok": False, "error": f"expected phrase not found in main text: {expect}"})

    with open(out, "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    emit({
        "ok": True,
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "chars": len(text),
        "h1": " ".join(h1.get_text().split()),
        "ended_at_updated": True,
    })


if __name__ == "__main__":
    main()
