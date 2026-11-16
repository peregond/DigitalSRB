"""Renders the eight detail pages (idea/<slug>/index.html). Called from build.py."""
import re
from html import escape
from pathlib import Path

from categories import cat_of
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
# block kinds that are not shown on the pages (the data stays in pages_data.py)
SKIP_KINDS = {"check"}
# pages whose hero has no "topic · idea number" line
NO_EYEBROW = set(ORDER)
# pages whose hero text differs from the short tagline on the home-page card
HERO_TEXT = {
    22: ("Otvaranje i zatvaranje firme za jedan radni dan, a konačan porez vidiš i plaćaš odmah, ne meseci kasnije.",
         "Opening and closing a business in one working day, with the final tax shown and paid at once, not months later."),
    21: ("Digitalizujemo sve što se i dalje radi na papiru i ukidamo ručni posao koji usporava svaki korak pošte: od slanja i obrade do isporuke i preuzimanja.",
         "We digitalise what is still done on paper and remove the manual work that slows every stage of the post: from sending and processing to delivery and pickup."),
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
    sid = f' id="{blk.get("id") or "s%d" % idx}"'
    tone = "alt" if idx % 2 else ""
    cls = f"{cls} {blk.get('cls', '')}"
    return f'<section class="pg-sec {tone} {cls}"{sid}><div class="wrap">{head(blk)}{inner}</div></section>'


def r_text(b):
    return '<div class="pg-prose">' + "".join(B(p, "p") for p in b["p"]) + "</div>"


def r_cards(b):
    n = len(b["items"])
    if not n:
        return ""
    cols = 5 if n == 5 else (3 if n % 3 == 0 or n == 3 else 2 if n == 2 else 4)
    items = "".join(
        f'<article class="pg-card"><span class="pg-dot"></span>{B((i[0], i[1]), "h3")}{B((i[2], i[3]), "p")}</article>'
        for i in b["items"])
    return f'<div class="pg-cards c{cols}">{items}</div>'


def r_flow(b):
    def count(n):
        return B((f"{n} koraka", f"{n} steps"), "em")

    def row(label, steps, cls):
        lis = "".join(f'<li><i>{k + 1}</i>{B(s)}</li>' for k, s in enumerate(steps))
        return (f'<div class="flow-row {cls}"><p class="flow-label">{B(label)}{count(len(steps))}</p><ol>{lis}</ol></div>')
    out = ('<div class="pg-flow">' + row(("Pre", "Before"), b["today"], "today") + row(("Posle", "After"), b["after"], "after") + "</div>")
    if b.get("note"):
        out += B(b["note"], "p", "pg-note")
    return out


def r_steps(b):
    if not b["items"]:
        return ""
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
    def node(day, what, cls=""):
        return f'<span class="jr2-node {cls}"><i></i>{B(day, "b")}{B(what, "small")}</span>'
    today = (node(("Dan 0", "Day 0"), ("Zatvaraš firmu", "You close the business"))
             + f'<span class="jr2-gap">{B(("Mesecima ne znaš koliko duguješ", "Months of not knowing what you owe"))}</span>'
             + node(("Posle 2–3 meseca", "After 2–3 months"), ("Stiže konačan porez", "The final tax bill arrives"), "late"))
    after = (node(("Dan 0", "Day 0"), ("Zatvaraš firmu, vidiš porez i plaćaš", "You close, see the final tax and pay"), "ok")
             + f'<span class="jr2-done"><i>✓</i>{B(("Gotovo istog dana", "Done the same day"))}</span>')
    return (f'<div class="jr2"><div class="jr2-row"><p class="jr2-name">{B(("Danas", "Today"))}</p><div class="jr2-line">{today}</div></div>'
            f'<div class="jr2-row after"><p class="jr2-name">{B(("Predlog", "Proposal"))}</p><div class="jr2-line">{after}</div></div></div>')


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


def c_licence53(b):
    def card(country, rows, alt=False):
        lis = "".join(f'<li class="{k}"><b>{"✓" if k == "ok" else "→" if k == "go" else "–"}</b>{B(t)}</li>' for k, t in rows)
        cls = " alt" if alt else ""
        return (f'<div class="lic-card{cls}"><p class="lic-pick">{B(("Zemlja izdavanja", "Country of issue"))}<b>{B(country)} ▾</b></p><ul>{lis}</ul></div>')
    a = card((" A", " A"), [("ok", ("Dozvola se priznaje", "The licence is recognised")), ("ok", ("Polaganje nije potrebno", "No test needed")),
                            ("ok", ("Dokumenta: spisak sa učitavanjem", "Documents: a list with upload")), ("ok", ("Taksa: iznos i onlajn plaćanje", "Fee: the amount and online payment"))])
    c = card((" B", " B"), [("no", ("Dozvola se ne priznaje", "The licence is not recognised")), ("go", ("Alternativni put: jasni koraci", "Alternative route: clear steps")),
                            ("ok", ("Dokumenta: spisak sa učitavanjem", "Documents: a list with upload")), ("ok", ("Taksa: iznos i onlajn plaćanje", "Fee: the amount and online payment"))], alt=True)
    note = B(("Primer rasporeda. Zemlje i pravila su ovde samo oznake, a ne stvarni podaci.", "A layout example. The countries and rules here are placeholders, not real data."), "p", "pg-note")
    return f'<div class="lic">{a}{c}</div>{note}'


STAGES = [
    ("search", "p1", ("Analiza i procesi", "Analysis and processes"), ("Popis svega na papiru i jasan plan digitalizacije, cilj 99,9%.", "An inventory of everything on paper and a clear digitisation plan, aiming at 99.9%.")),
    ("home", "p2", ("Aplikacije za klijente i zaposlene", "Apps for customers and staff"), ("Nova aplikacija, paket jednim QR kodom i digitalne poslovnice.", "A new app, a parcel with one QR code and digital branches.")),
    ("clock", "p3", ("Carina onlajn i za jedan dan", "Customs online and in a day"), ("Sve procedure onlajn, 99,9% pošiljki ocarinjeno za jedan radni dan.", "Every procedure online, 99.9% of parcels cleared in one working day.")),
]


def c_posta_stages(b):
    import posta_app
    cards = "".join(
        f'<a class="pg-stage" href="#{pid}"><span class="pg-stage-top"><b>{i:02d}</b><i>{posta_app.ic(icon)}</i></span>'
        f'{B(title, "h3")}{B(text, "p")}<span class="pg-stage-go" aria-hidden="true">›</span></a>'
        for i, (icon, pid, title, text) in enumerate(STAGES, 1))
    return f'<div class="pg-stages">{cards}</div>'


def _pair(part):
    def f(b):
        import posta_app
        return posta_app.pair_html(part)
    return f


POSTA_QR_FLOW = {
    "today": [("Doneseš papirni izveštaj", "Bring a paper notice"), ("Službenica ručno unosi podatke", "The clerk types the data"),
              ("Uzima i prepisuje ličnu kartu", "Takes and copies your ID"), ("Sve iz početka za svaku uslugu", "Everything from scratch for every service")],
    "after": [("Prijava u aplikaciju preko eUprave sa 2FA", "Log in to the app via eUprava with 2FA"), ("Paket ima QR kod za preuzimanje", "The parcel has a pickup QR code"),
              ("Službenica skenira, ništa ne kuca", "The clerk scans, types nothing"), ("Dodatna potvrda: četvorocifreni kod na telefon", "Extra check: a four-digit code on your phone"),
              ("Lična karta samo za carinu ili taksu, posebno", "ID only for duty or fees, as a separate step")],
}


def c_posta_target(b):
    rows = [(("Cilj: digitalno", "Target: digital"), 99.9, ("99,9%", "99.9%"), "hi"), (("Papir", "Paper"), 0.1, ("0,1%", "0.1%"), "lo")]
    return r_bars({"rows": rows, "note": (("Udeo procesa u pošti koji su elektronski. Papir ostaje samo tamo gde ga propis izričito traži.",
                                           "The share of the post's processes that are electronic. Paper stays only where a regulation expressly requires it."))})


def _sub(sr_en, intro=None):
    out = f'<h3 class="pg-sub">{B(sr_en)}</h3>'
    if intro:
        out += B(intro, "p", "pg-intro")
    return out


def c_posta_part2(b):
    import posta_app
    clients = (_sub(("Za klijente: aplikacija", "For customers: the app"),
                    ("Jedna prijava preko eUprave, praćenje, preuzimanje, carina i plaćanje, na jednom mestu.",
                     "One sign-in through eUprava, tracking, pickup, customs and payment in one place.")) + posta_app.phones_html())
    staff = (_sub(("Za zaposlene: aplikacija i šalter", "For staff: the app and the counter"),
                  ("QR je unapred potvrđen jer je prijava već dvofaktorska, pa službenik samo skenira, a poštar na adresi pravi IPS QR za doplatu. Ništa se ne kuca ručno i lična karta se ne prepisuje.",
                   "The QR is verified in advance because the sign-in is already two-factor, so the clerk only scans, and the postman creates an IPS QR for a top-up at the door. Nothing is typed by hand and the ID is not copied."))
             + r_flow(POSTA_QR_FLOW) + posta_app.pair_html("emp"))
    return clients + staff


def c_posta_part3(b):
    import posta_app
    bars = r_bars({"rows": [(("Danas", "Today"), 35, ("35+ dana", "35+ days"), "lo"), (("Cilj", "Target"), 1, ("1 radni dan", "1 working day"), "hi")],
                   "note": ("Danas nema zakonskog roka za carinjenje. Izvor: Kurir, pošiljke na carini i više od 35 dana.",
                            "Today there is no legal deadline for clearance. Source: Kurir, parcels at customs for over 35 days.")})
    return (_sub(("Deklaracija i plaćanje onlajn", "Declaration and payment online"),
                 ("Deklarišeš u aplikaciji, unapred vidiš javni obračun i plaćaš onlajn, a ako ipak treba doplatiti na adresi, koristiš NBS IPS QR.",
                  "You declare in the app, see a public calculation up front and pay online, and if something is still due at the door you use an NBS IPS QR."))
            + posta_app.pair_html("p3")
            + _sub(("Carinjenje za jedan radni dan", "Clearance within one working day"),
                   ("Sistem je gotovo potpuno automatizovan, a na odluku automata možeš da se žališ, pa je pregleda živ čovek.",
                    "The system is almost fully automated, and you can appeal an automatic decision so a human reviews it."))
            + bars + posta_app.pair_html("p4"))


def c_posta_app(b):
    import posta_app
    return posta_app.phones_html()


STAGES22 = [
    ("send", ("Zahtev onlajn", "Request online"), ("Jedan zahtev u APR-u, bez šaltera.", "One request at APR, no counter.")),
    ("calc", ("Porez odmah", "Tax at once"), ("Poreska iz svojih podataka računa konačan porez.", "Poreska works out the final tax from its own data.")),
    ("card", ("Vidiš i plaćaš", "You see and pay"), ("Iznos je na ekranu pri odjavi, bez rešenja posle meseci.", "The amount is on screen at deregistration, with no decision months later.")),
    ("check", ("Zatvoreno za dan", "Closed in a day"), ("Brisanje i plaćanje u istom radnom danu.", "Deletion and payment in the same working day.")),
]


def c_stages22(b):
    import posta_app
    cards = "".join(
        f'<a class="pg-stage" href="#c1"><span class="pg-stage-top"><b>{i:02d}</b><i>{posta_app.ic(icon)}</i></span>'
        f'{B(title, "h3")}{B(text, "p")}<span class="pg-stage-go" aria-hidden="true">›</span></a>'
        for i, (icon, title, text) in enumerate(STAGES22, 1))
    return f'<div class="pg-stages">{cards}</div>'


def c_versus22(b):
    return (f'<div class="pg-versus"><div class="pg-vs today"><p class="pg-vs-k">{B(("Danas", "Today"))}</p>'
            f'<b class="pg-vs-n">2–3<small>{B(("meseca", "months"))}</small></b>{B(("Posle odjave tek stiže konačan obračun poreza.", "The final tax assessment only arrives after deregistration."), "p")}</div>'
            f'<span class="pg-vs-arrow" aria-hidden="true">›</span>'
            f'<div class="pg-vs after"><p class="pg-vs-k">{B(("Predlog", "Proposal"))}</p>'
            f'<b class="pg-vs-n">1<small>{B(("dan", "day"))}</small></b>{B(("Konačan porez vidiš i plaćaš pri zatvaranju.", "You see and pay the final tax when you close."), "p")}</div></div>')


def c_countries22(b):
    items = [("🇷🇸", ("Srbija danas", "Serbia today"), ("Onlajn zahtev za brisanje, obračun posle 2–3 meseca.", "An online deregistration request, assessment after 2–3 months."), ""),
             ("🇬🇪", ("Gruzija", "Georgia"), ("Registracija i brisanje za 1 radni dan.", "Registration and deletion in 1 working day."), ""),
             ("🇪🇪", ("Estonija", "Estonia"), ("Brisanje firme onlajn.", "Online deletion of a company."), ""),
             ("🇷🇸", ("Predlog za Srbiju", "The proposal for Serbia"), ("Jedan dan, konačan porez plaćen odmah.", "One day, the final tax settled at once."), " mine")]
    cards = "".join(f'<article class="pg-country{cls}"><span class="pg-flag" aria-hidden="true">{flag}</span>{B(t, "h3")}{B(x, "p")}</article>' for flag, t, x, cls in items)
    return f'<div class="pg-countries">{cards}</div>'


CUSTOM = {"posta_target": c_posta_target, "posta_part2": c_posta_part2, "posta_part3": c_posta_part3, "stages22": c_stages22, "versus22": c_versus22, "countries22": c_countries22, "biz_c1": _pair("c1"), "posta_p2": _pair("p2"), "posta_p3": _pair("p3"), "posta_p4": _pair("p4"), "posta_stages": c_posta_stages, "posta_app": c_posta_app, "licence53": c_licence53, "clerk": c_clerk, "journey22": c_journey22, "network30": c_network30, "stats30": c_stats30,
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
    return (f'<div class="pg-vote" id="vote"><div class="wrap"><footer class="vote" data-vote="{n}">'
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
        tsub = tuple(f'{tier[l]["name"]} · {tier[l]["sub"]} · {tier[l]["time"]}' for l in LANGS)
        sections, navitems = "", []
        for i, blk in enumerate(page["blocks"]):
            if blk["k"] in SKIP_KINDS:
                continue
            if blk["k"] == "custom":
                inner = CUSTOM[blk["name"]](blk)
            else:
                inner = RENDER[blk["k"]](blk)
                if blk.get("extra"):
                    inner += CUSTOM[blk["extra"]](blk)
            sections += sec(blk, inner, i, "dark" if blk["k"] == "check" else "")
            lab = blk.get("nav") or blk["eb"]
            m = re.match(r"^(\d)/\d$", lab[1])
            if m:
                lab = (f"Deo {m.group(1)}", f"Part {m.group(1)}")
            if lab[1] not in {x[1][1] for x in navitems}:
                navitems.append((blk.get("id") or f"s{i}", lab))
        links = "".join(f'<a href="#{i}">{B(l)}</a>' for i, l in navitems)
        local = (f'<div class="pg-local"><div class="wrap pg-local-in"><a class="pg-local-t" href="#top">{B(titles[n])}</a>'
                 f'<nav class="pg-local-links" aria-label="Sections">{links}</nav></div><i class="pg-progress"></i></div>')
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
                .replace("{{HL}}", "#F1BD40" if n == 21 else "#FFFFFF").replace("{{TH}}", th).replace("{{TH2}}", dk).replace("{{TINT}}", mix(th, 9)).replace("{{TINT2}}", mix(th, 18))
                .replace("{{NUM}}", f"{n:02d}").replace("{{N}}", str(n))
                .replace("{{EYEBROW}}", B((cat_of(n)["sr"][0], cat_of(n)["en"][0])) + " · " + B(UI["idea"]) + f" {n:02d}")
                .replace("{{H1}}", B(titles[n], "h1")).replace("{{TAGLINE}}", B(HERO_TEXT.get(n, taglines[n]), "p", "pg-tag"))
                .replace("{{TIERLINE}}", B(tsub, "p", "pg-tier"))
                .replace("{{EXTRA_HEAD}}", '<link rel="stylesheet" href="../../assets/posta-app.css?v=%s">' % ver if n in (21, 22) else "").replace("{{LOCAL}}", local).replace("{{HSTATS}}", hstats).replace("{{SECTIONS}}", sections)
                .replace("{{RELATED}}", rel).replace("{{SOURCES}}", sources_html(parts))
                .replace("{{VOTE}}", vote_html(n))
                .replace("{{PREV}}", nb(prev_n, UI["prev"])).replace("{{NEXT}}", nb(next_n, UI["next"]))
                .replace("{{V}}", ver))
        if not page["stats"]:
            html = html.replace('<div class="wrap"><ul class="pg-hstats"></ul></div>', "", 1).replace('<header class="pg-hero" id="top">', '<header class="pg-hero no-stats" id="top">', 1)
        if n in NO_EYEBROW:
            html = re.sub(r'\s*<p class="pg-hero-eye">.*?</p>', "", html, count=1, flags=re.S)
        assert "{{" not in html, re.findall(r"\{\{[A-Z0-9_]+\}\}", html)
        out = ROOT / "idea" / slug
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(html, encoding="utf-8")
    print(f"idea/: {len(ORDER)} pages")
