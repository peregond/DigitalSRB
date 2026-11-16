#!/usr/bin/env python3
"""Renders the concept screenshots for the single tax portal page to assets/shots/*.webp.

  portal-sr.webp / portal-en.webp   the proposed single tax portal (Apple-style), Serbian is the default
  old-eporezi.webp / old-apr.webp   simplified, deliberately dated ("90s") views of today's ePorezi and APR sites

The old views are real screenshots supplied by the author (src-*.webp, personal data removed from the ePorezi header). Earlier drawn versions were based on public descriptions (ePorezi start page: eID / SmartBox / ePorezi app sign-in, downloads,
user guides; APR: eID sign-in and e-services for sole traders), not copied from the sites. All names, amounts and dates
are examples. Run:  python3 tools/shots.py   (needs node + playwright and Pillow)
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "shots"
TMP = ROOT / "tools" / "shots"
W, H, SCALE = 1348, 730, 1.6   # the window only: transparent corners, no backdrop; the page adds the shadow

ICON = {
    "home": "M3 11l9-8 9 8v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z",
    "search": "M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM21 21l-4.3-4.3",
    "user": "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
    "bell": "M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 0 1-3.4 0",
    "check": "M20 6L9 17l-5-5",
    "card": "M2 6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2zM2 10h20",
    "qr": "M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h3v3h-3zM20 14v3M14 20h3M20 20v1",
    "cal": "M3 5h18v16H3zM3 10h18M8 3v4M16 3v4",
    "shield": "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10zM9 12l2 2 4-4",
    "lock": "M5 11h14v10H5zM8 11V7a4 4 0 0 1 8 0v4",
    "file": "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6",
    "edit": "M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z",
    "arrow": "M5 12h14M13 6l6 6-6 6",
    "mail": "M3 5h18v14H3zM3 7l9 7 9-7",
    "help": "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3M12 17h.01",
    "cog": "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2",
    "build": "M4 21V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v16M15 9h4a1 1 0 0 1 1 1v11M8 8h3M8 12h3M8 16h3M3 21h18",
    "list": "M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01",
    "down": "M6 9l6 6 6-6",
    "doc": "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M9 13h6M9 17h6",
    "trend": "M3 17l6-6 4 4 8-8M15 7h6v6",
}


def ic(n, cls=""):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="{ICON[n]}"/></svg>')


# ------------------------------------------------------------------ shared browser frame
FRAME_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1348px;height:730px;overflow:hidden;background:transparent}
body{font-family:'Manrope','Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased;position:relative}
.win{position:absolute;left:0;top:0;right:0;bottom:0;border-radius:20px;background:#fff;overflow:hidden;display:flex;flex-direction:column;
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}
.chrome{height:48px;flex:none;display:flex;align-items:center;gap:9px;padding:0 18px}
.chrome i{width:12px;height:12px;border-radius:50%;display:block}
.chrome i:nth-child(1){background:#FF5F57}.chrome i:nth-child(2){background:#FEBC2E}.chrome i:nth-child(3){background:#28C840}
.url{flex:1;max-width:460px;margin:0 auto;transform:translateX(-30px);display:flex;align-items:center;justify-content:center;gap:7px;height:28px;border-radius:9px;font-size:13px;font-weight:600}
.url svg{width:12px;height:12px}
"""


def page(css, body, bg):
    return (f'<!doctype html><html><head><meta charset="utf-8"><link rel="preconnect" href="https://fonts.googleapis.com">'
            f'<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
            f'<style>{FRAME_CSS}{css}</style></head><body style="background:transparent">{body}</body></html>')


# ------------------------------------------------------------------ the new portal
PORTAL_CSS = """
.win{background:#fff}
.chrome{background:#F5F5F7}.url{background:#E8E8ED;color:#6e6e73}
.app{flex:1;min-height:0;display:grid;grid-template-columns:232px 1fr;font-family:Inter,'Manrope',system-ui,sans-serif;font-size:13.5px;color:#1d1d1f;letter-spacing:-.005em;font-variant-numeric:tabular-nums}
.side{background:#F5F5F7;border-right:1px solid #E5E5EA;padding:16px 12px;display:flex;flex-direction:column;gap:2px;min-height:0}
.brand{display:flex;align-items:center;gap:10px;padding:2px 8px 14px}
.logo{width:30px;height:30px;border-radius:9px;background:#1d1d1f;color:#fff;display:grid;place-items:center}.logo svg{width:17px;height:17px}
.brand b{font-size:15px;font-weight:700;letter-spacing:-.01em}
.firm{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid #E5E5EA;border-radius:10px;padding:9px 10px;margin-bottom:12px}
.firm i{font-style:normal;width:28px;height:28px;border-radius:8px;background:#E8E8ED;display:grid;place-items:center;font-weight:700;font-size:11.5px;color:#3a3a3c}
.firm div{flex:1;line-height:1.25}.firm b{display:block;font-size:13px;font-weight:600}.firm small{font-size:11.5px;color:#6e6e73}
.firm svg{width:15px;height:15px;color:#8e8e93}
.grp{font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:#8e8e93;padding:10px 10px 5px}
.it{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:8px;font-weight:500;color:#3a3a3c}
.it svg{width:17px;height:17px;color:#6e6e73;flex:none}
.it.on{background:#E8E8ED;font-weight:600;color:#1d1d1f}.it.on svg{color:#0066CC}
.it .own{margin-left:auto;font-size:10.5px;font-weight:600;color:#8e8e93}
.it .cnt{margin-left:auto;background:#0071E3;color:#fff;font-size:11px;font-weight:600;border-radius:999px;padding:1px 7px}
.sp{flex:1}
.main{display:flex;flex-direction:column;min-width:0;min-height:0;background:#fff}
.top{display:flex;align-items:center;gap:14px;height:52px;border-bottom:1px solid #E5E5EA;padding:0 26px;flex:none}
.crumb{display:flex;align-items:center;gap:8px;color:#6e6e73;font-weight:500}.crumb b{color:#1d1d1f;font-weight:600}
.find{margin-left:auto;display:flex;align-items:center;gap:8px;background:#F5F5F7;border:1px solid #E5E5EA;border-radius:9px;padding:7px 12px;color:#8e8e93;min-width:290px}
.find svg{width:15px;height:15px}.find kbd{margin-left:auto;font:600 11px Inter,sans-serif;color:#8e8e93;background:#fff;border:1px solid #E5E5EA;border-radius:5px;padding:1px 6px}
.lang{display:flex;background:#F5F5F7;border:1px solid #E5E5EA;border-radius:8px;padding:2px}.lang i{font-style:normal;font-weight:600;font-size:11.5px;padding:4px 9px;border-radius:6px;color:#6e6e73}.lang i.on{background:#fff;color:#1d1d1f;box-shadow:0 1px 3px rgba(0,0,0,.12)}
.ic{position:relative;width:32px;height:32px;border-radius:8px;display:grid;place-items:center;color:#3a3a3c}.ic svg{width:17px;height:17px}
.ic u{position:absolute;top:5px;right:6px;width:8px;height:8px;border-radius:50%;background:#0071E3;border:2px solid #fff}
.me{display:flex;align-items:center;gap:8px;font-weight:600}.me i{font-style:normal;width:30px;height:30px;border-radius:50%;background:#1d1d1f;color:#fff;display:grid;place-items:center;font-size:11.5px}
.body{flex:1;min-height:0;padding:20px 26px 14px;display:flex;flex-direction:column;gap:14px}
.head{display:flex;align-items:flex-end;justify-content:space-between}
h1{font-size:26px;font-weight:700;letter-spacing:-.025em;line-height:1.15}
.sub{color:#6e6e73;margin-top:3px;font-size:13px}
.acts{display:flex;gap:8px}
.b{display:inline-flex;align-items:center;gap:7px;border-radius:9px;padding:8px 14px;font-weight:600;font-size:13px;border:1px solid #D2D2D7;background:#fff;color:#1d1d1f}
.b svg{width:15px;height:15px}
.b.p{background:#0071E3;border-color:#0071E3;color:#fff}
.strip{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid #E5E5EA;border-radius:12px;background:#fff}
.strip div{padding:11px 16px;border-left:1px solid #E5E5EA;display:grid;gap:2px}.strip div:first-child{border-left:0}
.strip small{font-size:11.5px;color:#6e6e73;font-weight:500}.strip b{font-size:17px;font-weight:650;letter-spacing:-.015em}
.strip b.w{color:#B25E00}.strip b.g{color:#1F8A3B}
.cols{flex:1;min-height:0;display:grid;grid-template-columns:1fr 292px;gap:16px}
.panel{border:1px solid #E5E5EA;border-radius:12px;background:#fff;display:flex;flex-direction:column;min-height:0;overflow:hidden}
.ph{display:flex;align-items:center;gap:12px;padding:12px 16px;border-bottom:1px solid #E5E5EA}.ph b{font-size:14px;font-weight:650}
.tabs{display:flex;gap:2px;margin-left:8px}.tabs span{padding:5px 10px;border-radius:7px;font-weight:500;color:#6e6e73;font-size:12.5px}.tabs span.on{background:#F5F5F7;color:#1d1d1f;font-weight:600}
.tabs em{font-style:normal;color:#8e8e93;margin-left:4px;font-size:11.5px}
.ph .fl{margin-left:auto;display:flex;align-items:center;gap:6px;color:#6e6e73;font-weight:500;font-size:12.5px}.ph .fl svg{width:14px;height:14px}
table{width:100%;border-collapse:collapse}
th{font-size:11px;font-weight:600;letter-spacing:.03em;text-transform:uppercase;color:#8e8e93;text-align:left;padding:8px 12px;background:#FAFAFA;border-bottom:1px solid #E5E5EA}
td{padding:0 12px;height:47px;border-bottom:1px solid #F0F0F2;vertical-align:middle}
tr:last-child td{border-bottom:0}
td.n{text-align:right}th.n{text-align:right}
.cb{width:16px;height:16px;border-radius:5px;border:1.5px solid #C7C7CC;display:grid;place-items:center;background:#fff}
.cb.on{background:#0071E3;border-color:#0071E3;color:#fff}.cb svg{width:11px;height:11px;stroke-width:3.5}
.nm b{display:block;font-weight:600}.nm small{color:#6e6e73;font-size:12px}
.ag{font-size:11.5px;font-weight:600;color:#3a3a3c;background:#F2F2F7;border-radius:6px;padding:2px 8px}
.st{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600;border-radius:999px;padding:3px 10px}
.st::before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}
.st.w{background:#FFF4E0;color:#B25E00}.st.b{background:#E8F1FD;color:#0059B8}.st.g{background:#E8F6EC;color:#1F8A3B}.st.n{background:#F2F2F7;color:#6e6e73}
.due b{font-weight:600}.due small{display:block;color:#6e6e73;font-size:12px}
.act{color:#0066CC;font-weight:600}
.bar{display:flex;align-items:center;gap:14px;margin-top:auto;border-top:1px solid #E5E5EA;background:#F5F9FF;padding:10px 16px}
.bar b{font-weight:600}.bar span{color:#3a3a3c}.bar .b{margin-left:auto}
.right{display:flex;flex-direction:column;gap:14px;min-height:0}
.right .panel{flex:none}
.tl{list-style:none;padding:6px 16px 12px;display:grid;gap:0}
.tl li{display:grid;grid-template-columns:18px 1fr;gap:10px;padding:8px 0;position:relative}
.tl li::before{content:"";position:absolute;left:8px;top:22px;bottom:-8px;width:1.5px;background:#E5E5EA}.tl li:last-child::before{display:none}
.tl i{width:17px;height:17px;border-radius:50%;background:#E8F6EC;color:#1F8A3B;display:grid;place-items:center;margin-top:1px}.tl i svg{width:10px;height:10px;stroke-width:3.5}
.tl b{font-weight:600;font-size:13px}.tl small{display:block;color:#6e6e73;font-size:12px;margin-top:1px}
.help{display:flex;align-items:center;gap:12px;padding:12px 16px}
.help i{width:34px;height:34px;border-radius:9px;background:#F2F2F7;display:grid;place-items:center;color:#3a3a3c}.help svg{width:17px;height:17px}
.help div{flex:1;line-height:1.3}.help b{font-weight:600}.help small{display:block;color:#6e6e73;font-size:12px}
.msg{padding:6px 16px 12px;display:grid;gap:10px}
.msg div{display:grid;grid-template-columns:30px 1fr auto;gap:10px;align-items:center}
.msg i{font-style:normal;width:30px;height:30px;border-radius:50%;background:#F2F2F7;display:grid;place-items:center;font-weight:700;font-size:11px;color:#3a3a3c}
.msg b{font-weight:600;font-size:13px;display:block}.msg small{color:#6e6e73;font-size:12px}.msg em{font-style:normal;color:#8e8e93;font-size:11.5px}
"""

STR = {
    "sr": {
        "lang": "sr-Latn", "url": "portal.gov.rs", "brand": "Poreski portal", "firm": "Primer d.o.o.", "pib": "PIB 100000001",
        "g1": "Pregled", "n_over": "Pregled", "n_firm": "Moja firma", "n_reg": "Registracija", "n_tax": "Porezi i prijave", "n_pay": "Plaćanja", "n_doc": "Uverenja i dokumenta", "n_msg": "Poruke",
        "g2": "Pomoć", "n_help": "Pomoć i kontakt", "n_set": "Podešavanja", "apr": "APR", "pu": "Poreska",
        "crumb": "Početna", "find": "Pretraži usluge, obrasce i uverenja", "me": "PD",
        "h1": "Pregled", "sub": "Primer d.o.o. · ažurirano danas u 09:41", "b1": "Nova prijava", "b2": "Plati",
        "s1": "Za plaćanje", "s1v": "16.000 RSD", "s2": "Najbliži rok", "s2v": "za 12 dana", "s3": "Registracija", "s3v": "U redu", "s4": "Nove poruke", "s4v": "2",
        "pt": "Obaveze", "tabs": [("Sve", "6"), ("Za plaćanje", "2"), ("Prijave", "2"), ("Registracija", "1")], "sort": "Rok",
        "c1": "Obaveza", "c2": "Ustanova", "c3": "Rok", "c4": "Iznos", "c5": "Status", "c6": "",
        "rows": [
            ("Porez na dohodak, mesečno", "Akontacija za oktobar", "Poreska", "28.11.2026.", "za 12 dana", "9.600", "Za plaćanje", "w", "Plati", True),
            ("Doprinosi za zaposlene", "PIO, zdravstvo, nezaposlenost", "Poreska", "12.12.2026.", "za 26 dana", "6.400", "Za plaćanje", "w", "Plati", True),
            ("Poreska prijava PP-PDV", "Novembar 2026.", "Poreska", "15.12.2026.", "za 29 dana", "—", "Čeka prijavu", "b", "Podnesi", False),
            ("Godišnji finansijski izveštaj", "Za 2025. godinu", "APR", "31.03.2027.", "za 4 meseca", "—", "Čeka prijavu", "b", "Podnesi", False),
            ("Potvrda podataka o firmi", "Poslednja izmena pre 3 meseca", "APR", "—", "", "—", "U redu", "g", "Pogledaj", False),
            ("Porez na dohodak, mesečno", "Akontacija za septembar", "Poreska", "28.10.2026.", "plaćeno pre 5 dana", "9.200", "Plaćeno", "n", "Potvrda", False),
        ],
        "sel": "izabrane obaveze", "selv": "16.000 RSD", "pay": "Plati izabrano",
        "ap": "Aktivnost", "a1": "Prijava poreza primljena", "a1d": "Poreska uprava · juče, 14:20", "a2": "Uplata evidentirana", "a2d": "Poreska uprava · pre 5 dana", "a3": "Registracija potvrđena", "a3d": "APR · pre 3 meseca",
        "mp": "Poruke", "m1": "Poreska uprava", "m1d": "Podsetnik: rok za akontaciju", "m1t": "09:12", "m2": "APR", "m2d": "Godišnji izveštaj: novi obrazac", "m2t": "juče",
        "hlp": "Treba ti pomoć?", "hlpd": "Razgovaraj sa podrškom ili zakaži poziv",
    },
    "en": {
        "lang": "en", "url": "portal.gov.rs", "brand": "Tax portal", "firm": "Example Ltd.", "pib": "Tax ID 100000001",
        "g1": "Overview", "n_over": "Overview", "n_firm": "My business", "n_reg": "Registration", "n_tax": "Taxes and filings", "n_pay": "Payments", "n_doc": "Certificates and documents", "n_msg": "Messages",
        "g2": "Help", "n_help": "Help and contact", "n_set": "Settings", "apr": "APR", "pu": "Tax Admin.",
        "crumb": "Home", "find": "Search services, forms and certificates", "me": "EL",
        "h1": "Overview", "sub": "Example Ltd. · updated today at 09:41", "b1": "New filing", "b2": "Pay",
        "s1": "To pay", "s1v": "16,000 RSD", "s2": "Next deadline", "s2v": "in 12 days", "s3": "Registration", "s3v": "In order", "s4": "New messages", "s4v": "2",
        "pt": "Obligations", "tabs": [("All", "6"), ("To pay", "2"), ("Filings", "2"), ("Registration", "1")], "sort": "Deadline",
        "c1": "Obligation", "c2": "Agency", "c3": "Deadline", "c4": "Amount", "c5": "Status", "c6": "",
        "rows": [
            ("Income tax, monthly", "Advance for October", "Tax Admin.", "28 Nov 2026", "in 12 days", "9,600", "To pay", "w", "Pay", True),
            ("Employee contributions", "Pension, health, unemployment", "Tax Admin.", "12 Dec 2026", "in 26 days", "6,400", "To pay", "w", "Pay", True),
            ("VAT return PP-PDV", "November 2026", "Tax Admin.", "15 Dec 2026", "in 29 days", "—", "To file", "b", "File", False),
            ("Annual financial statement", "For 2025", "APR", "31 Mar 2027", "in 4 months", "—", "To file", "b", "File", False),
            ("Business data confirmation", "Last change 3 months ago", "APR", "—", "", "—", "In order", "g", "View", False),
            ("Income tax, monthly", "Advance for September", "Tax Admin.", "28 Oct 2026", "paid 5 days ago", "9,200", "Paid", "n", "Receipt", False),
        ],
        "sel": "obligations selected", "selv": "16,000 RSD", "pay": "Pay selected",
        "ap": "Activity", "a1": "Tax return received", "a1d": "Tax Administration · yesterday, 14:20", "a2": "Payment recorded", "a2d": "Tax Administration · 5 days ago", "a3": "Registration confirmed", "a3d": "APR · 3 months ago",
        "mp": "Messages", "m1": "Tax Administration", "m1d": "Reminder: advance payment due", "m1t": "09:12", "m2": "APR", "m2d": "Annual statement: new form", "m2t": "yesterday",
        "hlp": "Need help?", "hlpd": "Chat with support or book a call",
    },
}


def portal_html(lang):
    t = STR[lang]
    def it(icon, label, on=False, extra=""):
        return f'<div class="it{" on" if on else ""}">{ic(icon)}{label}{extra}</div>'
    side = (f'<aside class="side"><div class="brand"><span class="logo">{ic("home")}</span><b>{t["brand"]}</b></div>'
            f'<div class="firm"><i>{t["me"]}</i><div><b>{t["firm"]}</b><small>{t["pib"]}</small></div>{ic("down")}</div>'
            + it("home", t["n_over"], True) + it("build", t["n_firm"])
            + it("file", t["n_reg"], False, f'<span class="own">{t["apr"]}</span>') + it("list", t["n_tax"], False, f'<span class="own">{t["pu"]}</span>')
            + it("card", t["n_pay"]) + it("doc", t["n_doc"]) + it("mail", t["n_msg"], False, '<span class="cnt">2</span>')
            + f'<div class="sp"></div><div class="grp">{t["g2"]}</div>' + it("help", t["n_help"]) + it("cog", t["n_set"]) + '</aside>')
    tabs = "".join(f'<span class="{"on" if i == 0 else ""}">{n}<em>{c}</em></span>' for i, (n, c) in enumerate(t["tabs"]))
    rows = ""
    for name, sub, ag, dl, dls, amt, st, k, act, sel in t["rows"]:
        cb = f'<span class="cb{" on" if sel else ""}">{ic("check") if sel else ""}</span>'
        due = f'<div class="due"><b>{dl}</b><small>{dls}</small></div>' if dl != "—" else "—"
        rows += (f'<tr><td style="width:34px">{cb}</td><td class="nm"><b>{name}</b><small>{sub}</small></td><td><span class="ag">{ag}</span></td>'
                 f'<td>{due}</td><td class="n"><b>{amt}</b></td><td><span class="st {k}">{st}</span></td><td class="act n">{act}</td></tr>')
    body = f"""
<div class="win"><div class="chrome"><i></i><i></i><i></i><div class="url">{ic('lock')}{t['url']}</div></div>
<div class="app" lang="{t['lang']}">{side}
<div class="main">
<div class="top"><div class="crumb">{t['crumb']}<span>/</span><b>{t['n_over']}</b></div><div class="find">{ic('search')}{t['find']}<kbd>⌘K</kbd></div>
<span class="lang"><i class="on">SR</i><i>EN</i></span><span class="ic">{ic('bell')}<u></u></span><span class="me"><i>{t['me']}</i></span></div>
<div class="body">
<div class="head"><div><h1>{t['h1']}</h1><p class="sub">{t['sub']}</p></div><div class="acts"><span class="b">{ic('file')}{t['b1']}</span><span class="b p">{ic('card')}{t['b2']}</span></div></div>
<div class="strip"><div><small>{t['s1']}</small><b>{t['s1v']}</b></div><div><small>{t['s2']}</small><b class="w">{t['s2v']}</b></div><div><small>{t['s3']}</small><b class="g">{t['s3v']}</b></div><div><small>{t['s4']}</small><b>{t['s4v']}</b></div></div>
<div class="cols">
<section class="panel"><div class="ph"><b>{t['pt']}</b><div class="tabs">{tabs}</div><span class="fl">{ic('list')}{t['sort']}</span></div>
<table><tr><th style="width:34px"></th><th>{t['c1']}</th><th>{t['c2']}</th><th>{t['c3']}</th><th class="n">{t['c4']}</th><th>{t['c5']}</th><th></th></tr>{rows}</table>
<div class="bar"><span class="cb on">{ic('check')}</span><span><b>2</b> {t['sel']}</span><b>{t['selv']}</b><span class="b p">{ic('card')}{t['pay']}</span></div></section>
<div class="right">
<section class="panel"><div class="ph"><b>{t['ap']}</b></div><ul class="tl">
<li><i>{ic('check')}</i><div><b>{t['a1']}</b><small>{t['a1d']}</small></div></li><li><i>{ic('check')}</i><div><b>{t['a2']}</b><small>{t['a2d']}</small></div></li><li><i>{ic('check')}</i><div><b>{t['a3']}</b><small>{t['a3d']}</small></div></li></ul></section>
<section class="panel"><div class="ph"><b>{t['mp']}</b></div><div class="msg"><div><i>PU</i><span><b>{t['m1']}</b><small>{t['m1d']}</small></span><em>{t['m1t']}</em></div><div><i>AP</i><span><b>{t['m2']}</b><small>{t['m2d']}</small></span><em>{t['m2t']}</em></div></div></section>
<section class="panel"><div class="help"><i>{ic('help')}</i><div><b>{t['hlp']}</b><small>{t['hlpd']}</small></div></div></section>
</div></div></div></div></div></div>"""
    return page(PORTAL_CSS, body, "linear-gradient(135deg,#E5E5EA 0%,#F2F2F5 60%,#FAFAFC 100%)")


# ------------------------------------------------------------------ today: two deliberately dated pages
OLD_CSS = """
.win{background:#fff}
.chrome{background:#E9E9E9}.url{background:#fff;color:#555}
.old{flex:1;min-height:0;overflow:hidden;font-family:Verdana,'DejaVu Sans',Geneva,sans-serif;font-size:12px;color:#000;position:relative}
.old a{color:#0000EE;text-decoration:underline}
.bevel{display:inline-block;background:#D4D0C8;border:2px outset #fff;border-right-color:#404040;border-bottom-color:#404040;padding:5px 14px;font:12px Arial,sans-serif;color:#000;text-align:center}
.blink{color:#FF0000;font-weight:bold}
"""

APR_OLD = """
<style>
.old{background:#C8D8F0 url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%224%22 height=%224%22><rect width=%224%22 height=%224%22 fill=%22%23C8D8F0%22/><rect width=%222%22 height=%222%22 fill=%22%23BCCDE8%22/></svg>')}
.wrap{width:1000px;margin:10px auto 0;background:#fff;border:2px solid #000080;height:662px;overflow:hidden}
.hd{background:linear-gradient(90deg,#000080,#1084D0);height:84px;display:flex;align-items:center;gap:16px;padding:0 16px;border-bottom:3px double #FFD700}
.hd .logo{width:56px;height:56px;border:2px solid #FFD700;background:#000080;color:#FFD700;font:bold 20px 'Times New Roman',serif;display:grid;place-items:center}
.hd h1{font:bold 25px 'Times New Roman',serif;color:#fff;letter-spacing:1px;text-shadow:2px 2px #000}
.hd small{display:block;font:italic 13px 'Times New Roman',serif;color:#FFD700}
.cols{display:flex}
.left{width:200px;background:#E8EEF8;border-right:1px solid #8899BB;padding:8px;min-height:572px}
.left h4{background:#000080;color:#fff;font:bold 11px Verdana;padding:3px 6px;margin:6px 0 4px}
.left ul{list-style:none}.left li{padding:3px 2px;border-bottom:1px dotted #99A}
.left li:before{content:'» ';color:#000080}
.cnt{margin-top:14px;text-align:center;font-size:10px}.cnt b{display:inline-block;background:#000;color:#0F0;font:bold 14px 'Courier New',monospace;padding:2px 6px;letter-spacing:2px}
.main{flex:1;padding:10px 14px}
.main h2{font:bold 18px 'Times New Roman',serif;color:#800000;border-bottom:2px solid #800000;padding-bottom:3px;margin-bottom:8px}
.main p{line-height:1.5;margin-bottom:8px}
.box{border:2px groove #888;background:#FFFFE0;padding:8px 10px;margin:10px 0}
.box h3{font:bold 13px Arial;color:#000080;margin-bottom:5px}.box li{margin:3px 0 3px 18px}
.right{width:200px;padding:8px;border-left:1px solid #8899BB;background:#F4F4F4}
.right h4{background:#800000;color:#fff;font:bold 11px Verdana;padding:3px 6px;margin-bottom:5px}
.right p{font-size:11px;margin-bottom:8px;border-bottom:1px dotted #999;padding-bottom:6px}
.ie{margin:8px 0;border:1px solid #000;background:#EEE;padding:6px;font-size:10px;text-align:center}
.mq{background:#000080;color:#FFFF00;font:bold 12px Verdana;padding:4px 8px;white-space:nowrap;overflow:hidden}
.ft{border-top:3px double #000080;margin-top:6px;padding:6px;text-align:center;font-size:10px;color:#444;background:#E8EEF8}
</style>
<div class="win"><div class="chrome"><i></i><i></i><i></i><div class="url">apr.gov.rs</div></div>
<div class="old"><div class="wrap">
<div class="hd"><div class="logo">АПР</div><div><h1>АГЕНЦИЈА ЗА ПРИВРЕДНЕ РЕГИСТРЕ</h1><small>Званични сајт &bull; Београд</small></div></div>
<div class="mq">&raquo;&raquo; Од 1. јуна е-услуге АПР-а доступне само преко еИД налога &laquo;&laquo; Добродошли &laquo;&laquo; Плаћање накнада платним картицама &laquo;&laquo;</div>
<div class="cols">
<div class="left"><h4>МЕНИ</h4><ul><li><a>Почетна</a></li><li><a>О нама</a></li><li><a>Регистри</a></li><li><a>Е-услуге</a></li><li><a>Претрага података</a></li><li><a>Накнаде</a></li><li><a>Прописи</a></li><li><a>Обрасци</a></li><li><a>Контакт</a></li></ul>
<h4 style="margin-top:14px">ЛИНКОВИ</h4><ul><li><a>еУправа</a></li><li><a>Пореска управа</a></li><li><a>Министарства</a></li></ul>
<div class="cnt">Посетилаца:<br><b>0001234567</b></div></div>
<div class="main"><h2>Добродошли на сајт АПР-а!</h2>
<p>Агенција за привредне регистре води регистре привредних субјеката. Преко портала можете електронски да региструјете предузетника, измените податке или се бришете из евиденције.</p>
<div class="box"><h3>Е-УСЛУГЕ <span class="blink">НОВО!</span></h3><ul><li><a>Регистрација предузетника</a></li><li><a>Промена података</a></li><li><a>Брисање из евиденције</a></li><li><a>Плаћање накнада платном картицом</a></li></ul></div>
<p style="text-align:center"><span class="bevel">&nbsp;Пријава (еИД налог)&nbsp;</span> &nbsp; <span class="bevel">Претрага регистра</span></p>
<p style="font-size:11px;color:#555">Напомена: за пореске пријаве користите посебан портал Пореске управе (одвојена пријава).</p></div>
<div class="right"><h4>НОВОСТИ</h4><p><b>12.11.</b> Обавештење о раду у празничним данима</p><p><b>05.11.</b> Нове накнаде за приступ подацима</p><p><b>29.10.</b> Упутство за е-регистрацију</p>
<div class="ie">Најбоље погледати у<br><b>Internet Explorer 6</b><br>на 1024x768</div><div class="ie" style="background:#FFD">Анкета: Како вам се свиђа сајт?<br><a>Гласајте</a></div></div>
</div>
<div class="ft">&copy; Агенција за привредне регистре &bull; Сва права задржана &bull; <a>Мапа сајта</a> &bull; <a>Помоћ</a></div>
</div></div></div>
"""

EPOREZI_OLD = """
<style>
.old{background:#DCE3EC}
.wrap{width:820px;margin:12px auto 0;background:#fff;border:2px solid #333;height:660px;overflow:hidden}
.hd{background:linear-gradient(180deg,#1E3F7A,#0C2150);height:74px;display:flex;align-items:center;gap:14px;padding:0 20px;border-bottom:4px solid #C0392B}
.hd b{font:bold 30px Arial,sans-serif;color:#fff;letter-spacing:1px}.hd small{color:#CDD8EE;font:12px Arial}
.body{padding:14px 26px}
.body h2{font:bold 19px Arial;color:#0C2150;margin-bottom:12px}
.btn3{display:block;width:100%;text-align:left;margin-bottom:9px;padding:10px 14px;background:#E6E6E6;border:2px outset #fff;border-right-color:#555;border-bottom-color:#555;font:13px Arial;color:#000}
.btn3 i{display:inline-block;width:18px;height:18px;margin-right:10px;background:#0C2150;vertical-align:middle;border-radius:2px}
.sec{border-top:1px solid #999;margin-top:10px;padding-top:8px}
.sec h3{font:bold 14px Arial;color:#0C2150;margin-bottom:6px}
.tb{width:100%;border-collapse:collapse;font:12px Arial}.tb td,.tb th{border:1px solid #888;padding:5px 8px;text-align:left}.tb th{background:#D9D9D9}
.term{background:#000;color:#C0C0C0;font:12px 'Courier New',monospace;padding:10px 12px;margin-top:8px;line-height:1.5}
.guides a{margin-right:18px}
.ft{background:#E6E6E6;border-top:1px solid #888;text-align:center;font:11px Arial;color:#444;padding:6px;margin-top:8px}
</style>
<div class="win"><div class="chrome"><i></i><i></i><i></i><div class="url">eporezi.purs.gov.rs</div></div>
<div class="old"><div class="wrap">
<div class="hd"><b>еПорези</b><small>Министарство финансија &bull; Пореска управа</small></div>
<div class="body"><h2>Добродошли на портал еПорези</h2>
<span class="btn3"><i></i>Пријава са еИД</span>
<span class="btn3"><i></i>Пријава квалификованим електронским сертификатом преко SmartBox-а</span>
<span class="btn3"><i></i>Пријава квалификованим електронским сертификатом преко апликације еПорези</span>
<div class="sec"><h3>Региструјте ваш еИД налог</h3><p>Налог креирате на порталу eid.gov.rs. Потребна је мобилна апликација ConsentID.</p></div>
<div class="sec"><h3>Преузимање програма</h3>
<table class="tb"><tr><th>Програм</th><th>Платформа</th></tr><tr><td><a>SmartBox</a></td><td>macOS, Windows, Ubuntu</td></tr><tr><td><a>Апликација еПорези</a></td><td>само Windows</td></tr></table>
<div class="term">$ sudo apt update<br>$ sudo apt install smartbox …<br># подржано: Ubuntu 22.04 и 24.04 (x64)</div></div>
<div class="sec guides"><h3>Корисничка упутства</h3><a>Пријава еИД (PDF)</a><a>SmartBox (PDF)</a><a>Апликација еПорези (PDF)</a></div>
</div><div class="ft">&copy; 2013&ndash;2026 &bull; Пореска управа &bull; Подршка: <a>контакт центар</a></div>
</div></div></div>
"""


def old_html(inner):
    return (f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&display=swap" rel="stylesheet">'
            f'<style>{FRAME_CSS}{OLD_CSS}</style></head><body style="background:transparent">{inner}</body></html>')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    def real(file, url):
        inner = (f'<div class="win"><div class="chrome"><i></i><i></i><i></i><div class="url">{url}</div></div>'
                 f'<div style="flex:1;min-height:0;overflow:hidden;position:relative"><img src="../../assets/shots/{file}" '
                 f'style="position:absolute;left:-1%;top:-1%;width:102%;display:block"></div></div>')
        return old_html(inner)
    jobs = {"portal-sr": portal_html("sr"), "portal-en": portal_html("en"),
            "old-apr": real("src-apr.webp", "apr.gov.rs"), "old-eporezi": real("src-eporezi.webp", "eporezi.purs.gov.rs")}
    for name, html in jobs.items():
        (TMP / f"{name}.html").write_text(html, encoding="utf-8")
    js = ROOT / "tools" / "render_shots.js"
    subprocess.run(["node", str(js), str(TMP), str(W), str(H), str(SCALE), "transparent"], check=True)
    for name in jobs:
        png = TMP / f"{name}.png"
        im = Image.open(png).convert("RGBA")
        im.save(OUT / f"{name}.webp", "WEBP", quality=90, method=6, alpha_quality=100)
        png.unlink()
        print(name, im.size, (OUT / f"{name}.webp").stat().st_size // 1024, "KB")


if __name__ == "__main__":
    sys.exit(main())
