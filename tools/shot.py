import asyncio, sys, time
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        pg = await ctx.new_page()
        await pg.set_viewport_size({"width": 390, "height": 780})
        await pg.goto("file:///F:/APP%20BY%20HOANG/HOC%20TIENG%20ANH/index.html?v=" + str(int(time.time())))
        await asyncio.sleep(2.5)
        await pg.screenshot(path="dist/shot_home.png")
        await pg.click(".topic >> nth=0"); await asyncio.sleep(1.5)
        await pg.screenshot(path="dist/shot_learn.png")
        await pg.click(".mode[data-mode=quiz]"); await asyncio.sleep(1.5)
        await pg.screenshot(path="dist/shot_quiz.png")
        await pg.click(".mode[data-mode=speak]"); await asyncio.sleep(1.5)
        await pg.screenshot(path="dist/shot_speak.png")
        await pg.click(".mode[data-mode=memory]"); await asyncio.sleep(1.2)
        await pg.click(".mcard >> nth=0"); await asyncio.sleep(1)
        await pg.screenshot(path="dist/shot_memory.png")
        await pg.close()
        print("shots ok")
asyncio.run(main())
