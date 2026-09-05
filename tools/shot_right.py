import asyncio, time
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pg=await b.contexts[0].new_page()
        await pg.set_viewport_size({"width":390,"height":780})
        await pg.goto("file:///F:/APP%20BY%20HOANG/HOC%20TIENG%20ANH/index.html?v="+str(int(time.time())))
        await asyncio.sleep(2)
        await pg.click(".topic >> nth=1"); await asyncio.sleep(1)  # Fruits
        await pg.click(".mode[data-mode=quiz]"); await asyncio.sleep(1.5)
        # chọn đúng
        target = await pg.eval_on_selector(".ask .q b", "e=>e.textContent.trim().toLowerCase()")
        btns = await pg.query_selector_all(".opt")
        for bt in btns:
            if (await bt.get_attribute("data-en")).lower()==target:
                await bt.click(); break
        await asyncio.sleep(0.8)
        await pg.screenshot(path="dist/c_right.png")
        await pg.close(); print("ok")
asyncio.run(main())
