# -*- coding: utf-8 -*-
"""Gen bộ giọng tiếng Anh bằng ElevenLabs (giọng gần như người thật) -> audio/<key>/.
Dùng:
  set ELEVEN_KEY=sk_...
  python tools/gen_audio_11.py <voice_id> <ten_thu_muc>
Ví dụ: python tools/gen_audio_11.py 21m00Tcm4TlvDq8ikWAM eleven
"""
import os, sys, json, time, urllib.request, urllib.error
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get("ELEVEN_KEY", "").strip()
VOICE_ID = sys.argv[1] if len(sys.argv) > 1 else ""
FOLDER = sys.argv[2] if len(sys.argv) > 2 else "eleven"
MODEL = os.environ.get("ELEVEN_MODEL", "eleven_multilingual_v2")
if not KEY or not VOICE_ID:
    print("Dung: set ELEVEN_KEY=sk_... && python tools/gen_audio_11.py <voice_id> <folder>"); sys.exit(1)

words = json.load(open(os.path.join(ROOT, "tools", "words.json"), encoding="utf-8"))
key = lambda s: s.replace(" ", "_")
TOPICS = [("animals","Animals"),("fruits","Fruits"),("colors","Colors"),("numbers","Numbers"),
          ("body","My Body"),("family","Family"),("vehicles","Vehicles"),("things","Things")]
jobs = {}
for topic, ws in words.items():
    for w, _ in ws:
        k = key(w)
        jobs[f"w_{k}"] = w + "."
        if topic in ("colors", "family"):
            jobs[f"find_{k}"] = f"Find {w}!"; jobs[f"thats_{k}"] = f"That's {w}."
        elif topic == "numbers":
            jobs[f"find_{k}"] = f"Find number {w}!"; jobs[f"thats_{k}"] = f"That's number {w}."
        else:
            jobs[f"find_{k}"] = f"Find the {w}!"
            jobs[f"thats_{k}"] = f"That's {'an' if w[0] in 'aeiou' else 'a'} {w}."
for i, p in enumerate(["Great job!","Well done!","Excellent!","You did it!","Awesome!","Super!","Wonderful!","Yay!"]):
    jobs[f"praise_{i}"] = p
jobs.update({"hooray":"Hooray! You did it!","tryagain":"Try again!",
    "q_what":"What is this?","q_color":"What color is this?","q_number":"What number is this?","q_who":"Who is this?",
    "notquite":"Not quite. Listen and repeat:","sayit":"Now you say it!","louder":"I didn't hear you. Say it louder!",
    "sample":"Hello! I'm your English teacher. Let's learn together!"})
for t, name in TOPICS:
    jobs[f"topic_{t}"] = name + "!"

OUT = os.path.join(ROOT, "audio", FOLDER)
os.makedirs(OUT, exist_ok=True)

def synth(text, path):
    body = json.dumps({"text": text, "model_id": MODEL,
        "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True}}).encode("utf-8")
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}", data=body,
        headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    wait = 8
    for _ in range(10):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            if len(data) > 800:
                open(path, "wb").write(data); return True
            return False
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"    bận, chờ {wait}s...", flush=True); time.sleep(wait); wait = min(wait+8, 40); continue
            print("    HTTP", e.code, e.read()[:200]); return False
        except Exception as ex:
            print("    lỗi", ex); time.sleep(3)
    return False

items = [(n, t) for n, t in jobs.items()
         if not (os.path.exists(os.path.join(OUT, n + ".mp3")) and os.path.getsize(os.path.join(OUT, n + ".mp3")) > 800)]
print(f"Can gen {len(items)}/{len(jobs)} cau -> giong {VOICE_ID} ({FOLDER})", flush=True)
ok = 0
for i, (name, text) in enumerate(items):
    if synth(text, os.path.join(OUT, name + ".mp3")):
        ok += 1
        if ok % 20 == 0: print(f"  ...{ok}/{len(items)}", flush=True)
    else:
        print("LOI", name, "-", text, flush=True)
    time.sleep(0.4)
print(f"DONE {ok}/{len(items)} file")
