# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, r"F:\DESIGN\scripts"); sys.path.insert(0, r"F:\KIT MKT\scripts")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from gpt_gen_safe import run_jobs
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out=os.path.join(ROOT,"img","sheets","hand_new.png")
prompt=("A soft 3D clay plasticine render of a cute child's open hand, palm facing forward, "
        "with FIVE clearly separated and COMPLETE fingers (thumb and four fingers), rounded matte clay, "
        "soft studio lighting, gentle shadow, centered, large, on a plain pure white background. "
        "No text, no letters, no watermark. Single hand only.")
run_jobs([("hand", prompt, out)], concurrency=1)
