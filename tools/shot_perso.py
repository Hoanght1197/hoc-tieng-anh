import asyncio, time
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pg=await b.contexts[0].new_page()
        await pg.set_viewport_size({"width":390,"height":800})
        await pg.goto("file:///F:/APP%20BY%20HOANG/HOC%20TIENG%20ANH/index.html?v="+str(int(time.time())))
        await asyncio.sleep(1.5)
        await pg.evaluate("localStorage.clear()")
        await pg.reload(); await asyncio.sleep(2)
        await pg.screenshot(path="dist/p_setup.png")
        # nhập tên + chọn mascot + bắt đầu
        await pg.fill("#nameIn", "Su")
        await pg.click(".mascot-opt >> nth=2"); await asyncio.sleep(0.4)
        await pg.click("#startBtn"); await asyncio.sleep(1.2)
        await pg.screenshot(path="dist/p_home.png")
        # mở cài đặt, đổi theme hồng
        await pg.click("#gear"); await asyncio.sleep(0.6)
        await pg.click('.themeseg button[data-v=pink]'); await asyncio.sleep(0.5)
        await pg.screenshot(path="dist/p_settings.png")
        await pg.click("#closeDlg"); await asyncio.sleep(0.5)
        await pg.screenshot(path="dist/p_home_pink.png")
        await pg.close(); print("ok")
asyncio.run(main())
