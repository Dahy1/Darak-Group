import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1440,'height':1000},device_scale_factor=2)
        await pg.goto('https://architects.framer.website/contact-us', wait_until='networkidle', timeout=60000)
        await pg.wait_for_timeout(3000)
        f=await pg.query_selector('form')
        if f:
            box=await f.bounding_box()
            print('form box', box)
            await f.scroll_into_view_if_needed()
            await pg.wait_for_timeout(800)
            await f.screenshot(path='shots/ref-form-card.png')
        # computed styles of inputs
        info=await pg.evaluate("""()=>{
          const inp=document.querySelector('form input[type=text], form input:not([type=hidden])');
          const btn=document.querySelector('form button, form input[type=submit]');
          const cs=inp?getComputedStyle(inp):null; const bs=btn?getComputedStyle(btn):null;
          const card=document.querySelector('form')&&document.querySelector('form').closest('div');
          return {
            input: cs?{bg:cs.backgroundColor,color:cs.color,border:cs.border,radius:cs.borderRadius,padding:cs.padding,font:cs.fontFamily,fs:cs.fontSize,h:cs.height}:null,
            btn: bs?{bg:bs.backgroundColor,color:bs.color,radius:bs.borderRadius,padding:bs.padding,fs:bs.fontSize}:null,
            labels:[...document.querySelectorAll('form label, form .framer-text')].slice(0,12).map(e=>e.textContent.trim()).filter(Boolean)
          };
        }""")
        print(info)
        await b.close()
asyncio.run(main())
