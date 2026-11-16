"""Concept screens for a redesigned Pošta Srbije app (static visual, not interactive).

phones_html() is used in Part 1 of the Pošta reform page.
Edit the texts and layout of each screen in the functions below, then run `python3 tools/build.py`.
Colours: Serbian flag (blue, red, white) with the Pošta yellow as a small accent.
All names, tracking numbers, amounts and branches are placeholders.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LA = {"sr": "sr-Latn", "en": "en"}

ICONS = {
    "home": "M3 11l9-8 9 8v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z",
    "box": "M21 8l-9-5-9 5v8l9 5 9-5zM3 8l9 5 9-5M12 13v8",
    "qr": "M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h3v3h-3zM20 14v3M14 20h3M20 20v1",
    "pin": "M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12zM12 12.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z",
    "card": "M2 6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2zM2 10h20",
    "user": "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
    "scan": "M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3M4 12h16",
    "bell": "M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 0 1-3.4 0",
    "check": "M20 6L9 17l-5-5",
    "clock": "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 6v6l4 2",
    "shield": "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10zM9 12l2 2 4-4",
    "chat": "M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z",
    "globe": "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20",
    "send": "M22 2L11 13M22 2l-7 20-4-9-9-4z",
    "calc": "M5 2h14a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1zM8 6h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01M8 19h.01M12 19h.01",
    "back": "M15 18l-6-6 6-6",
    "search": "M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM21 21l-4.3-4.3",
    "truck": "M1 3h15v13H1zM16 8h4l3 3v5h-7zM5.5 21a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zM18.5 21a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z",
    "lock": "M5 11h14v10H5zM8 11V7a4 4 0 0 1 8 0v4",
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true"><path d="{ICONS[name]}"/></svg>')


def B(sr, en, tag="span", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} lang="{LA["sr"]}">{sr}</{tag}><{tag}{c} lang="{LA["en"]}">{en}</{tag}>'


def qr(size=100, fill="#0A335F"):
    """A believable QR-like pattern: three real finder patterns plus pseudo-random modules."""
    n = 21
    u = size / n
    grid = [[False] * n for _ in range(n)]
    keep = set()
    for ox, oy in ((0, 0), (n - 7, 0), (0, n - 7)):
        for dx in range(-1, 8):
            for dy in range(-1, 8):
                x, y = ox + dx, oy + dy
                if 0 <= x < n and 0 <= y < n:
                    keep.add((x, y))
        for dx in range(7):
            for dy in range(7):
                ring = dx in (0, 6) or dy in (0, 6)
                core = 2 <= dx <= 4 and 2 <= dy <= 4
                grid[oy + dy][ox + dx] = ring or core
    seed = 11
    for y in range(n):
        for x in range(n):
            if (x, y) in keep:
                continue
            seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
            grid[y][x] = (seed >> 16) % 100 < 46
    d = "".join(f"M{x * u:.2f} {y * u:.2f}h{u:.2f}v{u:.2f}h-{u:.2f}z" for y in range(n) for x in range(n) if grid[y][x])
    return f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" aria-hidden="true"><path d="{d}" fill="{fill}"/></svg>'


TABS = [("home", ("Početna", "Home")), ("box", ("Paketi", "Parcels")), ("card", ("Plaćanja", "Payments")), ("user", ("Profil", "Profile"))]


def tabs(active):
    out = "".join(f'<span class="pa-tab{" on" if key == active else ""}">{ic(key)}{B(*label, "em")}</span>' for key, label in TABS)
    return f'<nav class="pa-tabs">{out}</nav>'


def phone(body, tab=None, dark=False):
    tabs_on = tab is not None
    status = ('<div class="pa-status"><b>9:41</b><span class="pa-sig"><i></i><i></i><i></i><i></i></span></div>')
    return (f'<div class="pa-phone"><span class="pa-island"></span><div class="pa-screen{" dark" if dark else ""}{" has-tabs" if tabs_on else ""}">{status}'
            f'<div class="pa-body">{body}</div>{tabs(tab) if tab else ""}</div></div>')


def chip(kind, sr, en):
    return f'<span class="pa-chip {kind}">{B(sr, en)}</span>'


# ------------------------------------------------------------------ screens
def s_login():
    return phone(f'''
<div class="pa-hero-login"><div class="pa-stripes"><i></i><i></i><i></i></div>
<span class="pa-logo">{ic("send")}</span><h3>Pošta Srbije</h3>{B("Paketi, plaćanja i carina na jednom mestu.", "Parcels, payments and customs in one place.", "p")}</div>
<div class="pa-login">
<button class="pa-btn primary">{ic("shield")}{B("Prijavi se preko eUprave", "Sign in with eUprava")}</button>
<p class="pa-fine">{B("Dvofaktorska potvrda. Bez novih lozinki.", "Two-factor confirmation. No new passwords.", "span")}</p>
<div class="pa-2fa"><p>{B("Potvrdi na telefonu", "Confirm on your phone", "b")}</p><div class="pa-num">42</div>{B("Izaberi isti broj u aplikaciji eUprava.", "Pick the same number in the eUprava app.", "small")}</div>
</div>''')


def s_home():
    quick = [("send", ("Pošalji", "Send")), ("qr", ("Preuzmi", "Collect")), ("calc", ("Carina", "Customs")), ("pin", ("Poslovnice", "Branches")), ("card", ("Plati", "Pay")), ("chat", ("Podrška", "Help"))]
    q = "".join(f'<span class="pa-q"><i>{ic(k)}</i>{B(*t, "em")}</span>' for k, t in quick)
    return phone(f'''
<div class="pa-top"><div>{B("Dobar dan", "Good afternoon", "small")}{B("Tvoja pošta", "Your post", "b")}</div><span class="pa-bell">{ic("bell")}<u></u></span></div>
<div class="pa-search">{ic("search")}{B("Broj pošiljke", "Tracking number")}<span class="pa-scan">{ic("scan")}</span></div>
<div class="pa-card hero"><div class="pa-stripes sm"><i></i><i></i><i></i></div>
<p class="pa-k">{B("Paket stiže danas", "Your parcel arrives today")}</p>
<div class="pa-prog"><i class="d"></i><i class="d"></i><i class="d"></i><i class="n"></i><b></b></div>
<div class="pa-prog-l">{B("Carina", "Customs", "span")}{B("Poslovnica", "Branch", "span")}</div>
<span class="pa-ready">{ic("qr")}{B("QR za preuzimanje je spreman", "Pickup QR is ready")}</span></div>
<div class="pa-grid">{q}</div>''', tab="home")


def s_list():
    def item(icon, title_sr, title_en, kind, st_sr, st_en, date):
        return (f'<div class="pa-item"><i class="pa-ico">{ic(icon)}</i><div>{B(title_sr, title_en, "b")}<code>RS ••••• ••••• RS</code>{chip(kind, st_sr, st_en)}</div><time>{B(date[0], date[1])}</time></div>')
    return phone(f'''
<div class="pa-title">{B("Moji paketi", "My parcels", "h4")}</div>
<div class="pa-seg"><span class="on">{B("U toku", "In transit")}<b>3</b></span><span>{B("Preuzmi", "To collect")}<b>1</b></span><span>{B("Istorija", "History")}</span></div>
<div class="pa-list">
{item("box", "Onlajn prodavnica", "Online shop", "ok", "Spreman za preuzimanje", "Ready to collect", ("danas", "today"))}
{item("globe", "Pošiljka iz inostranstva", "Parcel from abroad", "blue", "Carina: plaćeno", "Customs: paid", ("juče", "yesterday"))}
{item("truck", "Kurirska služba", "Courier", "grey", "Na putu", "On the way", ("pre 2 d", "2 d ago"))}
{item("box", "Poklon", "Gift", "grey", "Preuzeto", "Collected", ("12. nov", "12 Nov"))}
</div>''', tab="box")


def s_detail():
    def step(kind, sr, en, sub_sr="", sub_en=""):
        sub = B(sub_sr, sub_en, "small") if sub_sr else ""
        mark = ic("check") if kind == "done" else ""
        return f'<li class="{kind}"><i>{mark}</i><div>{B(sr, en, "b")}{sub}</div></li>'
    return phone(f'''
<div class="pa-nav"><span>{ic("back")}</span>{B("Pošiljka", "Parcel", "b")}<span></span></div>
<div class="pa-card"><p class="pa-k">{B("Pošiljka iz inostranstva", "Parcel from abroad")}</p><code>RS ••••• ••••• RS</code></div>
<ul class="pa-steps">
{step("done", "Primljeno u inostranstvu", "Received abroad")}
{step("done", "Stiglo u Srbiju", "Arrived in Serbia")}
{step("done", "Carinjenje završeno", "Customs cleared", "Za 1 radni dan", "In 1 working day")}
{step("now", "U poslovnici, spremno", "At the branch, ready", "Preuzmi QR kodom", "Collect with a QR code")}
{step("todo", "Preuzeto", "Collected")}
</ul>
<button class="pa-btn primary">{ic("qr")}{B("Prikaži QR kod", "Show QR code")}</button>
<p class="pa-link">{B("Ne slažeš se sa odlukom? Žalba: pregleda je čovek.", "Disagree with a decision? Appeal: a human reviews it.")}</p>''', tab="box")


def s_pickup():
    return phone(f'''
<div class="pa-nav"><span>{ic("back")}</span>{B("Preuzimanje", "Pickup", "b")}<span></span></div>
<div class="pa-qrcard"><div class="pa-qrframe">{qr(150)}</div>{B("Pokaži službeniku", "Show to the clerk", "p")}
{B("Službenik skenira kod, ništa se ne kuca ručno.", "The clerk scans the code, nothing is typed by hand.", "small")}</div>
<div class="pa-card"><p class="pa-k">{B("Dodatna potvrda, ako treba", "Extra check, if needed")}</p>
<div class="pa-code"><i>4</i><i>7</i><i>1</i><i>9</i></div>{B("Četvorocifreni kod stiže na telefon.", "A four-digit code arrives on your phone.", "small")}</div>
<div class="pa-row-info">{ic("pin")}<div>{B("Poslovnica Beograd 1", "Branch Belgrade 1", "b")}{B("Radi do 20h", "Open until 8 pm", "small")}</div></div>''', tab=None)


def s_declare():
    def chips_(items):
        return "".join(f'<span class="{"on" if i == 0 else ""}">{B(*t)}</span>' for i, t in enumerate(items))
    return phone(f'''
<div class="pa-nav"><span>{ic("back")}</span>{B("Deklaracija", "Declaration", "b")}<span class="pa-step">1/3</span></div>
<div class="pa-progress"><i class="d"></i><i></i><i></i></div>
<div class="pa-card">
<div class="pa-field">{B("Poreklo pošiljke", "Where it comes from", "small")}<div class="pa-select">{B("Inostranstvo", "Abroad")}{ic("back", "pa-chev")}</div></div>
<div class="pa-field">{B("Šta je u paketu?", "What is inside?", "small")}<div class="pa-chips">{chips_([("Odeća", "Clothing"), ("Elektronika", "Electronics"), ("Knjige", "Books"), ("Ostalo", "Other")])}</div></div>
<div class="pa-field">{B("Vrednost", "Value", "small")}<div>6.000 RSD</div></div>
<div class="pa-attach">{ic("scan")}<div>{B("Račun priložen", "Invoice attached", "b")}{B("Podaci su popunjeni sa računa", "Details filled in from the invoice", "small")}</div><i class="ok">{ic("check")}</i></div>
</div>
<div class="pa-estimate">{B("Procena dažbina", "Estimated duties")}<b>2.170 RSD</b></div>
<button class="pa-btn primary">{B("Nastavi na obračun", "Continue to the calculation")}</button>''', tab=None)


def s_customs():
    def row(sr, en, amt, cls=""):
        return f'<div class="pa-line {cls}">{B(sr, en)}<b>{amt}</b></div>'
    return phone(f'''
<div class="pa-nav"><span>{ic("back")}</span>{B("Carina i plaćanje", "Customs and payment", "b")}<span></span></div>
<div class="pa-card"><p class="pa-k">{B("Deklaracija", "Declaration")}</p>
<div class="pa-line">{B("Poreklo", "Origin")}<b>{B("Inostranstvo", "Abroad")}</b></div>
<div class="pa-line">{B("Sadržaj", "Contents")}<b>{B("Odeća", "Clothing")}</b></div>
<div class="pa-line">{B("Vrednost", "Value")}<b>6.000 RSD</b></div></div>
<div class="pa-card"><p class="pa-k">{B("Kako se računa", "How it is calculated")} <em class="pa-ex">{B("primer", "example")}</em></p>
{row("Carina", "Customs duty", "600 RSD")}{row("PDV", "VAT", "1.320 RSD")}{row("Obrada", "Handling", "250 RSD")}{row("Ukupno", "Total", "2.170 RSD", "tot")}</div>
<button class="pa-btn primary">{ic("card")}{B("Plati odmah", "Pay now")}</button>
<button class="pa-btn ghost">{ic("qr")}{B("Plati preko IPS QR", "Pay by IPS QR")}</button>''', tab="card")


def s_ips():
    banks = "".join('<i></i>' for _ in range(4))
    return phone(f'''
<div class="pa-nav"><span>{ic("back")}</span>{B("Doplata na adresi", "Top-up at the door", "b")}<span></span></div>
<div class="pa-qrcard"><p class="pa-ips">NBS IPS QR</p><div class="pa-qrframe">{qr(150)}</div>
<div class="pa-amount">1.250 <small>RSD</small></div>{B("Skeniraj bankarskom aplikacijom.", "Scan with your banking app.", "small")}</div>
<div class="pa-card"><p class="pa-k">{B("Radi sa svim bankama", "Works with any bank")}</p><div class="pa-banks">{banks}</div></div>
<p class="pa-fine c">{B("Poštar ga pravi u svojoj aplikaciji, a ti plaćaš na licu mesta.", "The postman creates it in the app and you pay on the spot.")}</p>''', tab=None)


def s_branches():
    def row(name_sr, name_en, dist, kind, lvl_sr, lvl_en):
        return (f'<div class="pa-branch"><i class="pa-ico">{ic("pin")}</i><div>{B(name_sr, name_en, "b")}<small>{dist}</small></div>{chip(kind, lvl_sr, lvl_en)}</div>')
    return phone(f'''
<div class="pa-title">{B("Poslovnice", "Branches", "h4")}</div>
<div class="pa-search">{ic("search")}{B("Pretraži adresu", "Search an address")}</div>
<div class="pa-map"><i class="r1"></i><i class="r2"></i><i class="r3"></i><u style="left:26%;top:38%"></u><u style="left:62%;top:24%"></u><u class="me" style="left:48%;top:60%"></u></div>
<div class="pa-list tight">
{row("Beograd 1", "Belgrade 1", "350 m", "ok", "Gužva: mala", "Queue: short")}
{row("Beograd 11", "Belgrade 11", "1,2 km", "warn", "Gužva: srednja", "Queue: medium")}
{row("Beograd 4", "Belgrade 4", "2,0 km", "ok", "Gužva: mala", "Queue: short")}
</div>''', tab="home")


SCREENS = [
    (s_login, ("Prijava preko eUprave", "One login through eUprava"), ("Dvofaktorska potvrda, bez novih lozinki.", "Two-factor confirmation, no new passwords.")),
    (s_home, ("Sve na jednom ekranu", "Everything on one screen"), ("Praćenje, preuzimanje, carina i plaćanje.", "Tracking, pickup, customs and payment.")),
    (s_list, ("Paketi i jasni statusi", "Parcels with clear statuses"), ("Za preuzimanje, u toku i istorija.", "To collect, in transit and history.")),
    (s_detail, ("Carinjenje za jedan radni dan", "Customs in one working day"), ("Svaki korak vidljiv, uz pravo na žalbu.", "Every step visible, with the right to appeal.")),
    (s_pickup, ("Paket jednim QR kodom", "A parcel with one QR code"), ("Službenik skenira, ništa se ne kuca.", "The clerk scans, nothing is typed.")),
    (s_declare, ("Deklaracija robe u aplikaciji", "Declaring the goods in the app"), ("Poreklo, sadržaj i vrednost, uz račun koji se učitava.", "Origin, contents and value, with the invoice read in.")),
    (s_customs, ("Carina i PDV unapred", "Duty and VAT up front"), ("Javni obračun i plaćanje onlajn.", "A public calculation and online payment.")),
    (s_ips, ("Doplata: IPS QR", "Top-up: IPS QR"), ("Plaćanje na vratima iz bankarske aplikacije.", "Pay at the door from a banking app.")),
    (s_branches, ("Poslovnice i gužva", "Branches and queues"), ("Najbliža poslovnica sa kratkim redom.", "The nearest branch with a short queue.")),
]


def phones_html():
    figs = ""
    for i, (fn, title, desc) in enumerate(SCREENS, 1):
        figs += (f'<figure class="pa-fig">{fn()}<figcaption><span class="pa-n">{i:02d}</span>{B(title[0], title[1], "b")}'
                 f'{B(desc[0], desc[1], "small")}</figcaption></figure>')
    note = B("Vizualizacija je napravljena uz pomoć veštačke inteligencije (AI) i predstavlja koncept. Imena, brojevi pošiljki, iznosi i poslovnice su primeri.",
             "This visual was created with the help of AI and shows a concept. Names, tracking numbers, amounts and branches are examples.", "p", "pa-note")
    note = f'<div class="pa-ai"><span class="pa-ai-tag">AI</span>{note}</div>'
    ctrl = ('<div class="pa-ctrl"><button type="button" class="fc-arrow" data-pa="-1" aria-label="Previous / Prethodna">‹</button>'
            '<button type="button" class="fc-arrow" data-pa="1" aria-label="Next / Sledeća">›</button></div>')
    return f'<div class="pa">{note}<div class="pa-row">{figs}</div>{ctrl}</div>'


# ------------------------------------------------------------------ web versions and app+web pairs
def browser(body, url="posta.rs"):
    return (f'<div class="pa-browser"><div class="pa-bbar"><i></i><i></i><i></i><span class="pa-url">{ic("lock")}{url}</span></div>'
            f'<div class="pa-wbody">{body}</div></div>')


def wnav(active=0):
    items = [("Paketi", "Parcels"), ("Plaćanja", "Payments"), ("Poslovnice", "Branches"), ("Podrška", "Help")]
    nav = "".join(f'<span class="{"on" if i == active else ""}">{B(*t)}</span>' for i, t in enumerate(items))
    return (f'<div class="pa-wnav"><span class="pa-wlogo">{ic("send")}</span><b>Pošta Srbije</b><nav>{nav}</nav>'
            f'<span class="pa-wuser">{ic("user")}eUprava</span></div>')


def w_clerk():
    def chk(sr, en):
        return f'<li><b>{ic("check")}</b>{B(sr, en)}</li>'
    return browser(f'''
<div class="pa-wnav clerk"><span class="pa-wlogo">{ic("send")}</span><b>{B("Šalter 3 · Poslovnica Beograd 1", "Counter 3 · Branch Belgrade 1")}</b><span class="pa-wuser">{ic("scan")}{B("Skenirano", "Scanned")}</span></div>
<div class="pa-wgrid">
<div class="pa-card"><p class="pa-k">{B("Paket pronađen", "Parcel found")}</p>{B("Onlajn prodavnica", "Online shop", "h5")}<code>RS ••••• ••••• RS</code>
<div class="pa-shelf">{ic("box")}<span>{B("Polica", "Shelf")}</span><b>B-14</b></div></div>
<div class="pa-card"><p class="pa-k">{B("Provere", "Checks")}</p><ul class="pa-checks">
{chk("QR kod potvrđen", "QR code verified")}{chk("Carina plaćena unapred", "Customs paid in advance")}{chk("Identitet potvrđen preko eUprave", "Identity confirmed through eUprava")}{chk("Dodatni kod nije potreban", "No extra code needed")}</ul></div></div>
<div class="pa-wfoot"><button class="pa-btn primary">{ic("check")}{B("Predaj paket", "Hand over the parcel")}</button><p class="pa-fine">{B("Ništa se ne kuca ručno, ni lična karta se ne prepisuje.", "Nothing is typed by hand, and the ID is not copied.")}</p></div>''')


def w_declaration():
    def field(sr, en, val_sr, val_en):
        return f'<div class="pa-field">{B(sr, en, "small")}<div>{B(val_sr, val_en)}</div></div>'
    return browser(f'''
{wnav(1)}
<div class="pa-stepper"><span class="d">{ic("check")}{B("Deklaracija", "Declaration")}</span><span class="n">2 {B("Obračun", "Calculation")}</span><span>3 {B("Plaćanje", "Payment")}</span></div>
<div class="pa-wgrid">
<div class="pa-card"><p class="pa-k">{B("Deklaracija", "Declaration")}</p>{field("Poreklo", "Origin", "Inostranstvo", "Abroad")}{field("Sadržaj", "Contents", "Odeća", "Clothing")}{field("Vrednost", "Value", "6.000 RSD", "6,000 RSD")}</div>
<div class="pa-card"><p class="pa-k">{B("Kako se računa", "How it is calculated")} <em class="pa-ex">{B("primer", "example")}</em></p>
<div class="pa-line">{B("Carina", "Customs duty")}<b>600 RSD</b></div><div class="pa-line">{B("PDV", "VAT")}<b>1.320 RSD</b></div><div class="pa-line">{B("Obrada", "Handling")}<b>250 RSD</b></div>
<div class="pa-line tot">{B("Ukupno", "Total")}<b>2.170 RSD</b></div></div></div>
<div class="pa-wfoot row"><button class="pa-btn primary">{ic("card")}{B("Plati odmah", "Pay now")}</button><button class="pa-btn ghost">{ic("qr")}{B("Plati preko IPS QR", "Pay by IPS QR")}</button></div>''')


def w_status():
    def st(kind, sr, en, sub_sr="", sub_en=""):
        sub = B(sub_sr, sub_en, "small") if sub_sr else ""
        mark = ic("check") if kind == "done" else ""
        return f'<li class="{kind}"><i>{mark}</i>{B(sr, en, "b")}{sub}</li>'
    return browser(f'''
{wnav(0)}
<div class="pa-wtitle">{B("Pošiljka iz inostranstva", "Parcel from abroad", "b")}<code>RS ••••• ••••• RS</code></div>
<ol class="pa-hsteps">{st("done", "Primljeno", "Received")}{st("done", "Stiglo u Srbiju", "Arrived in Serbia")}{st("done", "Carinjenje", "Customs cleared", "1 radni dan", "1 working day")}{st("now", "U poslovnici", "At the branch")}{st("todo", "Preuzeto", "Collected")}</ol>
<div class="pa-wgrid">
<div class="pa-card"><p class="pa-k">{B("Automatska odluka", "Automatic decision")}</p>{chip("ok", "Ocarinjeno", "Cleared")}<small>{B("Odluka je doneta za jedan radni dan od dolaska.", "The decision was made within one working day of arrival.")}</small></div>
<div class="pa-card"><p class="pa-k">{B("Ne slažeš se?", "Disagree?")}</p><div class="pa-lines"><i></i><i></i><i class="s"></i></div>
<button class="pa-btn ghost">{ic("chat")}{B("Pošalji na pregled", "Send for review")}</button><small>{B("Žalbu pregleda čovek.", "A human reviews the appeal.")}</small></div></div>''')


PAIRS = {
    "p2": (s_pickup, w_clerk, ("Aplikacija: QR i kod", "App: QR and code"), ("Šalter: službenik skenira", "Counter: the clerk scans")),
    "p3": (s_declare, w_declaration, ("Aplikacija: deklaracija robe", "App: declaring the goods"), ("Veb: deklaracija i kalkulator", "Web: declaration and calculator")),
    "p4": (s_detail, w_status, ("Aplikacija: status i žalba", "App: status and appeal"), ("Veb: status i žalba", "Web: status and appeal")),
}


def pair_html(part):
    ph, web, cap_a, cap_w = PAIRS[part]
    tag = '<span class="pa-aitag">AI</span>'
    cap = lambda cp, label: f'<figcaption><span class="pa-n">{label}{tag}</span>{B(cp[0], cp[1], "b")}</figcaption>'
    cls = {"c1": " pa-apr", "q1": " pa-green", "n30": " pa-amber", "l2": " pa-teal", "b48": " pa-red", "f50": " pa-pink"}.get(part, "")
    return (f'<div class="pa pa-pairwrap{cls}"><div class="pa-pair"><figure class="pa-fig">{ph()}{cap(cap_a, "APP")}</figure>'
            f'<figure class="pa-webfig">{web()}{cap(cap_w, "WEB")}</figure></div></div>')


# ------------------------------------------------------------------ business closing (APR / eUprava concept)
def s_close():
    def chk(sr, en):
        return f'<li><b>{ic("check")}</b>{B(sr, en)}</li>'
    return phone(f'''
<div class="pa-nav"><span>{ic("back")}</span>{B("Zatvaranje firme", "Closing a business", "b")}<span></span></div>
<div class="pa-card"><div class="pa-co"><i class="pa-ico">{ic("home")}</i><div>{B("Moja firma", "My business", "b")}{B("preduzetnik (primer)", "sole trader (example)", "small")}</div></div>{chip("ok", "Nema otvorenih obaveza", "No open obligations")}</div>
<div class="pa-card center"><p class="pa-k">{B("Konačan porez", "Final tax")} <em class="pa-ex">{B("primer", "example")}</em></p><div class="pa-bigamt">16.000 <small>RSD</small></div>{B("Obračunato odmah, iz podataka Poreske uprave.", "Calculated at once, from Poreska uprava data.", "small")}</div>
<ul class="pa-checks flat">{chk("Zahtev podnet", "Request filed")}{chk("Porez obračunat", "Tax calculated")}{chk("Spremno za plaćanje", "Ready to pay")}</ul>
<button class="pa-btn primary">{B("Plati i zatvori firmu", "Pay and close the business")}</button>''', tab=None)


def w_close():
    nav = "".join(f'<span class="{"on" if i == 0 else ""}">{B(*t)}</span>' for i, t in enumerate([("Moja firma", "My business"), ("Registracija", "Registration"), ("Izveštaji", "Reports"), ("Podrška", "Help")]))
    return browser(f'''
<div class="pa-wnav"><span class="pa-wlogo">{ic("home")}</span><b>APR</b><nav>{nav}</nav><span class="pa-wuser">{ic("user")}eUprava</span></div>
<div class="pa-stepper"><span class="d">{ic("check")}{B("Zahtev", "Request")}</span><span class="n">2 {B("Konačan porez", "Final tax")}</span><span>3 {B("Plaćanje", "Payment")}</span><span>4 {B("Gotovo", "Done")}</span></div>
<div class="pa-wgrid">
<div class="pa-card"><p class="pa-k">{B("Firma", "Business")}</p>
<div class="pa-field">{B("Naziv", "Name", "small")}<div>{B("Moja firma", "My business")}</div></div>
<div class="pa-field">{B("Datum zatvaranja", "Closing date", "small")}<div>{B("Danas", "Today")}</div></div>
{chip("ok", "Nema otvorenih obaveza", "No open obligations")}</div>
<div class="pa-card"><p class="pa-k">{B("Konačan obračun poreza", "Final tax calculation")} <em class="pa-ex">{B("primer", "example")}</em></p>
<div class="pa-line">{B("Porez", "Tax")}<b>9.600 RSD</b></div><div class="pa-line">{B("Doprinosi", "Contributions")}<b>6.400 RSD</b></div>
<div class="pa-line tot">{B("Ukupno", "Total")}<b>16.000 RSD</b></div>{B("Obračunato odmah.", "Calculated at once.", "small")}</div></div>
<div class="pa-wfoot row"><button class="pa-btn primary">{ic("check")}{B("Plati i zatvori firmu", "Pay and close the business")}</button><button class="pa-btn ghost">{ic("qr")}{B("Plati preko IPS QR", "Pay by IPS QR")}</button></div>''', url="apr.gov.rs")


PAIRS["c1"] = (s_close, w_close, ("Aplikacija: plati i zatvori", "App: pay and close"), ("Veb: portal za zatvaranje", "Web: the closing portal"))


# ------------------------------------------------------------------ employee side: the postman's phone
def s_postman():
    return phone(f'''
<div class="pa-nav"><span>{ic("back")}</span>{B("Dostava", "Delivery", "b")}<span></span></div>
<div class="pa-card"><p class="pa-k">{B("Adresa dostave", "Delivery address")}</p>
<div class="pa-co"><i class="pa-ico">{ic("pin")}</i><div>{B("Primer ulice 12, Beograd", "Example Street 12, Belgrade", "b")}{B("Paket 3 od 14 danas", "Parcel 3 of 14 today", "small")}</div></div>
<code>RS ••••• ••••• RS</code></div>
<div class="pa-card center"><p class="pa-k">{B("Za doplatu", "To be paid")}</p><div class="pa-bigamt">1.250 <small>RSD</small></div>{B("Carinska doplata, primer.", "A customs top-up, example.", "small")}</div>
<ul class="pa-checks flat"><li><b>{ic("check")}</b>{B("Primalac potvrđen QR kodom", "Recipient confirmed by QR")}</li><li><b>{ic("check")}</b>{B("Ništa se ne kuca ručno", "Nothing typed by hand")}</li></ul>
<button class="pa-btn primary">{ic("qr")}{B("Napravi NBS IPS QR", "Create the NBS IPS QR")}</button>''', tab=None)


PAIRS["emp"] = (s_postman, w_clerk, ("Aplikacija poštara: doplata", "Postman app: top-up"), ("Šalter: službenik skenira", "Counter: the clerk scans"))


# ------------------------------------------------------------------ staff interface (internal screens)
def snav(title, items, active=0, who=("Šalter 3", "Counter 3")):
    nav = "".join(f'<span class="{"on" if i == active else ""}">{B(*t)}</span>' for i, t in enumerate(items))
    return (f'<div class="pa-wnav"><span class="pa-wlogo">{ic("send")}</span><b>{B(*title)}</b><nav>{nav}</nav>'
            f'<span class="pa-wuser">{ic("user")}{B(*who)}</span></div>')


STAFF_URL = "posta.rs/zaposleni"


def w_intake():
    return browser(f'''
{snav(("Prijem pošiljke", "Accepting a parcel"), [("Prijem", "Intake"), ("Preuzimanje", "Pickup"), ("Red", "Queue")], 0)}
<div class="pa-stepper"><span class="d">{ic("check")}{B("QR skeniran", "QR scanned")}</span><span class="n">2 {B("Provera", "Check")}</span><span>3 {B("Nalepnica", "Label")}</span></div>
<div class="pa-wgrid">
<div class="pa-card"><p class="pa-k">{B("Pošiljalac", "Sender")} {chip("blue", "Iz aplikacije", "From the app")}</p>
<div class="pa-field">{B("Ime", "Name", "small")}<div>{B("Ime Prezime (primer)", "Name Surname (example)")}</div></div>
<div class="pa-field">{B("Primalac", "Recipient", "small")}<div>{B("Primer ulice 12, Beograd", "Example Street 12, Belgrade")}</div></div></div>
<div class="pa-card"><p class="pa-k">{B("Pošiljka", "Parcel")}</p>
<div class="pa-line">{B("Težina", "Weight")}<b>1,2 kg</b></div><div class="pa-line">{B("Usluga", "Service")}<b>{B("Standard", "Standard")}</b></div>
<div class="pa-line tot">{B("Cena", "Price")}<b>380 RSD</b></div>{B("Obračunato automatski.", "Calculated automatically.", "small")}</div></div>
<div class="pa-wfoot"><button class="pa-btn primary">{ic("send")}{B("Odštampaj nalepnicu i primi", "Print the label and accept")}</button><p class="pa-fine">{B("Podaci su stigli iz aplikacije, ništa se ne kuca.", "The data came from the app, nothing is typed.")}</p></div>''', url=STAFF_URL)


def w_dash():
    bars = "".join(f'<i style="--h:{h}"></i>' for h in (18, 34, 52, 80, 64, 46, 58, 70, 40, 24))
    def kpi(sr, en, val, sub_sr="", sub_en=""):
        sub = B(sub_sr, sub_en, "small") if sub_sr else ""
        return f'<div class="pa-kpi">{B(sr, en, "small")}<b>{val}</b>{sub}</div>'
    return browser(f'''
{snav(("Poslovnica Beograd 1", "Branch Belgrade 1"), [("Danas", "Today"), ("Paketi", "Parcels"), ("Osoblje", "Staff")], 0, ("Upravnik", "Manager"))}
<div class="pa-kpis">{kpi("Red sada", "In the queue", "4", "pre 20 min: 11", "20 min ago: 11")}{kpi("Prosečno čekanje", "Average wait", "2 min", "juče: 9 min", "yesterday: 9 min")}{kpi("Spremno za preuzimanje", "Ready for pickup", "128")}</div>
<div class="pa-wgrid">
<div class="pa-card"><p class="pa-k">{B("Gužva po satima", "Queue by hour")} <em class="pa-ex">{B("primer", "example")}</em></p><div class="pa-hours">{bars}</div>
<div class="pa-hlab"><span>8</span><span>10</span><span>12</span><span>14</span><span>16</span><span>18</span></div></div>
<div class="pa-card"><p class="pa-k">{B("Papir i digitalno", "Paper and digital")} <em class="pa-ex">{B("primer", "example")}</em></p>
<div class="pa-meter"><i style="width:99.9%"></i></div><div class="pa-line">{B("Digitalno", "Digital")}<b>99,9%</b></div><div class="pa-line">{B("Papir", "Paper")}<b>0,1%</b></div>
{B("Cilj iz prvog koraka, uživo.", "The goal from step one, live.", "small")}</div></div>''', url=STAFF_URL)


def w_pipeline():
    def col(title, n, kind, k):
        pk = "".join(f'<span class="pa-pk {kind}"><code>RS •••• RS</code></span>' for _ in range(k))
        return f'<div class="pa-col"><p class="pa-k">{B(*title)} <em>{n}</em></p>{pk}</div>'
    return browser(f'''
{snav(("Tok pošiljki", "Parcel flow"), [("Tok", "Flow"), ("Carina", "Customs"), ("Izuzeci", "Exceptions")], 0, ("Logistika", "Logistics"))}
<div class="pa-kan">{col(("Primljeno", "Received"), 24, "", 3)}{col(("Carina", "Customs"), 6, "warn", 2)}{col(("U poslovnici", "At the branch"), 128, "ok", 3)}{col(("Isporučeno", "Delivered"), 312, "done", 2)}</div>
<div class="pa-wgrid"><div class="pa-card"><p class="pa-k">{B("Izuzeci koji traže pažnju", "Exceptions needing attention")}</p>
<div class="pa-line">{B("Pošiljka bez adrese", "Parcel without an address")}<b>1</b></div><div class="pa-line">{B("Čeka dokument", "Waiting for a document")}<b>2</b></div></div>
<div class="pa-card"><p class="pa-k">{B("Sve ostalo", "Everything else")}</p>{chip("ok", "Automatski, bez ručnog rada", "Automatic, no manual work")}{B("Sistem sam vodi pošiljke kroz korake.", "The system moves parcels through the steps on its own.", "small")}</div></div>''', url=STAFF_URL)


def w_customs():
    def row(code, kind, sr, en):
        return f'<div class="pa-trow"><code>{code}</code>{chip(kind, sr, en)}</div>'
    return browser(f'''
{snav(("Carinska služba", "Customs service"), [("Odluke", "Decisions"), ("Žalbe", "Appeals"), ("Izveštaji", "Reports")], 1, ("Carinik", "Officer"))}
<div class="pa-wgrid">
<div class="pa-card"><p class="pa-k">{B("Odluke danas", "Decisions today")}</p>
{row("RS ••••• RS", "ok", "Ocarinjeno automatski", "Cleared automatically")}{row("RS ••••• RS", "ok", "Ocarinjeno automatski", "Cleared automatically")}
{row("RS ••••• RS", "warn", "Žalba: čeka pregled", "Appeal: awaiting review")}{row("RS ••••• RS", "ok", "Ocarinjeno automatski", "Cleared automatically")}
<small>{B("Većinu odlučuje sistem, u roku od jednog radnog dana.", "The system decides most of them, within one working day.")}</small></div>
<div class="pa-card"><p class="pa-k">{B("Pregled žalbe", "Appeal review")}</p>
<div class="pa-line">{B("Automatska odluka", "Automatic decision")}<b>{B("Doplata", "Duty due")}</b></div>
<div class="pa-lines"><i></i><i></i><i class="s"></i></div><small>{B("Razlog žalbe i priloženi račun.", "Reason for the appeal and the attached invoice.")}</small>
<div class="pa-wfoot row"><button class="pa-btn primary">{B("Potvrdi", "Confirm")}</button><button class="pa-btn ghost">{B("Izmeni odluku", "Change the decision")}</button></div></div></div>''', url=STAFF_URL)


def s_route():
    def stop(sr, en, kind, st_sr, st_en, time):
        return (f'<div class="pa-branch"><i class="pa-ico">{ic("pin")}</i><div>{B(sr, en, "b")}<small>{time}</small></div>{chip(kind, st_sr, st_en)}</div>')
    return phone(f'''
<div class="pa-title">{B("Moja ruta", "My route", "h4")}</div>
<div class="pa-card"><div class="pa-line">{B("Danas", "Today")}<b>3 / 14</b></div><div class="pa-meter"><i style="width:21%"></i></div></div>
<div class="pa-map"><i class="r1"></i><i class="r2"></i><i class="r3"></i><u style="left:26%;top:40%"></u><u style="left:60%;top:26%"></u><u class="me" style="left:46%;top:62%"></u></div>
<div class="pa-list tight">
{stop("Primer ulice 12", "Example Street 12", "ok", "Sada", "Now", "09:40")}
{stop("Primer trg 3", "Example Square 3", "grey", "Sledeće", "Next", "10:05")}
</div>''', tab=None)


def web_fig(web, caption):
    return (f'<figure class="pa-webfig">{web()}<figcaption><span class="pa-n">WEB<span class="pa-aitag">AI</span></span>{B(caption[0], caption[1], "b")}</figcaption></figure>')


def phone_fig(screen, caption):
    return (f'<figure class="pa-fig">{screen()}<figcaption><span class="pa-n">APP<span class="pa-aitag">AI</span></span>{B(caption[0], caption[1], "b")}</figcaption></figure>')


def web_gallery(items):
    return '<div class="pa pa-wgallery">' + "".join(web_fig(w, cap) for w, cap in items) + "</div>"


def phone_pair(items):
    return '<div class="pa pa-phonepair">' + "".join(phone_fig(s, cap) for s, cap in items) + "</div>"


# ------------------------------------------------------------------ QR at every counter (eUprava concept, green variant)
def s_case():
    def st(kind, sr, en):
        mark = ic("check") if kind == "done" else ""
        return f'<li class="{kind}"><i>{mark}</i><div>{B(sr, en, "b")}</div></li>'
    return phone(f'''
<div class="pa-nav"><span>{ic("back")}</span>{B("Moj predmet", "My case", "b")}<span></span></div>
<div class="pa-card"><p class="pa-k">{B("Obnova boravišne dozvole", "Residence permit renewal")} <em class="pa-ex">{B("primer", "example")}</em></p>{chip("warn", "Nedostaje jedan dokument", "One document missing")}</div>
<div class="pa-qrcard"><div class="pa-qrframe">{qr(120)}</div>{B("Pokaži službeniku", "Show to the clerk", "p")}{B("Službenik skenira kod i odmah vidi ceo slučaj.", "The clerk scans the code and sees the whole case at once.", "small")}</div>
<ul class="pa-steps">{st("done", "Zahtev podnet", "Application filed")}{st("now", "Dokaz o adresi", "Proof of address")}{st("todo", "Taksa i termin", "Fee and slot")}</ul>''', tab=None)


def w_case():
    def chk(kind, sr, en):
        mark = {"ok": ic("check"), "miss": "!", "next": "›"}[kind]
        return f'<li class="{kind}"><b>{mark}</b>{B(sr, en)}</li>'
    return browser(f'''
<div class="pa-wnav"><span class="pa-wlogo">{ic("scan")}</span><b>{B("Šalter 2 · Opština (primer)", "Counter 2 · Municipality (example)")}</b><span class="pa-wuser">{ic("scan")}{B("Skenirano", "Scanned")}</span></div>
<div class="pa-wgrid">
<div class="pa-card"><p class="pa-k">{B("Predmet", "Case")}</p>{B("Obnova boravišne dozvole", "Residence permit renewal", "h5")}
<div class="pa-line">{B("Podnosilac", "Applicant")}<b>{B("Ime Prezime (primer)", "Name Surname (example)")}</b></div>
<div class="pa-line">{B("Podneto", "Filed")}<b>{B("pre 2 dana", "2 days ago")}</b></div>{chip("ok", "Podaci već u sistemu", "Data already in the system")}</div>
<div class="pa-card"><p class="pa-k">{B("Status", "Status")}</p><ul class="pa-checks case">{chk("ok", "Zahtev podnet", "Application filed")}{chk("ok", "Fotografija priložena", "Photo attached")}{chk("miss", "Nedostaje: dokaz o adresi", "Missing: proof of address")}{chk("next", "Sledeće: taksa, pa termin", "Next: pay the fee, then book a slot")}</ul></div></div>
<div class="pa-wfoot"><button class="pa-btn primary">{B("Pitaj samo ono što fali", "Ask only what is missing")}</button><p class="pa-fine">{B("Ništa se ne objašnjava iznova i ništa se ne kuca ručno.", "Nothing is explained again and nothing is typed by hand.")}</p></div>''', url="gov.rs/sluzbenik")


PAIRS["q1"] = (s_case, w_case, ("Aplikacija: tvoj predmet i QR", "App: your case and QR"), ("Šalter: službenik vidi ceo slučaj", "Counter: the clerk sees the whole case"))


# ------------------------------------------------------------------ never ask for papers the state already has (amber variant)
def s_apply():
    def src(sr, en, inst_sr, inst_en):
        return f'<li><b>{ic("check")}</b><div>{B(sr, en, "b")}{B(inst_sr, inst_en, "small")}</div></li>'
    return phone(f'''
<div class="pa-nav"><span>{ic("back")}</span>{B("Zahtev", "Application", "b")}<span class="pa-step">2/3</span></div>
<div class="pa-card"><p class="pa-k">{B("Zahtev za subvenciju", "Subsidy application")} <em class="pa-ex">{B("primer", "example")}</em></p>
{chip("ok", "Podaci preuzeti sami", "Data fetched automatically")}</div>
<div class="pa-card"><p class="pa-k">{B("Iz službenih evidencija", "From official records")}</p>
<ul class="pa-checks src">{src("Izvod iz matične knjige", "Birth register extract", "Matične knjige", "Civil registers")}{src("Podaci o prihodima", "Income data", "Poreska uprava", "Poreska uprava")}{src("Nepokretnosti", "Property", "RGZ", "RGZ")}</ul></div>
<div class="pa-estimate">{B("Papira za nošenje", "Papers to carry")}<b>0</b></div>
<button class="pa-btn primary">{B("Podnesi zahtev", "Submit the application")}</button>''', tab=None)


def w_justify():
    def src(sr, en):
        return f'<li><b>{ic("check")}</b>{B(sr, en)}</li>'
    return browser(f'''
<div class="pa-wnav"><span class="pa-wlogo">{ic("search")}</span><b>{B("Pregled zahteva · Službenik", "Reviewing an application · Clerk")}</b><span class="pa-wuser">{ic("user")}eZUP</span></div>
<div class="pa-wgrid">
<div class="pa-card"><p class="pa-k">{B("Podaci iz registara (eZUP)", "Data from registers (eZUP)")}</p>
<ul class="pa-checks">{src("Matične knjige", "Civil registers")}{src("Poreska uprava", "Poreska uprava")}{src("RGZ", "RGZ")}{src("MUP", "MUP")}</ul>{chip("ok", "Sve već postoji u sistemu", "All of it is already in the system")}</div>
<div class="pa-card"><p class="pa-k">{B("Traženje dodatnog papira", "Asking for an extra paper")}</p>
<div class="pa-field">{B("Dokument", "Document", "small")}<div>{B("Uverenje (primer)", "Certificate (example)")}</div></div>
<div class="pa-field">{B("Obrazloženje, obavezno", "Written reason, required", "small")}<div class="pa-textarea"><i></i><i></i><i class="s"></i></div></div>
{chip("warn", "Beleži se u javnu statistiku", "Logged in the public statistics")}</div></div>
<div class="pa-wfoot"><button class="pa-btn primary">{B("Pošalji zahtev građaninu", "Send the request to the citizen")}</button><p class="pa-fine">{B("Papir se traži samo uz pisano obrazloženje, a građanin može da se žali onlajn.", "A paper is requested only with a written reason, and the citizen can complain online.")}</p></div>''', url="gov.rs/sluzbenik")


def w_board():
    rows = [(("Služba A", "Office A"), 82), (("Služba B", "Office B"), 55), (("Služba C", "Office C"), 28), (("Služba D", "Office D"), 12)]
    bars = "".join(f'<div class="pa-brow">{B(*l, "span")}<div class="pa-meter"><i style="width:{w}%"></i></div><b>{w}</b></div>' for l, w in rows)
    return browser(f'''
<div class="pa-wnav"><span class="pa-wlogo">{ic("search")}</span><b>{B("Javna statistika", "Public statistics")}</b><span class="pa-wuser">{ic("globe")}{B("Otvoreno za sve", "Open to everyone")}</span></div>
<div class="pa-card"><p class="pa-k">{B("Uverenja izdata samo da bi se nosila drugoj službi", "Certificates issued only to be carried to another office")} <em class="pa-ex">{B("primer", "example")}</em></p>{bars}{B("Po službi, objavljeno javno. Cilj je da broj padne ka nuli.", "Per office, published openly. The goal is for the number to fall towards zero.", "small")}</div>''', url="gov.rs/statistika")


PAIRS["n30"] = (s_apply, w_justify, ("Aplikacija: podaci stižu sami", "App: the data arrives by itself"), ("Šalter: papir samo uz razlog", "Counter: a paper only with a reason"))


# ------------------------------------------------------------------ two eUprava levels (teal variant)
def s_level():
    def opt(sr, en):
        return f'<span class="pa-opt">{B(sr, en)}{ic("back", "pa-chev")}</span>'
    return phone(f'''
<div class="pa-nav"><span>{ic("back")}</span>{B("Nivo naloga", "Account level", "b")}<span></span></div>
<div class="pa-card"><div class="pa-lv"><i class="pa-ico">{ic("user")}</i><div>{B("Osnovni nivo", "Basic level", "b")}{B("E-pošta i snimak dokumenta", "Email and a document scan", "small")}</div>{chip("ok", "Aktivan", "Active")}</div></div>
<div class="pa-card"><div class="pa-lv"><i class="pa-ico">{ic("shield")}</i><div>{B("Puni nivo", "Full level", "b")}{B("Sve usluge i potpis", "Every service and signing", "small")}</div></div>
<p class="pa-k">{B("Potvrdi identitet", "Confirm your identity")}</p>
{opt("Preko banke", "Through a bank")}{opt("Čip lična karta", "Chip ID card")}{opt("Preko pošte", "Through the pošta")}</div>
<p class="pa-fine c">{B("Bez dolaska na šalter.", "With no counter visit.")}</p>''', tab=None)


def w_verify():
    def bank(i):
        return f'<span class="pa-bank"><i></i>{B("Banka " + i, "Bank " + i)}</span>'
    return browser(f'''
<div class="pa-wnav"><span class="pa-wlogo">{ic("user")}</span><b>eUprava</b><span class="pa-wuser">{ic("shield")}{B("Puni nivo", "Full level")}</span></div>
<div class="pa-stepper"><span class="d">{ic("check")}{B("E-pošta", "Email")}</span><span class="d">{ic("check")}{B("Snimak dokumenta", "Document scan")}</span><span class="n">3 {B("Potvrda identiteta", "Identity check")}</span></div>
<div class="pa-wgrid">
<div class="pa-card"><p class="pa-k">{B("Izaberi način potvrde", "Pick how to confirm")}</p><div class="pa-banks2">{bank("A")}{bank("B")}{bank("C")}</div>
<div class="pa-line">{B("Čip lična karta", "Chip ID card")}<b>NFC</b></div><div class="pa-line">{B("Pošta", "Pošta")}<b>{B("jednom", "once")}</b></div></div>
<div class="pa-card"><p class="pa-k">{B("Šta dobijaš", "What you get")}</p><ul class="pa-checks">
<li><b>{ic("check")}</b>{B("Sve usluge eUprave", "Every eUprava service")}</li><li><b>{ic("check")}</b>{B("Elektronski potpis", "Electronic signing")}</li><li><b>{ic("check")}</b>{B("Bez šaltera i aktivacionog koda", "No counter, no activation code")}</li></ul>{chip("blue", "eIDAS standard", "eIDAS standard")}</div></div>
<div class="pa-wfoot"><button class="pa-btn primary">{B("Potvrdi preko banke", "Confirm through a bank")}</button><p class="pa-fine">{B("Stranci dobijaju osnovni nivo odmah, a puni sa boravkom.", "Foreigners get the basic level at once and the full level with residence.")}</p></div>''', url="euprava.gov.rs")


PAIRS["l2"] = (s_level, w_verify, ("Aplikacija: izbor nivoa", "App: choosing the level"), ("Veb: potvrda identiteta", "Web: the identity check"))


# ------------------------------------------------------------------ no registration of stay (red variant)
def s_stay():
    return phone(f'''
<div class="pa-nav"><span>{ic("back")}</span>{B("Moj boravak", "My stay", "b")}<span></span></div>
<div class="pa-card center"><p class="pa-k">{B("Preostalo dana", "Days left")} <em class="pa-ex">{B("primer", "example")}</em></p><div class="pa-bigamt">62 <small>{B("dana", "days")}</small></div>
<div class="pa-meter w"><i style="width:31%"></i></div>{B("Računa sistem, iz podataka sa granice.", "Calculated by the system from the border data.", "small")}</div>
<div class="pa-card"><div class="pa-line">{B("Ulazak", "Entry")}<b>{B("datum sa granice", "date from the border")}</b></div><div class="pa-line">{B("Osnov", "Basis")}<b>{B("bezvizno 90/180", "visa-free 90/180")}</b></div></div>
<div class="pa-card"><div class="pa-lv"><i class="pa-ico">{ic("check")}</i><div>{B("Prijava boravka", "Registration of stay", "b")}{B("Nije potrebna", "Not needed", "small")}</div>{chip("ok", "Ništa da radiš", "Nothing to do")}</div></div>''', tab=None)


def w_border():
    return browser(f'''
<div class="pa-wnav"><span class="pa-wlogo">{ic("shield")}</span><b>{B("Granična baza", "Border database")}</b><span class="pa-wuser">{ic("scan")}{B("Provera", "Lookup")}</span></div>
<div class="pa-wgrid">
<div class="pa-card"><p class="pa-k">{B("Ulazak i izlazak", "Entry and exit")} <em class="pa-ex">{B("primer", "example")}</em></p>
<div class="pa-line">{B("Ulazak", "Entry")}<b>{B("datum, granični prelaz", "date, border crossing")}</b></div><div class="pa-line">{B("Osnov", "Basis")}<b>{B("bezvizno ili viza", "visa-free or visa")}</b></div><div class="pa-line">{B("Izlazak", "Exit")}<b>{B("datum", "date")}</b></div></div>
<div class="pa-card"><p class="pa-k">{B("Dani", "Days")}</p><div class="pa-kpi plain"><b>62</b>{B("preostalo", "left", "small")}</div><div class="pa-meter w"><i style="width:31%"></i></div>{chip("ok", "Sistem računa sam", "Calculated by the system")}</div></div>
<div class="pa-wfoot"><p class="pa-fine">{B("Sve što treba već je u bazi: bez prijave od hotela i stanodavca.", "Everything needed is already in the database: no report from hotels or landlords.")}</p></div>''', url="granica.gov.rs")


PAIRS["b48"] = (s_stay, w_border, ("Aplikacija: dani boravka", "App: days of stay"), ("Granica: ulazak i dani", "Border: entry and days"))

# ------------------------------------------------------------------ legal fast track (pink variant)
def s_speed():
    def opt(sr, en, days_sr, days_en, fee, on=False):
        return (f'<div class="pa-speedopt{" on" if on else ""}"><div>{B(sr, en, "b")}{B(days_sr, days_en, "small")}</div><strong>{fee}</strong></div>')
    return phone(f'''
<div class="pa-nav"><span>{ic("back")}</span>{B("Brzina izdavanja", "Processing speed", "b")}<span class="pa-step">2/3</span></div>
<div class="pa-card"><p class="pa-k">{B("Dokument", "Document")} <em class="pa-ex">{B("primer", "example")}</em></p>{B("Izdavanje dokumenta", "Issuing a document", "b")}</div>
{opt("Standard", "Standard", "30 dana", "30 days", "1.000 RSD")}{opt("Brže", "Faster", "15 dana, +50%", "15 days, +50%", "1.500 RSD", True)}{opt("Hitno", "Urgent", "7 dana, dvostruka taksa", "7 days, double fee", "2.000 RSD")}
<p class="pa-fine c">{B("Osnovna taksa je primer. Novac ide u budžet službe.", "The base fee is an example. The money goes to the office budget.")}</p>
<button class="pa-btn primary">{B("Nastavi", "Continue")}</button>''', tab=None)


def w_pay50():
    return browser(f'''
<div class="pa-wnav"><span class="pa-wlogo">{ic("card")}</span><b>{B("Plaćanje takse", "Paying the fee")}</b><span class="pa-wuser">{ic("user")}eUprava</span></div>
<div class="pa-stepper"><span class="d">{ic("check")}{B("Dokument", "Document")}</span><span class="d">{ic("check")}{B("Brzina", "Speed")}</span><span class="n">3 {B("Plaćanje", "Payment")}</span></div>
<div class="pa-wgrid">
<div class="pa-card"><p class="pa-k">{B("Izabrano", "Selected")} <em class="pa-ex">{B("primer", "example")}</em></p>
<div class="pa-line">{B("Brzina", "Speed")}<b>{B("Brže, 15 dana", "Faster, 15 days")}</b></div><div class="pa-line">{B("Osnovna taksa", "Base fee")}<b>1.000 RSD</b></div><div class="pa-line">{B("Dodatak +50%", "Surcharge +50%")}<b>500 RSD</b></div>
<div class="pa-line tot">{B("Ukupno", "Total")}<b>1.500 RSD</b></div></div>
<div class="pa-card"><p class="pa-k">{B("Gde ide novac", "Where the money goes")}</p>
<div class="pa-flowbox"><span>{B("Tvoja uplata", "Your payment")}</span><i>›</i><span class="on">{B("Budžet službe", "The office budget")}</span></div>
{chip("ok", "Službeni račun i potvrda", "An official account and receipt")}{B("Bez „veze”, uz rok koji se vidi unapred.", "No “connections”, with a deadline you see up front.", "small")}</div></div>
<div class="pa-wfoot row"><button class="pa-btn primary">{ic("card")}{B("Plati", "Pay")}</button><button class="pa-btn ghost">{ic("qr")}{B("Plati preko IPS QR", "Pay by IPS QR")}</button></div>''', url="euprava.gov.rs")


PAIRS["f50"] = (s_speed, w_pay50, ("Aplikacija: izbor brzine", "App: choosing the speed"), ("Veb: plaćanje takse", "Web: paying the fee"))
