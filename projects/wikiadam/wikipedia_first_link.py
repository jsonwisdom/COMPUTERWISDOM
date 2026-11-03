#!/usr/bin/env python3
"""WikiAdam Wikipedia first-link game, powered by Playwright.

A PUBLIC navigation exercise only. It does not prove creator identity or
ownership, nor reproduce any historical 97% claim. This implementation uses
a documented, versioned approximation of the traditional first-link rules:
article-body prose paragraphs; skip italic, superscript, navigation elements,
non-article namespace, external links, and links inside parentheses.
Wikipedia's rendered DOM changes; every traversal is a dated observation.
No login, rate-limit bypass, CAPTCHA evasion, or offsite navigation.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import time
from urllib.parse import quote, unquote, urlsplit

EN = "en.wikipedia.org"
VERSION = "WIKIADAM_FIRST_LINK_RULE_V0_1"
MAX_HOPS_CAP = 40

FIRST_ARTICLE_LINK_JS = r"""() => {
  const root = document.querySelector(
    '#mw-content-text .mw-parser-output, .mw-parser-output'
  );
  if (!root) return {next: null, reason: 'BODY_NOT_FOUND'};
  const skipped = '.hatnote, .navbox, .infobox, .metadata, .toc,' +
    '.mw-editsection, .shortdescription, .thumb, .sidebar,' +
    '.reflist, .references, .mw-collapsible, .ambox';
  const paragraphs = Array.from(root.querySelectorAll('p'))
    .filter(p => !p.closest(skipped));
  for (const p of paragraphs) {
    let depth = 0;
    const walker = document.createTreeWalker(
      p, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT
    );
    let node;
    while ((node = walker.nextNode())) {
      if (node.nodeType === Node.TEXT_NODE) {
        for (const c of node.textContent || '') {
          if (c === '(') depth++;
          else if (c === ')') depth = Math.max(0, depth - 1);
        }
        continue;
      }
      if (node.nodeType !== Node.ELEMENT_NODE || node.tagName !== 'A') continue;
      if (depth !== 0 || node.closest('i, em, sup, sub, ' + skipped)) continue;
      const href = node.getAttribute('href') || '';
      if (!href || href.startsWith('#')) continue;
      let target;
      try { target = new URL(href, 'https://en.wikipedia.org/'); }
      catch (_) { continue; }
      if (target.protocol !== 'https:' || target.hostname !== 'en.wikipedia.org')
        continue;
      if (!target.pathname.startsWith('/wiki/')) continue;
      let title;
      try { title = decodeURIComponent(target.pathname.slice(6)); }
      catch (_) { continue; }
      if (!title || title.includes(':')) continue;
      target.search = '';
      target.hash = '';
      return {next: target.toString(), reason: 'FIRST_BODY_LINK'};
    }
  }
  return {next: null, reason: 'NO_QUALIFIED_BODY_LINK'};
}"""


def allowed_article(url: str) -> bool:
    u = urlsplit(url)
    if u.scheme != "https" or u.hostname != EN or u.username or u.password:
        return False
    if not u.path.startswith("/wiki/") or not u.path[6:]:
        return False
    title = unquote(u.path[6:])
    return ":" not in title and not u.query


def start_url(start: str | None = None, random_article: bool = False) -> str:
    if random_article:
        if start:
            raise ValueError("Choose either --start or --random")
        return "https://en.wikipedia.org/wiki/Special:Random"
    if not start:
        raise ValueError("Provide --start or --random")
    if start.startswith(("http://", "https://")):
        if not allowed_article(start):
            raise ValueError("Start URL must be an English Wikipedia article")
        return start
    if ":" in start:
        raise ValueError("Only article titles, no namespace commands")
    return "https://en.wikipedia.org/wiki/" + quote(start.replace(" ", "_"), safe="()'-_,")


def is_philosophy(url: str) -> bool:
    return allowed_article(url) and unquote(urlsplit(url).path[6:]).replace("_", " ").casefold() == "philosophy"


def walk(page, initial: str, max_hops: int = 12, delay_seconds: float = 1.0,
         sleep_fn=time.sleep) -> dict:
    """Consumes a Playwright Page or a deterministic fake Page in offline tests."""
    if not 1 <= max_hops <= MAX_HOPS_CAP:
        raise ValueError(f"max_hops must be 1..{MAX_HOPS_CAP}")
    if not 1.0 <= delay_seconds <= 10.0:
        raise ValueError("delay_seconds must be between 1 and 10")
    if initial != "https://en.wikipedia.org/wiki/Special:Random" and not allowed_article(initial):
        raise ValueError("Initial URL must be a public Wikipedia article")
    visited, steps = set(), []
    current = initial
    stop = "MAX_HOPS_REACHED"
    for hop in range(max_hops):
        try:
            page.goto(current, wait_until="domcontentloaded", timeout=25000)
        except Exception as exc:
            # Do not treat a connection failure as a loop or as a nonexistent article.
            stop = "NAVIGATION_ERROR_" + type(exc).__name__
            break
        observed = page.url.split("#", 1)[0]
        if not allowed_article(observed):
            stop = "NON_ARTICLE_OR_OFFSITE_REDIRECT"
            break
        if observed in visited:
            stop = "CYCLE_DETECTED"
            break
        visited.add(observed)
        now = datetime.now(timezone.utc).isoformat()
        html_sha256 = hashlib.sha256(page.content().encode("utf-8")).hexdigest()
        if is_philosophy(observed):
            steps.append({"hop": hop, "url": observed, "next_url": None,
                          "observed_at_utc": now, "rendered_html_sha256": html_sha256})
            stop = "REACHED_PHILOSOPHY"
            break
        answer = page.evaluate(FIRST_ARTICLE_LINK_JS)
        nxt = answer.get("next") if isinstance(answer, dict) else None
        steps.append({"hop": hop, "url": observed, "next_url": nxt,
                      "observed_at_utc": now, "rendered_html_sha256": html_sha256,
                      "selection_reason": answer.get("reason") if isinstance(answer, dict) else "INVALID_EVALUATION"})
        if not nxt or not allowed_article(nxt):
            stop = "NO_QUALIFIED_FIRST_LINK"
            break
        current = nxt
        if hop < max_hops - 1:
            sleep_fn(delay_seconds)
    return {
        "schema": "WIKIADAM_WIKIPEDIA_WALK_V0_1",
        "mode": "PUBLIC_CONCEPTUAL_LINK_NAVIGATION",
        "rule_version": VERSION,
        "start": initial,
        "max_hops": max_hops,
        "stop_reason": stop,
        "steps": steps,
        "reached_philosophy": stop == "REACHED_PHILOSOPHY",
        "historical_wikipedia_97_percent_verified": False,
        "person_authorship_proof": False,
    }


def crawl_live(start: str | None = None, random_article: bool = False,
               max_hops: int = 12, delay_seconds: float = 1.5):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Install Playwright and Chromium before --live") from exc
    url = start_url(start, random_article)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            context = browser.new_context()
            # Abort offsite/subresource traffic: this demo never explores other sites.
            def permit(route):
                host = urlsplit(route.request.url).hostname
                if host == EN and urlsplit(route.request.url).scheme == "https":
                    route.continue_()
                else:
                    route.abort()
            context.route("**/*", permit)
            page = context.new_page()
            return walk(page, url, max_hops, delay_seconds)
        finally:
            browser.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--start", help="English Wikipedia article title or URL")
    group.add_argument("--random", action="store_true", help="Use Special:Random")
    parser.add_argument("--max-hops", type=int, default=12)
    parser.add_argument("--delay-seconds", type=float, default=1.5)
    parser.add_argument("--live", action="store_true", help="Explicit opt-in to browser network browsing")
    args = parser.parse_args()
    if not args.live:
        parser.error("Live public browsing is opt-in; add --live")
    report = crawl_live(args.start, args.random, args.max_hops, args.delay_seconds)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
