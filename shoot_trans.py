import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:3000'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        # 1. home nav
        await pg.goto(BASE+'/', wait_until='load'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='shots/t-home-nav.png', clip={'x':0,'y':0,'width':1440,'height':140})
        # 2. inner page nav (about-us)
        await pg.goto(BASE+'/about-us/', wait_until='load'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='shots/t-about-nav.png', clip={'x':0,'y':0,'width':1440,'height':140})
        # 3. inner page footer
        h=await pg.evaluate("document.body.scrollHeight")
        await pg.evaluate(f"window.scrollTo(0,{h})"); await pg.wait_for_timeout(1200)
        await pg.screenshot(path='shots/t-about-foot.png', clip={'x':0,'y':760,'width':1440,'height':140})
        # 4. transition: capture mid-exit curtain
        await pg.goto(BASE+'/', wait_until='load'); await pg.wait_for_timeout(1600)
        # find a same-origin nav link to another page
        href=await pg.evaluate("""()=>{const as=[...document.querySelectorAll('a')];
            const a=as.find(a=>{try{const u=new URL(a.href,location.href);return u.origin===location.origin && u.pathname!==location.pathname && !a.target;}catch(e){return false;}});
            return a?a.href:null;}""")
        print('clicking', href)
        if href:
            await pg.evaluate("""(h)=>{const as=[...document.querySelectorAll('a')];const a=as.find(a=>a.href===h);a.click();}""", href)
            await pg.wait_for_timeout(240)
            await pg.screenshot(path='shots/t-exit-mid.png')
            await pg.wait_for_timeout(1400)  # land on new page (entry overlay should be revealing/gone)
            await pg.screenshot(path='shots/t-enter-after.png')
            print('url now', pg.url)
        await b.close()
asyncio.run(main())
