#!/usr/bin/env python3
"""Copy the weak.intel submodule site into docs/weak.intel and wrap it with bubble-map chrome.

Live address: https://pq-cybarg.github.io/bubble-map/weak.intel/
The nested pages self-identify as weak.intel. Separate proof core: do not mix
attack-layer edges into the financial SCC.
"""
from __future__ import annotations

import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nav as _nav  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "weak.intel", "docs")
DST = os.path.join(ROOT, "docs", "weak.intel")
NEST_LABEL = "weak.intel"
BODY_RE = re.compile(r"(<body[^>]*>)", re.I)


def parent_navbar() -> str:
    bits = []
    for h, t in _nav.NAV_ITEMS:
        if t == NEST_LABEL:
            href = "index.html"
        elif h.startswith("http"):
            href = h
        else:
            href = "../" + h
        cur = t == NEST_LABEL
        color = "#7b2d26" if cur else "#1f4e79"
        wt = 700 if cur else 400
        bits.append(
            f'<a href="{href}" style="color:{color};text-decoration:none;'
            f'white-space:nowrap;font-weight:{wt}">{t}</a>'
        )
    disc = _nav.DISCLAIMER.replace('href="methodology.html"', 'href="../methodology.html"')
    return (
        '<nav style="position:sticky;top:0;z-index:260;background:#fffdf8;'
        'border-bottom:1px solid #e4ddcc;padding:9px 14px;'
        'box-shadow:0 1px 6px rgba(60,50,30,.06);'
        'display:flex;flex-wrap:wrap;gap:5px 15px;justify-content:center;align-items:center;'
        'font:13.5px/1.55 -apple-system,Segoe UI,Roboto,sans-serif">'
        + "".join(bits)
        + "</nav>"
        + '<div style="background:#faf8f2;color:#8a8378;font:11px/1.5 -apple-system,Segoe UI,'
        'Roboto,sans-serif;text-align:center;padding:6px 16px;border-bottom:1px solid #e4ddcc">'
        + disc
        + "</div>"
        + '<div style="background:#12161f;color:#e0c07a;font:11px/1.4 IBM Plex Mono,monospace;'
        'text-align:center;padding:5px 12px;letter-spacing:.14em;text-transform:uppercase">'
        "weak.intel · nested dual-use companion"
        "</div>"
    )


def rewrite_brand(html: str) -> str:
    html = html.replace("Weak.Intel", "weak.intel")
    html = html.replace("Weak.intel", "weak.intel")
    html = html.replace("<title>Home — weak.intel</title>", "<title>weak.intel</title>")
    html = html.replace("<title>Home - weak.intel</title>", "<title>weak.intel</title>")
    return html


def main() -> None:
    if not os.path.isdir(SRC):
        raise SystemExit("missing submodule site: " + SRC)
    if os.path.isdir(DST):
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)
    open(os.path.join(DST, ".nojekyll"), "w").close()
    bar = parent_navbar()
    n = 0
    for dirpath, _, files in os.walk(DST):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            path = os.path.join(dirpath, fn)
            raw = open(path, encoding="utf-8").read()
            raw = rewrite_brand(raw)
            raw = BODY_RE.sub(r"\1" + bar, raw, count=1)
            open(path, "w", encoding="utf-8").write(raw)
            n += 1
    print("nested weak.intel: %d html pages -> docs/weak.intel/" % n)


if __name__ == "__main__":
    main()
