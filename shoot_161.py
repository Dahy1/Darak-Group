import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        try:
            await pg.goto('https://www.161london.com/projects/the-estate/', wait_until='domcontentloaded', timeout=60000)
        except Exception as e: print('goto', str(e)[:100])
        await pg.wait_for_timeout(5000)
        docH=await pg.evaluate("document.body.scrollHeight"); vh=900
        print('docH', docH)
        n=0; y=0
        while y < docH and n < 26:
            await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(850)
            await pg.screenshot(path=f'shots/l-{n:02d}.png')
            docH=await pg.evaluate("document.body.scrollHeight"); y+=int(vh*0.92); n+=1
        print('captured', n, 'finalDocH', docH)
        await b.close()
asyncio.run(main())
