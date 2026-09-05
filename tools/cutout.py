# -*- coding: utf-8 -*-
"""Tách nền trắng CHỈ vùng nối với mép ảnh (flood fill) -> img/cut/<key>.webp có alpha.
Vùng trắng bên trong (răng, mắt, áo) giữ nguyên vì không nối ra mép. Dùng cho chế độ Khám phá."""
import os, sys, glob
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "img"); OUT = os.path.join(ROOT, "img", "cut")
os.makedirs(OUT, exist_ok=True)

def cut(path, name):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    mn = a.min(axis=2); mx = a.max(axis=2)
    whiteish = (mn > 232) & ((mx - mn) < 14)          # gần trắng, trung tính
    lab, n = ndimage.label(whiteish)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    border.discard(0)
    bg = np.isin(lab, list(border))
    # nới nhẹ vùng nền vào 1px để bỏ viền trắng mờ quanh vật
    bg = ndimage.binary_dilation(bg, iterations=1)
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    al = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(0.8))
    rgba = im.convert("RGBA"); rgba.putalpha(al)
    # crop sát vật + pad
    box = al.point(lambda p: 255 if p > 8 else 0).getbbox()
    if box:
        pad = 6
        box = (max(0, box[0]-pad), max(0, box[1]-pad), min(im.width, box[2]+pad), min(im.height, box[3]+pad))
        rgba = rgba.crop(box)
    rgba.save(os.path.join(OUT, name + ".webp"), "WEBP", quality=88)
    return rgba.size

if __name__ == "__main__":
    names = sys.argv[1:] or [os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(SRC, "*.webp"))]
    for n in names:
        print(n, cut(os.path.join(SRC, n + ".webp"), n))
