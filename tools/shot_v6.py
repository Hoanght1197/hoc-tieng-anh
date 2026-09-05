import asyncio, time
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pg=await b.contexts[0].new_page()
        pg.on("pageerror", lambda e: print("PAGEERR", e))
        await pg.set_viewport_size({"width":390,"height":800})
        await pg.goto("file:///F:/APP%20BY%20HOANG/HOC%20TIENG%20ANH/index.html?v="+str(int(time.time())))
        await asyncio.sleep(1.2)
        await pg.evaluate("localStorage.setItem('bhta_profile', JSON.stringify({name:'Su',mascot:'cat',setup:true}))")
        await pg.reload(); await asyncio.sleep(1.5)
        for idx,name in [(0,"farm"),(6,"town"),(7,"room"),(5,"family"),(4,"body"),(3,"numbers")]:
            await pg.click(".topic >> nth=%d" % idx); await asyncio.sleep(0.9)
            await pg.click(".mode[data-nav=explore]"); await asyncio.sleep(1.6)
            await pg.screenshot(path="dist/v6_%s.png" % name)
            await pg.click("#back"); await asyncio.sleep(0.7)
        await pg.close(); print("ok")
asyncio.run(main())
