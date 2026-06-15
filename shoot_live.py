import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto('https://dahy1.github.io/Darak-Group/',wait_until='load')
        await pg.wait_for_timeout(5000)  # let the preloader finish + reveal
        await pg.screenshot(path='shots/live-home.png')
        await b.close()
asyncio.run(main())
