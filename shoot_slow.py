import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:3000'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(viewport={'width':1440,'height':900})
        # force a slow reveal so the feathered band is visible mid-sweep
        await ctx.add_init_script("""
          const s=document.createElement('style');
          s.textContent=':root{--oht-dur:4s !important;}';
          (document.head||document.documentElement).appendChild(s);
        """)
        pg=await ctx.new_page()
        await pg.goto(BASE+'/about-us/', wait_until='commit')
        for i,d in enumerate([700,1500,2600]):
            await pg.wait_for_timeout(d if i==0 else d-[700,1500,2600][i-1])
            await pg.screenshot(path=f'shots/tr-slow-{i}.png')
        await b.close()
asyncio.run(main())
