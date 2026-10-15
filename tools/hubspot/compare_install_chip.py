#!/usr/bin/env python3
"""Add or remove the install chip in the CLOSE section of every comparison page.

    python tools/hubspot/compare_install_chip.py            # add the chip (idempotent)
    python tools/hubspot/compare_install_chip.py --remove   # take it out again

The chip sits after the Talk to Akka button. Everything this adds lives between the
compare-install markers or in the install-line block, so --remove returns each page to
its previous text. Both directions regenerate comparisons/hubspot/ from the pages.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "sales-presentation" / "builder"))
import install_line  # noqa: E402
from hubspot import to_hubspot_fragment  # noqa: E402

PAGES = ROOT / "comparisons"
CTA = '<a class="cta" href="https://akka.io/contact-us">Talk to Akka <span aria-hidden="true">→</span></a>'
# The CTA's own top margin moves to the row, so the chip and the button share a centre line.
ROW_CSS = ("<style>.close .rv:has(> button.akka-install){display:flex;flex-wrap:wrap;"
           "justify-content:center;align-items:center;gap:16px 20px;margin-top:34px}"
           ".close .rv:has(> button.akka-install) .cta{margin-top:0}</style>")
CHIP = "<!-- compare-install:start -->" + ROW_CSS + install_line.button("chip", lead=True) + "<!-- compare-install:end -->"
CHIP_RE = re.compile(r"<!-- compare-install:start -->.*?<!-- compare-install:end -->", re.S)
ASSETS_RE = re.compile(r"\r?\n" + re.escape(install_line.START) + r".*?" + re.escape(install_line.END)
                       + r"\r?\n(?=</body>)", re.S)


def add(s):
    if CHIP_RE.search(s):
        return s
    if s.count(CTA) != 1:
        raise SystemExit("expected one Talk to Akka button")
    s = s.replace(CTA, CTA + CHIP)
    block = "\n" + install_line.assets() + "\n"
    if "\r\n" in s:
        block = block.replace("\n", "\r\n")
    return s.replace("</body>", block + "</body>", 1)


def remove(s):
    return ASSETS_RE.sub("", CHIP_RE.sub("", s))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--remove", action="store_true")
    a = ap.parse_args()
    pages = sorted(PAGES.glob("compare-*.html"))
    for p in pages:
        # Bytes in and out: the pages mix LF and CRLF, and each keeps its own.
        s = p.read_bytes().decode("utf-8")
        p.write_bytes((remove(s) if a.remove else add(s)).encode("utf-8"))
    # Written the way build-all.py writes them, so a later build leaves them unchanged.
    for p in pages:
        with open(p, encoding="utf-8") as f:
            frag = to_hubspot_fragment(f.read(), base_dir=str(PAGES), label=p.stem)
        with open(PAGES / "hubspot" / p.name, "w", encoding="utf-8") as f:
            f.write(frag)
    print(("removed from" if a.remove else "added to"), len(pages), "pages")


if __name__ == "__main__":
    main()
