#!/usr/bin/env python3
"""Builds index.html (the website) from source/print.html (the A4 bilingual document).

Usage: python3 tools/build.py
Edit texts in source/print.html, edit the page shell in tools/template.html, then rebuild.
"""
import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
LANGS = ("sr", "en")
LANG_ATTR = {"sr": "sr-Latn", "en": "en"}

TIERS = [
    {"n": 1, "color": "#12A150", "first": 1, "last": 24,
     "sr": {"name": "Odmah", "sub": "Samo tehnika", "time": "3–12 meseci",
            "desc": "Ne treba menjati nijedan zakon. Dovoljni su programeri, dizajn i volja službe."},
     "en": {"name": "Right away", "sub": "Technology only", "time": "3–12 months",
            "desc": "No law needs to change. Developers, design and the will of the office are enough."}},
    {"n": 2, "color": "#F2A100", "first": 25, "last": 46,
     "sr": {"name": "Malo duže", "sub": "Povezivanje i pravilnici", "time": "1–2 godine",
            "desc": "Bez novog zakona, ali traži povezivanje registara, podzakonske akte i dogovor sa NBS i bankama."},
     "en": {"name": "A bit longer", "sub": "Integration and bylaws", "time": "1–2 years",
            "desc": "No new law, but it needs connected registers, bylaws and agreements with NBS (the central bank) and banks."}},
    {"n": 3, "color": "#E30613", "first": 47, "last": 60,
     "sr": {"name": "Novi zakon", "sub": "Odluka Skupštine", "time": "2+ godine",
            "desc": "Traži izmenu postojećeg ili potpuno nov zakon."},
     "en": {"name": "A new law", "sub": "A decision of Parliament", "time": "2+ years",
            "desc": "Needs an amendment to an existing law or an entirely new one."}},
]
# Main ideas shown as animated cards on the home page.
# Artwork: assets/featured/NN.webp (1200x900). Without the file a coloured animated card is shown.
FEATURED = [
    (1, "Skeniraš jednom. Službenik već zna tvoj slučaj.", "Scan once. The clerk already knows your case."),
    (22, "Firma se otvara i zatvara za jedan dan. Konačni porez odmah.", "Open or close a business in a day. Final tax paid on the spot."),
    (30, "Država već ima tvoja dokumenta. Ne nosi ih više.", "The state already has your papers. Stop carrying them."),
    (21, "Paket jednim QR kodom, carina u roku od jednog radnog dana.", "A parcel with one QR code, customs within one working day."),
    (47, "Lična karta i boravak u novčaniku na telefonu.", "Your ID and residence card in your phone wallet."),
    (48, "Nema više prijave boravka stranaca u roku od 24 sata.", "No more 24-hour registration of stay for foreigners."),
    (50, "Tri zvanična roka. Taksa ide u budžet, ne u džep.", "Three official speeds. The fee goes to the budget, not a pocket."),
    (53, "Digitalni sud za više od milion nerešenih predmeta.", "A digital court for over a million pending cases."),
]

UI = {
    "problem": {"sr": "Problem", "en": "The problem"},
    "proposal": {"sr": "Predlog", "en": "The proposal"},
    "sources": {"sr": "Izvori", "en": "Sources"},
    "ideas": {"sr": "ideja", "en": "ideas"},
    "tier": {"sr": "Nivo", "en": "Tier"},
    "list": {"sr": "Spisak ideja", "en": "List of ideas"},
    "vote_q": {"sr": "Šta misliš o ovoj ideji?", "en": "What do you think of this idea?"},
    "vote_up": {"sr": "Za", "en": "For"},
    "vote_down": {"sr": "Protiv", "en": "Against"},
}


def bi(key_or_map, tag="span", cls=""):
    """Both language versions of a UI string, one element per language."""
    m = UI[key_or_map] if isinstance(key_or_map, str) else key_or_map
    c = f' class="{cls}"' if cls else ""
    return "".join(f'<{tag}{c} lang="{LANG_ATTR[l]}">{m[l]}</{tag}>' for l in LANGS)


def inner(el):
    return el.decode_contents().strip() if el else ""


def clean_svg(svg, lang, uid):
    """Drop print-only fonts and make ids unique per language copy."""
    for t in svg.find_all(attrs={"font-family": True}):
        del t["font-family"]
        t["class"] = (t.get("class") or []) + ["dsp"]
    out = str(svg)
    for i in set(re.findall(r'\bid="([^"]+)"', out)):
        out = out.replace(f'id="{i}"', f'id="{i}-{uid}-{lang}"').replace(f"url(#{i})", f"url(#{i}-{uid}-{lang})")
    return out


def parse():
    soup = BeautifulSoup((ROOT / "source" / "print.html").read_text(encoding="utf-8"), "html.parser")
    pages = soup.select("section.page")
    intro = {l: pages[1].select_one(f".half.{l}") for l in LANGS}
    ideas = {}
    for l in LANGS:
        for art in soup.select(f".half.{l} article.item"):
            num = int(art.select_one(".num").get_text())
            kick = art.select_one(".kick")
            part = {
                "kick": kick.get_text() if kick else "",
                "title": inner(art.select_one("h3")),
                "prob": inner(art.select_one(".prob")),
                "prop": inner(art.select_one(".prop")),
                "extra": art.select_one(".extra"),
                "src": inner(art.select_one(".src")),
                "svg": art.select_one("svg.vis, svg.mock"),
                "mock": "mockpage" in art.get("class", []),
            }
            if part["svg"]:
                part["svg"] = clean_svg(part["svg"], l, art["id"])
            ideas.setdefault(num, {}).setdefault(l, []).append(part)
    sources = {l: pages[-1].select_one(f".half.{l}") for l in LANGS}
    # the print sheet splits one numbered list across two halves; merge them
    src_items = "".join(str(li) for l in LANGS for li in sources[l].select("ol.srcs li"))
    src_note = {l: sources[l].select_one(".note").get_text() for l in LANGS}
    toc = {l: {int(a["href"].split("-")[1]): re.sub(r"^<b>\d+</b>\s*", "", inner(a))
               for a in soup.select(f".half.{l} ol.toc a")} for l in LANGS}
    return intro, ideas, toc, src_items, src_note


def is_rich(by_lang):
    """Ideas with a visual, extra blocks or several parts need the full row."""
    return any(p["svg"] or p["extra"] for p in by_lang["en"]) or len(by_lang["en"]) > 1


def wide_set(nums, ideas):
    """Rich ideas take a full row; so does a plain one left without a neighbour."""
    wide, run = set(), []
    for n in list(nums) + [None]:
        if n is None or is_rich(ideas[n]):
            if len(run) % 2:
                wide.add(run[-1])
            run = []
            if n is not None:
                wide.add(n)
        else:
            run.append(n)
    return wide


def render_idea(num, by_lang, tier, toc, wide):
    body = []
    for l in LANGS:
        parts = by_lang[l]
        series = len(parts) > 1 and not any(p["mock"] for p in parts)  # e.g. the 4-part post reform
        title = re.sub(r"\s*\(.*?\)\s*$", "", toc[l][num]) if series else parts[0]["title"]
        h = [f'<div class="idea-body" lang="{LANG_ATTR[l]}">', f"<h3>{title}</h3>"]
        text, visual, tail = [], "", []
        for i, p in enumerate(parts):
            if p["mock"]:
                visual = p["svg"]
                continue
            blk = []
            if series:
                blk.append(f'<p class="step">{i + 1}/{len(parts)}</p><h4>{p["title"]}</h4>')
            blk.append(f'<p class="lbl">{UI["problem"][l]}</p><p class="prob">{p["prob"]}</p>')
            blk.append(f'<p class="lbl accent">{UI["proposal"][l]}</p><p class="prop">{p["prop"]}</p>')
            if p["src"] and series:
                blk.append(f'<p class="src">{p["src"]}</p>')
            elif p["src"]:
                tail.append(f'<p class="src">{p["src"]}</p>')
            if p["svg"]:
                visual = p["svg"]
            if p["extra"]:
                cols = []
                for d in p["extra"].find_all("div", recursive=False):
                    lbl, txt = d.select_one(".lbl"), d.find_all("p")[-1]
                    meter = lbl.select_one(".meter")
                    dots = ""
                    if meter:
                        on = len(meter.select(".m.on"))
                        dots = f'<span class="meter" aria-label="{on}/3">' + "".join(
                            f'<i class="{"on" if k < on else ""}"></i>' for k in range(3)) + "</span>"
                        meter.extract()
                    cols.append(f'<div><p class="lbl">{lbl.get_text().strip()}{dots}</p><p>{inner(txt)}</p></div>')
                tail.insert(0, f'<div class="extra">{"".join(cols)}</div>')
            text.append(f'<div class="part">{"".join(blk)}</div>')
        if series:
            h.append(f'<div class="parts">{"".join(text)}</div>')
        elif visual:
            h.append(f'<div class="split"><div>{"".join(text)}</div><figure class="visual">{visual}</figure></div>')
        else:
            h.append("".join(text))
        h.append("".join(tail))
        h.append("</div>")
        body.append("".join(h))
    vote = (
        f'<footer class="vote" data-vote="{num}">{bi("vote_q", cls="vote-q")}'
        f'<div class="vote-btns">'
        f'<button type="button" class="vbtn up" data-dir="up" aria-pressed="false">'
        f'<span class="sign" aria-hidden="true">+</span>{bi("vote_up", cls="sr-only")}<span class="count" hidden></span></button>'
        f'<button type="button" class="vbtn down" data-dir="down" aria-pressed="false">'
        f'<span class="sign" aria-hidden="true">−</span>{bi("vote_down", cls="sr-only")}<span class="count" hidden></span></button>'
        f"</div></footer>"
    )
    return (
        f'<article class="idea reveal{" wide" if wide else ""}" id="idea-{num}" data-tier="{tier["n"]}" style="--tc:{tier["color"]}">'
        f'<p class="idea-num"><span>{num:02d}</span><i class="tdot"></i>{bi({l: tier[l]["name"] for l in LANGS}, cls="tname")}</p>'
        f'{"".join(body)}{vote}</article>'
    )


def tier_of(n):
    return next(t for t in TIERS if t["first"] <= n <= t["last"])


def render_featured(toc):
    out = []
    for i, (n, sr, en) in enumerate(FEATURED):
        t = tier_of(n)
        title = {l: re.sub(r"\s*\(.*?\)\s*$", "", re.sub(r"</?strong>", "", toc[l][n])) for l in LANGS}
        out.append(
            f'<a class="fcard" href="#idea-{n}" style="--tc:{t["color"]};--i:{i}">'
            f'<div class="fc-art" aria-hidden="true"><span class="fc-ring r1"></span><span class="fc-ring r2"></span>'
            f'<span class="fc-n">{n:02d}</span>'
            f'<img class="fc-img" src="assets/featured/{n:02d}.webp" alt="" loading="lazy" decoding="async" '
            f'onerror="this.style.display=\'none\'"></div>'
            f'<div class="fc-body"><p class="fc-tier"><i class="tdot"></i>{bi({l: t[l]["name"] for l in LANGS})}</p>'
            f'{bi(title, "h3")}{bi({"sr": sr, "en": en}, "p", "fc-text")}</div></a>'
        )
    return "".join(out)


def main():
    intro, ideas, toc, src_items, src_note = parse()
    assert sorted(ideas) == list(range(1, 61)), sorted(ideas)

    intro_html = ""
    for l in LANGS:
        ps = intro[l].find_all("p")
        intro_html += (f'<div lang="{LANG_ATTR[l]}"><p class="lead">{inner(ps[0])}</p>'
                       + "".join(f"<p>{inner(p)}</p>" for p in ps[1:]) + "</div>")

    tier_cards, tier_sections, nav_links, filters = "", "", "", ""
    for t in TIERS:
        count = t["last"] - t["first"] + 1
        tier_cards += (
            f'<a class="tile reveal" href="#tier-{t["n"]}" style="--tc:{t["color"]}">'
            f'<p class="tile-eyebrow"><i class="tdot"></i>{bi({l: UI["tier"][l] + " " + str(t["n"]) for l in LANGS})}</p>'
            f'<p class="tile-count">{count}<small>{bi("ideas")}</small></p>'
            f'{bi({l: t[l]["name"] for l in LANGS}, "h3")}'
            f'{bi({l: t[l]["sub"] + " · " + t[l]["time"] for l in LANGS}, "p", "tile-sub")}'
            f'{bi({l: t[l]["desc"] for l in LANGS}, "p", "tile-desc")}</a>'
        )
        nav_links += f'<a href="#tier-{t["n"]}">{bi({l: t[l]["name"] for l in LANGS})}</a>'
        filters += (f'<button type="button" class="chip" data-filter="{t["n"]}" aria-pressed="false" style="--tc:{t["color"]}">'
                    f'<i class="tdot"></i>{bi({l: t[l]["name"] for l in LANGS})}<b>{count}</b></button>')
        nums = range(t["first"], t["last"] + 1)
        wide = wide_set(nums, ideas)
        toc_html = "".join(
            f'<li><a href="#idea-{n}"><b>{n:02d}</b>{bi({l: re.sub(r"</?strong>", "", toc[l][n]) for l in LANGS})}</a></li>'
            for n in nums)
        tier_sections += (
            f'<section class="tier-section" id="tier-{t["n"]}" data-tier="{t["n"]}" style="--tc:{t["color"]}">'
            f'<header class="tier-head reveal"><p class="eyebrow"><i class="tdot"></i>'
            f'{bi({l: UI["tier"][l] + " " + str(t["n"]) + " · " + t[l]["sub"] + " · " + t[l]["time"] for l in LANGS})}</p>'
            f'{bi({l: t[l]["name"] for l in LANGS}, "h2")}{bi({l: t[l]["desc"] for l in LANGS}, "p", "tier-desc")}'
            f'<details class="toc"><summary>{bi("list")} <span class="n">{count}</span></summary><ol>{toc_html}</ol></details></header>'
            f'<div class="ideas">{"".join(render_idea(n, ideas[n], t, toc, n in wide) for n in nums)}</div></section>'
        )

    tpl = (ROOT / "tools" / "template.html").read_text(encoding="utf-8")
    out = (tpl.replace("{{INTRO}}", intro_html).replace("{{TIER_CARDS}}", tier_cards)
           .replace("{{NAV_LINKS}}", nav_links).replace("{{FILTERS}}", filters).replace("{{FEATURED}}", render_featured(toc))
           .replace("{{TIER_SECTIONS}}", tier_sections).replace("{{SOURCES}}", src_items)
           .replace("{{SOURCES_NOTE}}", bi(src_note, "p", "note")))
    assert "{{" not in out
    (ROOT / "index.html").write_text(out, encoding="utf-8")
    print(f"index.html: {len(out) // 1024} KB, {len(ideas)} ideas")


if __name__ == "__main__":
    main()
