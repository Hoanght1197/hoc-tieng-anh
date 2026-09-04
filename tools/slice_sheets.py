# -*- coding: utf-8 -*-
"""Cat bang 2x3 / 2x2 thanh tung hinh vuong 512px .webp, ten theo tu tieng Anh. Tu do khoang trang, pad vuong."""
import os, sys, json
from PIL import Image, ImageChops
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHEETS = os.path.join(ROOT, "img", "sheets")
OUT = os.path.join(ROOT, "img")
MAP = {
 "s01": ["dog","cat","cow","pig","duck","fish"],
 "s02": ["bird","elephant","lion","monkey","rabbit","frog"],
 "s03": ["apple","banana","orange","grapes","watermelon","strawberry"],
 "s04": ["pineapple","mango","pear","cherry","ball","book"],
 "s05": ["eye","nose","mouth","ear","hand","foot"],
 "s06": ["tooth","leg","tongue","arm","hat","shoes"],
 "s07": ["mommy","daddy","baby","grandma","grandpa","sister"],
 "s08": ["brother","car","bus","bike","train","plane"],
 "s09": ["boat","truck","rocket","motorbike","bed","chair"],
 "s10": ["clock","umbrella","bag","teddy_bear"],
}
SIZE = 512

def autocrop(im, pad_ratio=0.08):
    """Cat sat vien noi dung (nen trang), roi pad thanh hinh vuong nen trang."""
    rgb = im.convert("RGB")
    bg = Image.new("RGB", rgb.size, (255, 255, 255))
    diff = ImageChops.difference(rgb, bg).convert("L").point(lambda p: 255 if p > 28 else 0)
    box = diff.getbbox()
    if box:
        # bo qua duong ke luoi sat mep: thu hep bbox neu no cham mep
        rgb = rgb.crop(box)
    w, h = rgb.size
    side = int(max(w, h) * (1 + pad_ratio * 2))
    sq = Image.new("RGB", (side, side), (255, 255, 255))
    sq.paste(rgb, ((side - w) // 2, (side - h) // 2))
    return sq.resize((SIZE, SIZE), Image.LANCZOS)

def slice_one(name, words):
    path = os.path.join(SHEETS, name + ".png")
    if not os.path.exists(path):
        print("thieu", name); return
    im = Image.open(path).convert("RGB")
    W, H = im.size
    cols, rows = (2, 3) if len(words) == 6 else (2, 2)
    cw, ch = W / cols, H / rows
    inset = 0.045  # bo mep de tranh duong ke luoi
    for i, w in enumerate(words):
        r, c = divmod(i, cols)
        box = (int(c * cw + cw * inset), int(r * ch + ch * inset), int((c + 1) * cw - cw * inset), int((r + 1) * ch - ch * inset))
        cell = autocrop(im.crop(box))
        out = os.path.join(OUT, w + ".webp")
        cell.save(out, "WEBP", quality=86)
        print("ok", out)

only = sys.argv[1:] or list(MAP)
for n in only:
    slice_one(n, MAP[n])
