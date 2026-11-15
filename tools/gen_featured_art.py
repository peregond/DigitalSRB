#!/usr/bin/env python3
"""Generates the 8 featured-card illustrations as flat vector SVG (400x300, no text)."""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "featured"
INK = "#111"
GREY = "#D9D5CF"
GREEN, AMBER, RED = "#12A150", "#F2A100", "#E30613"
TINT = {GREEN: "#DDF2E6", AMBER: "#FCEBC4", RED: "#FADADC"}


def wrap(c, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="1200" height="900" role="img" aria-hidden="true">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{TINT[c]}"/><stop offset="1" stop-color="#fff"/></linearGradient>
<filter id="s" x="-25%" y="-25%" width="150%" height="160%"><feDropShadow dx="0" dy="7" stdDeviation="8" flood-color="#111" flood-opacity=".15"/></filter>
</defs>
<style>
.fl{{animation:fl 5s ease-in-out infinite}}.fl2{{animation:fl 6.5s ease-in-out -2s infinite}}
.da{{stroke-dasharray:7 9;animation:da 1.2s linear infinite}}
.pu{{animation:pu 2.6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
.wv{{animation:wv 2.4s ease-in-out infinite}}.wv2{{animation:wv 2.4s ease-in-out .4s infinite}}.wv3{{animation:wv 2.4s ease-in-out .8s infinite}}
.sw{{animation:sw 6s ease-in-out infinite;transform-origin:200px 76px}}
.ch{{animation:ch 2s ease-in-out infinite}}.ch2{{animation:ch 2s ease-in-out .3s infinite}}.ch3{{animation:ch 2s ease-in-out .6s infinite}}
@keyframes fl{{50%{{transform:translateY(-6px)}}}}
@keyframes da{{to{{stroke-dashoffset:-16}}}}
@keyframes pu{{50%{{transform:scale(1.18);opacity:.55}}}}
@keyframes wv{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
@keyframes sw{{0%,100%{{transform:rotate(-3deg)}}50%{{transform:rotate(3deg)}}}}
@keyframes ch{{0%,100%{{opacity:.3}}50%{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<rect width="400" height="300" fill="url(#bg)"/>
<circle cx="350" cy="30" r="70" fill="{c}" opacity=".08"/><circle cx="30" cy="285" r="80" fill="{c}" opacity=".08"/>
{body}
</svg>
'''


def qr(x, y, size, fill=INK):
    u = size / 7
    out = []
    for fx, fy in ((0, 0), (4, 0), (0, 4)):
        out.append(f'<rect x="{x+fx*u:.1f}" y="{y+fy*u:.1f}" width="{3*u:.1f}" height="{3*u:.1f}" rx="{u*.5:.1f}" fill="none" stroke="{fill}" stroke-width="{u*.6:.1f}"/>')
        out.append(f'<rect x="{x+(fx+1)*u:.1f}" y="{y+(fy+1)*u:.1f}" width="{u:.1f}" height="{u:.1f}" fill="{fill}"/>')
    for cx, cy in ((4, 4), (5, 4), (6, 5), (4, 6), (6, 6), (5, 5), (3, 3), (3, 5), (3, 1), (1, 3)):
        out.append(f'<rect x="{x+cx*u:.1f}" y="{y+cy*u:.1f}" width="{u*.9:.1f}" height="{u*.9:.1f}" fill="{fill}"/>')
    return "".join(out)


def check(cx, cy, r, c, w=None):
    w = w or r * .28
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}"/>'
            f'<path d="M{cx-r*.42:.1f} {cy+r*.02:.1f}l{r*.28:.1f} {r*.3:.1f} {r*.56:.1f}-{r*.6:.1f}" fill="none" stroke="#fff" stroke-width="{w:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')


def cyl(cx, cy, w, h, c):
    rx, ry = w / 2, h * .16
    return (f'<g filter="url(#s)"><path d="M{cx-rx} {cy-h/2+ry}v{h-2*ry}a{rx} {ry} 0 0 0 {w} 0v-{h-2*ry}z" fill="{c}"/>'
            f'<ellipse cx="{cx}" cy="{cy-h/2+ry}" rx="{rx}" ry="{ry}" fill="#fff" stroke="{c}" stroke-width="4"/>'
            f'<path d="M{cx-rx} {cy}a{rx} {ry} 0 0 0 {w} 0" fill="none" stroke="#fff" stroke-width="3" opacity=".7"/></g>')


ART = {}

# 01 one QR code for every counter
ART[1] = (GREEN, f'''
<g class="fl"><rect x="58" y="58" width="100" height="184" rx="20" fill="#fff" stroke="{INK}" stroke-width="5" filter="url(#s)"/>
<rect x="92" y="68" width="32" height="6" rx="3" fill="{INK}"/>{qr(78,96,60)}
<rect x="78" y="176" width="60" height="8" rx="4" fill="{GREY}"/><rect x="88" y="194" width="40" height="8" rx="4" fill="{GREY}"/></g>
<path class="da" d="M170 150H212" stroke="{GREEN}" stroke-width="5" stroke-linecap="round"/>
<path d="M206 138l14 12-14 12" fill="none" stroke="{GREEN}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
<g class="fl2"><rect x="228" y="88" width="136" height="104" rx="12" fill="#fff" stroke="{INK}" stroke-width="5" filter="url(#s)"/>
<rect x="284" y="192" width="24" height="16" fill="{INK}"/><rect x="262" y="206" width="68" height="8" rx="4" fill="{INK}"/>
{check(250,114,10,GREEN)}<rect x="268" y="110" width="76" height="8" rx="4" fill="{GREY}"/>
{check(250,140,10,GREEN)}<rect x="268" y="136" width="58" height="8" rx="4" fill="{GREY}"/>
<circle cx="250" cy="166" r="8" fill="none" stroke="{GREEN}" stroke-width="3.5" stroke-dasharray="4 4"/><rect x="268" y="162" width="68" height="8" rx="4" fill="{GREY}"/></g>
''')

# 22 open and close a business in one day
ART[22] = (GREEN, f'''
<g class="fl"><rect x="96" y="58" width="208" height="186" rx="22" fill="#fff" filter="url(#s)"/>
<path d="M96 80a22 22 0 0 1 22-22h164a22 22 0 0 1 22 22v24H96z" fill="{GREEN}"/>
<rect x="128" y="44" width="9" height="26" rx="4.5" fill="{INK}"/><rect x="263" y="44" width="9" height="26" rx="4.5" fill="{INK}"/>
{"".join(f'<circle cx="{132+i*34}" cy="{130+j*34}" r="5" fill="{GREY}"/>' for j in range(3) for i in range(5) if (i, j) != (2, 1))}
<circle class="pu" cx="200" cy="164" r="17" fill="{GREEN}" opacity=".2"/>{check(200,164,14,GREEN)}</g>
<g class="fl2"><circle cx="300" cy="226" r="32" fill="{INK}" filter="url(#s)"/>
<circle cx="300" cy="226" r="17" fill="none" stroke="#fff" stroke-width="5"/><path d="M300 215v22M293 222h10a4 4 0 0 1 0 8h-8" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/></g>
''')

# 30 never ask for papers the state already has
ART[30] = (AMBER, f'''
{cyl(100,84,66,62,AMBER)}{cyl(200,84,66,62,AMBER)}{cyl(300,84,66,62,AMBER)}
<path class="da" d="M100 122Q100 150 200 150M200 122V150M300 122Q300 150 200 150" fill="none" stroke="{AMBER}" stroke-width="4.5" stroke-linecap="round"/>
<g class="fl"><g transform="rotate(-7 200 205)"><rect x="152" y="150" width="96" height="80" rx="8" fill="#fff" stroke="{GREY}" stroke-width="3" filter="url(#s)"/></g>
<g transform="rotate(5 200 205)"><rect x="152" y="152" width="96" height="80" rx="8" fill="#fff" stroke="{GREY}" stroke-width="3"/></g>
<rect x="152" y="156" width="96" height="80" rx="8" fill="#fff" stroke="{INK}" stroke-width="4" filter="url(#s)"/>
<rect x="168" y="174" width="50" height="8" rx="4" fill="{INK}"/><rect x="168" y="194" width="64" height="7" rx="3.5" fill="{GREY}"/><rect x="168" y="210" width="44" height="7" rx="3.5" fill="{GREY}"/>
<circle cx="250" cy="226" r="28" fill="#fff" stroke="{RED}" stroke-width="7"/><path d="M230 246L270 206" stroke="{RED}" stroke-width="7" stroke-linecap="round"/></g>
''')

# 21 parcel with one QR code, customs within one working day
ART[21] = (GREEN, f'''
<g class="fl"><path d="M70 122l22-34h186l22 34z" fill="#D9A55F"/>
<rect x="76" y="122" width="248" height="124" rx="10" fill="#EBC48A" filter="url(#s)"/>
<rect x="182" y="88" width="36" height="158" fill="#fff" opacity=".55"/>
<rect x="96" y="150" width="58" height="8" rx="4" fill="#B9854A" opacity=".6"/><rect x="96" y="168" width="40" height="8" rx="4" fill="#B9854A" opacity=".6"/>
<rect x="232" y="150" width="76" height="76" rx="8" fill="#fff"/>{qr(242,160,56)}</g>
<g class="fl2"><circle cx="318" cy="70" r="42" fill="#fff" stroke="{GREEN}" stroke-width="7" filter="url(#s)"/>
<path d="M318 70V46M318 70l16 10" stroke="{INK}" stroke-width="6" stroke-linecap="round" fill="none"/><circle cx="318" cy="70" r="4" fill="{INK}"/></g>
{check(352,112,15,GREEN)}
<path class="da" d="M24 160h34M14 186h44M30 212h28" stroke="{GREEN}" stroke-width="5" stroke-linecap="round"/>
''')

# 47 ID and residence card in the phone wallet
ART[47] = (RED, f'''
<g class="fl"><rect x="124" y="36" width="152" height="228" rx="28" fill="#fff" stroke="{INK}" stroke-width="6" filter="url(#s)"/>
<rect x="176" y="48" width="48" height="8" rx="4" fill="{INK}"/>
<rect x="144" y="82" width="112" height="22" rx="9" fill="{INK}"/>
<rect x="140" y="94" width="120" height="76" rx="12" fill="{RED}"/>
<circle cx="166" cy="124" r="11" fill="#fff" opacity=".92"/><path d="M148 154a18 15 0 0 1 36 0z" fill="#fff" opacity=".92"/>
<rect x="196" y="112" width="52" height="7" rx="3.5" fill="#fff" opacity=".9"/><rect x="196" y="128" width="38" height="7" rx="3.5" fill="#fff" opacity=".7"/><rect x="196" y="144" width="46" height="7" rx="3.5" fill="#fff" opacity=".7"/>
<rect x="144" y="188" width="112" height="22" rx="11" fill="{TINT[RED]}"/>{check(158,199,8,GREEN)}<rect x="172" y="195" width="60" height="8" rx="4" fill="#fff"/>
<rect x="144" y="218" width="112" height="22" rx="11" fill="{TINT[RED]}"/>{check(158,229,8,GREEN)}<rect x="172" y="225" width="44" height="8" rx="4" fill="#fff"/></g>
<g fill="none" stroke="{RED}" stroke-width="6" stroke-linecap="round"><path class="wv" d="M296 126a30 30 0 0 1 0 48"/><path class="wv2" d="M312 108a54 54 0 0 1 0 84"/><path class="wv3" d="M328 90a78 78 0 0 1 0 120"/></g>
{check(104,222,20,INK)}
''')

# 48 abolish registration of stay for foreigners
ART[48] = (RED, f'''
<g class="fl"><rect x="112" y="46" width="176" height="208" rx="16" fill="#fff" filter="url(#s)"/>
<rect x="134" y="70" width="84" height="11" rx="5.5" fill="{INK}"/>
{"".join(f'<rect x="134" y="{104+i*26}" width="132" height="8" rx="4" fill="{GREY}"/>' for i in range(3))}
<rect x="134" y="184" width="62" height="44" rx="8" fill="none" stroke="{GREY}" stroke-width="3" stroke-dasharray="6 6"/>
<rect x="214" y="190" width="52" height="8" rx="4" fill="{GREY}"/><rect x="214" y="208" width="36" height="8" rx="4" fill="{GREY}"/></g>
<g class="fl2"><circle cx="300" cy="212" r="50" fill="{RED}" filter="url(#s)"/>
<path d="M278 190l44 44M322 190l-44 44" stroke="#fff" stroke-width="12" stroke-linecap="round"/></g>
<g class="fl2"><circle cx="86" cy="220" r="36" fill="#fff" stroke="{INK}" stroke-width="5" filter="url(#s)"/>
<path d="M86 220V196M86 220l16 10" stroke="{INK}" stroke-width="5" stroke-linecap="round" fill="none"/>
<path d="M58 248L114 192" stroke="{RED}" stroke-width="7" stroke-linecap="round"/></g>
''')

# 50 legal fast track: three official speeds, fee goes to the budget
def chev(x, y, n, col, cls):
    return "".join(f'<path class="{cls[i]}" d="M{x+i*16} {y-9}l10 9-10 9" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>' for i in range(n))

def coins(x, y, n):
    out = []
    for i in range(n):
        cx = x + i * 32
        out.append(f'<circle cx="{cx}" cy="{y}" r="17" fill="#fff" stroke="{INK}" stroke-width="4"/><circle cx="{cx}" cy="{y}" r="8" fill="none" stroke="{INK}" stroke-width="3"/>')
    return "".join(out)

ART[50] = (RED, f'''
<g class="fl"><rect x="46" y="62" width="104" height="38" rx="19" fill="{GREY}"/>{chev(100,81,1,INK,["ch"])}
<rect x="46" y="130" width="164" height="38" rx="19" fill="#F4A3A8"/>{chev(150,149,2,"#fff",["ch","ch2"])}
<rect x="46" y="198" width="224" height="38" rx="19" fill="{RED}"/>{chev(196,217,3,"#fff",["ch","ch2","ch3"])}</g>
<g class="fl2">{coins(184,81,1)}{coins(240,149,2)}{coins(296,217,3)}</g>
''')

# 53 a digital court
ART[53] = (RED, f'''
<g class="fl2"><rect x="36" y="210" width="96" height="66" rx="9" fill="#fff" stroke="{INK}" stroke-width="4.5" filter="url(#s)"/>
<rect x="36" y="210" width="96" height="16" rx="9" fill="{INK}"/><rect x="48" y="238" width="56" height="7" rx="3.5" fill="{GREY}"/><rect x="48" y="254" width="72" height="7" rx="3.5" fill="{GREY}"/></g>
<rect x="196" y="76" width="8" height="136" fill="{INK}"/><rect x="156" y="208" width="88" height="16" rx="8" fill="{INK}"/><circle cx="200" cy="76" r="9" fill="{RED}"/>
<g class="sw"><rect x="98" y="72" width="204" height="8" rx="4" fill="{INK}"/>
<path d="M104 76L78 150M104 76L130 150M296 76L270 150M296 76L322 150" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
<path d="M70 150h68a34 30 0 0 1-68 0z" fill="{RED}"/><path d="M262 150h68a34 30 0 0 1-68 0z" fill="{RED}"/></g>
<g fill="#fff" stroke="{INK}" stroke-width="3.5" filter="url(#s)" class="fl"><rect x="278" y="232" width="80" height="14" rx="4"/><rect x="284" y="248" width="68" height="14" rx="4"/><rect x="272" y="264" width="92" height="14" rx="4"/></g>
''')

OUT.mkdir(parents=True, exist_ok=True)
for n, (c, body) in ART.items():
    (OUT / f"{n:02d}.svg").write_text(wrap(c, body), encoding="utf-8")
    print(f"{n:02d}.svg", len(wrap(c, body)) // 1024 or 1, "KB")
