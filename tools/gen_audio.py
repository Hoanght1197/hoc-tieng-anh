# -*- coding: utf-8 -*-
"""Tao file mp3 giong doc bang Microsoft neural TTS (edge-tts). Chay lai la bo qua file da co."""
import asyncio, json, os, sys
import edge_tts
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "audio")
VOICE = "en-US-JennyNeural"
RATE = "-12%"
words = json.load(open(os.path.join(ROOT, "tools", "words.json"), encoding="utf-8"))
key = lambda s: s.replace(" ", "_")
jobs = {}
for topic, ws in words.items():
    for en, _ in ws:
        k = key(en)
        jobs[f"w_{k}"] = en + "."
        if topic == "colors":
            jobs[f"find_{k}"] = f"Find {en}!"
            jobs[f"thats_{k}"] = f"That's {en}."
        elif topic == "numbers":
            jobs[f"find_{k}"] = f"Find number {en}!"
            jobs[f"thats_{k}"] = f"That's number {en}."
        elif topic == "family":
            jobs[f"find_{k}"] = f"Find {en}!"
            jobs[f"thats_{k}"] = f"That's {en}."
        else:
            jobs[f"find_{k}"] = f"Find the {en}!"
            art = "an" if en[0] in "aeiou" else "a"
            jobs[f"thats_{k}"] = f"That's {art} {en}."
for i, p in enumerate(["Great job!", "Well done!", "Excellent!", "You did it!", "Awesome!", "Super!", "Wonderful!", "Yay!"]):
    jobs[f"praise_{i}"] = p
jobs["hooray"] = "Hooray! You did it!"
jobs["q_what"] = "What is this?"
jobs["q_color"] = "What color is this?"
jobs["q_number"] = "What number is this?"
jobs["q_who"] = "Who is this?"
jobs["notquite"] = "Not quite. Listen and repeat:"
jobs["sayit"] = "Now you say it!"
jobs["louder"] = "I didn't hear you. Say it louder!"
jobs["tryagain"] = "Try again!"
for t, name in [("animals","Animals"),("fruits","Fruits"),("colors","Colors"),("numbers","Numbers"),("body","My Body"),("family","Family"),("vehicles","Vehicles"),("things","Things")]:
    jobs[f"topic_{t}"] = name + "!"

async def one(name, text):
    path = os.path.join(OUT, name + ".mp3")
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return
    for attempt in range(4):
        try:
            await edge_tts.Communicate(text, VOICE, rate=RATE).save(path)
            print("ok", name, "-", text)
            return
        except Exception as e:
            print("retry", name, e)
            await asyncio.sleep(2)

async def main():
    os.makedirs(OUT, exist_ok=True)
    items = list(jobs.items())
    sem = asyncio.Semaphore(4)
    async def guarded(n, t):
        async with sem:
            await one(n, t)
    await asyncio.gather(*(guarded(n, t) for n, t in items))
    print("DONE", len(items), "files")

asyncio.run(main())
