import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:3000'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(BASE+'/vision/', wait_until='commit')
        for _ in range(8):
            v=await pg.evaluate("""()=>{const bn=document.querySelector('#oh-reveal .oh-band');if(!bn)return null;const m=new DOMMatrix(getComputedStyle(bn).transform);const a=bn.getAnimations&&bn.getAnimations()[0];return {tx:Math.round(m.m41), t:a?Math.round(a.currentTime):-1, state:a?a.playState:'?'};}""")
            print(v)
            await pg.wait_for_timeout(90)
        await b.close()
asyncio.run(main())
