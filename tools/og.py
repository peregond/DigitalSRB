#!/usr/bin/env python3
"""Renders the link-preview images (1200 x 630) for the home page and every detail page to assets/og/*.jpg.

Run:  python3 tools/og.py   (needs node + playwright and Pillow; the images are committed)
"""
import html
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402
from pages_data import THEMES  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TMP = ROOT / "tools" / "og_tmp"
OUT = ROOT / "assets" / "og"

CSS = """
*{box-sizing:border-box;margin:0;padding:0}html,body{width:1200px;height:630px;overflow:hidden}
body{font-family:'Manrope',system-ui,sans-serif;color:#fff;position:relative}
.top{position:absolute;left:64px;top:44px;display:flex;align-items:center;gap:14px;padding:13px 26px 13px 18px;border-radius:999px;background:#fff;color:#111;box-shadow:0 10px 30px rgba(0,0,0,.22);font-family:'Unbounded',sans-serif;font-weight:700;font-size:26px}
.top i{display:block;width:28px;height:20px;border-radius:4px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.18);background:linear-gradient(#C6363C 0 33.3%,#0C4076 33.3% 66.6%,#fff 66.6%)}
.txt{position:absolute;left:64px;top:150px;width:560px}
h1{font-family:'Unbounded',sans-serif;font-weight:800;letter-spacing:-.03em;line-height:1.08}
p{font-size:28px;font-weight:600;line-height:1.3;margin-top:22px;opacity:.92}
.art{position:absolute;right:56px;top:96px;width:520px;height:390px;border-radius:36px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.35)}
.art img{width:100%;height:100%;display:block}
.three{position:absolute;right:48px;top:80px;width:540px;height:470px}
.three div{position:absolute;width:330px;height:248px;border-radius:30px;overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.35)}
.three img{width:100%;height:100%;display:block}
"""


def page(bg, title, tag, size, art_html):
    return (f'<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700&'
            f'family=Unbounded:wght@700;800&display=swap" rel="stylesheet"><style>{CSS}</style></head><body style="background:{bg}">'
            f'<div class="top"><i></i>Digitalna Srbija</div>'
            f'<div class="txt"><h1 style="font-size:{size}px">{html.escape(title)}</h1><p>{html.escape(tag)}</p></div>'
            f'{art_html}</body></html>')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    _, ideas, toc, _, _ = build.parse()
    taglines = {47: "Lična karta i boravak u novčaniku na telefonu.", 53: "Zamena strane vozačke dozvole bez nagađanja."}
    taglines.update({n: sr for n, sr, en in build.FEATURED})
    jobs = {}
    three = "".join(f'<div style="right:{r}px;top:{t}px"><img src="../../assets/featured/{n:02d}.svg"></div>' for n, r, t in ((9, 0, 0), (1, 120, 110), (22, 30, 220)))
    jobs["home"] = page("linear-gradient(135deg,#E30613 0%,#9d0410 100%)", "60 ideja protiv birokratije i korupcije", "Za građane i strance.", 54, f'<div class="three">{three}</div>')
    for n, (slug, th, dk) in THEMES.items():
        title = re.sub(r"\s*\(.*?\)\s*$", "", re.sub(r"</?strong>", "", toc["sr"][n]))
        size = 56 if len(title) < 32 else 46
        jobs[slug] = page(f"linear-gradient(135deg,{dk} 0%,{th} 160%)", title, taglines.get(n, ""), size,
                          f'<div class="art"><img src="../../assets/featured/{n:02d}.svg"></div>')
    for name, h in jobs.items():
        (TMP / f"{name}.html").write_text(h, encoding="utf-8")
    subprocess.run(["node", str(ROOT / "tools" / "render_shots.js"), str(TMP), "1200", "630", "1"], check=True)
    for name in jobs:
        png = TMP / f"{name}.png"
        Image.open(png).convert("RGB").save(OUT / f"{name}.jpg", "JPEG", quality=86, optimize=True)
        png.unlink()
    print(len(jobs), "images in", OUT)


if __name__ == "__main__":
    main()
