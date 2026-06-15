import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':1000})
        try:
            await pg.goto('https://www.auremin.com/careers', wait_until='networkidle', timeout=60000)
        except Exception as e: print('goto', str(e)[:100])
        await pg.wait_for_timeout(3500)
        h=await pg.evaluate("document.body.scrollHeight"); print('docH',h)
        n=0;y=0
        while y<h and n<12:
            await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(700)
            await pg.screenshot(path=f'shots/aur-{n}.png'); y+=950; n+=1; h=await pg.evaluate("document.body.scrollHeight")
        # grab text outline
        txt=await pg.evaluate("()=>[...document.querySelectorAll('h1,h2,h3')].map(e=>e.tagName+': '+e.innerText.trim().slice(0,60)).slice(0,30)")
        import pathlib; pathlib.Path('shots/aur-text.txt').write_text('\n'.join(txt),encoding='utf-8')
        print('captured',n)
        await b.close()
asyncio.run(main())
