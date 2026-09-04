# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, r"F:\DESIGN\scripts"); sys.path.insert(0, r"F:\KIT MKT\scripts")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from gpt_gen_safe import run_jobs
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "img", "styletest")

SHEETS = {
 "styleA": [
   "flat vector illustration, modern geometric, bold flat colors, no gradients",
   "soft 3D clay plasticine render, rounded, matte, cute",
   "kawaii chibi cartoon, big head, big sparkly eyes, pastel",
   "glossy die-cut sticker with thick white outline, vivid, drop shadow",
   "soft watercolor painting, gentle washes, artistic",
   "cute isometric 3D render, smooth shading, playful",
 ],
 "styleB": [
   "pastel line art, clean outline with soft flat pastel fill",
   "layered paper cut craft style, stacked colored paper, soft shadows",
   "claymorphism, matte 3D clay, fluffy soft look, dreamy",
   "bold-outline cartoon, children storybook, clean thick lines",
   "low-poly geometric 3D, faceted, colorful",
   "childlike crayon hand-drawn doodle, warm and playful",
 ],
}
def prompt(items):
    order=", ".join(f"{i+1}. {it}" for i,it in enumerate(items))
    return ("Create a portrait image, a clean grid of 6 equal cells (2 columns, 3 rows) separated by thin light gray lines, "
            "each cell a plain pure white background. In EVERY cell draw the SAME subject: one cute friendly sitting puppy dog, "
            "centered and large. BUT render each cell in a DIFFERENT illustration style as listed. Make the style differences obvious. "
            "No text, no letters, no labels, no watermark. "
            f"Cell styles left-to-right, top-to-bottom: {order}.")
jobs=[]
for name,items in SHEETS.items():
    out=os.path.join(OUT,name+".png")
    if os.path.exists(out) and os.path.getsize(out)>50000: continue
    jobs.append((name, prompt(items), out))
print("Jobs:", [j[0] for j in jobs])
if jobs: run_jobs(jobs, concurrency=2)
