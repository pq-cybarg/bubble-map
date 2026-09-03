#!/usr/bin/env python3
"""nav.py - the ONE canonical site navbar, used by every page builder so all pages show the
full nav. Self-contained inline styles (works on any page's theme); flex-wrap so the complete
set is always visible and never clipped/overflowed."""

NAV_ITEMS = [   # order matches build_dashboard.navlinks() so every page's nav is identical
    ("index.html", "Home"), ("atlas.html", "Atlas"), ("dashboard.html", "Dashboard"),
    ("charts.html", "Charts"), ("multidenom.html", "Real value"), ("research.html", "Research"),
    ("persons.html", "Persons"), ("blockchain.html", "Blockchain"),
    ("bubblemap.html", "Bubble Map"), ("globe.html", "Globe"),
    ("quantum.html", "Quantum"),
    ("leadership.html", "Leadership"), ("lenses.html", "Lenses"), ("methodology.html", "Methodology"),
    ("glossary.html", "Glossary"), ("https://github.com/pq-cybarg/bubble-map", "Source ↗"),
]

DISCLAIMER = ('Independent research &amp; opinion. Gradings are automated / LLM-assisted and may '
    'contain errors or hallucinations; nothing here is a statement of fact, financial advice, or an '
    'accusation of wrongdoing by any party. Claims about identifiable people or organizations reflect '
    'public records + good-faith interpretation; intent is not inferred from association. '
    '<a href="methodology.html" style="color:#6b665d;text-decoration:underline">Methodology &amp; disclaimer</a>.')

def navbar(active="", disclaimer=False):
    """Return the canonical nav strip (optionally + the disclaimer sub-bar). `active` = the label
    of the current page (rendered bold/maroon)."""
    def a(h, t):
        cur = (t == active)
        return (f'<a href="{h}" style="color:{"#7b2d26" if cur else "#1f4e79"};text-decoration:none;'
                f'white-space:nowrap;font-weight:{700 if cur else 400}">{t}</a>')
    strip = ('<nav style="position:sticky;top:0;z-index:60;background:#fffdf8;'
             'border-bottom:1px solid #e4ddcc;padding:9px 14px;box-shadow:0 1px 6px rgba(60,50,30,.06);'
             'display:flex;flex-wrap:wrap;gap:5px 15px;justify-content:center;align-items:center;'
             'font:13.5px/1.55 -apple-system,Segoe UI,Roboto,sans-serif">'
             + "".join(a(h, t) for h, t in NAV_ITEMS) + '</nav>')
    if disclaimer:
        strip += ('<div style="background:#faf8f2;color:#8a8378;font:11px/1.5 -apple-system,Segoe UI,'
                  'Roboto,sans-serif;text-align:center;padding:6px 16px;border-bottom:1px solid #e4ddcc">'
                  + DISCLAIMER + '</div>')
    return strip
