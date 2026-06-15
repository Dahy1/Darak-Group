import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:3000'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        bad=[]
        def on_resp(r):
            if r.status>=400: bad.append(f"{r.status} {r.url}")
        pg.on('response', on_resp)
        pg.on('requestfailed', lambda r: bad.append(f"FAILED {r.failure} {r.url}"))
        await pg.goto(BASE+'/', wait_until='load')
        await pg.wait_for_timeout(8000)
        # how many scripts has SiteScripts appended so far?
        cnt=await pg.evaluate("()=>document.querySelectorAll('body > script').length")
        loaded=await pg.evaluate("""()=>({gsap:!!window.gsap, jq:!!window.jQuery, lenis:!!window.Lenis, ST:!!window.ScrollTrigger})""")
        print('body scripts appended:', cnt, '| libs:', loaded)
        print('--- non-200 responses ---')
        for x in bad[:25]: print(x[:160])
        await b.close()
asyncio.run(main())
