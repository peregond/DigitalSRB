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
    return f'<div class="pa">{note}<div class="pa-row">{figs}</div></div>'
