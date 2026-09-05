import asyncio, time
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pg=await b.contexts[0].new_page()
        await pg.set_viewport_size({"width":390,"height":780})
        await pg.goto("file:///F:/APP%20BY%20HOANG/HOC%20TIENG%20ANH/index.html?v="+str(int(time.time())))
        await asyncio.sleep(2)
        await pg.click(".topic >> nth=0"); await asyncio.sleep(1)
        await pg.click(".mode[data-mode=bubble]"); await asyncio.sleep(1.8)
        await pg.screenshot(path="dist/c_bubble.png")
        await pg.close(); print("ok")
asyncio.run(main())
