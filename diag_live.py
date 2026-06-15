import asyncio
from playwright.async_api import async_playwright
async def main():
    fails=[]; console=[]
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        pg.on('requestfailed', lambda r: fails.append('FAIL '+r.url))
        pg.on('response', lambda r: fails.append('HTTP%d %s'%(r.status,r.url)) if r.status>=400 else None)
        pg.on('console', lambda m: console.append('%s: %s'%(m.type,m.text)) if m.type in ('error','warning') else None)
        await pg.goto('https://dahy1.github.io/Darak-Group/',wait_until='load')
        await pg.wait_for_timeout(6000)
        await pg.screenshot(path='shots/live-diag.png')
        # measure hero text styling to see if fonts/layout applied
        info=await pg.evaluate("""()=>{
          const out={};
          const pre=document.getElementById('ohPreloader'); out.preloaderPresent=!!pre; if(pre) out.preloaderDisplay=getComputedStyle(pre).display;
          const h=document.querySelector('.zt-hero, .ohz-hero, [class*=hero] h1, h1');
          return out;
        }""")
        print('=== 4xx / failed requests ===')
        for u in fails:
            if any(x in u for x in ['.css','.js','.woff','.jpg','.png','.svg','.mp4','FAIL']): print(' ', u)
        print('=== console errors/warnings ===')
        for c in console[:15]: print(' ', c)
        print('=== info ===', info)
        await b.close()
asyncio.run(main())
