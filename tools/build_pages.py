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
    ("home", "p2", ("Aplikacija za klijente", "App for customers"), ("Sve usluge i paket jednim QR kodom, u jednoj aplikaciji.", "Every service and a parcel with one QR code, in one app.")),
    ("user", "p3", ("Aplikacija za zaposlene", "App for staff"), ("Šalter, poslovnica, logistika, carina i poštar u jednom sistemu.", "The counter, branch, logistics, customs and postman in one system.")),
    ("clock", "p4", ("Carina onlajn i za jedan dan", "Customs online and in a day"), ("Sve procedure onlajn, 99,9% pošiljki ocarinjeno za jedan radni dan.", "Every procedure online, 99.9% of parcels cleared in one working day.")),
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
    return (posta_app.phones_html()
            + _sub(("Paket jednim QR kodom", "A parcel with one QR code"),
                   ("QR je unapred potvrđen jer je prijava u aplikaciju već dvofaktorska. Isti QR radi za plaćanja i druge državne usluge na pošti.",
                    "The QR is verified in advance because the app login is already two-factor. The same QR works for payments and other state services at the post office."))
            + r_flow(POSTA_QR_FLOW))


def c_posta_part3(b):
    import posta_app as pa
    return (_sub(("Šalter", "The counter"),
                 ("Službenik skenira QR i odmah vidi ceo slučaj, a prijem pošiljke ide iz podataka iz aplikacije.", "The clerk scans the QR and sees the whole case at once, and accepting a parcel runs on the data from the app."))
            + pa.web_gallery([(pa.w_clerk, ("Šalter: preuzimanje paketa", "Counter: handing over a parcel")), (pa.w_intake, ("Šalter: prijem pošiljke", "Counter: accepting a parcel"))])
            + _sub(("Poslovnica i logistika", "Branch and logistics"),
                   ("Upravnik vidi red, čekanje i udeo papira u realnom vremenu, a logistika tok svake pošiljke i samo izuzetke.", "The manager sees the queue, the wait and the share of paper in real time, and logistics sees the flow of every parcel and only the exceptions."))
            + pa.web_gallery([(pa.w_dash, ("Upravnik: poslovnica danas", "Manager: the branch today")), (pa.w_pipeline, ("Logistika: tok pošiljki", "Logistics: the parcel flow"))])
            + _sub(("Poštar", "The postman"),
                   ("Ruta za dan, adresa i doplata na vratima preko NBS IPS QR koda.", "The day's route, the address and a top-up at the door by an NBS IPS QR."))
            + pa.phone_pair([(pa.s_route, ("Poštar: ruta za danas", "Postman: today's route")), (pa.s_postman, ("Poštar: doplata na adresi", "Postman: top-up at the door"))]))


def c_posta_part4(b):
    import posta_app as pa
    bars = r_bars({"rows": [(("Danas", "Today"), 35, ("35+ dana", "35+ days"), "lo"), (("Cilj", "Target"), 1, ("1 radni dan", "1 working day"), "hi")],
                   "note": ("Danas nema zakonskog roka za carinjenje. Izvor: Kurir, pošiljke na carini i više od 35 dana.",
                            "Today there is no legal deadline for clearance. Source: Kurir, parcels at customs for over 35 days.")})
    return (_sub(("Deklaracija i plaćanje onlajn", "Declaration and payment online"),
                 ("Deklarišeš u aplikaciji, unapred vidiš javni obračun i plaćaš onlajn, a ako ipak treba doplatiti na adresi, koristiš NBS IPS QR.",
                  "You declare in the app, see a public calculation up front and pay online, and if something is still due at the door you use an NBS IPS QR."))
            + pa.pair_html("p3")
            + _sub(("Carinjenje za jedan radni dan", "Clearance within one working day"),
                   ("Sistem je gotovo potpuno automatizovan, a na odluku automata možeš da se žališ, pa je pregleda živ čovek.",
                    "The system is almost fully automated, and you can appeal an automatic decision so a human reviews it."))
            + bars + pa.pair_html("p4")
            + _sub(("Carinska služba iznutra", "Inside the customs service"),
                   ("Većinu odluka donosi sistem, a službenik pregleda samo žalbe.", "The system makes most decisions, and the officer reviews only the appeals."))
            + pa.web_gallery([(pa.w_customs, ("Carinik: odluke i žalbe", "Officer: decisions and appeals"))]))


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


STAGES1 = [
    ("qr", ("QR kod za predmet", "A QR code per case"), ("U eUpravi svaki predmet ima lični QR kod.", "In eUprava every case has a personal QR code.")),
    ("send", ("Pokažeš ga na šalteru", "Show it at the counter"), ("Telefonom, odštampano ili linkom iz SMS-a.", "On your phone, printed or as an SMS link.")),
    ("scan", ("Službenik skenira", "The clerk scans"), ("Otvara se tvoj slučaj: istorija i status.", "Your case opens: its history and status.")),
    ("check", ("Samo što fali", "Only what is missing"), ("Službenik pita samo konkretno, ti vidiš novi status.", "The clerk asks only what is specific, and you see the new status.")),
]


def c_stages1(b):
    import posta_app
    cards = "".join(
        f'<a class="pg-stage" href="#c1"><span class="pg-stage-top"><b>{i:02d}</b><i>{posta_app.ic(icon)}</i></span>'
        f'{B(title, "h3")}{B(text, "p")}<span class="pg-stage-go" aria-hidden="true">›</span></a>'
        for i, (icon, title, text) in enumerate(STAGES1, 1))
    return f'<div class="pg-stages">{cards}</div>'


def c_versus1(b):
    return (f'<div class="pg-versus"><div class="pg-vs today"><p class="pg-vs-k">{B(("Danas", "Today"))}</p>'
            f'<b class="pg-vs-n w">{B(("Objašnjavaš", "You explain"))}</b>{B(("Isto na svakom šalteru, a službenik pogađa postupak i prepisuje podatke.", "The same story at every counter, while the clerk guesses the procedure and retypes the data."), "p")}</div>'
            f'<span class="pg-vs-arrow" aria-hidden="true">›</span>'
            f'<div class="pg-vs after"><p class="pg-vs-k">{B(("Predlog", "Proposal"))}</p>'
            f'<b class="pg-vs-n w">{B(("Skeniraš", "You scan"))}</b>{B(("Službenik odmah vidi tvoj slučaj, a ti ništa ne objašnjavaš.", "The clerk sees your case at once and you explain nothing."), "p")}</div></div>')


def _qr_pair(b):
    import posta_app
    return posta_app.pair_html("q1")


STAGES30 = [
    ("search", ("Svi registri u eZUP-u", "Every register in eZUP"), ("Uključujući lokalne registre i javna preduzeća.", "Including local registers and public companies.")),
    ("check", ("Papir samo uz razlog", "A paper only with a reason"), ("Službenik koji traži papir mora to pisano da obrazloži.", "A clerk who asks for a paper must justify it in writing.")),
    ("chat", ("Žalba onlajn", "Complain online"), ("Građanin se žali bez odlaska na šalter.", "The citizen complains without going to a counter.")),
    ("globe", ("Javna statistika", "Public statistics"), ("Po službi: koliko se uverenja izdaje samo da bi se nosila dalje.", "Per office: how many certificates are issued only to be carried on.")),
]


def c_stages30(b):
    import posta_app
    cards = "".join(
        f'<a class="pg-stage" href="#c1"><span class="pg-stage-top"><b>{i:02d}</b><i>{posta_app.ic(icon)}</i></span>'
        f'{B(title, "h3")}{B(text, "p")}<span class="pg-stage-go" aria-hidden="true">›</span></a>'
        for i, (icon, title, text) in enumerate(STAGES30, 1))
    return f'<div class="pg-stages">{cards}</div>'


def c_versus30(b):
    return (f'<div class="pg-versus"><div class="pg-vs today"><p class="pg-vs-k">{B(("Danas", "Today"))}</p>'
            f'<b class="pg-vs-n">{B(("do 50 €", "up to €50"))}</b>{B(("Toliko se plaća list nepokretnosti koji nosiš iz jedne službe u drugu.", "What a list nepokretnosti (property sheet) costs when you carry it from one office to another."), "p")}</div>'
            f'<span class="pg-vs-arrow" aria-hidden="true">›</span>'
            f'<div class="pg-vs after"><p class="pg-vs-k">{B(("Predlog", "Proposal"))}</p>'
            f'<b class="pg-vs-n">0 €</b>{B(("Služba sama preuzima podatke iz registra, a ti ne nosiš ništa.", "The office pulls the data from the register itself, and you carry nothing."), "p")}</div></div>'
            + B(("Izvor: Novosti, list nepokretnosti do 50 € umesto 0 din.", "Source: Novosti, a property sheet up to €50 instead of 0 din."), "p", "pg-note"))


def c_board30(b):
    import posta_app
    return posta_app.web_gallery([(posta_app.w_board, ("Javna tabla po službama", "A public board per office"))])


def _n30_pair(b):
    import posta_app
    return posta_app.pair_html("n30")


STAGES2 = [
    ("user", ("Osnovni nivo", "Basic level"), ("E-pošta i snimak dokumenta, odmah i za strance.", "An email and a document scan, at once and also for foreigners.")),
    ("shield", ("Puni nivo", "Full level"), ("Potvrda preko banke, čip lične karte ili pošte.", "Confirmation through a bank, a chip ID card or the pošta.")),
    ("check", ("Bez šaltera", "No counter"), ("Bez dolaska na šalter i bez aktivacionog koda.", "No counter visit and no activation code.")),
    ("globe", ("Za strance", "For foreigners"), ("Osnovni pristup odmah, puni sa boravkom.", "Basic access at once, full access with residence.")),
]


def c_stages2(b):
    import posta_app
    cards = "".join(
        f'<a class="pg-stage" href="#c1"><span class="pg-stage-top"><b>{i:02d}</b><i>{posta_app.ic(icon)}</i></span>'
        f'{B(title, "h3")}{B(text, "p")}<span class="pg-stage-go" aria-hidden="true">›</span></a>'
        for i, (icon, title, text) in enumerate(STAGES2, 1))
    return f'<div class="pg-stages">{cards}</div>'


def c_versus2(b):
    return (f'<div class="pg-versus"><div class="pg-vs today"><p class="pg-vs-k">{B(("Danas", "Today"))}</p>'
            f'<b class="pg-vs-n">3<small>{B(("načina", "ways"))}</small></b>{B(("Lozinka, ConsentID i sertifikat, a viši nivo traži šalter.", "A password, ConsentID and a certificate, and the higher level needs a counter."), "p")}</div>'
            f'<span class="pg-vs-arrow" aria-hidden="true">›</span>'
            f'<div class="pg-vs after"><p class="pg-vs-k">{B(("Predlog", "Proposal"))}</p>'
            f'<b class="pg-vs-n">2<small>{B(("nivoa", "levels"))}</small></b>{B(("Osnovni i puni, bez dolaska na šalter.", "Basic and full, with no counter visit."), "p")}</div></div>'
            + B(("Izvor: eID portal, prijava lozinkom, aplikacijom ConsentID ili sertifikatom.", "Source: the eID portal, sign-in by password, the ConsentID app or a certificate."), "p", "pg-note"))


def _l2_pair(b):
    import posta_app
    return posta_app.pair_html("l2")


CUSTOM = {"stages2": c_stages2, "versus2": c_versus2, "l2_pair": _l2_pair, "stages30": c_stages30, "versus30": c_versus30, "board30": c_board30, "n30_pair": _n30_pair, "stages1": c_stages1, "versus1": c_versus1, "qr_pair": _qr_pair, "posta_target": c_posta_target, "posta_part2": c_posta_part2, "posta_part3": c_posta_part3, "posta_part4": c_posta_part4, "stages22": c_stages22, "versus22": c_versus22, "countries22": c_countries22, "biz_c1": _pair("c1"), "posta_p2": _pair("p2"), "posta_p3": _pair("p3"), "posta_p4": _pair("p4"), "posta_stages": c_posta_stages, "posta_app": c_posta_app, "licence53": c_licence53, "clerk": c_clerk, "journey22": c_journey22, "network30": c_network30, "stats30": c_stats30,
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


def build_share(key):
    from build import share_btn
    return share_btn(key)


def vote_html(n):
    return (f'<div class="pg-vote" id="vote"><div class="wrap"><footer class="vote" data-vote="{n}">'
            f'{B(UI["vote_q"], "span", "vote-q")}<div class="vote-btns">'
            f'<button type="button" class="vbtn up" data-dir="up" aria-pressed="false"><span class="sign" aria-hidden="true">+</span>{B(UI["up"], "span", "sr-only")}<span class="count" hidden></span></button>'
            f'<button type="button" class="vbtn down" data-dir="down" aria-pressed="false"><span class="sign" aria-hidden="true">−</span>{B(UI["down"], "span", "sr-only")}<span class="count" hidden></span></button>'
            f'</div>{build_share("page")}</footer></div></div>')


def build_all(ctx):
    """ctx: toc, ideas, tier_of, tiers, featured, ver, template (str)."""
    toc, ideas, tier_of, ver = ctx["toc"], ctx["ideas"], ctx["tier_of"], ctx["ver"]
    taglines = {47: ("Lična karta i boravak u novčaniku na telefonu.", "Your ID and residence card in your phone wallet."),
                53: ("Zamena strane vozačke dozvole bez nagađanja.", "Exchange a foreign driving licence without the guesswork.")}
    taglines.update({n: (sr, en) for n, sr, en in ctx["featured"]})
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
                .replace("{{EXTRA_HEAD}}", '<link rel="stylesheet" href="../../assets/posta-app.css?v=%s">' % ver if n in (1, 2, 9, 21, 22, 30, 47, 48, 50, 53) else "").replace("{{LOCAL}}", local).replace("{{HSTATS}}", hstats).replace("{{SECTIONS}}", sections)
                .replace("{{RELATED}}", rel).replace("{{SOURCES}}", sources_html(parts))
                .replace("{{VOTE}}", vote_html(n))
                .replace("{{PREV}}", nb(prev_n, UI["prev"])).replace("{{NEXT}}", nb(next_n, UI["next"]))
                .replace("{{URL}}", f"{ctx['site']}/idea/{slug}/").replace("{{OG}}", f"{ctx['site']}/assets/og/{slug}.jpg")
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


# ---------------------------------------------------------------- generic helpers for the redesigned pages
def make_stages(items):
    def f(b):
        import posta_app
        cards = "".join(
            f'<a class="pg-stage" href="#c1"><span class="pg-stage-top"><b>{i:02d}</b><i>{posta_app.ic(icon)}</i></span>'
            f'{B(title, "h3")}{B(text, "p")}<span class="pg-stage-go" aria-hidden="true">›</span></a>'
            for i, (icon, title, text) in enumerate(items, 1))
        return f'<div class="pg-stages">{cards}</div>'
    return f


def make_versus(today, today_text, after, after_text, note=None, words=False):
    def big(x):
        cls = " w" if words else ""
        return f'<b class="pg-vs-n{cls}">{B(x) if isinstance(x, tuple) else x}</b>'
    def f(b):
        out = (f'<div class="pg-versus"><div class="pg-vs today"><p class="pg-vs-k">{B(("Danas", "Today"))}</p>{big(today)}{B(today_text, "p")}</div>'
               f'<span class="pg-vs-arrow" aria-hidden="true">›</span>'
               f'<div class="pg-vs after"><p class="pg-vs-k">{B(("Predlog", "Proposal"))}</p>{big(after)}{B(after_text, "p")}</div></div>')
        if note:
            out += B(note, "p", "pg-note")
        return out
    return f


def make_countries(items):
    def f(b):
        cards = "".join(f'<article class="pg-country{cls}"><span class="pg-flag" aria-hidden="true">{flag}</span>{B(t, "h3")}{B(x, "p")}</article>' for flag, t, x, cls in items)
        return f'<div class="pg-countries">{cards}</div>'
    return f


def make_pair(key):
    def f(b):
        import posta_app
        return posta_app.pair_html(key)
    return f


CUSTOM.update({
    "stages48": make_stages([
        ("scan", ("Granica beleži ulazak", "The border logs the entry"), ("Ko je ušao, kada i na kom osnovu.", "Who entered, when and on what basis.")),
        ("clock", ("Sistem računa dane", "The system counts the days"), ("Bezvizno 90/180, viza ili dozvola: preostali dani se računaju sami.", "Visa-free 90/180, a visa or a permit: the days left are calculated by themselves.")),
        ("check", ("Nema prijave boravka", "No registration of stay"), ("Ni papirno ni onlajn, ni od hotela ni od stanodavca.", "Not on paper or online, not from hotels or landlords.")),
        ("shield", ("Kontrola ostaje na granici", "Control stays at the border"), ("Bezbednost se ne smanjuje, a papira nema.", "Security is not reduced and the paperwork is gone.")),
    ]),
    "versus48": make_versus("24 h", ("Toliko ima stranac da prijavi adresu, i posle svake selidbe.", "That is how long a foreigner has to register an address, and again after every move."),
                            "0", ("Nema prijave boravka, ni papirne ni onlajn. Dovoljna je granična baza.", "No registration of stay, on paper or online. The border database is enough."),
                            note=("Izvor: MSP Srbije, prijava boravka stranaca u roku od 24 časa.", "Source: the Serbian MFA, foreigners register stay within 24 hours.")),
    "countries48": make_countries([
        ("🇷🇸", ("Srbija danas", "Serbia today"), ("Prijava u roku od 24 h i posle svake selidbe.", "Register within 24 h and after every move."), ""),
        ("🇰🇿", ("Kazahstan, 2020.", "Kazakhstan, 2020"), ("Registracija ukinuta za boravak do 30 dana.", "Registration dropped for stays up to 30 days."), ""),
        ("🇬🇧", ("Velika Britanija, 2022.", "United Kingdom, 2022"), ("Prijava stranaca policiji ukinuta.", "Police registration of foreigners dropped."), ""),
        ("🇷🇸", ("Predlog za Srbiju", "The proposal for Serbia"), ("Potpuno ukinuti, i papirno i onlajn.", "Abolish fully, paper and online."), " mine"),
    ]),
    "b48_pair": make_pair("b48"),
    "stages50": make_stages([
        ("clock", ("Tri brzine", "Three speeds"), ("Standard 30 dana, 15 dana uz +50% i 7 dana uz dvostruku taksu.", "Standard 30 days, 15 days for +50% and 7 days for double the fee.")),
        ("check", ("Biraš pri podnošenju", "Pick when filing"), ("Brzina i taksa se vide unapred.", "The speed and the fee are visible up front.")),
        ("card", ("Plaćaš službeno", "Pay officially"), ("Zvanična uplata i potvrda, bez „veze”.", "An official payment and receipt, without “connections”.")),
        ("home", ("Novac u budžet", "Money to the budget"), ("Taksa ide u budžet službe, ne u nečiji džep.", "The fee goes to the office budget, not into someone's pocket.")),
    ]),
    "versus50": make_versus(("Veza", "A connection"), ("Hitnost postoji, ali neformalno: poznanik, usluga ili novac u džep.", "Urgency exists, but informally: an acquaintance, a favour or money into a pocket."),
                            ("Račun", "A receipt"), ("Ista hitnost, ali javna, jednaka za sve i uz zvaničnu potvrdu.", "The same urgency, but public, equal for all and with an official receipt."), words=True),
    "f50_pair": make_pair("f50"),
})


CUSTOM.update({
    "stages9": make_stages([
        ("home", ("Jedan ulaz", "One entry point"), ("Jedinstveni poreski portal, jedna prijava.", "A single tax portal, one sign-in.")),
        ("send", ("Registruješ firmu", "Register a business"), ("Registracija i izmene podataka u istom portalu.", "Registration and changes of data in the same portal.")),
        ("card", ("Plaćaš poreze", "Pay taxes"), ("Prijave i plaćanja bez prelaska u drugi sistem.", "Filings and payments without moving to another system.")),
        ("shield", ("Ustanove nezavisne", "Agencies stay independent"), ("Objedinjuju se samo elektronske usluge.", "Only the electronic services are brought together.")),
    ]),
    "versus9": make_versus("2", ("Zasebna elektronska sistema: jedan za registraciju firme, drugi za poreze.", "Separate electronic systems: one to register a business, another for taxes."),
                           "1", ("Jedinstveni poreski portal za registraciju i plaćanje poreza.", "A single tax portal for registration and paying taxes.")),
    "t9_pair": make_pair("t9"),
})


def _portal9(b):
    import portal_mock
    return portal_mock.portal_html()


CUSTOM["portal9"] = _portal9


import screens_wl  # noqa: F401  (registers the Wallet and licence screens)

CUSTOM.update({
    "stages47": make_stages([
        ("wallet", ("Isprava u novčaniku", "The document in the wallet"), ("Lična karta i boravak u Apple i Google novčaniku.", "ID and residence card in Apple and Google Wallet.")),
        ("clock", ("Provera za sekundu", "A check in a second"), ("QR ili NFC, bez vađenja kartice.", "QR or NFC, without taking out a card.")),
        ("shield", ("Deliš samo potrebno", "Share only what is needed"), ("Na primer samo da si punoletan.", "For example only that you are over 18.")),
        ("check", ("Ista pravna snaga", "The same legal force"), ("Kao kartica, po ISO 18013-5 i EUDI.", "As the card, under ISO 18013-5 and EUDI.")),
    ]),
    "versus47": make_versus(("Celu karticu", "The whole card"), ("Pri svakoj proveri pokazuješ sve što je na njoj.", "At every check you show everything printed on it."),
                            ("Jedan podatak", "One fact"), ("Čitač dobija samo traženo, na primer da si punoletan.", "The reader gets only what it asks for, for example that you are over 18."), words=True),
    "w47_pair": make_pair("w47"),
    "stages53": make_stages([
        ("globe", ("Pravila po zemlji", "Rules per country"), ("Priznaje li se dozvola, treba li polaganje, dokumenta i taksa.", "Whether the licence is recognised, a test, documents and the fee.")),
        ("send", ("Jedan onlajn tok", "One online flow"), ("Zahtev, dokumenta i taksa u istom koraku.", "The application, documents and fee in one step.")),
        ("user", ("Uživo samo što mora", "In person only what must be"), ("Termin samo za korak koji ne ide onlajn.", "An appointment only for the step that cannot be done online.")),
        ("clock", ("Status i rok", "Status and deadline"), ("Vidiš gde je zahtev i do kada stiže odluka.", "You see where it stands and when a decision is due.")),
    ]),
    "versus53": make_versus(("Forumi", "Forums"), ("Odgovore na „šta mi treba?” tražiš po blogovima i forumima.", "You look for the answer to “what do I need?” on blogs and forums."),
                            ("Jedna stranica", "One page"), ("Pravila, dokumenta i taksa za tvoju zemlju, na jednom mestu.", "The rules, documents and fee for your country, in one place."), words=True),
    "d53_pair": make_pair("d53"),
})
