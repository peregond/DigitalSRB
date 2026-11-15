"""Renders the eight detail pages (idea/<slug>/index.html). Called from build.py."""
import re
from html import escape
from pathlib import Path

from pages_data import ORDER, PAGES, THEMES

ROOT = Path(__file__).resolve().parent.parent
LANGS = ("sr", "en")
LA = {"sr": "sr-Latn", "en": "en"}

UI = {
    "all": ("Sve ideje", "All ideas"),
    "idea": ("Ideja", "Idea"),
    "tier": ("Nivo", "Tier"),
    "sources": ("Izvori", "Sources"),
    "next": ("Sledeća ideja", "Next idea"),
    "prev": ("Prethodna ideja", "Previous idea"),
    "more": ("Sve ideje", "All ideas"),
    "vote_q": ("Šta misliš o ovoj ideji?", "What do you think of this idea?"),
    "up": ("Za", "For"), "down": ("Protiv", "Against"),
    "related": ("Povezane ideje", "Related ideas"),
    "today": ("Danas", "Today"), "after": ("Predlog", "Proposal"),
    "draft": ("Nacrt, novembar 2026.", "Draft, November 2026"),
    "print": ("Verzija za štampu (A4)", "Print version (A4)"),
    "skip": ("Preskoči na sadržaj", "Skip to content"),
    "example": ("Primer", "Example"),
}
KIND = {"law": ("Zakon", "Law"), "tech": ("Tehnika", "Technology"), "org": ("Organizacija", "Organisation")}


def B(pair, tag="span", cls=""):
    if isinstance(pair, str):
        return pair
    c = f' class="{cls}"' if cls else ""
    return "".join(f'<{tag}{c} lang="{LA[l]}">{pair[i]}</{tag}>' for i, l in enumerate(LANGS))


def mix(hexc, pct):
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    f = pct / 100
    return "#%02X%02X%02X" % tuple(round(255 - (255 - v) * f) for v in (r, g, b))


# ------------------------------------------------------------------ components
def head(blk, extra=""):
    out = f'<header class="pg-head"><p class="pg-eyebrow">{B(blk["eb"])}</p>{B(blk["t"], "h2")}'
    if blk.get("intro"):
        out += B(blk["intro"], "p", "pg-intro")
    return out + extra + "</header>"


def sec(blk, inner, idx, cls=""):
    sid = f' id="{blk["id"]}"' if blk.get("id") else ""
    tone = "alt" if idx % 2 else ""
    return f'<section class="pg-sec {tone} {cls}"{sid}><div class="wrap">{head(blk)}{inner}</div></section>'


def r_text(b):
    return '<div class="pg-prose">' + "".join(B(p, "p") for p in b["p"]) + "</div>"


def r_cards(b):
    n = len(b["items"])
    cols = 5 if n == 5 else (3 if n % 3 == 0 or n == 3 else 2 if n == 2 else 4)
    items = "".join(
        f'<article class="pg-card"><span class="pg-dot"></span>{B((i[0], i[1]), "h3")}{B((i[2], i[3]), "p")}</article>'
        for i in b["items"])
    return f'<div class="pg-cards c{cols}">{items}</div>'


def r_flow(b):
    def row(label, steps, cls):
        lis = "".join(f'<li><i>{k + 1}</i>{B(s)}</li>' for k, s in enumerate(steps))
        return f'<div class="flow-row {cls}"><p class="flow-label">{B(label)}</p><ol>{lis}</ol></div>'
    out = '<div class="pg-flow">' + row(UI["today"], b["today"], "today") + row(UI["after"], b["after"], "after") + "</div>"
    if b.get("note"):
        out += B(b["note"], "p", "pg-note")
    return out


def r_steps(b):
    items = "".join(f'<li><span class="n">{k + 1}</span>{B(t, "h3")}{B(x, "p")}</li>' for k, (t, x) in enumerate(b["items"]))
    return f'<ol class="pg-steps">{items}</ol>'


def r_bars(b):
    mx = max(r[1] for r in b["rows"]) or 1
    rows = ""
    for label, val, disp, mark in b["rows"]:
        w = max(val / mx * 100, 1.6)
        rows += (f'<div class="bar-row {mark}"><span class="bar-l">{B(label)}</span>'
                 f'<span class="bar-t"><i style="width:{w:.1f}%"></i></span><b>{B(disp)}</b></div>')
    out = f'<div class="pg-bars">{rows}</div>'
    if b.get("note"):
        out += B(b["note"], "p", "pg-note")
    return out


def r_table(b):
    th = "".join(f"<th>{B(h)}</th>" for h in b["head"])
    body = ""
    for i, row in enumerate(b["rows"]):
        cls = ' class="hl"' if b["hl"] == i else ""
        cells = "".join((f"<th scope=\"row\">{B(c)}</th>" if j == 0 else f"<td>{B(c)}</td>") for j, c in enumerate(row))
        body += f"<tr{cls}>{cells}</tr>"
    return f'<div class="pg-tablewrap"><table class="pg-table"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def r_check(b):
    items = "".join(f'<li><span class="tag {k}">{B(KIND[k])}</span>{B(t)}</li>' for k, t in b["items"])
    return f'<ul class="pg-check">{items}</ul>'


def r_faq(b):
    items = "".join(f'<details class="pg-q"><summary>{B(q)}</summary><div>{B(a, "p")}</div></details>' for q, a in b["items"])
    return f'<div class="pg-faq">{items}</div>'


# ---- custom infographics
def qr(x, y, size, fill="#111"):
    u = size / 7
    o = []
    for fx, fy in ((0, 0), (4, 0), (0, 4)):
        o.append(f'<rect x="{x + fx * u:.1f}" y="{y + fy * u:.1f}" width="{3 * u:.1f}" height="{3 * u:.1f}" rx="{u * .5:.1f}" fill="none" stroke="{fill}" stroke-width="{u * .6:.1f}"/>')
        o.append(f'<rect x="{x + (fx + 1) * u:.1f}" y="{y + (fy + 1) * u:.1f}" width="{u:.1f}" height="{u:.1f}" fill="{fill}"/>')
    for cx, cy in ((4, 4), (5, 4), (6, 5), (4, 6), (6, 6), (5, 5), (3, 3), (3, 5), (3, 1), (1, 3)):
        o.append(f'<rect x="{x + cx * u:.1f}" y="{y + cy * u:.1f}" width="{u * .9:.1f}" height="{u * .9:.1f}" fill="{fill}"/>')
    return "".join(o)


def c_clerk(b):
    return f'''<div class="clerk">
<div class="clerk-phone"><span class="clerk-notch"></span><svg viewBox="0 0 100 100" aria-hidden="true">{qr(8, 8, 84)}</svg>{B(("Predmet", "Case"), "b")}</div>
<div class="clerk-arrow" aria-hidden="true">→</div>
<div class="clerk-win"><div class="clerk-bar"><i></i><i></i><i></i></div>
<p class="clerk-title">{B(("Predmet: obnova boravišne dozvole", "Case: residence permit renewal"))} <em>{B(UI["example"])}</em></p>
<ul>
<li class="ok"><b>✓</b>{B(("Podnet zahtev", "Application filed"))}</li>
<li class="ok"><b>✓</b>{B(("Fotografija priložena", "Photo attached"))}</li>
<li class="miss"><b>!</b>{B(("Nedostaje: dokaz o adresi", "Missing: proof of address"))}</li>
<li class="next"><b>→</b>{B(("Sledeće: taksa, pa termin", "Next: pay the fee, then book a slot"))}</li>
</ul></div></div>'''


def c_journey22(b):
    axis = "".join(f'<span style="left:{p}%">{B(t)}</span>' for p, t in
                   ((0, ("dan 0", "day 0")), (33.3, ("1 mesec", "1 month")), (66.6, ("2 meseca", "2 months")), (100, ("3 meseca", "3 months"))))
    return f'''<div class="jr"><div class="jr-axis">{axis}</div>
<div class="jr-row"><p class="jr-name">{B(UI["today"])}</p><div class="jr-track">
<i class="jr-dot" style="left:0"></i><span class="jr-wait">{B(("čekanje, bez iznosa", "waiting, no figure"))}</span>
<span class="jr-win" style="left:66.6%;width:33.4%">{B(("konačan obračun: 2–3 meseca", "final assessment: 2–3 months"))}</span></div></div>
<div class="jr-row after"><p class="jr-name">{B(UI["after"])}</p><div class="jr-track">
<span class="jr-pill">{B(("isti dan: prijava, porez, plaćanje", "same day: request, tax, payment"))}</span></div></div></div>'''


NODES = [("Matične knjige", "Civil registers"), ("MUP", "MUP"), ("Poreska uprava", "Poreska uprava"), ("PIO", "PIO"),
         ("NSZ", "NSZ"), ("CROSO", "CROSO"), ("RGZ", "RGZ"), ("Pravosuđe", "Judiciary")]


def c_network30(b):
    import math
    cx, cy, rx, ry = 320, 190, 235, 135
    lines, nodes = [], []
    for i, (sr, en) in enumerate(NODES):
        a = -math.pi / 2 + i * 2 * math.pi / len(NODES)
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        lines.append(f'<line class="da" x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}"/>')
        nodes.append(f'<g><rect x="{x - 62:.0f}" y="{y - 19:.0f}" width="124" height="38" rx="19"/>'
                     f'<text x="{x:.0f}" y="{y + 5:.0f}" text-anchor="middle" lang="sr-Latn">{sr}</text>'
                     f'<text x="{x:.0f}" y="{y + 5:.0f}" text-anchor="middle" lang="en">{en}</text></g>')
    return f'''<figure class="net"><svg viewBox="0 0 640 380" role="img" aria-hidden="true">
<g class="net-l">{"".join(lines)}</g><g class="net-n">{"".join(nodes)}</g>
<circle class="net-c" cx="{cx}" cy="{cy}" r="54"/><text class="net-ct" x="{cx}" y="{cy + 7}" text-anchor="middle">eZUP</text></svg></figure>'''


def c_stats30(b):
    rows = [(("Služba A", "Office A"), 82), (("Služba B", "Office B"), 55), (("Služba C", "Office C"), 28), (("Služba D", "Office D"), 12)]
    inner = "".join(f'<div class="bar-row"><span class="bar-l">{B(l)}</span><span class="bar-t"><i style="width:{w}%"></i></span><b>…</b></div>' for l, w in rows)
    return (f'<div class="pg-bars ghost">{inner}</div>'
            + B(("Uverenja izdata samo da bi se nosila drugoj službi. Primer rasporeda, nema stvarnih podataka.",
                 "Certificates issued only to be carried to another office. A layout example with no real data."), "p", "pg-note"))


def c_phone47(b):
    rows = [(("punoletan", "over 18"), "on"), (("ime i fotografija", "name and photo"), "on"), (("JMBG, adresa", "personal number, address"), "off")]
    lis = "".join(f'<li class="{k}"><b>{"✓" if k == "on" else "–"}</b>{B(t)}</li>' for t, k in rows)
    return f'''<div class="phone-wrap"><div class="phone"><span class="ph-notch"></span>
<div class="ph-card"><span class="ph-flag">{B(("REPUBLIKA SRBIJA", "REPUBLIC OF SERBIA"))}</span><b>{B(("Boravišna dozvola", "Residence permit"))}</b>
<div class="ph-id"><i></i><p>{B(("IME PREZIME", "NAME SURNAME"))}<small>{B(("Privremeni boravak", "Temporary residence"))}</small></p></div></div>
<div class="ph-nfc" aria-hidden="true"><i></i><i></i><i></i></div>
<p class="ph-q">{B(("Deli samo:", "Share only:"))}</p><ul class="ph-share">{lis}</ul></div>
<div class="phone-side"><p class="ps-t">{B(("Kako ide provera", "How a check goes"))}</p><ol>
<li>{B(("Prineseš telefon čitaču ili pokažeš QR", "Hold the phone to the reader or show the QR"))}</li>
<li>{B(("Čitač traži jedan podatak", "The reader asks for one fact"))}</li>
<li>{B(("Ti potvrdiš", "You approve"))}</li>
<li>{B(("Deli se samo taj podatak", "Only that fact is shared"))}</li></ol></div></div>'''


def c_border48(b):
    items = [(("Ulazak", "Entry"), ("datum i granični prelaz", "date and border crossing")),
             (("Osnov", "Basis"), ("bezvizno 90/180, viza ili dozvola", "visa-free 90/180, visa or permit")),
             (("Preostali dani", "Days left"), ("računa sistem", "calculated by the system")),
             (("Izlazak", "Exit"), ("datum", "date"))]
    lis = "".join(f'<li>{B(t, "b")}{B(s, "span")}</li>' for t, s in items)
    return f'<ol class="chain">{lis}</ol>'


def c_speed50(b):
    t = [(("Standard", "Standard"), "30", ("dana", "days"), "×1", 34), (("Brže", "Faster"), "15", ("dana", "days"), "+50%", 62), (("Hitno", "Urgent"), "7", ("dana", "days"), "×2", 100)]
    cols = "".join(f'<div class="sp"><div class="sp-bar" style="--h:{h}"><b>{fee}</b></div>'
                   f'<p class="sp-days"><strong>{d}</strong> {B(u)}</p>{B(n, "p", "sp-n")}</div>' for n, d, u, fee, h in t)
    return (f'<div class="speeds"><p class="sp-cap">{B(("Taksa", "Fee"))}</p>{cols}</div>')


CUSTOM = {"clerk": c_clerk, "journey22": c_journey22, "network30": c_network30, "stats30": c_stats30,
          "phone47": c_phone47, "border48": c_border48, "speed50": c_speed50}
RENDER = {"text": r_text, "cards": r_cards, "flow": r_flow, "steps": r_steps, "bars": r_bars, "table": r_table,
          "check": r_check, "faq": r_faq}


# ------------------------------------------------------------------ page
def sources_html(parts):
    seen, out = set(), []
    for p in parts:
        for m in re.finditer(r'<a href="([^"]+)">(.*?)</a>', p["src"]):
            if m.group(1) not in seen:
                seen.add(m.group(1))
                out.append(f'<li><a href="{m.group(1)}" rel="noopener">{m.group(2)}</a></li>')
    return "".join(out)


def vote_html(n):
    return (f'<div class="pg-vote"><div class="wrap"><footer class="vote" data-vote="{n}">'
            f'{B(UI["vote_q"], "span", "vote-q")}<div class="vote-btns">'
            f'<button type="button" class="vbtn up" data-dir="up" aria-pressed="false"><span class="sign" aria-hidden="true">+</span>{B(UI["up"], "span", "sr-only")}<span class="count" hidden></span></button>'
            f'<button type="button" class="vbtn down" data-dir="down" aria-pressed="false"><span class="sign" aria-hidden="true">−</span>{B(UI["down"], "span", "sr-only")}<span class="count" hidden></span></button>'
            f'</div></footer></div></div>')


def build_all(ctx):
    """ctx: toc, ideas, tier_of, tiers, featured, ver, template (str)."""
    toc, ideas, tier_of, ver = ctx["toc"], ctx["ideas"], ctx["tier_of"], ctx["ver"]
    taglines = {n: (sr, en) for n, sr, en in ctx["featured"]}
    clean = lambda l, n: re.sub(r"\s*\(.*?\)\s*$", "", re.sub(r"</?strong>", "", toc[l][n]))
    titles = {n: (clean("sr", n), clean("en", n)) for n in ORDER}
    tpl = ctx["template"]
    for pos, n in enumerate(ORDER):
        slug, th, dk = THEMES[n]
        page, tier = PAGES[n], tier_of(n)
        tname = (tier["sr"]["name"], tier["en"]["name"])
        tsub = (f'{tier["sr"]["sub"]} · {tier["sr"]["time"]}', f'{tier["en"]["sub"]} · {tier["en"]["time"]}')
        sections = ""
        for i, blk in enumerate(page["blocks"]):
            if blk["k"] == "custom":
                inner = CUSTOM[blk["name"]](blk)
            else:
                inner = RENDER[blk["k"]](blk)
            sections += sec(blk, inner, i)
        hstats = "".join(f'<li><b>{B(v)}</b>{B(l, "span")}</li>' for v, l in page["stats"])
        rel = "".join(
            f'<a href="../../index.html#idea-{r}"><b>{r:02d}</b>{B((clean("sr", r), clean("en", r)))}</a>' for r in page["related"])
        prev_n, next_n = ORDER[pos - 1], ORDER[(pos + 1) % len(ORDER)]

        def nb(m, label):
            ms, _, md = THEMES[m]
            return (f'<a class="pg-nb" href="../{ms}/" style="--th:{THEMES[m][1]}"><span class="pg-nb-l">{B(label)}</span>'
                    f'<img src="../../assets/featured/{m:02d}.svg" alt="" loading="lazy">{B(titles[m], "strong")}</a>')

        parts = ideas[n]["en"]
        html = (tpl.replace("{{TITLE_SR}}", escape(titles[n][0] + " · Digitalna Srbija"))
                .replace("{{TITLE_EN}}", escape(titles[n][1] + " · Digital Serbia"))
                .replace("{{DESC_SR}}", escape(taglines[n][0])).replace("{{DESC_EN}}", escape(taglines[n][1]))
                .replace("{{TH}}", th).replace("{{TH2}}", dk).replace("{{TINT}}", mix(th, 9)).replace("{{TINT2}}", mix(th, 18))
                .replace("{{NUM}}", f"{n:02d}").replace("{{N}}", str(n))
                .replace("{{EYEBROW}}", B(UI["idea"]) + f" {n:02d} · " + B(tname))
                .replace("{{H1}}", B(titles[n], "h1")).replace("{{TAGLINE}}", B(taglines[n], "p", "pg-tag"))
                .replace("{{TIERLINE}}", B(tsub, "p", "pg-tier"))
                .replace("{{HSTATS}}", hstats).replace("{{SECTIONS}}", sections)
                .replace("{{RELATED}}", rel).replace("{{SOURCES}}", sources_html(parts))
                .replace("{{VOTE}}", vote_html(n))
                .replace("{{PREV}}", nb(prev_n, UI["prev"])).replace("{{NEXT}}", nb(next_n, UI["next"]))
                .replace("{{V}}", ver))
        assert "{{" not in html, re.findall(r"\{\{[A-Z0-9_]+\}\}", html)
        out = ROOT / "idea" / slug
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(html, encoding="utf-8")
    print(f"idea/: {len(ORDER)} pages")
