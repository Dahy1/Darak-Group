import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:3000'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for i,delay in enumerate([60,160,300,500]):
            pg=await b.new_page(viewport={'width':1440,'height':900})
            await pg.goto(BASE+'/services/', wait_until='commit')
            await pg.wait_for_timeout(delay)
            await pg.screenshot(path=f'shots/tr-rev-{i}-{delay}.png')
            await pg.close()
        await b.close()
asyncio.run(main())
