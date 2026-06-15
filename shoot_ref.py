import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':2200})
        try:
            await pg.goto('https://architects.framer.website/contact-us', wait_until='networkidle', timeout=60000)
        except Exception as e: print('goto', str(e)[:120])
        await pg.wait_for_timeout(3500)
        # try to scroll the form into view
        await pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path='shots/ref-contact-full.png', full_page=True)
        # dump form-ish html
        html = await pg.evaluate("""()=>{const f=document.querySelector('form'); return f?f.outerHTML.slice(0,4000):'NO FORM';}""")
        import pathlib; pathlib.Path('shots/ref-form.html').write_text(html, encoding='utf-8')
        print('formlen', len(html))
        await b.close()
asyncio.run(main())
