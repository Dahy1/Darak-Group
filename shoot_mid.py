import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:3000'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(viewport={'width':1440,'height':900})
        await ctx.add_init_script("const s=document.createElement('style');s.id='ovr';s.textContent='html{--oht-dur:2.4s !important}';document.documentElement.appendChild(s);")
        pg=await ctx.new_page()
        await pg.goto(BASE+'/about-us/', wait_until='commit')
        # wait until band animation has progressed ~40%
        await pg.wait_for_function("""()=>{const bn=document.querySelector('#oh-reveal .oh-band');if(!bn||!bn.getAnimations)return false;const a=bn.getAnimations()[0];return a&&a.currentTime>800;}""", timeout=8000)
        await pg.screenshot(path='shots/tr-enter-mid.png')
        await b.close()
asyncio.run(main())
