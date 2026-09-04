# -*- coding: utf-8 -*-
"""Gen bang minh hoa 2x3 qua pool ChatGPT (gpt_gen_safe.run_jobs). Moi bang 6 hinh, cat sau bang slice_sheets.py"""
import sys, os
sys.path.insert(0, r"F:\DESIGN\scripts"); sys.path.insert(0, r"F:\KIT MKT\scripts")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from gpt_gen_safe import run_jobs
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "img", "sheets")

SHEETS = {
 "s01": ["a dog", "a cat", "a cow", "a pig", "a duck", "a fish"],
 "s02": ["a small bird", "an elephant", "a lion", "a monkey", "a rabbit", "a frog"],
 "s03": ["a red apple", "a banana", "an orange", "a bunch of purple grapes", "a slice of watermelon", "a strawberry"],
 "s04": ["a pineapple", "a mango", "a pear", "two cherries", "a soccer ball", "an open book"],
 "s05": ["one human eye", "a human nose", "a smiling human mouth with lips", "a human ear", "an open human hand palm", "a bare human foot"],
 "s06": ["a single white tooth", "a human leg", "a tongue sticking out of a mouth", "a human arm", "a hat", "a pair of sneaker shoes"],
 "s07": ["a mommy (young woman with a warm smile)", "a daddy (young man with a warm smile)", "a baby in a onesie", "a grandma with gray hair and glasses", "a grandpa with gray hair and a beard", "a little girl (sister)"],
 "s08": ["a little boy (brother)", "a red car", "a yellow school bus", "a bicycle", "a train", "an airplane"],
 "s09": ["a sailboat", "a truck", "a rocket", "a motorbike", "a bed with pillow and blanket", "a wooden chair"],
 "s10": ["an alarm clock", "an open umbrella", "a school backpack", "a teddy bear"],
}

def prompt(items):
    n = len(items)
    if n == 6:
        layout = "a portrait image with a clean grid of 6 equal square cells: 2 columns and 3 rows"
    else:
        layout = "a square image with a clean grid of 4 equal square cells: 2 columns and 2 rows"
    order = ", ".join(f"{i+1}. {it}" for i, it in enumerate(items))
    return (f"Create {layout}, separated by thin light gray lines. Every cell has a plain pure white background. "
            "In each cell draw exactly ONE subject, centered, large, fully visible inside the cell, in a cute, simple, friendly "
            "children's picture-book illustration style: bold clean outlines, soft flat colors, gentle shading, no background scenery, "
            "easy for a 4-year-old child to recognize. Absolutely no text, no letters, no numbers, no labels, no watermark. "
            f"Order of the cells reading left to right, then top to bottom: {order}.")

jobs = []
for name, items in SHEETS.items():
    out = os.path.join(OUT, name + ".png")
    if os.path.exists(out) and os.path.getsize(out) > 50000:
        continue
    jobs.append((name, prompt(items), out))
print("Jobs:", [j[0] for j in jobs])
if jobs:
    run_jobs(jobs, concurrency=5)
