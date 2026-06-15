import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:3000'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        errs=[]
        pg.on('console', lambda m: errs.append(m.type+': '+m.text) if m.type in ('error','warning') else None)
        pg.on('pageerror', lambda e: errs.append('PAGEERROR: '+str(e)))
        await pg.goto(BASE+'/', wait_until='load')
        await pg.wait_for_timeout(20000)
        info=await pg.evaluate("""()=>({
          finder: document.querySelectorAll('.ohs-finder').length,
          fields: document.querySelectorAll('.ohs-finder .ohs-field').length,
          selects: document.querySelectorAll('.ohs-finder select').length,
          enhanced: document.querySelectorAll('.ohs-finder .ohs-select').length,
          enhancedFlag: document.querySelectorAll('.ohs-field.ohs-enhanced').length,
          uiHidden: (document.getElementById('ohsUI')||{}).hidden,
          gsap: !!window.gsap
        })""")
        print('INFO', info)
        print('--- console errors/warnings (first 15) ---')
        for e in errs[:15]: print(e[:200])
        await b.close()
asyncio.run(main())
