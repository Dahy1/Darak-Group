import asyncio, os
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':560,'height':560})
        await pg.goto('file://'+os.path.abspath('shots/egypt_preview.html'))
        await pg.wait_for_timeout(400)
        await pg.screenshot(path='shots/egypt_preview.png')
        await b.close()
asyncio.run(main())
