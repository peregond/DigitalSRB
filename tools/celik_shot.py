#!/usr/bin/env python3
"""Composes the Super Čelik picture for the home page card: Mac window behind, an Android phone and an iPhone in front,
bleeding off the bottom. Sources are the product's own screenshots in tools/src-celik/. Output: assets/ideas/celik.webp.

Run:  python3 tools/celik_shot.py   (needs node + playwright and Pillow)
"""
import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "src-celik"
TMP = ROOT / "tools" / "shots"
W, H = 2400, 880

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:transparent}}
.mac{{position:absolute;left:520px;top:70px;width:1360px;border-radius:26px;overflow:hidden;box-shadow:0 40px 100px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.08)}}
.mac img{{display:block;width:100%}}
.ph{{position:absolute;border-radius:70px 70px 0 0;background:#0b0b0d;padding:14px 14px 0;box-shadow:0 40px 100px rgba(0,0,0,.6),inset 0 0 0 2px #3a3a40}}
.ph img{{display:block;width:100%;border-radius:58px 58px 0 0}}
.a{{left:250px;top:250px;width:560px}}
.i{{left:1590px;top:200px;width:560px}}
</style></head><body>
<div class="mac"><img src="{(SRC / 'mac.png').as_uri()}"></div>
<div class="ph a"><img src="{(SRC / 'android.png').as_uri()}"></div>
<div class="ph i"><img src="{(SRC / 'iphone.png').as_uri()}"></div>
</body></html>"""

TMP.mkdir(parents=True, exist_ok=True)
(TMP / "celik.html").write_text(HTML, encoding="utf-8")
for old in TMP.glob("*.html"):
    if old.name != "celik.html":
        old.rename(old.with_suffix(".html.bak"))
try:
    subprocess.run(["node", str(ROOT / "tools" / "render_shots.js"), str(TMP), str(W), str(H), "1", "transparent"], check=True)
finally:
    for bak in TMP.glob("*.html.bak"):
        bak.rename(bak.with_suffix(""))
im = Image.open(TMP / "celik.png").convert("RGBA")
im.save(ROOT / "assets" / "ideas" / "celik.webp", "WEBP", quality=88, method=6, alpha_quality=100)
print(im.size)
