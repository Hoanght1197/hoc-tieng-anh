import asyncio, time
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pg=await b.contexts[0].new_page()
        await pg.set_viewport_size({"width":390,"height":780})
        await pg.goto("file:///F:/APP%20BY%20HOANG/HOC%20TIENG%20ANH/index.html?v="+str(int(time.time())))
        await asyncio.sleep(2)
        # vào Nghe & chọn rồi bấm đúng liên tục để tới celebrate
        await pg.click(".topic >> nth=0"); await asyncio.sleep(1)
        await pg.click(".mode[data-mode=quiz]"); await asyncio.sleep(1.5)
        for _ in range(6):
            # đọc target tiếng anh trong .q b, tìm opt khớp qua alt img
            try:
                target = await pg.eval_on_selector(".ask .q b", "e=>e.textContent.trim().toLowerCase()")
            except: break
            btns = await pg.query_selector_all(".opt")
            clicked=False
            for bt in btns:
                en = await bt.get_attribute("data-en")
                if en and en.lower()==target:
                    await bt.click(); clicked=True; break
            if not clicked and btns:
                await btns[0].click()
            await asyncio.sleep(2.3)
            party = await pg.query_selector(".party")
            if party:
                break
        await asyncio.sleep(1)
        await pg.screenshot(path="dist/c_celeb.png")
        await pg.close(); print("ok")
asyncio.run(main())
