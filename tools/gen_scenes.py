# -*- coding: utf-8 -*-
"""Gen nền cảnh (không nhân vật) cho chế độ Khám phá, cùng phong cách đất sét."""
import sys, os
sys.path.insert(0, r"F:\DESIGN\scripts"); sys.path.insert(0, r"F:\KIT MKT\scripts")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from gpt_gen_safe import run_jobs
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "img", "scenes")
SCENES = {
 "farm": "a sunny farm meadow: green rolling hills, a small red barn on the left, a wooden fence, a little blue pond at the bottom right, a big tree, fluffy clouds and a smiling sun in the sky",
 "garden": "a fruit orchard garden: green grass ground, two round fruit trees without fruit, a wooden picnic table with an empty basket, flowers, blue sky with fluffy clouds",
 "town": "a cute little town street: a gray road with white dashes running across the bottom half, colorful small houses in the background, a traffic light, blue sky, a rainbow, fluffy clouds",
 "room": "a cozy child's bedroom: pastel walls, a window with curtains and sunlight, a wooden floor with a round rug, an empty shelf, a small nightstand, no furniture in the center",
 "home": "a warm family living room: a big soft sofa against the back wall, a framed picture on the wall, a window, a rug on the floor, a potted plant, soft afternoon light",
}
def prompt(desc):
    return ("Create a portrait background scene illustration in a soft 3D clay plasticine render style: rounded matte forms, smooth soft studio lighting, "
            "gentle soft shadows, bright cheerful pastel colors for a 4-year-old child. Scene: " + desc + ". "
            "IMPORTANT: the scene is EMPTY of characters - absolutely no people, no animals, no vehicles, no fruit, no toys; the bottom 60% of the image is open, "
            "uncluttered ground space so characters can be placed there later. Absolutely no text, no letters, no numbers, no watermark.")
jobs = []
for name, desc in SCENES.items():
    out = os.path.join(OUT, name + ".png")
    if os.path.exists(out) and os.path.getsize(out) > 50000: continue
    jobs.append((name, prompt(desc), out))
print("Jobs:", [j[0] for j in jobs])
if jobs: run_jobs(jobs, concurrency=5)
