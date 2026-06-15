import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:3000'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':900})
        # capture ENTER reveal on fresh load of about (early frames)
        await pg.goto(BASE+'/about-us/', wait_until='commit')
        await pg.wait_for_timeout(180)
        await pg.screenshot(path='shots/tr-enter-1.png')
        await pg.wait_for_timeout(220)
        await pg.screenshot(path='shots/tr-enter-2.png')
        await pg.wait_for_timeout(1600)
        # now trigger EXIT: click a nav link, capture mid-cover
        href=await pg.evaluate("""()=>{const as=[...document.querySelectorAll('a')];
          const a=as.find(a=>{try{const u=new URL(a.href,location.href);return u.origin===location.origin&&u.pathname!==location.pathname&&!a.target;}catch(e){return false;}});return a?a.href:null;}""")
        print('exit-click ->', href)
        if href:
            await pg.evaluate("(h)=>{[...document.querySelectorAll('a')].find(a=>a.href===h).click();}", href)
            await pg.wait_for_timeout(170)
            await pg.screenshot(path='shots/tr-cover-1.png')
            await pg.wait_for_timeout(160)
            await pg.screenshot(path='shots/tr-cover-2.png')
            await pg.wait_for_timeout(1500)
            print('landed', pg.url)
        await b.close()
asyncio.run(main())
