import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:3000'
FORCE="""()=>{const p=document.getElementById('ohPreloader'); if(p) p.remove();
  const ui=document.getElementById('ohsUI'); if(ui){ ui.hidden=false; document.body.appendChild(ui); }
  const f=document.querySelector('.ohs-finder'); if(f){ f.style.opacity='1'; f.style.pointerEvents='auto'; }
  document.dispatchEvent(new Event('oh:preloaded'));}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        # desktop next home: custom select
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(BASE+'/', wait_until='load'); await pg.wait_for_timeout(2500)
        await pg.evaluate(FORCE)
        # poll up to ~12s for the late global enhancement script to load + run
        n=0
        for _ in range(24):
            await pg.wait_for_timeout(500)
            await pg.evaluate("()=>document.dispatchEvent(new Event('oh:preloaded'))")
            n=await pg.evaluate("()=>document.querySelectorAll('.ohs-finder .ohs-select').length")
            if n: break
        print('custom selects built on Next home:', n)
        await pg.evaluate("()=>{const t=document.querySelector('.ohs-finder .ohs-select-trigger'); if(t) t.click();}")
        await pg.wait_for_timeout(700)
        await pg.screenshot(path='shots/next-sel-open.png', clip={'x':0,'y':300,'width':1440,'height':600})
        await pg.close()
        # mobile next stats page check (home)
        m=await b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2, is_mobile=True)
        await m.goto(BASE+'/', wait_until='load'); await m.wait_for_timeout(2500)
        await m.evaluate("()=>{const p=document.getElementById('ohPreloader'); if(p) p.remove(); document.dispatchEvent(new Event('oh:preloaded'));}")
        await m.wait_for_timeout(700)
        await m.evaluate("window.scrollTo(0,1400)"); await m.wait_for_timeout(800)
        await m.screenshot(path='shots/next-m-stats.png')
        await b.close()
asyncio.run(main())
