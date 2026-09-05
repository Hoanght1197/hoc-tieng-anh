# -*- coding: utf-8 -*-
"""img/scenes/*.png (gen) -> img/scenes/*.webp 768px rộng, nhẹ cho app."""
import os, glob, sys
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img", "scenes")
for p in glob.glob(os.path.join(D, "*.png")):
    im = Image.open(p).convert("RGB"); w = 768; im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    out = p[:-4] + ".webp"; im.save(out, "WEBP", quality=80); print(os.path.basename(out), os.path.getsize(out) // 1024, "KB")
