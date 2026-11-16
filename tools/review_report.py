#!/usr/bin/env python3
"""Writes docs/REVIEW.md: every text on the detail pages that was drafted (not taken from the source document), as a checklist.

Run after tools/build.py:  python3 tools/review_report.py
"""
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pages_data import ORDER, THEMES  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

INTRO = """# Review checklist for the drafted text

The detail pages mix **your ideas and sourced figures** with **text I drafted** to explain how an idea could work: the steps,
the before/after lists, the answers to "what if", the card texts and the comparisons. The drafted text has not been checked
against real procedures. Please read it and tick or fix each line. Texts live in `tools/pages_data.py` and `tools/build_pages.py`;
after editing run `python3 tools/build.py`.

**Always examples, never data:** names, amounts, dates, branches, countries ("Country A"), ID numbers and the "bank" names on the
screens and in the portal mock are made up and labelled "example". The old ePorezi and APR pictures are real screenshots (personal data removed).

## What I am least sure about

- **QR at the counter (idea 1):** a printed code or an SMS link for people without a smartphone, and the "system is down, fall back to paper" answer are my assumptions.
- **Business closing (idea 22):** that the state can calculate the final tax on the same day, and the larger-firm rule (pay now, top up after the report), are the proposal's logic, not an existing procedure. The 2-3 months figure and the Georgia/Estonia examples are sourced.
- **Papers the state already has (idea 30):** the 18 databases, eight institutions and the EUR 50 property sheet are sourced; "a clerk must justify a request in writing" and the public statistics per office are the proposal.
- **Wallet ID (idea 47):** ISO 18013-5 and EUDI are named in your text; the "share only what is needed" flow follows those standards but the screens are a concept.
- **Registration of stay (idea 48):** Kazakhstan (2020) and the UK (2022) come from your sources; the claim that the border database is enough is your argument, presented as such.
- **Fast track (idea 50):** 30 / 15 / 7 days with +50% and double fee are from your text; the Georgian passport prices and the UK options are sourced. The sample fee amounts on the screens are invented.
- **Driving licence (idea 53):** the six-month rule is sourced (Welcome to Serbia). I found **no official list of countries or procedure**, so the page proposes a public page per country and does not claim any country is recognised.
- **Single tax portal (idea 9):** how ePorezi and APR look today comes from screenshots you supplied; that agencies stay independent is your condition. The portal screens are a concept.

---
"""


def page_review(path):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    title = soup.select_one(".pg-hero h1[lang=en]").get_text(" ", strip=True)
    out = [f"## {title}", f"`/{path.parent.relative_to(ROOT)}/`", ""]
    for sec in soup.select("main > section.pg-sec, main > header.pg-hero"):
        head = sec.select_one("h2[lang=en]") or sec.select_one("h1[lang=en]")
        if "rel" in (sec.get("class") or []):
            continue
        if sec.get("id") == "sources":
            continue
        lines, seen = [], set()
        for el in sec.select("[lang=en]"):
            if el.find_parent(attrs={"lang": "en"}) or el.find_parent(class_=re.compile(r"^(pa-phone|pa-browser|pa-ai|pg-nb|pa-oldrow|shots-old)$")):
                continue
            if el.find_parent("figcaption") or el.find_parent(class_="shot"):
                continue
            if head is not None and el is head:
                continue
            t = re.sub(r"\s+", " ", el.get_text(" ", strip=True))
            cls = " ".join(el.get("class") or [])
            if len(t) < 3 or t in seen or el.find_parent(class_="vote") or re.search(r"pg-eyebrow|flow-label|pg-vs-k|pg-tier|step", cls):
                continue
            if re.fullmatch(r"(\d+ steps?|Before|After|Today|Proposal|Overview|\d+/\d)", t):
                continue
            seen.add(t)
            lines.append(t)
        if not lines:
            continue
        out.append(f"### {head.get_text(' ', strip=True) if head is not None else 'Intro'}")
        out += [f"- [ ] {l}" for l in lines]
        out.append("")
    srcs = soup.select("#sources .srcs li")
    if srcs:
        out.append("### Sources on this page")
        out += [f"- {li.get_text(' ', strip=True)}" for li in srcs]
        out.append("")
    return out


def main():
    lines = [INTRO]
    by_slug = {slug: n for n, (slug, _, _) in THEMES.items()}
    for n in ORDER:
        slug = THEMES[n][0]
        lines += page_review(ROOT / "idea" / slug / "index.html")
    (ROOT / "docs" / "REVIEW.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("docs/REVIEW.md:", sum(1 for l in lines if l.startswith("- [ ]")), "lines to check")


if __name__ == "__main__":
    main()
