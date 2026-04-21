#!/usr/bin/env python3
"""
validate.py — offline integrity check for thomasnendick.com

Runs in under three seconds, zero network, stdlib only. It exists so you can
hit save on index.html, run one command, and know the site still holds
together. No Claude API. No build step. No excuses.

Checks performed
----------------
  1. LINKS    — every relative href / src resolves to a file on disk
  2. IDS      — no duplicate id="..." values in any HTML file
  3. CLASSES  — every class name used in markup is defined in an adjacent
                <style> block or _shared.css; every defined class is used
                (with explicit allowlists for JS-toggled and compound-only
                selectors, so false positives don't drown the signal)
  4. TAGS     — rough balance check: count opening vs closing tags for
                structural elements (div, section, article, header, footer,
                main, figure, nav). Voids and self-closers ignored.
  5. ASSETS   — flag any asset in /assets larger than the budget (1 MB)

Exit code is 0 if the site is clean, 1 if any check reports a real failure.
Informational notices never fail the run.

Usage
-----
    cd ~/Documents/Claude/Projects/Website
    python3 scripts/validate.py
    python3 scripts/validate.py --verbose     # show all matches, not just failures
    python3 scripts/validate.py --strict      # fail on informational notices too
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
ARCH_DIR = ROOT / "docs" / "architecture"
ASSETS_DIR = ROOT / "assets"

ASSET_BUDGET_BYTES = 1 * 1024 * 1024  # 1 MB per asset — hard ceiling

# ---------------------------------------------------------------------------
# Allowlists — these prevent the detector from crying wolf
# ---------------------------------------------------------------------------

# Classes defined in CSS but toggled at runtime by JS, so they never appear
# in the static markup. Treat as "used" — they're load-bearing.
JS_TOGGLED_CLASSES = {
    "is-visible",       # scroll-reveal observer
    "locked",           # .project-card.protected.locked
    "open",             # .pw-modal.open
    "active",           # .tab-panel.active, .tab-btn.active
    "revealed",         # optional reveal state
    "hidden",           # generic JS show/hide
}

# Classes that only exist as part of compound selectors (e.g. ".parent .child")
# where the parser finds both but maps only the tail to the used set. Don't
# flag these. Keep the list short — if a class is here, write a comment why.
COMPOUND_ONLY_DEFINED: set[str] = set()
# (currently empty — populate as false positives surface)

# Classes referenced in markup that are styled via descendant selector alone
# (".parent .child" where the parser only sees the outer token). Allowlist
# these so the "used-but-undefined" pass doesn't complain.
COMPOUND_ONLY_USED = {
    "footer-left",   # styled via .footer-grid > * patterns
}

# Token patterns we should never treat as a CSS class. These live inside
# urls, namespace declarations, or similar non-selector contexts.
CLASS_NAME_DENYLIST = {
    "org", "w3",     # leaked from xmlns="http://www.w3.org/2000/svg"
}

# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

class Report:
    """Collects findings across checks. One call per discovery, no state hidden."""

    def __init__(self) -> None:
        self.failures: list[str] = []
        self.notices: list[str] = []
        self.checks: list[tuple[str, int, int]] = []  # (name, found, failed)

    def fail(self, msg: str) -> None:
        self.failures.append(msg)

    def note(self, msg: str) -> None:
        self.notices.append(msg)

    def record(self, name: str, found: int, failed: int) -> None:
        self.checks.append((name, found, failed))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def html_files() -> list[Path]:
    files = [INDEX]
    if ARCH_DIR.exists():
        files.extend(sorted(ARCH_DIR.glob("*.html")))
    return [f for f in files if f.exists()]


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

HREF_SRC_RE = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"', re.I)
ID_RE = re.compile(r'\bid\s*=\s*"([^"]+)"')
CLASS_ATTR_RE = re.compile(r'\bclass\s*=\s*"([^"]+)"')
STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
CSS_CLASS_RE = re.compile(r"\.([A-Za-z_][\w-]*)")
URL_RE = re.compile(r"url\([^)]*\)")
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
TAG_OPEN_RE = re.compile(r"<(\w+)\b[^>]*?(?<!/)>")
TAG_CLOSE_RE = re.compile(r"</(\w+)\s*>")

STRUCTURAL_TAGS = {
    "div", "section", "article", "header", "footer",
    "main", "figure", "nav", "ul", "ol", "table", "form",
}


def check_links(files: list[Path], report: Report) -> None:
    found = 0
    failed = 0
    for f in files:
        text = read(f)
        for match in HREF_SRC_RE.finditer(text):
            url = match.group(1)
            # Skip absolute, mailto, tel, anchors, data URIs.
            if url.startswith(("http://", "https://", "mailto:", "tel:",
                               "#", "data:", "//")):
                continue
            found += 1
            # Strip anchor fragments and query strings before resolving.
            path_part = url.split("#", 1)[0].split("?", 1)[0]
            if not path_part:
                continue  # pure anchor, already skipped above
            target = (f.parent / path_part).resolve()
            if not target.exists():
                failed += 1
                report.fail(
                    f"LINK  {f.relative_to(ROOT)} → {url}  (no file at {target})"
                )
    report.record("links", found, failed)


def check_ids(files: list[Path], report: Report) -> None:
    found = 0
    failed = 0
    for f in files:
        text = read(f)
        counts = Counter(ID_RE.findall(text))
        found += sum(counts.values())
        for id_value, n in counts.items():
            if n > 1:
                failed += 1
                report.fail(
                    f"ID    {f.relative_to(ROOT)} uses id=\"{id_value}\" {n}× (must be unique)"
                )
    report.record("ids", found, failed)


def _clean_css(source: str) -> str:
    """Strip comments and url() payloads so neither leaks into the selector set."""
    return URL_RE.sub("", CSS_COMMENT_RE.sub("", source))


def extract_defined_classes(text: str) -> set[str]:
    """Pull class selectors from every <style> block in a document."""
    names: set[str] = set()
    for block in STYLE_BLOCK_RE.findall(text):
        cleaned = _clean_css(block)
        for name in CSS_CLASS_RE.findall(cleaned):
            if name not in CLASS_NAME_DENYLIST:
                names.add(name)
    return names


def extract_defined_classes_from_css(path: Path) -> set[str]:
    if not path.exists():
        return set()
    cleaned = _clean_css(read(path))
    return {n for n in CSS_CLASS_RE.findall(cleaned) if n not in CLASS_NAME_DENYLIST}


def extract_used_classes(text: str) -> set[str]:
    names: set[str] = set()
    for attr in CLASS_ATTR_RE.findall(text):
        for token in attr.split():
            names.add(token)
    return names


def check_classes(files: list[Path], report: Report) -> None:
    # Shared CSS used by arch pages.
    shared_css = extract_defined_classes_from_css(ARCH_DIR / "_shared.css")

    total_orphans = 0
    total_undefined = 0

    for f in files:
        # Skip partials/templates — they aren't rendered pages, so the
        # used/defined ratio is meaningless.
        if f.name.startswith("_"):
            continue
        text = read(f)
        defined = extract_defined_classes(text)
        # Arch pages inherit from _shared.css — merge it in.
        if f.parent == ARCH_DIR:
            defined |= shared_css
        used = extract_used_classes(text)

        orphans = (defined - used) - JS_TOGGLED_CLASSES - COMPOUND_ONLY_DEFINED
        undefined = (used - defined) - COMPOUND_ONLY_USED

        for cls in sorted(orphans):
            total_orphans += 1
            report.note(
                f"CSS?  {f.relative_to(ROOT)} defines .{cls} but no element uses it"
            )
        for cls in sorted(undefined):
            total_undefined += 1
            report.note(
                f"CSS?  {f.relative_to(ROOT)} uses .{cls} but no rule defines it"
            )

    report.record("classes", total_orphans + total_undefined, 0)


def check_tags(files: list[Path], report: Report) -> None:
    found = 0
    failed = 0
    for f in files:
        text = read(f)
        # Strip comments and style/script blocks so their contents don't skew counts.
        stripped = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        stripped = re.sub(r"<style[^>]*>.*?</style>", "", stripped, flags=re.S | re.I)
        stripped = re.sub(r"<script[^>]*>.*?</script>", "", stripped, flags=re.S | re.I)

        opens = Counter(
            t.lower() for t in TAG_OPEN_RE.findall(stripped)
            if t.lower() in STRUCTURAL_TAGS
        )
        closes = Counter(
            t.lower() for t in TAG_CLOSE_RE.findall(stripped)
            if t.lower() in STRUCTURAL_TAGS
        )
        for tag in STRUCTURAL_TAGS:
            found += opens[tag]
            if opens[tag] != closes[tag]:
                failed += 1
                report.fail(
                    f"TAGS  {f.relative_to(ROOT)} <{tag}> opened {opens[tag]}× "
                    f"but closed {closes[tag]}×"
                )
    report.record("tags", found, failed)


def check_assets(report: Report) -> None:
    if not ASSETS_DIR.exists():
        report.record("assets", 0, 0)
        return
    found = 0
    failed = 0
    for path in sorted(ASSETS_DIR.rglob("*")):
        if not path.is_file():
            continue
        # Skip gitignored original-source backups stored as dotfiles.
        if path.name.startswith("."):
            continue
        found += 1
        size = path.stat().st_size
        if size > ASSET_BUDGET_BYTES:
            failed += 1
            report.fail(
                f"ASSET {path.relative_to(ROOT)} is {size/1024/1024:.2f} MB "
                f"(budget {ASSET_BUDGET_BYTES/1024/1024:.0f} MB)"
            )
    report.record("assets", found, failed)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main(argv: Iterable[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--verbose", action="store_true",
                        help="list every check, not just failures")
    parser.add_argument("--strict", action="store_true",
                        help="treat informational notices as failures")
    args = parser.parse_args(list(argv))

    start = time.perf_counter()
    report = Report()
    files = html_files()

    check_links(files, report)
    check_ids(files, report)
    check_classes(files, report)
    check_tags(files, report)
    check_assets(report)

    elapsed = time.perf_counter() - start

    print(f"validate.py · {len(files)} HTML files · {elapsed*1000:.0f} ms")
    for name, found, failed in report.checks:
        status = "OK" if failed == 0 else "FAIL"
        print(f"  [{status:4}] {name:<8} checked {found:>4}  issues {failed}")

    if report.failures:
        print("\nFailures:")
        for msg in report.failures:
            print(f"  {msg}")

    if report.notices and (args.verbose or args.strict):
        print("\nNotices:")
        for msg in report.notices:
            print(f"  {msg}")
    elif report.notices:
        print(f"\n{len(report.notices)} informational notice(s). Re-run with --verbose to show.")

    failed = bool(report.failures) or (args.strict and bool(report.notices))
    if failed:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
