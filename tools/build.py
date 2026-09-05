# -*- coding: utf-8 -*-
"""Ghép src/head.html + src/body.html thành:
  index.html            - bản PWA (ảnh/mp3 file rời, có manifest + service worker) -> đưa lên hosting để cài iPhone
  bundle.html           - bản 1 file, nhúng sẵn toàn bộ ảnh + mp3 (mở offline ở bất cứ đâu)
  dist/artifact.html    - nội dung cho Artifact claude.ai (không có wrapper html/head/body)
  sw.js, manifest.webmanifest, icons/
Chạy: python tools/build.py
"""
import os, sys, json, base64, hashlib, glob
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda p: open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, s):
    full = os.path.join(ROOT, p); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8", newline="\n").write(s); print("->", p, f"{os.path.getsize(full)/1024:.0f} KB")

head, body = rd("src/head.html"), rd("src/body.html")

# ---------- icons (từ hình con chó) ----------
os.makedirs(os.path.join(ROOT, "icons"), exist_ok=True)
src_icon = os.path.join(ROOT, "img", "dog.webp")
def make_icon(size, pad_ratio=0.12, out=None):
    bg = Image.new("RGBA", (size, size), (91, 167, 114, 255))
    d = ImageDraw.Draw(bg)
    r = int(size * 0.22)
    d.rounded_rectangle((0, 0, size - 1, size - 1), radius=r, fill=(91, 167, 114, 255))
    if os.path.exists(src_icon):
        im = Image.open(src_icon).convert("RGBA")
        inner = int(size * (1 - pad_ratio * 2))
        im = im.resize((inner, inner), Image.LANCZOS)
        # bo góc ảnh
        mask = Image.new("L", (inner, inner), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, inner - 1, inner - 1), radius=int(inner * 0.18), fill=255)
        bg.paste(im, ((size - inner) // 2, (size - inner) // 2), mask)
    bg.convert("RGB").save(os.path.join(ROOT, "icons", out or f"icon-{size}.png"), "PNG", optimize=True)
for s in (192, 512):
    make_icon(s)
make_icon(180, out="apple-touch-icon.png")
make_icon(512, pad_ratio=0.2, out="maskable-512.png")
print("-> icons/")

# ---------- manifest ----------
manifest = {
    "name": "Bé Học Tiếng Anh", "short_name": "Tiếng Anh", "lang": "vi", "start_url": "./index.html",
    "scope": "./", "display": "standalone", "orientation": "portrait",
    "background_color": "#E4F3DC", "theme_color": "#5BA772",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
wr("manifest.webmanifest", json.dumps(manifest, ensure_ascii=False, indent=2))

# ---------- index.html (PWA) ----------
PWA_HEAD = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">
<meta name="theme-color" content="#E4F3DC">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Tiếng Anh">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
"""
def wrap(head_extra, head_html, body_html):
    return "<!doctype html>\n<html lang=\"vi\">\n<head>\n" + head_extra + head_html + "</head>\n<body>\n" + body_html + "</body>\n</html>\n"
wr("index.html", wrap(PWA_HEAD, head, body))

# ---------- service worker: precache toàn bộ ----------
files = ["./", "index.html", "manifest.webmanifest"]
for pat in ("img/*.webp", "img/cut/*.webp", "img/scenes/*.webp", "audio/*/*.mp3", "icons/*.png"):
    files += sorted(p.replace(ROOT + os.sep, "").replace("\\", "/") for p in glob.glob(os.path.join(ROOT, pat)))
h = hashlib.md5()
for f in files:
    p = os.path.join(ROOT, f)
    if os.path.isfile(p): h.update(open(p, "rb").read())
h.update(head.encode()); h.update(body.encode())
ver = h.hexdigest()[:10]
sw = """// Service worker - cache toàn bộ app để chạy offline sau lần mở đầu. Phiên bản: %s
const CACHE = 'bhta-%s';
const FILES = %s;
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(r => r || fetch(e.request).then(res => {
    if (res.ok && new URL(e.request.url).origin === location.origin) {
      const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy));
    }
    return res;
  }).catch(() => caches.match('index.html'))));
});
""" % (ver, ver, json.dumps(files, ensure_ascii=False))
wr("sw.js", sw)

# ---------- bundle: nhúng ảnh + mp3 ----------
# artifact/bundle 1 file bị giới hạn 16MB -> chỉ nhúng vài giọng cho bản xem;
# app chính (index.html + file rời trên GitHub) vẫn đủ tất cả giọng.
BUNDLE_VOICES = {"matilda", "emma"}
assets = {}
for pat in ("img/*.webp", "img/cut/*.webp", "img/scenes/*.webp"):
  for p in sorted(glob.glob(os.path.join(ROOT, pat))):
    rel = p.replace(ROOT + os.sep, "").replace("\\", "/")
    assets[rel] = "data:image/webp;base64," + base64.b64encode(open(p, "rb").read()).decode()
for p in sorted(glob.glob(os.path.join(ROOT, "audio", "*", "*.mp3"))):
    rel = p.replace(ROOT + os.sep, "").replace("\\", "/")
    if rel.split("/")[1] not in BUNDLE_VOICES:
        continue
    assets[rel] = "data:audio/mpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()
inject = "<script>window.ASSETS=" + json.dumps(assets, separators=(",", ":")) + ";</script>\n"
body_bundled = body.replace('<div id="app">', inject + '<div id="app">', 1)
BUNDLE_HEAD = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">
<meta name="theme-color" content="#E4F3DC">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Tiếng Anh">
"""
wr("bundle.html", wrap(BUNDLE_HEAD, head, body_bundled))
wr("dist/artifact.html", head + body_bundled)
print("assets:", len(assets), "| sw version:", ver)
