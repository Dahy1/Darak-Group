import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':1000})
        await pg.goto('https://www.auremin.com/careers', wait_until='domcontentloaded', timeout=60000)
        await pg.wait_for_timeout(2500)
        for lbl in ['Allow all','Deny','Allow selection','Accept']:
            try:
                el=pg.get_by_text(lbl, exact=True)
                if await el.count(): await el.first.click(timeout=2000); break
            except Exception: pass
        await pg.wait_for_timeout(1500)
        h=await pg.evaluate("document.body.scrollHeight"); print('docH',h)
        n=0;y=0
        while y<h and n<10:
            await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(650)
            await pg.screenshot(path=f'shots/aur-{n}.png'); y+=950; n+=1; h=await pg.evaluate("document.body.scrollHeight")
        print('captured',n)
        await b.close()
asyncio.run(main())
