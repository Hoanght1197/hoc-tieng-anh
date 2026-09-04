# -*- coding: utf-8 -*-
"""Tao file mp3 giong doc bang Microsoft neural TTS (edge-tts).
- Tieng Anh: moi giong 1 thu muc audio/<key>/ (aria = co giao, ana = ban nho)
- Tieng Viet huong dan: audio/vi/
Chay lai la bo qua file da co. Xoa thu muc de gen lai."""
import asyncio, json, os, sys
import edge_tts
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(ROOT, "audio")
VOICES = {"emma": "en-US-EmmaMultilingualNeural", "aria": "en-US-AriaNeural", "ana": "en-US-AnaNeural"}
VI_VOICE = "vi-VN-HoaiMyNeural"
words = json.load(open(os.path.join(ROOT, "tools", "words.json"), encoding="utf-8"))
key = lambda s: s.replace(" ", "_")
TOPIC_NAMES = [("animals", "Animals", "Động vật"), ("fruits", "Fruits", "Trái cây"), ("colors", "Colors", "Màu sắc"), ("numbers", "Numbers", "Số đếm"),
               ("body", "My Body", "Cơ thể"), ("family", "Family", "Gia đình"), ("vehicles", "Vehicles", "Xe cộ"), ("things", "Things", "Đồ vật")]

# ---------- tieng Anh ----------
en = {}
for topic, ws in words.items():
    for w, _ in ws:
        k = key(w)
        en[f"w_{k}"] = w + "."
        if topic in ("colors", "family"):
            en[f"find_{k}"] = f"Find {w}!"; en[f"thats_{k}"] = f"That's {w}."
        elif topic == "numbers":
            en[f"find_{k}"] = f"Find number {w}!"; en[f"thats_{k}"] = f"That's number {w}."
        else:
            en[f"find_{k}"] = f"Find the {w}!"
            en[f"thats_{k}"] = f"That's {'an' if w[0] in 'aeiou' else 'a'} {w}."
for i, p in enumerate(["Great job!", "Well done!", "Excellent!", "You did it!", "Awesome!", "Super!", "Wonderful!", "Yay!"]):
    en[f"praise_{i}"] = p
en.update({
    "hooray": "Hooray! You did it!", "tryagain": "Try again!",
    "q_what": "What is this?", "q_color": "What color is this?", "q_number": "What number is this?", "q_who": "Who is this?",
    "notquite": "Not quite. Listen and repeat:", "sayit": "Now you say it!", "louder": "I didn't hear you. Say it louder!",
    "sample": "Hello! I'm your English teacher. Let's learn together!",
})
for t, name, _ in TOPIC_NAMES:
    en[f"topic_{t}"] = name + "!"

# ---------- tieng Viet huong dan ----------
vi = {
    "quiz": "Cô đọc tên, bé chọn đúng hình nhé!",
    "speak": "Cô hỏi, bé trả lời bằng tiếng Anh nhé. Bấm vào cái micro rồi nói to nào!",
    "memory": "Bé lật hai thẻ giống nhau nhé!",
    "done": "Bé giỏi quá! Mình chơi tiếp nhé.",
    "repeat": "Chưa đúng rồi. Bé nghe cô đọc rồi nói lại nhé:",
    "louder": "Cô chưa nghe thấy. Bé nói to hơn nhé!",
    "wrong": "Chưa đúng, bé nghe lại rồi tìm nhé.",
    "good": "Đúng rồi!",
    "sample": "Xin chào bé! Cô là cô giáo hướng dẫn. Mình cùng học tiếng Anh nhé!",
}
for t, _, name in TOPIC_NAMES:
    vi[f"topic_{t}"] = f"Giờ mình học chủ đề {name} nhé! Bé nghe rồi đọc theo cô nào."

async def one(path, text, voice, sem):
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return
    async with sem:
        for attempt in range(4):
            try:
                await edge_tts.Communicate(text, voice).save(path)
                print("ok", os.path.relpath(path, AUDIO), "-", text)
                return
            except Exception as e:
                print("retry", path, e); await asyncio.sleep(2)

async def main():
    sem = asyncio.Semaphore(4)
    tasks = []
    for k, v in VOICES.items():
        d = os.path.join(AUDIO, k); os.makedirs(d, exist_ok=True)
        tasks += [one(os.path.join(d, n + ".mp3"), t, v, sem) for n, t in en.items()]
    d = os.path.join(AUDIO, "vi"); os.makedirs(d, exist_ok=True)
    tasks += [one(os.path.join(d, n + ".mp3"), t, VI_VOICE, sem) for n, t in vi.items()]
    await asyncio.gather(*tasks)
    print("DONE", len(tasks), "files")

asyncio.run(main())
