# -*- coding: utf-8 -*-
"""Cắt bảng 2x3 / 2x2 thành từng hình vuông .webp NỀN TRẮNG (không tách nền).
Các khung trong app đều nền sáng nên hình nền trắng hòa liền, tránh lỗi tách nền."""
import os, sys
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

def square_white(rgb, pad=0.07):
    bg = Image.new("RGB", rgb.size, (255, 255, 255))
    diff = ImageChops.difference(rgb, bg).convert("L").point(lambda p: 255 if p > 18 else 0)
    box = diff.getbbox()
    if box:
        rgb = rgb.crop(box)
    w, h = rgb.size
    side = int(max(w, h) * (1 + pad * 2))
    sq = Image.new("RGB", (side, side), (255, 255, 255))
    sq.paste(rgb, ((side - w) // 2, (side - h) // 2))
    return sq.resize((SIZE, SIZE), Image.LANCZOS)

def save_single(src, name):
    """1 ảnh riêng (vd hand_new) -> img/<name>.webp nền trắng."""
    im = Image.open(src).convert("RGB")
    square_white(im).save(os.path.join(OUT, name + ".webp"), "WEBP", quality=90)
    print("ok(single)", name)

def slice_one(name, words):
    path = os.path.join(SHEETS, name + ".png")
    if not os.path.exists(path):
        print("thieu", name); return
    im = Image.open(path).convert("RGB")
    W, H = im.size
    cols, rows = (2, 3) if len(words) == 6 else (2, 2)
    cw, ch = W / cols, H / rows
    inset = 0.045
    for i, w in enumerate(words):
        r, c = divmod(i, cols)
        box = (int(c*cw + cw*inset), int(r*ch + ch*inset), int((c+1)*cw - cw*inset), int((r+1)*ch - ch*inset))
        square_white(im.crop(box)).save(os.path.join(OUT, w + ".webp"), "WEBP", quality=90)
        print("ok", w)

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "single":   # python slice_sheets.py single <src.png> <name>
        save_single(args[1], args[2])
    else:
        for n in (args or list(MAP)):
            slice_one(n, MAP[n])
