import asyncio, time, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pg=await b.contexts[0].new_page()
        pg.on("pageerror", lambda e: print("PAGEERR", e))
        pg.on("console", lambda m: print("CONSOLE", m.type, m.text) if m.type=="error" else None)
        await pg.set_viewport_size({"width":390,"height":800})
        await pg.goto("file:///F:/APP%20BY%20HOANG/HOC%20TIENG%20ANH/index.html?v="+str(int(time.time())))
        await asyncio.sleep(1.2)
        await pg.evaluate("""() => {
          localStorage.setItem('bhta_profile', JSON.stringify({name:'Su',mascot:'cat',setup:true}));
          localStorage.setItem('bhta_stars', '27');
          localStorage.setItem('bhta_album', JSON.stringify({got:['dog','apple','car','frog','banana'], claimed:1}));
          const k={}; ['dog','cat','cow','pig','duck','fish','bird','elephant','lion','monkey','rabbit','frog'].forEach(x=>k['animals/'+x]=1);
          ['apple','banana','orange'].forEach(x=>k['fruits/'+x]=1); ['car','bus'].forEach(x=>k['vehicles/'+x]=1);
          localStorage.setItem('bhta_known', JSON.stringify(k));
        }""")
        await pg.reload(); await asyncio.sleep(1.8)
        await pg.screenshot(path="dist/v2_home.png")
        await pg.click("#goal"); await asyncio.sleep(1.2)
        await pg.screenshot(path="dist/v2_album.png")
        await pg.click("#openSt"); await asyncio.sleep(1.3)
        await pg.screenshot(path="dist/v2_reveal.png")
        await pg.click("#back"); await asyncio.sleep(1)
        await pg.click(".topic >> nth=0"); await asyncio.sleep(1)
        await pg.click(".mode[data-nav=play]"); await asyncio.sleep(1)
        await pg.screenshot(path="dist/v2_hub.png")
        await pg.click(".gtile[data-g=quiz]"); await asyncio.sleep(1.3)
        await pg.screenshot(path="dist/v2_quiz.png")
        await pg.click(".mode[data-nav=play]"); await asyncio.sleep(0.8)
        await pg.click(".gtile[data-g=count]"); await asyncio.sleep(1.3)
        await pg.screenshot(path="dist/v2_count.png")
        # celebrate với sticker mới: ép sao lên mốc
        await pg.evaluate("localStorage.setItem('bhta_stars','39')")
        await pg.reload(); await asyncio.sleep(1.5)
        await pg.click(".topic >> nth=0"); await asyncio.sleep(0.8)
        await pg.click(".mode[data-nav=play]"); await asyncio.sleep(0.8)
        await pg.click(".gtile[data-g=fill]"); await asyncio.sleep(1)
        # trả lời đúng 5 vòng
        for i in range(5):
            ans = await pg.evaluate("(() => { const t=[...document.querySelectorAll('#tiles .tile')]; return null; })()")
            # tìm chữ đúng: so sánh với từ trong hình alt
            L = await pg.evaluate("""() => { const alt=document.querySelector('#fvis img').alt.toUpperCase(); const tiles=[...document.querySelectorAll('#tiles .tile')]; const i=tiles.findIndex(x=>x.classList.contains('blank')); return alt[i]; }""")
            await pg.click(".letterbtn[data-l='%s']" % L); await asyncio.sleep(1.7)
        await asyncio.sleep(1.2)
        await pg.screenshot(path="dist/v2_celebrate.png")
        await pg.click("#gear"); await asyncio.sleep(0.6)
        await pg.screenshot(path="dist/v2_settings.png")
        await pg.close(); print("ok")
asyncio.run(main())
