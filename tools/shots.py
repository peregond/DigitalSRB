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
W, H, SCALE = 1440, 810, 1.5

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
    "trend": "M3 17l6-6 4 4 8-8M15 7h6v6",
}


def ic(n, cls=""):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="{ICON[n]}"/></svg>')


# ------------------------------------------------------------------ shared browser frame
FRAME_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1440px;height:810px;overflow:hidden}
body{font-family:'Manrope','Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased;position:relative}
.win{position:absolute;left:46px;top:34px;right:46px;bottom:46px;border-radius:20px;background:#fff;overflow:hidden;display:flex;flex-direction:column;
  box-shadow:0 40px 90px rgba(20,30,5,.28),0 6px 18px rgba(0,0,0,.14),0 0 0 1px rgba(0,0,0,.08)}
.chrome{height:48px;flex:none;display:flex;align-items:center;gap:9px;padding:0 18px}
.chrome i{width:12px;height:12px;border-radius:50%;display:block}
.chrome i:nth-child(1){background:#FF5F57}.chrome i:nth-child(2){background:#FEBC2E}.chrome i:nth-child(3){background:#28C840}
.url{flex:1;max-width:460px;margin:0 auto;transform:translateX(-30px);display:flex;align-items:center;justify-content:center;gap:7px;height:28px;border-radius:9px;font-size:13px;font-weight:600}
.url svg{width:12px;height:12px}
"""


def page(css, body, bg):
    return (f'<!doctype html><html><head><meta charset="utf-8"><link rel="preconnect" href="https://fonts.googleapis.com">'
            f'<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
            f'<style>{FRAME_CSS}{css}</style></head><body style="background:{bg}">{body}</body></html>')


# ------------------------------------------------------------------ the new portal
PORTAL_CSS = """
.win{background:#fff}
.chrome{background:#F5F5F7}.url{background:#E8E8ED;color:#6e6e73}
.pg{flex:1;min-height:0;padding:0 34px 18px;display:grid;grid-template-rows:auto auto 1fr auto;gap:14px;background:#fff;color:#1d1d1f}
.nav{display:flex;align-items:center;gap:18px;height:56px;border-bottom:1px solid #E8E8ED;margin:0 -34px;padding:0 34px}
.logo{width:32px;height:32px;border-radius:10px;background:#1d1d1f;color:#fff;display:grid;place-items:center}
.logo svg{width:18px;height:18px}
.nav b{font-size:17px;font-weight:700;letter-spacing:-.01em}
.tabs{display:flex;gap:4px;margin-left:14px}
.tabs span{padding:8px 14px;font-weight:500;font-size:14.5px;color:#6e6e73;border-radius:999px}
.tabs span.on{color:#1d1d1f;font-weight:700;background:#F5F5F7}
.srch{margin-left:auto;display:flex;align-items:center;gap:9px;background:#F5F5F7;border-radius:999px;padding:9px 16px;font-weight:500;font-size:14px;color:#6e6e73;min-width:230px}
.srch svg{width:16px;height:16px}
.lang{display:flex;background:#F5F5F7;border-radius:999px;padding:3px}
.lang i{font-style:normal;font-weight:700;font-size:12px;padding:6px 12px;border-radius:999px;color:#6e6e73}
.lang i.on{background:#fff;color:#1d1d1f;box-shadow:0 1px 4px rgba(0,0,0,.14)}
.bell{position:relative;width:36px;height:36px;border-radius:50%;background:#F5F5F7;display:grid;place-items:center;color:#1d1d1f}
.bell svg{width:18px;height:18px}.bell u{position:absolute;top:8px;right:9px;width:9px;height:9px;border-radius:50%;background:#0071E3;border:2px solid #F5F5F7}
.av{width:36px;height:36px;border-radius:50%;background:#1d1d1f;color:#fff;display:grid;place-items:center}.av svg{width:18px;height:18px}
.hero{display:flex;justify-content:space-between;align-items:flex-end;padding:4px 4px 0}
.hi{font-size:15px;font-weight:600;color:#6e6e73}
h1{font-size:52px;font-weight:800;letter-spacing:-.04em;line-height:1.04;display:flex;align-items:center;gap:14px}
.ex{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;background:#F5F5F7;color:#6e6e73;border-radius:7px;padding:4px 9px}
.pills{display:flex;gap:9px}
.pill{display:flex;align-items:center;gap:7px;font-weight:600;font-size:13.5px;padding:8px 15px;border-radius:999px;background:#F5F5F7;color:#1d1d1f}
.pill.b{color:#0066CC}
.pill svg{width:14px;height:14px;stroke-width:3;color:#30B454}.pill.b svg{color:#0066CC}
.grid{display:grid;grid-template-columns:1.2fr 1fr 1fr;grid-template-rows:1fr 1fr;gap:14px;min-height:0}
.card{background:#F5F5F7;border-radius:28px;padding:18px 22px;display:flex;flex-direction:column;gap:9px;min-height:0;overflow:hidden}
.k{display:flex;align-items:center;gap:9px;font-size:13px;font-weight:700;letter-spacing:0;color:#6e6e73}
.tag{margin-left:auto;font-size:11.5px;font-weight:700;padding:4px 11px;border-radius:999px;background:#fff;color:#1d1d1f;text-transform:none}
.big{grid-row:1/3;background:linear-gradient(160deg,#2a2a2d 0%,#111113 100%);color:#fff;padding:22px 26px;gap:10px}
.big .k{color:rgba(255,255,255,.65)}
.amt{font-size:72px;font-weight:800;letter-spacing:-.05em;line-height:1}.amt small{font-size:24px;font-weight:700;letter-spacing:0;color:rgba(255,255,255,.7);margin-left:6px}
.bar{display:flex;gap:5px;height:12px}.bar i{display:block;border-radius:6px;background:#fff}.bar i+i{background:#6e6e73}
.leg{display:flex;gap:22px;font-size:14px;font-weight:600;color:rgba(255,255,255,.85)}.leg span{display:flex;align-items:center;gap:7px}.leg u{width:10px;height:10px;border-radius:50%;background:#fff}.leg u.b{background:#6e6e73}
.due{display:grid;gap:8px;margin-top:2px}
.due div{display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.08);border-radius:18px;padding:10px 16px;font-weight:600;font-size:15px}
.due svg{width:18px;height:18px;color:rgba(255,255,255,.7)}.due span{flex:1}.due b{color:#fff;font-weight:700}
.btns{display:grid;gap:9px;margin-top:auto}
.btn{display:flex;align-items:center;justify-content:center;gap:9px;border-radius:999px;padding:13px;font-weight:700;font-size:15.5px}
.btn svg{width:18px;height:18px}
.btn.w{background:#fff;color:#1d1d1f}
.btn.g{background:rgba(255,255,255,.1);color:#fff}
.btn.s{padding:0;font-size:14.5px;align-self:flex-start;background:none;color:#0066CC;font-weight:600}
.btn.s svg{width:16px;height:16px}
.list{list-style:none;display:grid;gap:11px}
.list li{display:flex;align-items:center;gap:12px;font-weight:700;font-size:14.5px}
.list li>div{flex:1;display:grid;gap:1px}.list small{font-size:12.5px;color:#6e6e73;font-weight:500}
.dot{flex:none;width:28px;height:28px;border-radius:50%;display:grid;place-items:center;background:#30B454;color:#fff}.dot svg{width:15px;height:15px;stroke-width:3}
.dot.c{background:#fff;color:#1d1d1f}.dot.c svg{stroke-width:2}.dot.s{background:#1d1d1f;color:#fff}.dot.s svg{stroke-width:2}
.chart{display:flex;align-items:flex-end;gap:16px;height:100%;min-height:0;padding-top:4px}
.chart>div{flex:1;display:flex;flex-direction:column;align-items:center;gap:7px;justify-content:flex-end;height:100%}
.pair{display:flex;gap:5px;align-items:flex-end;height:100%;width:100%;justify-content:center}
.pair i{display:block;width:36%;border-radius:8px 8px 3px 3px;background:#C7C7CC}.pair i+i{background:#1d1d1f}
.chart span{font-size:12px;font-weight:600;color:#6e6e73}
.chartwrap{flex:1;min-height:0;display:flex;flex-direction:column;gap:8px}
.lg{display:flex;gap:16px;font-size:12.5px;font-weight:600;color:#6e6e73}.lg span{display:flex;align-items:center;gap:6px}.lg u{width:10px;height:10px;border-radius:3px;background:#C7C7CC}.lg u.b{background:#1d1d1f}
.notes{display:flex;gap:14px}
.note{flex:1;display:flex;align-items:center;gap:12px;background:#F5F5F7;border-radius:22px;padding:11px 16px;font-weight:700;font-size:14px}
.note small{display:block;font-size:12px;color:#6e6e73;font-weight:500}
.note>div{flex:1}
"""

STR = {
    "sr": {
        "lang": "sr-Latn", "portal": "Poreski portal", "tabs": ["Pregled", "Firma", "Registracija", "Porezi", "Izveštaji"],
        "search": "Pretraži usluge", "hi": "Dobar dan", "firm": "Moja firma", "ex": "primer",
        "p1": "Registrovana", "p2": "Prijave u redu", "p3": "Jedan nalog, eUprava",
        "pay": "Za plaćanje", "tax": "Porez", "contrib": "Doprinosi", "f1": "Prijava poreza", "f1d": "za 12 dana", "f2": "Doprinosi", "f2d": "za 26 dana",
        "payall": "Plati sve odjednom", "ips": "Plati preko IPS QR koda",
        "reg": "Registracija", "r1": "Podaci o firmi", "r1d": "Svi podaci su ažurni", "r2": "Poslednja izmena", "r2d": "pre 3 meseca", "chg": "Izmeni podatke",
        "fil": "Prijave i rokovi", "fl1": "Prijava poreza", "fl1d": "rok za 12 dana", "fl2": "Doprinosi", "fl2d": "rok za 26 dana", "file": "Podnesi prijavu",
        "inc": "Prihodi i porez", "months": ["jun", "jul", "avg", "sep", "okt", "nov"], "l1": "Prihodi", "l2": "Porez",
        "n1": "Poreska prijava primljena", "n1d": "Poreska uprava, juče", "n2": "Registracija potvrđena", "n2d": "APR, pre 3 meseca", "n3": "Uplata evidentirana", "n3d": "Poreska uprava, pre 5 dana",
        "foot": "Svaku uslugu i dalje pruža njena ustanova, a ti sve vidiš na jednom mestu.", "url": "portal.gov.rs",
    },
    "en": {
        "lang": "en", "portal": "Tax portal", "tabs": ["Overview", "Business", "Registration", "Taxes", "Reports"],
        "search": "Search services", "hi": "Good afternoon", "firm": "My business", "ex": "example",
        "p1": "Registered", "p2": "Filings in order", "p3": "One account, eUprava",
        "pay": "To pay", "tax": "Tax", "contrib": "Contributions", "f1": "Tax filing", "f1d": "in 12 days", "f2": "Contributions", "f2d": "in 26 days",
        "payall": "Pay everything at once", "ips": "Pay by IPS QR",
        "reg": "Registration", "r1": "Business data", "r1d": "Everything is up to date", "r2": "Last change", "r2d": "3 months ago", "chg": "Change data",
        "fil": "Filings and deadlines", "fl1": "Tax filing", "fl1d": "due in 12 days", "fl2": "Contributions", "fl2d": "due in 26 days", "file": "File a return",
        "inc": "Income and tax", "months": ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"], "l1": "Income", "l2": "Tax",
        "n1": "Tax return received", "n1d": "Tax Administration, yesterday", "n2": "Registration confirmed", "n2d": "APR, 3 months ago", "n3": "Payment recorded", "n3d": "Tax Administration, 5 days ago",
        "foot": "Each service is still provided by its own agency, and you see it all in one place.", "url": "portal.gov.rs",
    },
}


def portal_html(lang):
    t = STR[lang]
    tabs = "".join(f'<span class="{"on" if i == 0 else ""}">{x}</span>' for i, x in enumerate(t["tabs"]))
    heights = [(46, 20), (58, 26), (52, 22), (70, 30), (62, 27), (84, 36)]
    bars = "".join(f'<div><div class="pair"><i style="height:{a}%"></i><i style="height:{b * 1.7:.0f}%"></i></div><span>{m}</span></div>' for (a, b), m in zip(heights, t["months"]))
    body = f"""
<div class="win"><div class="chrome"><i></i><i></i><i></i><div class="url">{ic('lock')}{t['url']}</div></div>
<div class="pg" lang="{t['lang']}">
<div class="nav"><span class="logo">{ic('home')}</span><b>{t['portal']}</b><div class="tabs">{tabs}</div>
<span class="srch">{ic('search')}{t['search']}</span><span class="lang"><i class="on">SR</i><i>EN</i></span><span class="bell">{ic('bell')}<u></u></span><span class="av">{ic('user')}</span></div>
<div class="hero"><div><p class="hi">{t['hi']}</p><h1>{t['firm']} <span class="ex">{t['ex']}</span></h1></div>
<div class="pills"><span class="pill">{ic('check')}{t['p1']}</span><span class="pill">{ic('check')}{t['p2']}</span><span class="pill b">{ic('shield')}{t['p3']}</span></div></div>
<div class="grid">
<section class="card big"><p class="k">{t['pay']}</p><div class="amt">16.000<small>RSD</small></div>
<div class="bar"><i style="width:60%"></i><i style="width:40%"></i></div>
<div class="leg"><span><u></u>{t['tax']} 9.600</span><span><u class="b"></u>{t['contrib']} 6.400</span></div>
<div class="due"><div>{ic('cal')}<span>{t['f1']}</span><b>{t['f1d']}</b></div><div>{ic('cal')}<span>{t['f2']}</span><b>{t['f2d']}</b></div></div>
<div class="btns"><span class="btn w">{ic('card')}{t['payall']}</span><span class="btn g">{ic('qr')}{t['ips']}</span></div></section>
<section class="card"><p class="k">{t['reg']}<span class="tag">APR</span></p>
<ul class="list"><li><span class="dot">{ic('check')}</span><div>{t['r1']}<small>{t['r1d']}</small></div></li><li><span class="dot">{ic('check')}</span><div>{t['r2']}<small>{t['r2d']}</small></div></li></ul>
<span class="btn s">{ic('edit')}{t['chg']}</span></section>
<section class="card"><p class="k">{t['fil']}<span class="tag">{'Poreska' if lang == 'sr' else 'Tax Admin.'}</span></p>
<ul class="list"><li><span class="dot s">{ic('cal')}</span><div>{t['fl1']}<small>{t['fl1d']}</small></div></li><li><span class="dot c">{ic('cal')}</span><div>{t['fl2']}<small>{t['fl2d']}</small></div></li></ul>
<span class="btn s">{ic('file')}{t['file']}</span></section>
<section class="card" style="grid-column:2/4"><p class="k">{t['inc']}<span class="tag">{t['ex']}</span></p>
<div class="chartwrap"><div class="chart">{bars}</div><div class="lg"><span><u></u>{t['l1']}</span><span><u class="b"></u>{t['l2']}</span></div></div></section>
</div>
<div class="notes"><div class="note"><span class="dot">{ic('check')}</span><div>{t['n1']}<small>{t['n1d']}</small></div></div>
<div class="note"><span class="dot">{ic('check')}</span><div>{t['n2']}<small>{t['n2d']}</small></div></div>
<div class="note"><span class="dot">{ic('check')}</span><div>{t['n3']}<small>{t['n3d']}</small></div></div></div>
</div></div>"""
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
            f'<style>{FRAME_CSS}{OLD_CSS}</style></head><body style="background:linear-gradient(135deg,#D9DDE3,#EEF0F3)">{inner}</body></html>')


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
    subprocess.run(["node", str(js), str(TMP), str(W), str(H), str(SCALE)], check=True)
    for name in jobs:
        png = TMP / f"{name}.png"
        im = Image.open(png).convert("RGB")
        im.save(OUT / f"{name}.webp", "WEBP", quality=88, method=6)
        png.unlink()
        print(name, im.size, (OUT / f"{name}.webp").stat().st_size // 1024, "KB")


if __name__ == "__main__":
    sys.exit(main())
