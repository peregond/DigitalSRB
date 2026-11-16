"""The single tax portal concept (idea 9): a large Apple-style dashboard and two simplified "today" wireframes.

Facts behind the "today" wireframes (all from public sources, drawn in a simplified way, not copies):
- ePorezi's start page offers sign-in with eID, or with a qualified certificate through SmartBox or the ePorezi app,
  plus downloads of SmartBox (macOS, Windows, Ubuntu) and the ePorezi app (Windows) and PDF user guides.
- APR services require an eID account since 2023; it offers electronic registration, changes and deletion of sole traders,
  and fees are paid by card.
Everything else (amounts, names, dates) is an example.
"""
from posta_app import B, ic, chip, browser, ICONS

ICONS.setdefault("calendar", "M3 5h18v16H3zM3 10h18M8 3v4M16 3v4")
ICONS.setdefault("download", "M12 3v12M7 10l5 5 5-5M4 21h16")
ICONS.setdefault("file", "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6")


# --------------------------------------------------------------------------- today: two simplified wireframes
def w_old_eporezi():
    btn = lambda sr, en: f'<span class="wf-btn">{ic("lock")}{B(sr, en)}</span>'
    return browser(f"""
<div class="wf-head"><b>ePorezi</b>{B("Poreska uprava", "Tax Administration", "small")}</div>
<div class="wf-col">
<p class="wf-h">{B("Dobrodošli na portal ePorezi", "Welcome to the ePorezi portal")}</p>
{btn("Prijava sa eID", "Sign in with eID")}
{btn("Prijava sertifikatom preko SmartBox-a", "Sign in with a certificate via SmartBox")}
{btn("Prijava sertifikatom preko aplikacije ePorezi", "Sign in with a certificate via the ePorezi app")}
<div class="wf-row"><span class="wf-dl">{ic("download")}{B("SmartBox: macOS, Windows, Ubuntu", "SmartBox: macOS, Windows, Ubuntu")}</span><span class="wf-dl">{ic("download")}{B("Aplikacija: samo Windows", "App: Windows only")}</span><span class="wf-dl">{ic("file")}{B("Uputstva (PDF)", "User guides (PDF)")}</span></div>
</div>""", url="eporezi.purs.gov.rs")


def w_old_apr():
    svc = lambda sr, en: f'<span class="wf-svc">{B(sr, en)}<i>›</i></span>'
    return browser(f"""
<div class="wf-head"><b>APR</b>{B("Agencija za privredne registre", "Business Registers Agency", "small")}</div>
<div class="wf-two">
<div class="wf-col"><p class="wf-h">{B("Prijava", "Sign in")}</p><span class="wf-btn">{ic("lock")}{B("eID nalog", "eID account")}</span><span class="wf-note">{B("Usluge APR-a rade samo uz eID nalog.", "APR services work only with an eID account.")}</span></div>
<div class="wf-col"><p class="wf-h">{B("Usluge", "Services")}</p>
{svc("Registracija preduzetnika", "Registering a sole trader")}{svc("Promena podataka", "Changing data")}{svc("Brisanje iz evidencije", "Deregistration")}{svc("Naknade, plaćanje karticom", "Fees, paid by card")}</div>
</div>""", url="apr.gov.rs")


# --------------------------------------------------------------------------- proposal: one large dashboard
def _cal():
    marks = {5: "tax", 12: "tax", 19: "reg", 26: "tax"}
    cells = "".join(f'<i class="{"on " + marks[d] if d in marks else ""}">{d if d <= 30 else ""}</i>' for d in range(1, 31))
    heads = "".join(f"<b>{d}</b>" for d in "PUSČPSN")
    return f'<div class="tp-cal">{heads}{cells}</div>'


def w_portal_lg():
    tabs = "".join(f'<span class="{"on" if i == 0 else ""}">{B(*t)}</span>' for i, t in enumerate(
        [("Pregled", "Overview"), ("Firma", "Business"), ("Registracija", "Registration"), ("Porezi", "Taxes"), ("Izveštaji", "Reports")]))
    tag = lambda t: f'<span class="pa-tag">{t}</span>'
    row = lambda sr, en, tg, extra="": (f'<li><i>{ic("check")}</i><div>{B(sr, en, "span")}{extra}</div>{tag(tg) if tg else ""}</li>')
    due = lambda sr, en, kind: f'<li><i class="{kind}">{ic("calendar")}</i><div>{B(sr, en, "span")}</div></li>'
    html = f"""
<div class="tp">
<div class="tp-nav"><span class="pa-wlogo">{ic("home")}</span><b>{B("Poreski portal", "Tax portal")}</b><nav>{tabs}</nav>
<span class="tp-search">{ic("search")}{B("Pretraži usluge", "Search services")}</span><span class="tp-lang"><i class="on">SR</i><i>EN</i></span><span class="tp-av">{ic("user")}</span></div>
<div class="tp-head"><div><p class="tp-hi">{B("Dobar dan", "Good afternoon")}</p><h4>{B("Moja firma", "My business")} <em class="pa-ex">{B("primer", "example")}</em></h4></div>
<div class="tp-pills">{chip("ok", "Registrovana", "Registered")}{chip("ok", "Prijave: u redu", "Filings: in order")}{chip("blue", "Jedan nalog, eUprava", "One account, eUprava")}</div></div>
<div class="tp-grid">
<section class="tp-card big"><p class="pa-k">{B("Za plaćanje", "To pay")}</p>
<div class="tp-amt">16.000 <small>RSD</small></div>
<div class="tp-split"><i style="width:60%"></i><i style="width:40%"></i></div>
<div class="tp-leg"><span><i></i>{B("Porez", "Tax")} 9.600</span><span><i class="b"></i>{B("Doprinosi", "Contributions")} 6.400</span></div>
<ul class="tp-mini"><li>{ic("calendar")}<span>{B("Prijava poreza", "Tax filing")}</span><b>{B("za 12 dana", "in 12 days")}</b></li><li>{ic("calendar")}<span>{B("Doprinosi", "Contributions")}</span><b>{B("za 26 dana", "in 26 days")}</b></li></ul>
<div class="tp-btns"><button class="pa-btn primary">{ic("card")}{B("Plati sve odjednom", "Pay everything at once")}</button><button class="pa-btn ghost">{ic("qr")}{B("Plati preko IPS QR", "Pay by IPS QR")}</button></div></section>
<section class="tp-card"><p class="pa-k">{B("Registracija", "Registration")} {tag("APR")}</p>
<ul class="tp-list">{row("Podaci o firmi", "Business data", "")}{row("Poslednja izmena", "Last change", "", B("pre 3 meseca", "3 months ago", "small"))}</ul>
<button class="pa-btn ghost sm">{B("Izmeni podatke", "Change data")}</button></section>
<section class="tp-card"><p class="pa-k">{B("Prijave", "Filings")} {tag("Poreska")}</p>
<ul class="tp-list due">{due("Prijava poreza, za 12 dana", "Tax filing, in 12 days", "soon")}{due("Doprinosi, za 26 dana", "Contributions, in 26 days", "")}</ul>
<button class="pa-btn ghost sm">{B("Podnesi prijavu", "File a return")}</button></section>
<section class="tp-card"><p class="pa-k">{B("Kalendar", "Calendar")}</p>{_cal()}</section>
<section class="tp-card"><p class="pa-k">{B("Obaveštenja", "Notices")}</p>
<ul class="tp-list">{row("Poreska prijava primljena", "Tax return received", "Poreska")}{row("Registracija potvrđena", "Registration confirmed", "APR")}</ul></section>
</div>
<div class="tp-foot">{ic("shield")}{B("Svaku uslugu i dalje pruža njena ustanova, a ti vidiš sve na jednom mestu.", "Each service is still provided by its own agency, and you see it all in one place.")}</div>
</div>"""
    return browser(html, url="portal.gov.rs").replace('class="pa-browser"', 'class="pa-browser lg"', 1)


def portal_html():
    tagai = '<span class="pa-aitag">AI</span>'
    note = (f'<div class="pa-ai"><span class="pa-ai-tag">AI</span>'
            f'{B("Vizualizacija je napravljena uz pomoć veštačke inteligencije (AI) i predstavlja koncept. Prikaz današnjih sajtova je uprošćen i nije tačna kopija.", "This visual was created with the help of AI and shows a concept. The view of today’s sites is simplified and not an exact copy.", "p", "pa-note")}</div>')
    old = (f'<div class="pa-oldrow"><figure class="pa-webfig">{w_old_eporezi()}<figcaption><span class="pa-n">{B("DANAS", "TODAY")}</span>{B("ePorezi: tri načina prijave i preuzimanje programa", "ePorezi: three ways to sign in and programs to download", "b")}</figcaption></figure>'
           f'<figure class="pa-webfig">{w_old_apr()}<figcaption><span class="pa-n">{B("DANAS", "TODAY")}</span>{B("APR: poseban portal i poseban nalog usluga", "APR: a separate portal with its own list of services", "b")}</figcaption></figure></div>')
    new = (f'<figure class="pa-webfig pa-lgfig">{w_portal_lg()}<figcaption><span class="pa-n">{B("PREDLOG", "PROPOSAL")}{tagai}</span>'
           f'{B("Jedinstveni poreski portal: registracija, porezi i obaveze na jednom ekranu", "The single tax portal: registration, taxes and obligations on one screen", "b")}</figcaption></figure>')
    return f'<div class="pa pa-olive pa-portal">{note}{old}<div class="pa-oldarrow" aria-hidden="true">↓</div>{new}</div>'
