# -*- coding: utf-8 -*-
"""Gen giọng CÔ HƯỚNG DẪN TIẾNG VIỆT bằng FPT.AI TTS (giọng tự nhiên VN).
Chỉ ghi đè thư mục audio/vi/. Phần tiếng Anh (aria/ana) giữ nguyên.

Dùng:
  set FPT_KEY=<mã api của bạn>        (Windows PowerShell: $env:FPT_KEY="...")
  python tools/gen_audio_fpt.py [voice]

Giọng FPT (mặc định banmai - nữ, ấm, hợp trẻ em):
  banmai lannhi thuminh myan  (nữ) | leminh minhquang giahuy  (nam)
"""
import os, sys, time, json, urllib.request, urllib.error
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get("FPT_KEY", "").strip()
VOICE = (sys.argv[1] if len(sys.argv) > 1 else "banmai").strip()
if not KEY:
    print("THIEU MA API. Chay:  set FPT_KEY=... rồi python tools/gen_audio_fpt.py"); sys.exit(1)

TOPICS = [("animals", "Động vật"), ("fruits", "Trái cây"), ("colors", "Màu sắc"), ("numbers", "Số đếm"),
          ("body", "Cơ thể"), ("family", "Gia đình"), ("vehicles", "Xe cộ"), ("things", "Đồ vật")]
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
for t, name in TOPICS:
    vi[f"topic_{t}"] = f"Giờ mình học chủ đề {name} nhé! Bé nghe rồi đọc theo cô nào."

OUT = os.path.join(ROOT, "audio", "vi")
os.makedirs(OUT, exist_ok=True)

def synth(text):
    req = urllib.request.Request("https://api.fpt.ai/hmi/tts/v5", data=text.encode("utf-8"),
        headers={"api-key": KEY, "voice": VOICE, "speed": "", "Content-Type": "text/plain; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.loads(r.read().decode("utf-8"))
    if res.get("error"):
        raise RuntimeError(res.get("message", res))
    return res["async"]

def download(url, path):
    for _ in range(20):  # file async, đợi FPT render xong
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                data = r.read()
            if len(data) > 1500:
                open(path, "wb").write(data); return True
        except Exception:
            pass
        time.sleep(1.5)
    return False

def synth_retry(text):
    """Gặp 429 (bản free bị chặn) thì chờ tăng dần rồi thử lại, tối đa ~8 phút/câu."""
    wait = 20
    for attempt in range(18):
        try:
            return synth(text)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"    bận, chờ {wait}s...", flush=True)
                time.sleep(wait); wait = min(wait + 15, 90); continue
            raise
    raise RuntimeError("van bi chan sau nhieu lan thu")

ok = 0
items = [(n, t) for n, t in vi.items() if not (os.path.exists(os.path.join(OUT, n + ".mp3")) and os.path.getsize(os.path.join(OUT, n + ".mp3")) > 1500)]
print(f"Can gen {len(items)} cau con thieu", flush=True)
for name, text in items:
    path = os.path.join(OUT, name + ".mp3")
    try:
        url = synth_retry(text)
        time.sleep(2)
        if download(url, path):
            print("ok", name, flush=True); ok += 1
        else:
            print("TAI LOI", name, flush=True)
        time.sleep(14)  # giãn cách để đỡ bị chặn
    except Exception as e:
        print("LOI", name, "-", e, flush=True)
print(f"DONE {ok}/{len(items)} file bằng giọng {VOICE}")
